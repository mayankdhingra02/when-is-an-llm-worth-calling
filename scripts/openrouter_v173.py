"""V173 guarded OpenRouter client: authorization gate, single key file, host allowlist, pinned provider, hard spend/request caps.

The key is read from one owner-created file and is never written to any record. Requests are refused before sending
when the recorded spend plus this request's worst-case cost would exceed the cap.
"""
import json, math, os, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from collect_smollm_v47 import ROOT, read, write, append, now

class Refused(RuntimeError): pass

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): raise Refused('Redirects refused')

def load_key(cfg):
    p = Path(os.path.expanduser(cfg['key_file']))
    if p.stat().st_mode & 0o077: raise Refused('Key file must be private (chmod 600)')
    key = p.read_text().strip()
    if not key.startswith('sk-or-v1-') or len(key) < 40 or any(c.isspace() for c in key): raise Refused('Unexpected key format')
    return key

def check_authorization(cfg):
    auth = read(ROOT/cfg['authorization'])
    a = auth['authorized']
    if not (cfg['allow_paid_api'] is True and a['paid_inference'] is True and a['model'] == cfg['model'] and a['client_side_spend_cap_usd'] >= cfg['spend_cap_usd'] and cfg['spend_cap_usd'] <= 3.0):
        raise Refused('Paid inference not authorized for this configuration')
    if urllib.parse.urlsplit(cfg['api_url']).hostname != cfg['api_host'] or cfg['api_host'] != 'openrouter.ai': raise Refused('Host not allowed')

class SpendLedger:
    """Global V173 spend ledger shared by all stages (file-backed so caps span processes)."""
    def __init__(self, path, cap, factor):
        self.path, self.cap, self.factor = Path(path), cap, factor
        if not self.path.exists(): write(self.path, {'spent_usd': 0.0, 'requests': 0, 'reported_cost_usd': 0.0, 'estimated_only_usd': 0.0, 'unknown_cost_requests': 0})
    def state(self): return read(self.path)
    def reserve(self, worst):
        s = self.state()
        if s['spent_usd']+worst > self.cap: raise Refused(f"Spend cap: spent {s['spent_usd']:.6f} + worst {worst:.6f} > {self.cap}")
    def record(self, reported, estimated):
        s = self.state(); s['requests'] += 1
        if reported is not None: s['spent_usd'] += max(reported, 0.); s['reported_cost_usd'] += max(reported, 0.)
        elif estimated is not None: s['spent_usd'] += estimated; s['estimated_only_usd'] += estimated
        else: s['unknown_cost_requests'] += 1; s['spent_usd'] += self.worst_default
        write(self.path, s); return s

class Client:
    def __init__(self, cfg, out, stage, provider, request_cap, spend_path):
        check_authorization(cfg); self.cfg, self.out, self.stage, self.provider = cfg, Path(out), stage, provider
        if provider not in cfg['provider_preference']: raise Refused('Provider not pre-registered')
        self.price_in, self.price_out = cfg['provider_prices_usd_per_token'][provider]
        self.key = load_key(cfg); self.request_cap = request_cap; self.requests = 0; self.started = time.monotonic()
        self.spend = SpendLedger(spend_path, cfg['spend_cap_usd'], cfg['cost_safety_factor'])
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def worst_case(self, body):
        est_in = math.ceil(len(json.dumps(body['messages']))/3)
        return (est_in*self.price_in+body['max_tokens']*self.price_out)*self.cfg['cost_safety_factor']

    def body(self, messages, schema, top_p, seed, max_tokens):
        return {'model': self.cfg['model'], 'messages': messages, 'temperature': self.cfg['temperature'], 'top_p': top_p, 'seed': seed, 'max_tokens': max_tokens,
                'reasoning': {'effort': self.cfg['reasoning_effort']}, 'response_format': {'type': 'json_schema', 'json_schema': {'name': 'proposals', 'strict': True, 'schema': schema}},
                'provider': {'order': [self.provider], 'allow_fallbacks': False, 'require_parameters': True}, 'usage': {'include': True}, 'stream': False}

    def send(self, body, identity, deadline):
        """One logical request. HTTP 429 (rejected before generation) is retried after the configured backoff (amendment 1);
        every attempt is recorded and charged to the ledger. Returns the final (status, response_json_or_None, error)."""
        if self.requests >= self.request_cap: raise Refused('Stage request cap')
        self.requests += 1; waits = list(self.cfg.get('rate_limit_backoff_seconds', []))
        while True:
            status, resp, err = self._attempt(body, identity, deadline, len(self.cfg.get('rate_limit_backoff_seconds', []))-len(waits))
            if status != 429 or not waits: return status, resp, err
            w = waits.pop(0)
            if time.monotonic()+w > deadline: return status, resp, err
            self.rate_limited = getattr(self, 'rate_limited', 0)+1; time.sleep(w)

    def _attempt(self, body, identity, deadline, rate_retry):
        if time.monotonic() > deadline: raise Refused('Stage wall cap')
        worst = self.worst_case(body); self.spend.worst_default = worst; self.spend.reserve(worst)
        record = {'identity': identity, 'stage': self.stage, 'at': now(), 'at_unix': time.time(), 'worst_case_usd': worst, 'rate_limit_retry': rate_retry, 'body': body}
        append(self.out/'requests.jsonl', record); t = time.monotonic(); resp = None; err = None; status = None
        req = urllib.request.Request(self.cfg['api_url'], data=json.dumps(body).encode(), headers={'Authorization': 'Bearer '+self.key, 'Content-Type': 'application/json'})
        try:
            with self.opener.open(req, timeout=min(self.cfg['request_timeout_seconds'], max(1., deadline-time.monotonic()))) as r: status = r.status; resp = json.loads(r.read())
        except urllib.error.HTTPError as e:
            status = e.code; err = f'HTTP {e.code}: '+e.read()[:2000].decode('utf8', 'replace')
        except Exception as e: err = repr(e)
        seconds = time.monotonic()-t; usage = (resp or {}).get('usage') or {}
        reported = usage.get('cost') if isinstance(usage.get('cost'), (int, float)) else None
        est = None
        if isinstance(usage.get('prompt_tokens'), int) and isinstance(usage.get('completion_tokens'), int):
            est = (usage['prompt_tokens']*self.price_in+usage['completion_tokens']*self.price_out)*self.cfg['cost_safety_factor']
        elif resp is None and err is not None and status is not None and 400 <= status < 500: est = 0.  # rejected before generation; still counted as a request
        spend = self.spend.record(reported, est)
        append(self.out/'responses.jsonl', {'identity': identity, 'stage': self.stage, 'at': now(), 'rate_limit_retry': rate_retry, 'http_status': status, 'seconds': seconds, 'error': err, 'response': resp,
                                            'reported_cost_usd': reported, 'estimated_cost_usd': est, 'cumulative_spent_usd': spend['spent_usd']})
        if resp is not None and self.provider_name_ok(resp) is False:
            raise Refused('Provider mismatch: '+str(resp.get('provider')))
        return status, resp, err

    def provider_name_ok(self, resp):
        name = resp.get('provider')
        if name is None: return None
        return name.lower().replace(' ', '') == self.provider.split('/')[0]

def content_of(resp):
    """Returns (content, finish_reason) from a chat completion, or raises ValueError."""
    ch = (resp or {}).get('choices') or []
    if len(ch) != 1: raise ValueError('Expected one choice')
    msg = ch[0].get('message') or {}; fr = ch[0].get('finish_reason')
    if fr != 'stop': raise ValueError(f'finish_reason {fr!r}')
    if not isinstance(msg.get('content'), str) or not msg['content'].strip(): raise ValueError('Empty content')
    return msg['content'], fr

"""V173 closeout: extend V172 counters with V173's measured ledgers (computed from files, not typed)."""
import json
from collect_smollm_v47 import ROOT, read, write, now
from analyze_v173 import stage_dirs
M = ROOT/'results/v173_models'

def main():
    old = read(ROOT/'artifacts/study_v172/closeout.json'); spend = read(M/'spend_ledger.json')
    rows = [json.loads(l) for s in stage_dirs() for l in (M/s/'responses.jsonl').read_text().splitlines()] if True else []
    in_flight = read(M/'A1'/'summary.json')['in_flight_without_response']
    generated = sum(r['http_status'] == 200 for r in rows); rate_limited = sum(r['http_status'] == 429 for r in rows); other = sum(r['http_status'] not in (200, 429) for r in rows)
    acq_a = read(ROOT/'results/v173_eval/completion.json')['acquisitions']; acq_b = read(M/'B_acquisitions'/'ledger.json')['acquisitions']
    snap = (ROOT/'artifacts/study_v173/openrouter_endpoints_snapshot.json').stat().st_size
    out = {'at': now(), 'stage': 'v173_snap2_model_hosted',
           'http_attempts_recorded': len(rows), 'http_attempts_in_flight_without_response': len(in_flight), 'responses_200': generated, 'rate_limited_429': rate_limited, 'other_http_errors': other,
           'new_generation_requests_counted': generated+len(in_flight), 'model_starts_cumulative': old['model_starts_cumulative']+generated+len(in_flight),
           'paid_spend_usd_reported': spend['spent_usd'], 'paid_spend_unknown_requests': len(in_flight), 'client_cap_usd': 3.0, 'owner_credit_usd': 5.0, 'key_reported_limit_usd_at_preflight': read(M/'P'/'summary.json')['key_info'].get('limit'),
           'provider_of_record': read(M/'P2'/'summary.json')['provider'], 'model': 'openai/gpt-oss-120b',
           'new_recorded_acquisitions': acq_a+acq_b, 'recorded_acquisition_charges_cumulative': old['recorded_acquisition_charges_cumulative']+acq_a+acq_b, 'historical_incidental_exposures': 2,
           'new_retained_download_bytes': snap, 'retained_download_bytes': old['retained_download_bytes']+snap, 'retained_download_cap_bytes': old['retained_download_cap_bytes'],
           'model_payload_bytes': old['model_payload_bytes'], 'caps_note': 'V172 download caps unchanged; V173 downloaded no weights',
           'authorization': 'artifacts/study_v173/authorization.json', 'cloud_resources': 0, 'publishing': 0}
    write(ROOT/'artifacts/study_v173/closeout.json', out); print(json.dumps(out, indent=1))

if __name__ == '__main__': main()

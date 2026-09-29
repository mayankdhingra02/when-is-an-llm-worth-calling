"""Render saved feasibility counts; deliberately no optimization-quality estimate."""
from collect_smollm_v47 import ROOT,read

def main():
    s=read(ROOT/'artifacts/study_v101/feasibility.json');l=s['ledger']
    usage='unknown' if s['total_generated_tokens'] is None else str(s['total_generated_tokens'])
    prefill='unknown' if s['total_actual_prefill_tokens'] is None else str(s['total_actual_prefill_tokens'])
    lines=['# V101: local model-loading feasibility','',
        f"Both-condition feasibility criterion passed: **{s['feasibility_passed']}**.",'',
        '| Intended condition | Status | Strict final answer valid |','|---|---|---|']
    lines += [f"| {c['key']} | {c['status']} | {c['valid']} |" for c in s['conditions']]
    lines += ['',f"Actual requests: {l['generation_requests']}; returned responses: {s['responses_returned']}; retries: {l['retries']}. Allocated output: {l['allocated_output_tokens']} of 768 tokens. Returned-response output sum: {s['returned_generated_tokens']}; all-request output total: {usage}. Actual prefill total: {prefill}. Missing responses remain unknown, not zero.",'',
        f"Lifecycle {l['stage_seconds']:.3f}s; startup {l.get('startup_seconds','unavailable')}s; peak sampled model RSS {l['peak_server_rss_bytes']:,}bytes; exit {l['server_exit_code']}; resource-stop reason {l['resource_stop_reason']}. Requests were serial with 120-second deadlines. The ten-minute stage cap and 8 GiB RSS guard were not raised.",'',
        'The server command is unchanged from V100: `--load-mode none` and the same limits, rerun after a user-performed Mac restart. The same pinned Qwen3-8B Q4_K_M model, 4096-token context, prompts, sampling and output limits were retained. A different execution environment and tiny sample prevent causal attribution or a general speed/reliability claim. No system settings or other applications were changed.','',
        'Zero new objective outcomes were acquired or scored. These two previously exposed development cases use different seeds: they are not a fair thinking-versus-nonthinking quality comparison, held-out validation or evidence of useful routing. No fallback quality is attributed to the model. V97 remains the latest complete optimization comparison.','',
        'Raw evidence: `results/v101_reasoning/`; frozen method/model/code: `reports/protocol_v101.freeze.json`; independent saved-evidence audit: `artifacts/study_v101/feasibility.json`. Run `.venv/bin/python scripts/audit_feasibility_v101.py` and this report script to replay without new inference or labels. Do not rerun the once-only collector into existing output.','']
    (ROOT/'reports/feasibility_v101.md').write_text('\n'.join(lines))
if __name__=='__main__':main()

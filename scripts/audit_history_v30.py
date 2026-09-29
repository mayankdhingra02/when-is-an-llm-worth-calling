"""Run historical checks with explicit archived V22 download-ledger identity.

The original audit predates the V30 source download. Verify its old ledger from
the before-admission archive, and independently require an append-only current
ledger with exactly the one recorded paper transfer. No scientific files change.
"""
import json
import audit_goal_completion as audit

def main():
    name = 'artifacts/download_ledger.json'
    archived = 'artifacts/history/v30_before_admission/' + name
    expected = audit.read('artifacts/study_v22/executed_evidence.json')['sha256'][name]
    audit.require(audit.sha(archived) == expected, 'Original V22 ledger identity')
    before, after = audit.read(archived), audit.read(name)
    source = audit.read('artifacts/study_v30/source.json')
    audit.require(after['transfers'][:-1] == before['transfers'], 'Unchanged historical transfers')
    transfer = after['transfers'][-1]
    audit.require(transfer['url'] == source['url'] and transfer['bytes_received'] == source['bytes'], 'Only new paper transfer')
    audit.require(after['accounted_bytes']-before['accounted_bytes'] == source['bytes'], 'Exact source byte delta')
    audit.require(after['model_bytes'] == before['model_bytes'], 'No model download')
    original_sha = audit.sha
    # Narrow substitution only for historical identity checks; never rewrite a file.
    audit.sha = lambda path: original_sha(archived if str(path) == name else path)
    try: audit.main()
    finally: audit.sha = original_sha

if __name__ == '__main__': main()

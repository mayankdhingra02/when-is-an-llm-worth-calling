# V39.1 packaging correction before repeated validation

The initial isolated V39 run failed because the allowlist omitted results/v22_larger/request_starts.jsonl needed by the historical verifier. The failed ZIP,build/execution logs and Python3.10 receipt remain under output/ and artifacts/reproduction_v39/. No new measured data or scientific conclusion arose from this failure.

V39.1 changes only the archive builder: include the prior request-start/runtime records and complete historical V34 result directory, as the earlier V35.1 builder did. The independent V39 verifier and all original experiment sources/results remain unchanged. Retain the original V39 freeze and add this supplement. Repeat the same predeclared two-interpreter isolated replay, ten corruption controls and byte-identical rebuild. No inference or acquisitions; costs and limits unchanged.

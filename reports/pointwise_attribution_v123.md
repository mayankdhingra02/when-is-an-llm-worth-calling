# V123 post-hoc attribution: numeric predictions and fixed ties

Repeated zero predictions were noticed during generation. This descriptive analysis was added after that observation. It changes no model inputs, selection rules, acquisitions or predeclared criteria. A tied cutoff uses the free fixed ID-order rule. We cannot infer how the model would rank tied configurations with a different prompt or output range.

| Family | At floor0 /20 | Distinct values | Cutoff | Tied at cutoff | Selected from tie | Same set as first-ten |
|---|---:|---:|---:|---:|---:|---|
| berkeleydb | 20 | 1 | 0.0 | 20 | 10 | True |
| dune_hsmgp | 14 | 2 | 0.0 | 14 | 10 | False |
| hipacc | 20 | 1 | 0.0 | 20 | 10 | True |

Selected-only outcome diagnostic (already charged labels):
- berkeleydb: 10selected floor predictions; 0actually beat the prefix best, while7were worse by more than0.05of the acquired prefix range.
- dune_hsmgp: 10selected floor predictions; 1actually beat the prefix best, while9were worse by more than0.05of the acquired prefix range.
- hipacc: 10selected floor predictions; 4actually beat the prefix best, while5were worse by more than0.05of the acquired prefix range.

This is conditioned on selected configurations and is not full-shortlist predictive accuracy. It uses only the10already charged continuation labels per family; no new objective probes.

These counts describe the measured adapter. Floor saturation may reflect the clipping contract, greedy numeric decoding, acquired examples, or model behavior; this experiment does not identify which cause dominates. Loss-removal responsiveness can coexist with uninformative within-condition rankings. A diagnostic pass alone is insufficient: the frozen quality comparison and cheap controls remain decisive. Further range/prompt changes would be another development adaptation and need a new protocol, not a reinterpretation of this test.

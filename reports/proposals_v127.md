# V127: full-domain feature proposals, exposed development

**Capacity correction:** The512-token cap cannot emit the required SAC representation (≥520tokens even before nonbinary settings/delimiters). Its six failures and the resulting impossible all-valid screen are design-caused. Raw results remain unchanged. All five families with valid normal outputs still have negative mean gains versus sequential3NN, and even an ideal SAC-only repair cannot make the overall primary means positive. See [capacity correction and repair bound](capacity_correction_v127.md).

Qwen3-8B proposes ten feature-setting strings from ten acquired examples and feature domains. Feature-only nearest-Hamming projection chooses valid unobserved configurations with frozen-order ties, sequentially excluding projected rows. No old shortlist or candidate IDs enter the model prompt. Matched random feature proposals use the identical projection. A new full-domain batch3NN arm and historical sequential/other controls share the same saved prefix. This is a constrained batch adaptation, not a complete SNAP2/LLAMBO reproduction.

| Comparator | Cases | Equal-family mean gain | Wins/ties/losses |
|---|---:|---:|---|
| batch_3nn | 30 | -2.889% | 2/16/12 |
| full_batch_3nn | 30 | -0.566% | 2/18/10 |
| full_sequential_3nn | 30 | -4.918% | 1/17/12 |
| presentation_first10 | 30 | 0.374% | 8/18/4 |
| random_full | 30 | -0.910% | 6/18/6 |
| random_projection | 30 | -0.855% | 5/21/4 |
| single_portfolio | 12 | -6.034% | 2/4/6 |

Normal valid responses: 25/30; six extra label-rotation probes retain their own validity status and acquire no new outcomes. Joint≥5%cases against sequential, random projection and full batch3NN: 0/30. Positive family means versus sequential: 0/6. Predeclared exploratory development screen met: False. Even passing would not establish generalization, novelty or journal readiness.

| Family | Gain vs sequential3NN | Gain vs random projection | Gain vs full batch3NN |
|---|---:|---:|---:|
| berkeleydb | -1.039% | -0.811% | -1.943% |
| dune_hsmgp | -21.032% | 0.312% | -0.247% |
| hipacc | -0.943% | 0.091% | 1.126% |
| llvm | -2.574% | -1.348% | -0.655% |
| openvpn | -3.786% | -3.641% | -1.676% |
| sac | -0.135% | 0.266% | 0.000% |

Projection audit: 250decoded proposals, 167with nonzero distance, 12repeated proposals, 20matching acquired configurations. Actual model-arm selections outside the old shortlist: 261/300 (includes declared fallback selections where any occur). Projection/duplicate behavior is preserved, not repaired by free model retries.

Actual cost: 36new real generation attempts, 36returned; 9361observed generated tokens with 0missing receipts; 18432allocated. Lifecycle 504.052s, peak sampled serverRSS 6,993,985,536bytes.900new recorded accesses across90pairedB20arms; all intended arms retained. Prefix/control costs remain historical. No retries, downloads, paid/cloud inference or new native execution.

Estimated deployment uses one model request (≤512output tokens) and ten new objective evaluations per escalation, plus projection/startup costs. The six rotation requests and extra paired research arms are collection overhead; they are not free deployment. No dollar or native-runtime savings are inferred. Missing usage is unknown, not zero.

All six families and all five seeds were retained, but are extensively exposed development data; seeds are grouped by family. V126hindsight maps and ranks never enter model/projection/baseline inputs. Prior wider-domain bounds motivated this intervention without selecting only favorable cases. Repeated proposals, projection constraints and tie-order can produce apparent gains without meaningful learned optimization; the matched cheap controls address that possibility in this assay. Rotation differences diagnose dependence on label assignment, not correctness or held-out benefit. No controller was fitted or held-out threshold tuned. Original correctness/equal-utility/noise and redistribution qualifications remain.

Source: existing owner model/runtime and V41data manifests; artifacts/study_v127freezes; results/v127_proposalsrawrequests; results/v127_analysischoices,chargedjournals,andcomparisons.

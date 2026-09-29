# STATUS — V101 post-restart feasibility partially restored

User restarted the Mac. Boot time and read-only memory counters saved in artifacts/study_v101/. Swap was zero before and during inference. V100 checkpoint verified before resuming; all prior failures remain preserved.

V101 repeated the identical two-condition feasibility configuration after restart. Two real Qwen3 requests: nonthinking returned a valid 20-token answer, thinking timed out at120s with no returned response. The separate thinking final-answer phase never ran. No new objective labels or quality scoring. Lifecycle137.293s, peak modelRSS5,954,420,736bytes, serverexit0. Allocated output640tokens. Actual total output/prefill usage unknown for the missing thought response. Returned-response output20 and prefill3306; partial progress in server logs is not a completed usage record. No retry, download or spending.

Saved-data audit passed. Four targeted guard/equivalence tests passed. V100's full771-test verification remains the last full suite; broader tests will follow any method change. Raw logs results/v101_reasoning; report reports/feasibility_v101.md; audit artifacts/study_v101/feasibility.json. Freeze SHA875cce3e1750f7807c157979455e71e7b49410cc81e08ce45657c782487fbdb7. Latest snapshot-aware integrity entrypoint scripts/seal_reasoning_v101.py --verify-only. Do not rerun old collectors into existing results.

Cumulative requests3,899; recorded-table acquisitions27,738; native numerical acquisitions790. Download/model payload totals unchanged; no external spending. All model processes exited. Prior root documents saved in artifacts/study_v101/previous_snapshot/.

Next: freeze a separately labeled smaller128-token thought allowance with the same128-token reserved final answer and unchanged120s deadline. Choose this using delivery/runtime evidence only; no objective outcomes have been inspected. Three-request feasibility cap remains, allocated-output cap reduces768 to384. Preserve V101 as failed both-condition feasibility, never as a successful reasoning trial.

V97 remains the latest complete optimization comparison. No useful learned routing, broader held-out-system generalization, independent-machine replication or Q2 readiness is established.

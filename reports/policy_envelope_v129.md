# V129 post-hoc routing ceiling

Exhaustively evaluated all 1024 binary escalation masks using the actual paired model/sequential3NN targets, with equal family weights. This is an evaluator-only, post-hoc diagnostic; no controller was fitted and no new model or objective calls were made. Fractions compute gains from serialized positive targets without a floating-point tie tolerance.

Policies with positive quality gain: **0**. Policies with exactly zero gain: **8** (including never-escalate). The hindsight oracle's mean gain is **0.000%**. Never-escalate dominates every nonempty mask in quality and model-call count: **True**. Tied-quality masks still make extra model requests. Random mixtures of these masks cannot have positive expected quality gain because expectations are convex combinations of the same nonpositive gains.

This result is restricted to these ten observed paired outcomes, this adapter/model/budget and these two exposed families. It is not a population guarantee, an untouched-system test, a calibrated risk bound or a claim about all LLM optimizers. The original six-family V127 study retained a positive exception and used a different output contract; it is not silently pooled into this certificate. No statistical independence is assigned to seeds. No native-time, energy or dollar saving is inferred.

![Hindsight envelope](../results/v129_analysis/policy_envelope.png)

Evidence: results/v129_analysis/policy_envelope.json retains every mask, exact rational gain, call count, case order and source hash. Run `.venv/bin/python scripts/policy_envelope_v129.py` to reproduce. This diagnostic explains why fitting a benefit router on these outcomes cannot demonstrate a quality gain over never-escalate; it does not validate any learned router.

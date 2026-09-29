# Research assessment after V121–V122

## Supported result

The newest evidence supports a narrow negative contribution: **apparent local-LLM continuation gains can be entirely reproduced by a zero-inference ordering rule, and a development-trained escalation controller can still select those calls.** WordCount provided five exact first-ten identities; the prospectively frozen MongoDB replication provided five more. Both observations concern the particular Qwen3-8B constrained configuration-selection adapter, not all LLM optimization. The ten seeds span two software families; WordCount was exploratory development, MongoDB was one prospective held-out family.

V121 collected100 real requests/400 recorded acquisitions, including paired loss removal; V122 added50 acquisitions using five provenance-checked real cached responses, with zero new requests. All intended cases were retained. Normal MongoDB gains were+0.729%vs batch3NN,+0.540%vs sequential3NN and0%vs first-ten. The first-ten-target router escalated5/5 with zero gain; its uncertainty counterpart also escalated5/5. The original-control-target router chose0/5. Four of five loss-removal cases preserved selections; one changed, so blanket claims of ignoring observations are false.

The cached configuration-string projection is not a rescue: it gains1.092%against batch but loses0.631%against sequential and9.465%against first-ten, with0/5 joint5%wins. Twenty of50proposals required projection;13nearest choices had already been used. This was explicitly development-only; original V119 strict-parser failures remain unchanged. Stop this stage rather than altering projection to fit the exposed outcomes.

## How this relates to prior evidence

The same-adapter context now covers40 paired optimization cases across eight families:30 V91 cases, five V120 WordCount cases and five normal V121 MongoDB cases. Seven families were used for development, only MongoDB for the new prospective test. Do not call the pooled40 a fresh held-out sample. Historical LLM gains over first-ten are nonzero in some V91 cases, including a6.603%family mean for Dune/HSMGP; the model is not universally equivalent to the rule.

Prior V92 loss/order/relabel interventions used three different development families and found partial loss responsiveness but failed the joint stability screen. Prior V93 native-decoder answers matched forced configuration sets for all53returned pairs, with one retained resource failure. Therefore simply removing the forced decoder is not a new untested explanation. V114's repeated nonthinking continuations and V117's influence analysis remain separate; do not pool all methods as one policy or select whichever wins per family.

The experimental contribution is budget-matched attribution and a prospectively evaluated controller failure, supported by exact traces and cheap controls. It is not a new discovery that language models have positional biases, a proof that LLMs are useless, or a positive generalizing routing method.

## Focused primary-source check (27 September2026)

- [Liu, Astorga, Seedat and van der Schaar, Large Language Models to Enhance Bayesian Optimization, arXiv2402.03921v2](https://arxiv.org/abs/2402.03921v2), ICLR2024: primary abstract and metadata checked. LLAMBO uses contextual warmstarting, surrogates and candidate sampling. Our nominal finite-domain ID-selection adaptation does not replicate that architecture and cannot refute its claims. Full new-method comparison was not executed.
- [Rychert, Spagnolo and Posashkov, Reproducibility Study of Large Language Model Bayesian Optimization, arXiv2511.18891v1](https://arxiv.org/abs/2511.18891v1): primary abstract/metadata checked; it reports successful70B replication and instability/invalid predictions for smaller backbones. The abstract incorrectly attributes the original LLAMBO to Daxberger; the original metadata lists Liu and colleagues. Do not propagate that attribution. This is related prior evidence, not an independently audited reproduction of that reproduction.
- [Wang et al., Large Language Models are not Fair Evaluators, ACL2024](https://aclanthology.org/2024.acl-long.511/): primary publisher abstract/metadata checked. Candidate-order bias in LLM evaluation is already established. Our incremental claim concerns charged software-optimization continuations, a free ordering control and escalation errors; novelty of that combination is not established by a bounded search.

Search discovery also returned secondary pages, non-SE hiring examples and a recent survey; they were not used to establish technical claims. No source-install scripts, credentials or external messages were used. This focused check is not a comprehensive systematic literature review.

## Readiness and next decision

There is now a reproducible, technically discussable negative-result study candidate. It is not evidence sufficient to claim the original benefit-aware router works or that a Q2 journal will accept it. Remaining weaknesses are one prospective test family, a constrained local-model adaptation, known source measurement limitations, no clean-machine fresh-inference replication, and uncertain incremental novelty over existing ablation/reproducibility work. A journal-quartile label cannot resolve these gaps.

The most important next research action is to test an explicitly different, task-grounded adapter on development groups against first-ten and strong classical controls, before reserving a further independent-family evaluation. Do not immediately consume another held-out family with the same failed adapter, relabel MongoDB as unseen again, or repeat V93's already completed decoder comparison. A candidate must demonstrate incremental value attributable to inference, not merely outperform a weak original comparator. Alternatively, retain the negative-result scope and prioritize independent reproduction and a broader source-grounded external evaluation of that fixed claim. Original-run/native correctness requires separate validation; it cannot be manufactured by replaying tables.

Both bounded stages are complete at their declared limits. No model server is running; no cloud spending, publishing, remote push, author contact or future background work is implied. `output/v121_replay.zip` is a private~392KB standard-library saved-evidence replay, already executed in isolated Python. It does not contain model weights or certify a fresh inference run. All research collection costs and original failures remain in the historical chain.

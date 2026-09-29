# V49 — focused primary-source check and contribution boundary

Checked 2026-09-25 after collection. This check changes interpretation, not the
frozen experiment or its pass/fail rule. It is a focused audit, not a systematic
review or proof that an SE-specific contribution is novel.

| Primary source and inspected version | Verified overlap | Consequence for this project |
|---|---|---|
| Chujie Zheng, Hao Zhou, Fandong Meng, Jie Zhou, Minlie Huang. *Large Language Models Are Not Robust Multiple Choice Selectors*, ICLR 2024. [Official proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/54dd9e0cff6d9214e20d97eb2a3bae49-Abstract-Conference.html). Publication metadata and abstract inspected. | Option-ID preference and sensitivity to option position were already studied; PriDe was proposed to address token bias. | Do not claim discovery of option-selection bias. Our display reversal versus ID rotation separates two interventions locally; it does not establish a new general theory. |
| Pouya Pezeshkpour, Estevam Hruschka. *Large Language Models Sensitivity to The Order of Options in Multiple-Choice Questions*, Findings of NAACL 2024, pp. 2006–2017, DOI 10.18653/v1/2024.findings-naacl.130. [Official paper](https://aclanthology.org/2024.findings-naacl.130.pdf), sections 2–4 inspected. | The study varies option ordering in multiple-choice tasks and examines position effects, uncertainty and calibration. | Order sensitivity alone is not a sufficient novelty claim. Their oracle accuracy-gap metric differs from our mapped ten-configuration overlap; do not compare percentages as if equivalent. |
| Xinpeng Wang, Chengzhi Hu, Bolei Ma, Paul Röttger, Barbara Plank. *Look at the Text: Instruction-Tuned Language Models are More Robust Multiple Choice Selectors than You Think*, COLM 2024; [arXiv v2, 20 August 2024](https://arxiv.org/html/2404.08382v2), sections 2–3 inspected; venue confirmed by [author institution](https://mcml.ai/publications/whm24/). | First-token probability choices can disagree with generated text answers; robustness differs with that mismatch and model. Their extraction includes a trained answer classifier. | Decoder/evaluation effects are established prior work. Our 53/53 valid set agreement is a limited observation for SmolLM3 and this prompt, not a refutation. We use strict parsing and ten selections from twenty, not their learned single-answer extractor. |

OpenReview PDF retrieval returned a browser-verification challenge for the first
and third papers. Used official proceedings metadata for the first and original
arXiv v2 for the third. No challenge was bypassed or credentials used. The first
paper's arXiv v2 has a different title (*On Large Language Models’ Selection Bias
in Multi-Choice Questions*); do not silently equate that version with the final
ICLR document. No third-party code was installed, copied or executed in this audit.

The defensible current observation is narrower: this small-model software
configuration-selection adaptation exhibits harmful/weak optimization results
against strong controls (V41/V44/V47), and its SmolLM3 selections show presentation
sensitivity that survives a removal of grammar and forced delimiters (V48/V49).
This is evidence about our adaptation, not a numerical SNAP2 replication or a
claim that LLM optimization cannot work. A controller cannot rescue useful
benefit that its intervention has not demonstrated.

A possible empirical contribution combines strict cost accounting, independently
replayed paired traces, strong classical comparators, candidate-pool ceilings,
and loss/order/decoder controls. Whether that combination is sufficiently novel
or broad for a journal remains unresolved. These controls should accompany any
future beneficial optimizer; having them is not itself a publication guarantee.

Priority now: audit the underlying benchmark's application-quality/correctness
constraints and define an independently grouped, utility-matched comparison.
Existing exposed cases cannot become fresh confirmation. Preserve the stopped
ID-selection pipeline as a negative baseline. Do not fund another wording or
small-decoder variation merely to find a favorable mean. Reasoning-enabled
inference, larger models and domain-informed configuration proposals remain
untested possibilities, not scheduled experiments or proven remedies.

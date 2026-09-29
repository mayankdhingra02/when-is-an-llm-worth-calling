# V114: fixed-prefix sampling reliability

Executed **36 real local model requests** for36intended replicas of12saved prefixes from six exposed software groups. Returned 36responses; 36valid final selections, 0fallback-policy conditions, 0unattempted conditions. Scoring acquired **360recorded outcomes**, independently charging ten per replica after its original ten-label prefix. These are real model responses and recorded-table acquisitions, not new native runtime measurements.

**0/36** intended replicas produced a valid>=5%gain over BOTH strong classical controls. Full fallback-policy mean gain, averaging within prefix and then equally across groups: **-2.67%** versus batch3NN and **-6.45%** versus sequential3NN.

|Software group|Mean gain vs batch3NN|Mean gain vs sequential3NN|
|---|---:|---:|
|berkeleydb|-0.12%|+2.56%|
|dune_hsmgp|-0.21%|-21.76%|
|hipacc|+0.81%|-2.59%|
|llvm|+0.00%|-0.29%|
|openvpn|-16.51%|-16.60%|
|sac|+0.00%|+0.00%|

## What varies at the same checkpoint

4/12prefixes produced more than one valid selected configuration set; 2/12produced more than one final incumbent value. Joint>=5%benefit classification changed across valid replicas for 0/12prefixes. Exact-set agreement, pairwise Jaccard, all min/max gains and valid/fallback denominators are saved for every prefix. Each group still contributes only one group to the evidence, regardless of response count.

|Prefix|Valid replicas|Distinct selected sets|Distinct final values|Mean Jaccard|Valid joint>=5%wins|
|---|---:|---:|---:|---:|---:|
|BDBC_AllNumeric_11|3/3|3|1|0.624|0/3|
|BDBC_AllNumeric_37|3/3|1|1|1.000|0/3|
|Dune_AllNumeric_11|3/3|1|1|1.000|0/3|
|Dune_AllNumeric_37|3/3|1|1|1.000|0/3|
|LLVM_AllNumeric_11|3/3|1|1|1.000|0/3|
|LLVM_AllNumeric_37|3/3|1|1|1.000|0/3|
|OpenVPN_11|3/3|1|1|1.000|0/3|
|OpenVPN_37|3/3|1|1|1.000|0/3|
|hipacc_AllNumeric_11|3/3|2|2|0.333|0/3|
|hipacc_AllNumeric_37|3/3|2|2|0.879|0/3|
|sac_AllNumeric_11|3/3|2|1|0.333|0/3|
|sac_AllNumeric_37|3/3|1|1|1.000|0/3|

## Actual collection cost and scope

Model lifecycle 293.705s; peak sampled RSS 6,808,207,360bytes. Allocated output tokens 4608; returned generated tokens 720; actual reported prefill tokens 59286; summed full contexts 59286. Missing request usage:0; retries:0. No new downloads or external spending. Prefix/control acquisition and historical inference costs remain in their old ledgers; they are not newly measured or free.

One deployed continuation would select one answer and spend ten new outcomes after its ten-outcome prefix. Running three candidates here costs three requests and thirty continuation acquisitions per prefix; selecting the best response after scoring all three would exceed that deployment budget. No best-seed deployment result is claimed. Model startup is reported separately in the raw ledger; electricity/hardware cost remains unknown.

All messages, candidate order, model/runtime, parser, prompt scaffold and nonthinking parameters were fixed. Only the model sampling seed changes within a prefix. Runtime nondeterminism may still contribute, and three samples cannot estimate a calibrated benefit probability. No new router was fit, no prompt was selected by outcomes, and historicalV103responses are not pooled into the primary sample.

This is an exploratory robustness result on six already exposed groups, two optimization seeds per group, one local model bundle and one host. It does not create36independent tasks, establish a population guarantee, resolve public-data contamination, or demonstrate useful benefit-aware routing. Native timing qualifications fromV113remain separate. A journal tier is not measured by the experiment.

![All36intended replica outcomes](../results/v114_analysis/sampling.png)

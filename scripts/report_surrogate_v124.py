"""Replay the frozen analysis with a documented wording-only correction.

The frozen generator mistakenly lists the model among changes from V123.
Both versions used the same Qwen3-8B model. No data/criterion/code is changed.
"""
from analyze_surrogate_v124 import report,ROOT

def main():
 report();p=ROOT/'reports/surrogate_v124.md';text=p.read_text();old='The model, JSON serialization, raw target contract, stochastic decoding and batch acquisition differ from V123; this is not a one-factor causal ablation.';new='The Qwen3-8B model and runtime are unchanged from V123. Prompt fields, raw target scale, stochastic decoding and batch acquisition differ; this is not a one-factor causal ablation.'
 assert text.count(old)==1;text=text.replace(old,new)
 note='**Interpretation correction:** Existing V42 hindsight bounds show that no case in this fixed shortlist cohort can meet the joint 5% quality criterion. These runs measure implementation/reliability and actual outcomes, but cannot fairly test that improvement hypothesis. See [attainability audit](attainability_v125.md); old raw results and the frozen criterion are unchanged.\n\n'
 title,rest=text.split('\n\n',1);p.write_text(title+'\n\n'+note+rest)
if __name__=='__main__':main()

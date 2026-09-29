"""V180: run the V176 table and text checks against the prose-revised manuscript (paper/overleaf_v180/main.tex).

Identical to check_tables_v176 except for the file checked and one merged sentence: V180 joins the two Spark Bayes
sentences, so the two phrases are rebuilt as one from the same recomputed values.
"""
import re, sys
import check_tables_v176 as base
from collect_smollm_v47 import ROOT

base.TEX = ROOT/'paper/overleaf_v180/main.tex'
_orig = base.text_phrases

def text_phrases(b, v174, v175):
    p = _orig(b, v174, v175)
    x = re.search(r'by (\d+\.\d)\\% in both one-shot draws', p[-2]).group(1)
    y, z = re.search(r'by (\d+\.\d)\\% in the loop, and GP-EI by (\d+)\\%', p[-1]).groups()
    return p[:-2]+[f'It beat the reference by {x}\\% in both one-shot draws and by {y}\\% in the loop, where it also beat GP-EI by {z}\\%']

base.text_phrases = text_phrases

if __name__ == '__main__': base.main()

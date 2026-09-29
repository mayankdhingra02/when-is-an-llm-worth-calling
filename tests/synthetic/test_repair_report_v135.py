"""Synthetic regressions for partial historical comparator availability."""
import sys
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from report_repair_v135 import summarize_comparators

def test_optional_comparator_keeps_actual_denominator():
 rows=[{'target':90,'references':{'full_sequential_3nn':100,'single_portfolio':100}}, {'target':210,'references':{'full_sequential_3nn':200}}]
 r=summarize_comparators(rows)
 assert r['full_sequential_3nn']['cases']==2
 assert Fraction(r['full_sequential_3nn']['mean_fraction'])==Fraction(1,40)
 assert r['full_sequential_3nn']['wins']==r['full_sequential_3nn']['losses']==1
 assert r['single_portfolio']['cases']==1 and Fraction(r['single_portfolio']['mean_fraction'])==Fraction(1,10)

def test_comparator_missing_first_case_is_retained():
 r=summarize_comparators([{'target':10,'references':{'a':10}}, {'target':10,'references':{'a':10,'b':20}}])
 assert r['a']['cases']==2 and r['a']['ties']==2 and r['b']['cases']==1

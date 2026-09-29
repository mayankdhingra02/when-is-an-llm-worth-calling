import pytest
from escalation.planning_v55 import Task, parse
D = '''(define (domain fixture) (:requirements :typing :action-costs)
(:types item place) (:predicates (at ?x - item ?p - place) (done ?x - item))
(:functions (total-cost) - number (fee ?p - place) - number)
(:action finish :parameters (?x - item ?p - place)
:precondition (and (at ?x ?p) (not (done ?x)))
:effect (and (not (at ?x ?p)) (done ?x) (increase (total-cost) (fee ?p)))))'''
P = '''(define (problem synthetic) (:domain fixture) (:objects a - item b - place)
(:init (at a b) (= (total-cost) 0) (= (fee b) 7))
(:goal (done a)) (:metric minimize (total-cost)))'''

def test_valid_cost_and_isolated_state():
    t = Task(D, P)
    assert t.validate('(finish a b) ; cost = 999')['cost'] == '7'
    assert t.validate('(finish a b)')['cost'] == '7'

@pytest.mark.parametrize('plan', ['', '(finish b a)', '(finish a b)(finish a b)',
                                 '(finish a)', '(unknown a b)', '(finish a b'])
def test_reject_invalid_plan(plan):
    with pytest.raises(ValueError):
        Task(D, P).validate(plan)

@pytest.mark.parametrize('domain', [D.replace('(at ?x ?p) (not', '(or (at ?x ?p)) (not'),
    D.replace('(done ?x) (increase', '(when (done ?x) (done ?x)) (increase'),
    D.replace('(fee ?p)))', '(total-cost)))')])
def test_reject_unsupported_domain_before_plan(domain):
    with pytest.raises(ValueError):
        Task(domain, P)

def test_zero_cost_and_missing_numeric():
    assert Task(D.replace('(fee ?p)', '0'), P).validate('(finish a b)')['cost'] == '0'
    with pytest.raises(ValueError):
        Task(D, P.replace('(= (fee b) 7)', '')).validate('(finish a b)')

def test_unknown_cost_or_task():
    with pytest.raises(ValueError):
        Task(D, P.replace('7)', '-1)'))
    with pytest.raises(ValueError):
        Task(D, P.replace('(:domain fixture)', '(:domain other)'))

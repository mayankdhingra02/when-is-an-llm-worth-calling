from escalation.h2_v81 import grid,expected,PROFILES,ORDER

def test_small_exact_answers():
    x=expected(2)
    assert x[0,0]==(1,0)
    assert x[1,0]==(1,0)
    assert x[2,0]==(2,7919)
    assert x[2,1]==(0,0)

def test_domain_and_prior():
    g=grid();assert len(g)==336 and len({tuple(c.values()) for c in g})==336
    assert all(bin(c['mask']).count('1')<=3 for c in g)
    assert all(p in g for p in PROFILES.values())
    assert {p:ORDER.count(p) for p in PROFILES}==dict(reference=3,prior=3,contrast=3)

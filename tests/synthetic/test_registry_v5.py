import itertools
import pytest
from escalation.registry_v5 import inspect,metadata_values,family,feature_model_mismatch
from escalation.finite_domain import FiniteCandidates,modal_centroid,encode_indices,decode_indices,uniform_proposals,recommend
from escalation.core import initial_state,recommend as binary_recommend
from escalation.data import Oracle


def test_source_schema_excludes_objective_payloads_and_metadata(tmp_path):
    p=tmp_path/'test.csv'
    p.write_text('real_INDEX,level,revision,performance\n0,9,v1,DO_NOT_READ\n1,3,v1,SECRET\n0,4,v2,SECRET\n')
    s=inspect(p,['performance'],['revision'],filters={'revision':'v1'})
    assert s['feature_names']==['real_INDEX','level']
    assert s['unique_configurations']==2 and s['objective_values_inspected'] is False
    p.write_text(p.read_text().replace('DO_NOT_READ','9').replace('SECRET','-100'))
    assert s==inspect(p,['performance'],['revision'],filters={'revision':'v1'})
    assert metadata_values(p,'revision')==['v1','v2']
    with pytest.raises(ValueError):inspect(p,[])
    with pytest.raises(ValueError):inspect(p,['performance'],filters={'performance':'9'})


def test_feature_alias_match_needs_values_and_names(tmp_path):
    a=tmp_path/'a.csv';b=tmp_path/'b.csv'
    a.write_text('A_flag,B,$target\n0,3,SECRET\n1,4,SECRET\n')
    b.write_text('$b,aFlag,outcome\n4,1,OTHER\n3,0,OTHER\n')
    assert inspect(a,['$target'])['feature_identity_sha256']==inspect(b,['outcome'])['feature_identity_sha256']
    b.write_text(b.read_text().replace('3,0','2,0'))
    assert inspect(a,['$target'])['feature_identity_sha256']!=inspect(b,['outcome'])['feature_identity_sha256']


def test_conservative_family_aliases():
    assert family('BDBC')==family('BDBJ')
    assert family('VP8')==family('VP9')
    assert family('MySQL')==family('MariaDB')
    assert family('Dune')==family('hsmgp')
    assert family('Apache_AllMeasurements')!=family('storm')
    assert family('X264')==family('X264_AllMeasurements')


def test_missing_feature_model_option_is_not_dropped(tmp_path):
    p=tmp_path/'model.xml'
    p.write_text('<vm><binaryOptions><configurationOption><name>real_INDEX</name></configurationOption></binaryOptions></vm>')
    assert feature_model_mismatch(p,['real_INDEX']) is None
    assert feature_model_mismatch(p,['real_INDEX','undocumented'])=={'model_only':[],'table_only':['undocumented']}


def test_finite_requires_one_named_objective():
    x=tuple(itertools.product((0.,1.),repeat=5))
    with pytest.raises(ValueError):FiniteCandidates(tuple('abcde'),x,('runtime','energy'),('-',),tuple(range(32)))


def finite_fixture():
    x=tuple(itertools.product((0.,1.),(1.,4.,9.),(16.,32.,64.,128.)))
    return FiniteCandidates(('flag','mode','size'),x,('runtime',),('-',),tuple(range(len(x))))


def test_finite_codec_domains_rejection_and_nominal_centroid():
    c=finite_fixture();proposal=[1.,9.,64.]
    assert decode_indices(c,encode_indices(c,proposal))==proposal
    assert modal_centroid(c,[0,1])==(0.,1.,16.)
    for bad in [[0,0,True],[0,0,-1],[0,3,0],[1],[0,0,1.0]]:
        with pytest.raises(ValueError):decode_indices(c,bad)
    assert uniform_proposals(c,11)==uniform_proposals(c,11)


def test_finite_baseline_budget_and_binary_compatibility():
    c=finite_fixture();s=initial_state(c,11);o=Oracle(tuple((float(i),) for i in range(len(c.x))))
    for _ in range(20):
        i=recommend(c,s);s.observe(i,o.acquire(i),c.directions)
    assert o.new_accesses==20 and len(set(s.ids))==20
    x=tuple(itertools.product((0.,1.),repeat=5))
    b=FiniteCandidates(tuple('abcde'),x,('loss',),('-',),tuple(range(32)))
    s=initial_state(b,23);o=Oracle(tuple((float(i),) for i in range(32)))
    for _ in range(20):
        assert recommend(b,s)==binary_recommend(b,s)
        i=recommend(b,s);s.observe(i,o.acquire(i),b.directions)

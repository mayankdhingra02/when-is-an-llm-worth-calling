"""Synthetic metadata only; tests never produce research measurements."""
import csv
import io
import pytest
from escalation.external_admission_v14 import META_FIELDS, metadata_rows, coverage_audit


def row(**changes):
    base = dict(zip(META_FIELDS, ['input', 'owner/input', 'zstd', '3', 'frame', '1.0',
                               '1048576', '1', '1', 'False', 'a'*64, 'ok']))
    return dict(base, **changes)


def test_repetitions_and_workloads_do_not_inflate_configuration_coverage():
    rows=[row(dataset=f'file{w}', repetition=str(r)) for w in range(15) for r in range(5)]
    result=coverage_audit(rows, {})
    assert result['contexts']==15 and result['measured_rows']==75
    assert all(r['distinct_measured_configurations']==1 for r in result['records'])
    assert result['contexts_supporting_budget']==0


def test_runtime_values_are_never_returned_or_parsed():
    stream=io.StringIO()
    fields=list(META_FIELDS)+['compression_ns', 'compressed_bytes']
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    writer.writerow(dict(row(),compression_ns='NOT_A_NUMBER',compressed_bytes='SECRET_OUTCOME'))
    stream.seek(0)
    rows=list(metadata_rows(stream))
    assert set(rows[0])==set(META_FIELDS)
    assert 'SECRET_OUTCOME' not in str(coverage_audit(rows,{}))


def test_warmups_do_not_count_as_measured_configurations():
    rows=[row(level=str(level),warmup='True') for level in range(20)]+[row()]
    result=coverage_audit(rows,{})
    assert result['warmup_rows']==20 and result['contexts_supporting_budget']==0


def test_unknown_execution_revision_is_not_repaired_by_download_pin():
    result=coverage_audit([row()], {'git_commit':'unknown','git_dirty':None,'download_commit':'a'*40})
    assert not result['clean_execution_revision_identified']
    assert not result['admitted_for_collection']


def test_failure_rows_stay_in_denominator_and_duplicate_ids_fail():
    result=coverage_audit([row(status='error'),row(repetition='2')],{})
    assert result['raw_rows']==2 and result['records'][0]['status_counts']=={'error':1,'ok':1}
    with pytest.raises(ValueError,match='Duplicate measurement'):
        coverage_audit([row(),row()],{})


def test_missing_metadata_fails_closed():
    with pytest.raises(ValueError,match='Missing configuration'):
        list(metadata_rows(io.StringIO('codec,compression_ns\nzstd,10\n')))

"""Structural audit; objective cells are neither returned nor used for admission."""
import csv, hashlib, json, sys, zipfile
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'artifacts/sources/v146'
ART = ROOT / 'artifacts/study_v146'
def main():
    for receipt in BASE.glob('*_receipt.json'):
        d = json.loads(receipt.read_text())
        assert d['error'] is None
        for f in d['files']:
            b = (ROOT/f['path']).read_bytes()
            assert len(b) == f['bytes'] and hashlib.sha256(b).hexdigest() == f['sha256']
            if 'git_sha' in f:
                assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == f['git_sha']
            if 'expected_sha256' in f:
                assert hashlib.sha256(b).hexdigest() == f['expected_sha256']
    wheel = BASE/'xlrd/xlrd-2.0.1-py2.py3-none-any.whl'
    assert hashlib.sha256(wheel.read_bytes()).hexdigest() == '6a33ee89877bd9abc1158129f6e94be74e2679636b8a205b43b85206c3f0bbdd'
    sys.path.insert(0, str(wheel))
    import xlrd
    schemas = {}
    for p in sorted((BASE/'ptss').glob('*.xls')):
        book = xlrd.open_workbook(str(p))
        schemas[p.name] = [{'sheet':s.name, 'rows':s.nrows, 'columns':s.ncols,
                            'header':s.row_values(0) if s.nrows else []} for s in book.sheets()]
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for p in sorted((BASE/'ptss').glob('*.xlsx')):
        with zipfile.ZipFile(p) as z:
            strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
            rows=ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:row',ns)
            schemas[p.name]={'rows':len(rows), 'header':strings[:6]}
    groups=defaultdict(set); valid=defaultdict(set); presence=defaultdict(lambda: [0,0])
    with (BASE/'hyrise/data/benchmark/runtimes.csv').open() as f:
        for r in csv.DictReader(f):
            context=tuple(r[k] for k in ['SCAN_COLUMN','SELECTIVITY','SCAN_TYPE'])
            config=tuple(r[k] for k in ['ORDER_BY','ENCODING','INDEX'])
            groups[context].add(config)
            if r['INDEX']=='0' or r['ENCODING']=='0':valid[context].add(config)
            # Presence only: do not parse, rank, average or display TIME values.
            presence[context][int(bool(r['TIME'].strip()))]+=1
    d={'ptss':{'schemas':schemas,'decision':'not admitted: metric and parameter definitions, not configuration/outcome measurements'},
       'hyrise':{'fixed_contexts':len(groups),'raw_config_counts':sorted(set(map(len,groups.values()))),
                 'valid_config_counts':sorted(set(map(len,valid.values()))),
                 'decision':'not admitted: upstream dictionary-only index rule leaves 36 valid settings per fixed scan, below unchanged 40-setting rule',
                 'target_presence_counts':{'missing':sum(x[0] for x in presence.values()),'present':sum(x[1] for x in presence.values())}},
       'cassandra':{'decision':'not admitted: inspected 23-parameter WLA 2000 log supplies elites/aggregate best costs, not the complete per-candidate per-instance matrix; throughput file supplies repeated final-configuration tests. No Rdata/raw matrix appears in pinned tree. Replication-factor changes also require utility review.',
                    'scope':'one representative log and test file plus complete pinned file inventory; do not claim every other log inspected'},
       'objective_acquisitions':0,'model_requests':0,'candidate_objective_values_displayed':0,
       'saved_bytes':sum(json.loads(p.read_text())['saved_bytes'] for p in BASE.glob('*_receipt.json'))}
    (ART/'audit.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d,indent=2))
if __name__=='__main__':main()

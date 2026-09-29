"""Outcome-blind feature auditing across explicit source schemas.

The caller must identify objective/metadata columns from primary documentation.
This module never reads those cells, except declared metadata row filters.
"""
import csv,hashlib,json,math,re
import xml.etree.ElementTree as ET
from pathlib import Path


def normalized_name(name):
    return re.sub(r'[^a-z0-9]','',name.lower())


def feature_model_mismatch(path, feature_names):
    model=ET.parse(path)
    names={e.findtext('name') for e in model.findall('./binaryOptions/configurationOption')}
    names.update(e.findtext('name') for e in model.findall('./numericOptions/configurationOption'))
    actual=set(feature_names)
    if names==actual:return None
    return {'model_only':sorted(names-actual),'table_only':sorted(actual-names)}


def inspect(path, objectives, metadata=(), delimiter=',', filters=None):
    if not objectives:raise ValueError('explicit objective column names required')
    filters=filters or {}
    with Path(path).open(newline='') as f:
        reader=csv.reader(f,delimiter=delimiter);header=[v.strip() for v in next(reader)]
        if len(header)!=len(set(header)):raise ValueError('duplicate headers')
        if not set(objectives).union(metadata).union(filters)<=set(header):raise ValueError('declared schema column absent')
        if set(objectives)&(set(metadata)|set(filters)):raise ValueError('objective cannot be metadata/filter')
        names=[h for h in header if h not in set(objectives)|set(metadata)]
        indices=[header.index(h) for h in names];fi={header.index(k):str(v) for k,v in filters.items()}
        rows=[];raw=0;invalid=0
        for row in reader:
            if len(row)!=len(header):raise ValueError('ragged table')
            if any(row[j].strip()!=v for j,v in fi.items()):continue
            raw+=1
            try:
                x=tuple(float(row[j]) for j in indices)
                if not all(math.isfinite(v) for v in x):raise ValueError()
            except ValueError:invalid+=1;continue
            rows.append(x)
    unique=sorted(set(rows));domains=[sorted({x[j] for x in unique}) for j in range(len(names))]
    canonical=[normalized_name(n) for n in names]
    if len(set(canonical))!=len(canonical):raise ValueError('ambiguous normalized feature names')
    order=sorted(range(len(names)),key=lambda j:canonical[j])
    payload={'names':[canonical[j] for j in order], 'rows':sorted({tuple(x[j] for j in order) for x in unique})}
    fingerprint=hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest()
    return {'feature_names':names,'objective_names':list(objectives),'metadata_columns':list(metadata),
            'row_filters':filters,'raw_rows':raw,'unique_configurations':len(unique),
            'duplicates':len(rows)-len(unique),'invalid_feature_rows':invalid,
            'feature_domains':domains,'binary':bool(domains) and all(set(d)<={0.,1.} for d in domains),
            'feature_identity_sha256':fingerprint,'objective_values_inspected':False}


def metadata_values(path, column, delimiter=','):
    with Path(path).open(newline='') as f:
        reader=csv.reader(f,delimiter=delimiter);header=next(reader);j=header.index(column)
        return sorted({row[j].strip() for row in reader})


def family(name):
    # Conservative related-product grouping. No claim of independent versions.
    name=name.lower()
    return {'bdbc':'berkeleydb','bdbj':'berkeleydb','berkeleydb_c':'berkeleydb',
            'mariadb':'mysql_family','mysql':'mysql_family','vp8':'libvpx','vp9':'libvpx',
            'dune':'dune_hsmgp','hsmgp':'dune_hsmgp','sql':'sqlite',
            'apache_allmeasurements':'apache','sql_allmeasurements':'sqlite',
            'x264_allmeasurements':'x264','7z':'7zip'}.get(name,name)


def schema_reasons(schema,max_features=39,max_rows=5000,binary=True):
    reasons=[]
    if schema['invalid_feature_rows']:reasons.append('invalid_feature_values')
    if not 1<=len(schema['feature_names'])<=max_features:reasons.append('feature_count')
    if not 20<=schema['unique_configurations']<=max_rows:reasons.append('row_count')
    if binary and not schema['binary']:reasons.append('nonbinary')
    return reasons

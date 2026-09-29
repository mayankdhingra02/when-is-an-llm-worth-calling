"""Outcome-blind schema inspection and fail-closed system-group selection."""
import csv
import hashlib
import json
import math
from pathlib import Path

EXPOSED_GROUPS = {'apache', 'sqlite', 'x264'}
SYSTEMS = {'7z':'7zip','BDBC':'berkeleydb_c','HSQLDB':'hsqldb','LLVM':'llvm',
           'PostgreSQL':'postgresql','dconvert':'dconvert','deeparch':'deeparch',
           'exastencils':'exastencils','javagc':'javagc','redis':'redis','storm':'storm',
           'x264':'x264','Apache_AllMeasurements':'apache',
           'SQL_AllMeasurements':'sqlite','X264_AllMeasurements':'x264'}


def inspect_features(path):
    """Read only feature cells. Objective payloads never parsed or summarized."""
    with Path(path).open(newline='') as f:
        rows=csv.reader(f); names=[s.strip() for s in next(rows)]
        if len(names)!=len(set(names)):raise ValueError('duplicate column names')
        ys=[j for j,n in enumerate(names) if n.endswith(('+','-'))]
        xs=[j for j in range(len(names)) if j not in ys]
        domains=[set() for _ in xs];seen=set();raw=0;invalid=0
        for row in rows:
            raw+=1
            if len(row)!=len(names):raise ValueError('ragged table')
            values=tuple(row[j].strip() for j in xs)
            # Numeric cells are canonically normalized; labels are never accessed.
            try:
                values=tuple(float(v) for v in values)
                if not all(math.isfinite(v) for v in values):raise ValueError()
            except ValueError:
                invalid+=1;continue
            seen.add(values)
            for domain,value in zip(domains,values):domain.add(value)
    fingerprint=hashlib.sha256(json.dumps(sorted(seen),separators=(',',':')).encode()).hexdigest()
    return {'feature_names':[names[j] for j in xs], 'objective_names':[names[j] for j in ys],
            'ignored_columns':[], 'raw_rows':raw,'unique_configurations':len(seen),
            'duplicate_rows':raw-invalid-len(seen),'invalid_feature_rows':invalid,
            'feature_domains':[sorted(d) for d in domains],
            'binary_features':all(d and d<={0.,1.} for d in domains),
            'feature_matrix_sha256':fingerprint,'objective_values_inspected':False}


def eligibility(row):
    reasons=[]
    if row['identity_status']!='source_named':reasons.append('unresolved_system_identity')
    if row['system_group'] in EXPOSED_GROUPS:reasons.append('previously_exposed_system')
    s=row['schema']
    if s['invalid_feature_rows']:reasons.append('invalid_features')
    if not s['binary_features']:reasons.append('nonbinary_schema_unsupported_by_frozen_treatment')
    if len(s['objective_names'])!=1:reasons.append('requires_single_objective')
    if not 1<=len(s['feature_names'])<=39:reasons.append('feature_count_outside_1_39')
    if not 20<=s['unique_configurations']<=5000:reasons.append('row_count_outside_20_5000')
    return reasons


def split_groups(rows, minimum=20, test_count=8):
    eligible=[r for r in rows if not r['exclusion_reasons']]
    groups=sorted({r['system_group'] for r in eligible},
                  key=lambda g:hashlib.sha256(('v4-group-split-20260924:'+g).encode()).hexdigest())
    if len(groups)<minimum:
        return {'ready':False,'reason':'insufficient_verified_eligible_untouched_groups',
                'available':len(groups),'required':minimum,'assignments':{}}
    selected=groups[:minimum]
    assignments={g:('test' if j<test_count else 'development') for j,g in enumerate(selected)}
    return {'ready':True,'available':len(groups),'required':minimum,'assignments':assignments}


def validate_assignments(rows, assignments):
    """Reject exposed, ineligible and alias/duplicate-feature crossing groups."""
    seen={};matrices={}
    for r in rows:
        g=r['system_group']
        if g not in assignments:continue
        if r['exclusion_reasons']:raise ValueError('ineligible row selected')
        if g in EXPOSED_GROUPS:raise ValueError('previously exposed group selected')
        role=assignments[g]
        if role not in ('development','test'):raise ValueError('unknown split')
        for alias in [g]+r['aliases']:
            if alias in seen and seen[alias]!=role:raise ValueError('alias crosses splits')
            seen[alias]=role
        matrix=r['schema']['feature_matrix_sha256']
        if matrix in matrices and matrices[matrix]!=role:raise ValueError('identical feature table crosses splits')
        matrices[matrix]=role

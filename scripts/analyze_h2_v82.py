"""Revalidate saved native receipts and report predeclared feasibility criteria."""
import csv,hashlib,json,math,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.h2_v82 import expected,validate,PROFILES,ORDER

def analyze(version=82):
    module=__import__('escalation.h2_v'+str(version),fromlist=['validate'])
    raw=ROOT/f'results/v{version}_h2_feasibility';truth=expected()
    freeze=json.loads((ROOT/f'reports/protocol_v{version}.freeze.json').read_text())
    for n,d in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==d,n
    rows=json.loads((raw/'acquisitions.json').read_text());summary=json.loads((raw/'summary.json').read_text())
    assert summary['complete'] and summary['charged_trials']==summary['valid_trials']==len(rows)==len(ORDER)==9 and summary['unattempted']==0 and summary['new_model_requests']==0
    lock=json.loads((ROOT/f'configs/runtime_v{version}.lock.json').read_text())
    for i,(r,profile) in enumerate(zip(rows,ORDER)):
        assert r['trial']==i and r['profile']==profile and r['config']==PROFILES[profile] and r['status']=='valid'
        p=raw/f'trial_{i}';assert r['path']==str(p.relative_to(ROOT))
        c=PROFILES[profile]
        command=[str(ROOT/lock['java']),'-Xmx512m','-XX:ActiveProcessorCount=4','-cp',str(ROOT/lock['jar'])+':'+str(ROOT/lock['classes']),'H2Probe',str(c['mask']),str(c['recompile']).lower(),str(c['analyze_sample']),str(p)]
        assert r['command']==command and json.loads((p/'charge.json').read_text())['command']==command
        receipt=json.loads((p/'process_receipt.json').read_text());assert receipt==r['process']
        assert receipt['exit_code']==0 and receipt['termination_reason'] is None and receipt['wall_seconds']<60
        assert receipt['sampled_maxima']['rss_bytes']<2*1024**3 and receipt['sampled_maxima']['scratch_bytes']<128*1024**2
        assert module.validate(p,c,truth)==r['metrics']
        assert hashlib.sha256((p/'answers.csv').read_bytes()).hexdigest()==r['answers_sha256']
        assert math.isfinite(r['metrics']['query_seconds']) and r['metrics']['query_seconds']>0
    profiles={}
    for profile in PROFILES:
        rr=[r for r in rows if r['profile']==profile];t=[r['metrics']['query_seconds'] for r in rr];med=statistics.median(t);spread=(max(t)-min(t))/med
        profiles[profile]={'query_seconds':t,'median_seconds':med,'min_seconds':min(t),'max_seconds':max(t),'range_over_median':spread,'precision_pass':med>=.1 and spread<=.2,'median_index_analyze_seconds':statistics.median(r['metrics']['index_and_analyze_seconds'] for r in rr)}
    return {'version':version,'correct_trials':9,'checked_scored_query_answers':9*module.ROUNDS*48 if hasattr(module,'ROUNDS') else 1728,'profiles':profiles,'precision_pass':all(p['precision_pass'] for p in profiles.values()),'collection_wall_seconds':summary['seconds'],'native_wall_seconds':sum(r['process']['wall_seconds'] for r in rows),'new_model_calls':0,'scope':'descriptive native development feasibility, not optimization or held-out evidence'}

def main():
    version=int(sys.argv[1]) if len(sys.argv)>1 else 82;data=analyze(version)
    out=ROOT/f'results/v{version}_h2_analysis';out.mkdir(exist_ok=False)
    (out/'summary.json').write_text(json.dumps(data,indent=2)+'\n')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,4))
    for i,(name,p) in enumerate(data['profiles'].items()):
        ax.scatter([i-.06,i,i+.06],p['query_seconds'],label=name)
        ax.plot([i-.16,i+.16],[p['median_seconds']]*2,color='black')
    ax.set_xticks(range(3),list(data['profiles']));ax.set_ylabel('Query suite seconds (log scale)');ax.set_yscale('log');ax.set_title(f'H2 V{version}: three fresh-process repeats per profile')
    fig.tight_layout();fig.savefig(out/'timings.png',dpi=160);plt.close(fig)
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()

"""Replay measured V41 classical results, summarize all controls and plot."""
import csv, hashlib, itertools, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
import numpy as np
from escalation.io import read, write, lines, digest
from escalation.core import State, initial_state
from escalation.finite_domain import recommend
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import restrict, branch, messages, best, relative_gain, MODES, current_config
from escalation.resources import Resources
from run_transfer_v41 import verify_freeze

OUT=Path('results/v41_transfer')

def main():
    verify_freeze();m=read('data/manifest_v41.json')
    if not read(OUT/'progress.json')['complete']:raise ValueError('Incomplete denominator; inspect failure log')
    for p,h in read(OUT/'collection_seal.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Changed raw input')
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        journal=lines(OUT/'acquisitions.jsonl');rows=[]
        if len(journal)!=2400:raise ValueError('Collection denominator')
        lookup={}
        for event in journal:lookup.setdefault((event['dataset'],event['seed'],event['arm']),[]).append(event)
        for spec in m['datasets']:
            c,subset=restrict(load_candidates(spec),spec['fixed_features'])
            if subset!=spec['subset']:raise ValueError('Candidate identity mismatch')
            with Path(spec['path']).open(newline='') as f:
                raw={i:row for i,row in enumerate(csv.DictReader(f,delimiter=spec['delimiter']),2) if i in set(c.source_ids)}
            for seed in m['seeds']:
                resource.check();key=f"{spec['id']}_{seed}";p=read(OUT/'prefixes'/f'{key}.json');prefix=initial_state(c,seed)
                def replay_events(mode):
                    events=iter(lookup[(spec['id'],seed,mode)])
                    def acquire(row):
                        e=next(events)
                        if e['row_id']!=row or e['source_line']!=c.source_ids[row] or raw[e['source_line']][spec['primary_objective']]!=e['raw_target']:
                            raise ValueError('Acquisition replay mismatch')
                        return [float(e['raw_target'])]
                    return acquire
                acquire=replay_events('prefix')
                for _ in range(10):
                    i=recommend(c,prefix);prefix.observe(i,acquire(i),c.directions)
                if prefix.record()!=p['state'] or digest(prefix.record())!=p['prefix_hash']:raise ValueError('Prefix replay')
                pool=shortlist(c,prefix,seed)
                if pool!=p['pool'] or messages(c,prefix,pool)!=p['messages']:raise ValueError('Predecision prompt replay')
                reference=read(OUT/'arms'/f'{key}_batch_3nn.json')
                ref=best(State(**reference['state']),spec['direction'])
                for mode in MODES:
                    record=read(OUT/'arms'/f'{key}_{mode}.json')
                    state=branch(c,prefix,pool['ranked'],seed,mode,replay_events(mode))
                    if record['state']!=state.record() or len(state.ids)!=20 or len(set(state.ids))!=20 or record['actual_new_accesses']!=10:raise ValueError('Paired arm replay')
                    target=best(state,spec['direction'])
                    rows.append({'dataset':spec['id'],'system_group':spec['system_group'],'seed':seed,'arm':mode,
                        'direction':spec['direction'],'best':target,'prefix_best':best(prefix,spec['direction']),
                        'gain_vs_batch_3nn':relative_gain(ref,target,spec['direction']),
                        'gain_vs_prefix':relative_gain(best(prefix,spec['direction']),target,spec['direction']),
                        'seconds':record['branch_seconds']})
        summary=[];families=sorted({r['system_group'] for r in rows})
        for mode in MODES:
            selected=[r for r in rows if r['arm']==mode]
            values=[float(np.mean([r['gain_vs_batch_3nn'] for r in selected if r['system_group']==g])) for g in families]
            rng=np.random.default_rng(41000);means=np.asarray(values)[rng.integers(0,6,size=(10000,6))].mean(axis=1)
            perm=[abs(np.mean(np.asarray(values)*signs)) for signs in itertools.product((-1,1),repeat=6)]
            summary.append({'arm':mode,'mean_gain_vs_batch_3nn':float(np.mean(values)),
                'family_means':dict(zip(families,values)), 'bootstrap95':np.quantile(means,[.025,.975]).tolist(),
                'exact_sign_flip_p':float(np.mean(np.asarray(perm)>=abs(np.mean(values))-1e-14)),
                'wins':sum(r['gain_vs_batch_3nn']>1e-12 for r in selected),'ties':sum(abs(r['gain_vs_batch_3nn'])<=1e-12 for r in selected),
                'harms':sum(r['gain_vs_batch_3nn']< -1e-12 for r in selected)})
        write(OUT/'classical_summary.json',{'families':6,'prefixes':30,'arms':210,'actual_new_accesses':2400,
            'new_model_calls':0,'comparisons':summary,'evidence':'Descriptive classical transfer; all seven controls retained. No LLM or router result yet.'})
        with (OUT/'classical_cases.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        matrix=np.asarray([[100*s['family_means'][g] for g in families] for s in summary])
        fig,ax=plt.subplots(figsize=(10,5));bound=max(abs(matrix.min()),abs(matrix.max()),1)
        im=ax.imshow(matrix,cmap='RdBu',vmin=-bound,vmax=bound,aspect='auto')
        ax.set_xticks(range(6),families,rotation=25,ha='right');ax.set_yticks(range(7),MODES)
        for i in range(7):
            for j in range(6):ax.text(j,i,f'{matrix[i,j]:+.1f}%',ha='center',va='center',fontsize=9)
        ax.set_title('New recorded-table transfer: relative gain vs batch 3NN\nFive paired seeds per family; classical results only')
        fig.colorbar(im,ax=ax,label='Positive = better acquired target (%)');fig.tight_layout()
        fig.savefig(OUT/'classical_transfer.png',dpi=170);fig.savefig(OUT/'classical_transfer.svg');plt.close(fig)
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/verification.json',{'verified_prefixes':30,'verified_arms':210,'verified_acquisition_events':2400,
        'prefix_prompt_branch_replay':True,'source_matches_only_acquired_targets':True,
        'new_objective_acquisitions':0,'new_model_calls':0,'analysis_seconds':after['experiment_seconds']-before['experiment_seconds']})
    print(__import__('json').dumps(summary,indent=2))

if __name__=='__main__':main()

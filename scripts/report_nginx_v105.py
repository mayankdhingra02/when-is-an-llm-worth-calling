"""Verify and report saved native feasibility; never starts NGINX or acquires labels."""
import csv,hashlib,json,math,statistics,os
from pathlib import Path
from native_nginx_v105 import ROOT,OUT,CASES,REFERENCE,CONTRAST,PAYLOAD,CONCURRENCY,PER_CLIENT,sha
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/v105/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(ROOT/'.cache/v105'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def verify(out=OUT):
    data=json.loads((out/'summary.json').read_text());rows=data['cases']
    assert len(rows)==len(CASES)
    charged=[json.loads(line) for line in (out/'attempts.jsonl').read_text().splitlines()]
    assert len(charged)==data['charged_native_configuration_attempts']<=6
    for i,row in enumerate(rows):
        assert row['index']==i and row['case']==CASES[i]
        if row['status']=='unattempted':continue
        folder=out/f'{i:02d}_{row["case"]}'
        assert json.loads((folder/'result.json').read_text())==row
        assert row['configuration']==(REFERENCE if row['case']=='reference' else CONTRAST)
        assert sha(folder/'nginx.conf')==row['config_sha256']
        assert (folder/'www/payload.bin').read_bytes()==PAYLOAD
        assert sha(folder/'www/payload.bin')==row['payload_sha256']
        assert charged[i]=={'index':i,'case':row['case'],'charged_native_configuration_attempt':True}
        assert row['requests_sent']==sum(c['sent'] for c in row['client_counts'])
        assert row['responses_byte_valid']==sum(c['valid'] for c in row['client_counts'])
        assert row['response_body_bytes_validated']==len(PAYLOAD)*row['responses_byte_valid']
        if row['status']=='valid':
            assert row['requests_sent']==row['responses_byte_valid']==CONCURRENCY*PER_CLIENT
            assert row['owned_process_group_absent'] and row['server_returncode']==0
            assert math.isclose(row['client_cpu_to_wall'],row['client_cpu_seconds']/row['workload_seconds'])
    return data

def derive(data):
    rows=data['cases'];valid=[r for r in rows if r['status']=='valid'];refs=[r['workload_seconds'] for r in valid if r['case']=='reference']
    reference_range=(max(refs)-min(refs))/statistics.mean(refs) if len(refs)==4 else None
    gates={'all_six_valid':len(valid)==6,
      'every_workload_at_least_two_seconds':len(valid)==6 and all(r['workload_seconds']>=2 for r in valid),
      'reference_relative_range_at_most_10_percent':reference_range is not None and reference_range<=.1,
      'every_client_cpu_wall_at_most_0_8':len(valid)==6 and all(r['client_cpu_to_wall']<=.8 for r in valid)}
    return {'gates':gates,'eligible_for_optimization_on_this_harness':all(gates.values()),
        'reference_relative_range':reference_range,'validated_responses':sum(r.get('responses_byte_valid',0) for r in rows),
        'validated_body_bytes':sum(r.get('response_body_bytes_validated',0) for r in rows),
        'native_configuration_attempts':data['charged_native_configuration_attempts'],'new_model_requests':0}

def main():
    for name in ['source','execution']:
        f=json.loads((ROOT/f'reports/protocol_v105.{name}_freeze.json').read_text())
        for n,h in f['sha256'].items():assert sha(ROOT/n)==h,n
    data=verify();result=derive(data);dest=ROOT/'results/v105_analysis';dest.mkdir(exist_ok=True)
    (dest/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    with (dest/'timings.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['index','case','status','workload_seconds','client_cpu_seconds','client_cpu_to_wall','responses_byte_valid'])
        for r in data['cases']:writer.writerow([r.get(k) for k in ['index','case','status','workload_seconds','client_cpu_seconds','client_cpu_to_wall','responses_byte_valid']])
    valid=[r for r in data['cases'] if r['status']=='valid'];x=[r['index']+1 for r in valid]
    fig,ax=plt.subplots(1,2,figsize=(9,3.6));colors=['#2563eb' if r['case']=='reference' else '#d97706' for r in valid]
    ax[0].scatter(x,[r['workload_seconds'] for r in valid],c=colors);ax[0].axhline(2,c='#b91c1c',ls='--',label='minimum 2 s')
    ax[0].set(ylabel='Fixed workload elapsed seconds',xlabel='Predeclared attempt order',ylim=(0,2.2));ax[0].legend()
    ax[1].scatter(x,[r['client_cpu_to_wall'] for r in valid],c=colors);ax[1].axhline(.8,c='#b91c1c',ls='--',label='maximum 0.8')
    ax[1].set(ylabel='Client CPU seconds / wall seconds',xlabel='Predeclared attempt order',ylim=(0,1.1));ax[1].legend()
    fig.suptitle('NGINX feasibility: valid responses, failed timing gates')
    fig.legend(handles=[Line2D([],[],marker='o',ls='',color='#2563eb',label='Reference'),Line2D([],[],marker='o',ls='',color='#d97706',label='Contrast')],loc='lower center',ncol=2)
    fig.tight_layout(rect=(0,.08,1,1));fig.savefig(dest/'feasibility.png',dpi=160);plt.close(fig)
    rows='\n'.join(f"|{r['index']+1}|{r['case']}|{r['status']}|{r.get('workload_seconds',float('nan')):.6f}|{r.get('client_cpu_to_wall',float('nan')):.3f}|" for r in data['cases'])
    text=f'''# V105: real NGINX feasibility, timing harness not admitted

Six frozen native configuration attempts ran. All49,152 HTTP responses were byte-exact and all six owned server process groups exited. The experiment validates the response-checking pipeline but **fails the predeclared optimization-feasibility screen**. No LLM called, no optimizer/controller trained, no archived target inspected, and no positive escalation claim.

|Attempt|Bundle|Status|Elapsed seconds|Client CPU/wall|
|---|---|---|---:|---:|
{rows}

Four-reference relative range: **{100*result['reference_relative_range']:.2f}%**, against the10%ceiling. Gate outcomes: `{json.dumps(result['gates'],sort_keys=True)}`. The short timings and near-full clientCPU utilization are consistent with substantial client overhead; this does not isolate or quantify every bottleneck. No speedup/causal bundle attribution, significance or native-server population claim is justified. Enlarging the request count alone may lengthen a client-limited benchmark without fixing it.

![Predeclared timing screens](../results/v105_analysis/feasibility.png)

## What actually ran

Pinned official NGINX1.28.3 owner archive SHA2562c96a946bfb0882a21744ed429770a2123ae1828c7c48665092993ddee91a918, built locally on arm64 macOS. The first configure attempt failed because installed Xcodeclang17 could not link against the selected macOS27SDK. The successful repair selected installed CommandLineToolsclang21 and its matching SDK only in the build process environment. No system settings/installations changed; both attempt logs remain. Two build jobs maximum, no third-party build dependencies downloaded. Owner license is preserved. [Official build documentation](https://nginx.org/en/docs/configure.html).

Each fresh foreground server listened only on127.0.0.1:18595.16asyncio clients made512requests each,8192requests per configuration; every200status, contentlength/encoding and32768-byte payload was checked inside the measured interval. No HTTP warm-up or reliability probe acquired uncharged outcomes. The six attempts transfer/validate1,610,612,736bodybytes locally; these are local workload bytes, not internet-download cost. Two bundles, sequenceR/C/R/R/C/R, are described in the frozen protocol. The payload is a generated benchmark input, not fabricated model output or a synthetic substitute for measured execution. Unit-test fixtures remain separate.

Actual collection: **6nativeconfigurationattempts,49,152validatedresponses**, lifecycle{data['lifecycle_seconds']:.6f}s including startup/cleanup. Build time and first failure are separately logged. No new model requests, recorded-table acquisitions, paid/cloud use or external service. Deployment cost is not estimated from this unqualified harness. Successful correctness checks do not establish runtime representativeness or>=400effective tuning settings.

Source/docs download1,320,382bytes in V105; combined with V104, cumulative9,875,903,117/10GiB, remaining861,515,123bytes. Modelpayload and3,938historical requests unchanged. Raw per-attempt counts, times/configurations, stderr, syntax checks and process cleanup: `results/v105_nginx/`. Verified derivatives/figure: `results/v105_analysis/`. Source/build/freeze/test logs: `artifacts/study_v105/` and `artifacts/sources/v105/`.

## Next action

Replace the single-process Python load generator with a bounded native or multi-process byte-validating client, then freeze a new feasibility protocol. Establish sufficient workload duration, tolerable client overhead and reference repeatability before any optimization/LLM run. Keep NGINX as one exposed development group now that native outcomes have been inspected. Do not label future NGINX seeds/versions untouched held-out systems. Archived NGINX admission is still unresolved, and this result does not establish Q2 readiness.

Replay `.venv/bin/python scripts/report_nginx_v105.py` uses only saved evidence and does not reacquire outcomes. Do not rerun the once-only native collector into its existing directory.
'''
    (ROOT/'reports/nginx_v105.md').write_text(text)
    print(json.dumps(result))
if __name__=='__main__':main()

"""Aggregate every fixed native probe; never relax the preregistered gate."""
import json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def summarize(version):
 out=ROOT/f'results/v{version}_native';rows=[json.loads(p.read_text()) for p in sorted(out.glob('probe_*.json'))];groups=[]
 for t in [1,4]:
  for r in [1,20]:
   rs=[p for p in rows if p['threads']==t and p['requests_per_event']==r];valid=[p for p in rs if p['status']=='correct'];times=[p['measurement']['seconds'] for p in valid];med=statistics.median(times) if times else None;mad=statistics.median(abs(x-med) for x in times) if times else None
   groups.append({'threads':t,'requests_per_event':r,'intended':5,'observed':len(rs),'correct':len(valid),'times_seconds':times,'median_seconds':med,'mad_seconds':mad,'relative_mad':mad/med if med else None,'noise_pass':len(valid)==5 and mad/med<=.01})
 meds=[g['median_seconds'] for g in groups if g['median_seconds'] is not None];contrast=(max(meds)-min(meds))/max(meds) if len(meds)==4 else None
 completion=json.loads((out/'completion.json').read_text());all_correct=len(rows)==20 and all(p['status']=='correct' and p['server_reaped'] and p['lifecycle_seconds']<=15 for p in rows);passed=all_correct and all(g['noise_pass'] for g in groups) and contrast is not None and contrast>=.05
 data={'version':version,'groups':groups,'all_correct_and_reaped':all_correct,'median_contrast':contrast,'feasible':passed,'gate':'20correct, no misses/evictions; allMAD/median<=.01; mediancontrast>=.05','completion':completion,'workload_operations_per_probe':128000 if version==150 else 2048000}
 (out/'summary.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');return data

def main():
 data=[summarize(v) for v in [150,152]];lines=['# V150/V152: actual native Memcached correctness and noise screening','', '**These are native feasibility measurements, not LLM outcomes or a B10/B20 optimization experiment.** All four configurations and all intended probes appear in each workload. Synthetic tests are excluded. Longer-workload V152 was frozen after observing V150 noise; it is a declared exploratory amendment, with both costs/results retained.','',
 'Memcached1.6.45 came from the [official release page](https://www.memcached.org/downloads), archive SHA256d362c64e6d8d5287153501eabf7c85b4a761432fbf53f5d7b085d0bb1653c1dd and matching owner SHA1. Static libevent2.1.13-stable came from the [owner release linked by libevent.org](https://libevent.org/), SHA256f7e9383b8c0baa81b687e5b5eecc01beefaf1b19b64151d95ed61647fe7a315c. Both BSD3-clause licenses, additional libevent notices, build instructions and receipts were inspected/preserved. No system-wide install. Initial defaultSDK build failed; process-local matching Xcode15.5SDK repaired it without system changes.','',
 'Four local C clients alternate GET/SET in32request pipelines, with exact response-byte validation.1024keys have1024-byte deterministic values, no expiry;64MiB cache. Final independent server stats require no misses/evictions and exact command/item counts. Each probe starts a fresh loopback-only server with UDPoff, and reaps it. Same client/server host means measured elapsed time includes client work, validation, socket I/O and scheduling. It is not isolated server speed.','',
 '| Version / operations per probe | Threads | Requests/event | Correct /5 | Median seconds | MAD/median | Pass1%noise gate |','|---|---:|---:|---:|---:|---:|---|']
 for d in data:
  for g in d['groups']:
   med='unknown' if g['median_seconds'] is None else f"{g['median_seconds']:.6f}";mad='unknown' if g['relative_mad'] is None else f"{100*g['relative_mad']:.3f}%"
   lines.append(f"| V{d['version']} / {d['workload_operations_per_probe']} | {g['threads']} | {g['requests_per_event']} | {g['correct']} | {med} | {mad} | {g['noise_pass']} |")
 lines+=['', 'The unchanged screening rule requires all20correct probes, every configurationMAD/median<=1%, and median configuration contrast>=5%. Five repetitions are a screen, not a population confidence interval. Settings with larger true effects can still be distinguishable when this conservative1%gate fails; failure does not mean Memcached is unoptimizable.','']
 for d in data:
  c=d['completion'];contrast='unknown' if d['median_contrast'] is None else f"{100*d['median_contrast']:.2f}%"
  lines.append(f"V{d['version']}: **gate {'PASS' if d['feasible'] else 'FAIL'}**; {c['correct']}/{c['intended_probes']}correct, {c['charged_probes']}charged probes, {c['wall_seconds']:.3f}seconds/300secondstagecap, mediancontrast{contrast}. All lifecycle/correctness/reaping conditions met: {d['all_correct_and_reaped']}.")
 lines += ['', 'New collection is40native feasibility probes total, with no LLM requests and no recorded-table acquisitions. Each includes prefilling and every checked timed operation; do not count these as40independent systems or free reliability probes within a future20evaluation budget. Source retrieval2,436,165bytes; builds3.046seconds failed +20.045seconds repaired, plus client compilation. CPU/wall estimates are local and no dollar/energy saving is inferred.','',
 'If either gate fails, preserve the failure. No immediate optimization run follows under the failed protocol. Any later noisy-objective study must predeclare its target (single-run time vs repeated-run estimate), charge repetitions, choose a noise-appropriate practical margin and validate the selected configurations with held-out repetitions. Changing a threshold after seeing these probes cannot create a confirmatory success. This family is now explored; later work must disclose that exposure. No remote/cloud/native production deployment or independent-host replication has occurred.','',
 'Raw commands, stdout/stderr, checked-operation counts, server statistics, lifecycle/reaping records, randomized plans and charged ledgers are in results/v150_native and results/v152_native. Protocols and preprobe hash freezes are in reports/protocol_v150.md, reports/protocol_v152.md and artifacts/study_v{150,152}. No inference or service remains running after completion.']
 (ROOT/'reports/native_feasibility_v152.md').write_text('\n'.join(lines)+'\n')
 import matplotlib
 matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='v152'
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(10,4.5),layout='constrained')
 for ax,d in zip(axes,data):
  vals=[g['times_seconds'] for g in d['groups']];ax.boxplot(vals,tick_labels=['t1/R1','t1/R20','t4/R1','t4/R20'],showfliers=True)
  for i,v in enumerate(vals,1):ax.scatter([i]*len(v),v,color='#336b87',s=15,zorder=3)
  ax.set_ylabel('Correct fixed-work elapsed seconds');ax.set_title(f"V{d['version']}: {d['workload_operations_per_probe']:,} operations/probe");ax.grid(axis='y',alpha=.2)
 fig.suptitle('Native Memcached noise screening • 5 blocks × 4 configurations\nDifferent workload sizes; compare within each panel')
 out=ROOT/'results/v152_native';fig.savefig(out/'noise.png',dpi=150);fig.savefig(out/'noise.svg',metadata={'Date':None});plt.close(fig)
 print(json.dumps({d['version']:{'gate_pass':d['feasible'],'max_relative_mad':max(g['relative_mad'] for g in d['groups'])} for d in data}))
if __name__=='__main__':main()

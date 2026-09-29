from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
    dest=ROOT/'reports/protocol_v129.freeze.json';assert not dest.exists();assert not (ROOT/'results/v129_proposals').exists()
    assert not (ROOT/'results/v128_analysis').exists(), 'Freeze recovery design before original continuation outcomes'
    old=ROOT/'reports/protocol_v128.freeze.json';paths={old}|{ROOT/n for n in read(old)['sha256']}
    paths.update(ROOT/n for n in ['reports/protocol_v129.md','reports/reporting_correction_v128.md','configs/study_v129.json','artifacts/study_v129/jobs.json','artifacts/study_v129/monitor_tests.log','artifacts/study_v128/tests_cost_correction.log'])
    for folder in ['scripts','tests/synthetic']:
        paths.update((ROOT/folder).glob('*v129.py'))
    for n in ['scripts/report_proposal_v128_corrected.py','scripts/verify_proposal_v128_interrupted.py','scripts/audit_cost_proposal_v128.py']:
        paths.add(ROOT/n)
    for folder in ['artifacts/study_v129/sdk_headers','results/v128_proposals']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    write(dest,{'at':now(),'scope':'Prospective resource-monitor recovery;11newcalls plus one compatible prior response,90additional labels after original300','sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}})
    print('Frozen',len(paths),'inputs',sha(dest))
if __name__=='__main__':main()

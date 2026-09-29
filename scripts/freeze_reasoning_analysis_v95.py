from collect_smollm_v47 import ROOT,read,write,sha,now
def main():
    out=ROOT/'reports/protocol_v95_analysis.freeze.json';assert not out.exists()
    assert not (ROOT/'results/v95_analysis').exists()
    names=['scripts/analyze_reasoning_v95.py','src/escalation/core.py','src/escalation/finite_v6.py',
           'src/escalation/finite_domain.py','src/escalation/transfer_v41.py','src/escalation/io.py',
           'data/manifest_v41.json','results/v91_analysis/cases.json','reports/protocol_v95b.freeze.json']
    names += [d['path'] for d in read(ROOT/'data/manifest_v41.json')['datasets']]
    write(out,{'at':now(),'scope':'freeze evaluator before acquiring V95 continuation labels; fixed primary comparisons',
               'sha256':{n:sha(ROOT/n) for n in names}})
    print('Frozen analysis',len(names),'files')
if __name__=='__main__':main()

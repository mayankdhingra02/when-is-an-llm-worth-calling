"""Private standard-library replay with the entire V126 frozen file set."""
import json,shutil,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 out=ROOT/'output/v126_replay';out.mkdir(exist_ok=False)
 names=set(json.loads((ROOT/'reports/protocol_v126.freeze.json').read_text())['sha256'])
 names.update(['reports/protocol_v126.freeze.json','reports/domain_audit_v126.md','reports/verification_correction_v126.md','reports/attainability_v125.md','scripts/verify_domain_v126_fixed.py','artifacts/study_v126/verification_original_failure.log','artifacts/study_v126/corruption_replay.json'])
 names.update(str(p.relative_to(ROOT)) for p in (ROOT/'results/v126_domain_audit').rglob('*') if p.is_file())
 for n in sorted(names):
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,p)
 (out/'README.md').write_text('# Private V126 feasibility replay\n\nRun `python3 -I -S replay.py`. Standard library only, no requests, model or new outcome acquisition. Includes the entire V126 frozen input file set, plus the corrected verifier and actual collection. Verify4,992 source cells,4,932charged journal entries,497bounded branches,30prefixes,102control states and all30priorV42ceilings. This is an evaluator-only hindsight bound on exposed families, not an achieved LLM improvement or held-out router validation.\n\nOriginal frozen verifier is retained and superseded for execution by verify_domain_v126_fixed.py; see the correction report. Data redistribution qualifications in data/manifest_v41.json remain: this package is for local private review, not a license to publish source tables. No model weights/runtime binaries, network or external spending.\n')
 (out/'replay.py').write_text('import hashlib,json,runpy\nfrom pathlib import Path\nr=Path(__file__).resolve().parent\nm=json.loads((r/"manifest.json").read_text())\nfor n,v in m["files"].items():\n p=r/n;assert p.stat().st_size==v["bytes"] and hashlib.sha256(p.read_bytes()).hexdigest()==v["sha256"],n\nrunpy.run_path(str(r/"scripts/verify_domain_v126_fixed.py"),run_name="__main__")\nprint("Verified",len(m["files"]),"hashed files and recorded-domain audit; zero new inference/acquisitions")\n')
 # Verifier writes this derived receipt, intentionally not part of package manifest.
 (out/'artifacts/study_v126').mkdir(parents=True,exist_ok=True)
 files={str(p.relative_to(out)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}
 (out/'manifest.json').write_text(json.dumps({'scope':'Private V126 evidence replay; full V126 frozen file set','files':files},indent=2)+'\n')
 archive=ROOT/'output/v126_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(files),'files;',archive.stat().st_size,'bytes')
if __name__=='__main__':main()

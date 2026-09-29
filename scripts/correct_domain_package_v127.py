"""Correct a packaging claim without changing the sealed original archive."""
import json,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 original=ROOT/'output/v126_replay.zip';out=ROOT/'output/v126_replay_corrected';out.mkdir(exist_ok=False)
 with zipfile.ZipFile(original) as z:
  for n in z.namelist():
   p=out/n;assert p.resolve().is_relative_to(out.resolve());p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
 p=out/'README.md';text=p.read_text().replace('No model weights/runtime binaries, network or external spending.','No model weights are included. The full frozen dependency set DOES include llama.cpp runtime binaries for byte-level provenance checks. The standard-library replay never executes them and requires no model, network or external spending. This corrects the original archive\'s inaccurate no-runtime-binaries sentence; original ZIP and measured evidence remain unchanged.');p.write_text(text)
 m=json.loads((out/'manifest.json').read_text());m['files']['README.md']={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size};m['scope']+=';README runtime-content correction';(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 dest=ROOT/'output/v126_replay_corrected.zip';assert not dest.exists()
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 receipt={'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'corrected_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'corrected_bytes':dest.stat().st_size,'runtime_file_count':sum(n.startswith('.local-runtime/') for n in m['files']),'changed_members':['README.md','manifest.json'],'scientific_data_changed':False};(ROOT/'artifacts/study_v127/package_correction.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
if __name__=='__main__':main()

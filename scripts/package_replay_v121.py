"""Assemble a private, compact saved-data replay; never publish or send."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/v121_replay'
def main():
    OUT.mkdir(exist_ok=False);paths=set()
    for folder in ['results/v121_classical','results/v121_qwen','results/v121_analysis','results/v121_report','results/v121_router','artifacts/study_v121/model_prefixes','results/v119_classical/prefixes','results/v120_analysis/arms']:
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
    for name in ['data/manifest_v121.json','artifacts/sources/v121/data/MongoDB/measurements.csv','artifacts/sources/v121/data/MongoDB/README.md','artifacts/sources/v121/data/MongoDB/FeatureModel.xml','artifacts/sources/v104/twins_LICENSE.txt','artifacts/study_v121/model_jobs.json','reports/protocol_v121.md','reports/protocol_v121.freeze.json','reports/replication_v121.md','results/v120_analysis/summary.json','artifacts/study_v91/model_manifest.json']:
        paths.add(ROOT/name)
    for p in paths:
        q=OUT/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    shutil.copyfile(ROOT/'scripts/standalone_replay_v121.py',OUT/'replay.py')
    (OUT/'README.md').write_text('''# Private V121 evidence replay

Run `python3 -I replay.py` in this directory. Python standard library only; no model/runtime download, network, installation or hidden objective acquisition. Verifies bundled hashes,100 actual requests/responses,400 acquired recorded source events, strict grammar/choice sequences, paired normal/blind inputs, budgets, gains,5 MongoDB first-ten identities and5 WordCount identities. Original full-project verifiers additionally replay optimizer decisions and controller fitting. This package does not rerun model inference, reproduce a hardware measurement, or verify dependencies omitted from the full195-file protocol freeze.

Raw observations are real local-model output, not synthetic fixtures. Source owner/revision/model metadata and license are retained. All MongoDB seeds are one prospective family; prior WordCount evidence is exploratory. Do not treat a replay as an independent experiment or infer a journal guarantee. No model weights/binary included. The owner MongoDB data derive from the GPL-2.0 TwinsOrFalseFriends artifact; license included, no public redistribution or upload has been performed. Full repository paths are retained beneath this directory. The manifest protects accidental integrity; it is not an externally signed attestation.
''')
    manifest={'files':{str(p.relative_to(OUT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'output/v121_replay.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():z.write(p,'v121_replay/'+str(p.relative_to(OUT)))
    print(len(manifest['files']),'files', (ROOT/'output/v121_replay.zip').stat().st_size,'zip bytes')
if __name__=='__main__':main()

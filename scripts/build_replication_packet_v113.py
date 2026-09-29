"""Local review packet, no upload, install, model weights or remote execution."""
import json,hashlib,platform,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/v113_replication'
def main():
 assert not OUT.exists();OUT.mkdir(parents=True)
 names=['scripts/worker_numerical_v94.py','src/escalation/__init__.py','src/escalation/core.py','src/escalation/finite_domain.py','src/escalation/numerical_v94.py','data/native_v94/orsreg_1.mtx','artifacts/sources/v94/25fv47.mps','artifacts/sources/v94/highs_LICENSE','artifacts/study_v94/dataset_manifest.json','reports/protocol_v113.md','configs/validation_v113.json']
 for n in names:
  dest=OUT/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
 # Worker hash remains unchanged: on Linux its self maxRSS field is KiB;
 # the new portable parent watchdog normalizes RSS independently via ps.
 (OUT/'requirements.txt').write_text('numpy==2.2.6\nscipy==1.13.1\nhighspy==1.7.2\n')
 (OUT/'source_host_sha256.txt').write_text(hashlib.sha256(platform.node().encode()).hexdigest()+'\n')
 shutil.copyfile(ROOT/'scripts/replicate_fixed_v113.py',OUT/'run.py')
 (OUT/'README.md').write_text('''# Independent-host confirmation packet

This local packet has NOT run on a second host. It contains no model, credentials, cloud client, or paid service. All30configuration choices and90validation slots were fixed from V94before V113confirmation outcomes. The goal is to check native timing reliability, including equal-configuration contrasts, not tune an LLM.

On a separate, otherwise quiet macOS or Linux machine with Python3.10:
```
python3.10 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
.venv/bin/python run.py --check-only
.venv/bin/python run.py --execute
```
Installation is a prospective command for the second machine, not an installation performed here. Packages come from the configured recognized registry; inspect that configuration before installing. The launch preflight requires exact versions and records native-extension hashes and environment. No model/GPU is needed. Limits:90configuration acquisitions,270planned physical solves,30seconds/2GiB per worker,1800seconds overall. Results are create-once underresults/. Each confirmation is charged separately; original20search outcomes plus3confirmations means23per arm, not20. No worker failure is removed. Same-host execution is refused using a hashed host name; this is a practical guard, not attestation of independent hardware. Do not rename the host to bypass it.

Send the resulting directory back by a user-chosen channel for independent certificate verification; this packet does not send anything. --check-only reads hashes/imports and records no objectives. Collection is untested on Linux and other hardware. The original worker's ru_maxrss units differ on Linux; the parent usesps RSS inKiB, converts tobytes, and records the worker-field unit without treating it as bytes.

TheHiGHS source license is preserved. TheHB/orsreg_1 workload's standalone redistribution terms remain unresolved as documented in the main repository. This is a private local replication packet, NOT a license-cleared public release. No publication or upload is authorized. See the dataset manifest for owner provenance and hashes. Project Python runner/certificate code is copied with its original identity; inherited functions are not claimed novel.
''')
 paths=[p for p in OUT.rglob('*') if p.is_file()]
 (OUT/'manifest.json').write_text(json.dumps({'scope':'independent-host confirmation only; unexecuted','sha256':{str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}},indent=2)+'\n')
 print(json.dumps({'files':len(paths)+1,'bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),'path':str(OUT)}))
if __name__=='__main__':main()

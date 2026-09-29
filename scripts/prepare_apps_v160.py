"""Safe local source extraction, provenance copy and input schema; no tuned app run."""
import hashlib,json,re,tarfile,zipfile,shutil,subprocess,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'artifacts/sources/v160';A=ROOT/'artifacts/study_v160';N=ROOT/'.native-v160'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def extract(source,dest):
 count=total=0
 with tarfile.open(source) as tf:
  for m in tf.getmembers():
   if not m.isfile():continue
   p=dest/m.name;assert p.resolve().is_relative_to(dest.resolve()) and m.size<=20000000
   total+=m.size;assert total<=200000000
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(tf.extractfile(m).read());p.chmod(m.mode&0o777);count+=1
 return {'files':count,'bytes':total}
def main():
 assert not N.exists();N.mkdir();rec=read=json.loads((S/'receipt.json').read_text());assert rec['error'] is None
 for r in rec['files']:assert sha(ROOT/r['path'])==r['sha256']
 extractions={}
 for name in ['Python-3.10.13.tar.xz','hnswlib-v0.8.0.tar.gz','ripgrep-15.2.0-aarch64-apple-darwin.tar.gz']:extractions[name]=extract(S/name,N)
 N.joinpath('bin').mkdir();shutil.copy2('/opt/homebrew/bin/gsort',N/'bin/gsort')
 for name in ['COPYING','INSTALL_RECEIPT.json']:shutil.copy2('/opt/homebrew/opt/coreutils/'+name,A/('coreutils_'+name))
 for e,p in [('ripgrep',N/'ripgrep-15.2.0-aarch64-apple-darwin/rg'),('gsort',N/'bin/gsort')]:
  v=subprocess.run([str(p),'--version'],check=True,capture_output=True,text=True);helptext=subprocess.run([str(p),'--help'],check=True,capture_output=True,text=True);(A/(e+'_version.txt')).write_text(v.stdout);(A/(e+'_help.txt')).write_text(helptext.stdout)
  write(A/(e+'_binary.json'),{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'version':v.stdout})
 with zipfile.ZipFile(S/'optdigits.zip') as z:
  for name in ['optdigits.tra','optdigits.tes','optdigits.names']:
   content=z.read(name);(A/name).write_bytes(content)
 train=np.loadtxt(A/'optdigits.tra',delimiter=',',dtype=np.int32);test=np.loadtxt(A/'optdigits.tes',delimiter=',',dtype=np.int32)
 assert train.shape==(3823,65) and test.shape==(1797,65) and np.min(train[:,:64])>=0 and np.max(train[:,:64])<=16 and np.min(test[:,:64])>=0 and np.max(test[:,:64])<=16
 train[:,:64].astype('<f4').tofile(A/'ann_train.f32');test[:,:64].astype('<f4').tofile(A/'ann_query.f32')
 # Corpus consists of real source/documentation, not synthetic repetitions.
 corpus=N/'Python-3.10.13';files=[];excluded=[];parts=[]
 for p in sorted(corpus.rglob('*')):
  if not p.is_file() or p.suffix not in ['.py','.c','.h','.rst','.txt']:continue
  body=p.read_bytes()
  if b'\0' in body:excluded.append(str(p.relative_to(corpus)));continue
  files.append({'path':str(p.relative_to(corpus)),'bytes':len(body),'sha256':sha(p)})
  parts.append(body if body.endswith(b'\n') else body+b'\n')
 (A/'sort_input.bin').write_bytes(b''.join(parts));write(A/'corpus_files.json',files);write(A/'nul_excluded.json',excluded)
 # Scope recheck includes engine predecessors but no target conversion.
 prior=json.loads((ROOT/'artifacts/study_v156/audit.json').read_text())['exposure_scope'];paths={ROOT/r['path'] for r in prior}
 for folder in ['reports','configs']:
  for v in [156,157,158,159]:paths.update((ROOT/folder).glob('*v'+str(v)+'*'))
 patterns={'ripgrep':r'\bripgrep\b','gnu_sort':r'\b(?:gsort|gnu\s+sort|coreutils)\b','hnswlib_nmslib':r'\b(?:hnswlib|nmslib|non-metric space library)\b'}
 hits={k:[] for k in patterns};scanned=[]
 for p in sorted(paths):
  if not p.is_file():continue
  t=p.read_text(errors='replace');scanned.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
  for k,regex in patterns.items():
   for m in re.finditer(regex,t,re.I):hits[k].append({'path':str(p.relative_to(ROOT)),'context':t[max(0,m.start()-80):m.end()+120]})
 write(A/'preparation.json',{'at_unix':time.time(),'extractions':extractions,'train_shape':list(train.shape),'query_shape':list(test.shape),'class_labels_discarded':True,'sort_bytes':(A/'sort_input.bin').stat().st_size,'corpus_files':len(files),'nul_excluded':excluded,'source_http_bytes':rec['retained_http_bytes'],'exposure_files':scanned,'identity_hits':hits,'objective_calls':0})
 print(json.dumps({'corpus_files':len(files),'sort_bytes':(A/'sort_input.bin').stat().st_size,'identity_hits':hits,'objective_calls':0},indent=2))
if __name__=='__main__':main()

"""Feature-only coverage audit: objective cells are never converted or reported."""
import csv,hashlib,io,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FEATURES={
 'gcc':['optim','-floop-interchange','-fprefetch-loop-arrays','-ffloat-store','-fno-asm'],
 'imagemagick':['memory_r','posterize_r','gaussian-blur','thread','quality'],
 'nodejs':['--jitless','--experimental-wasm-modules','--experimental-vm-modules','--preserve-symlinks-main','--no-warnings','--node-memory-debug'],
 'poppler':['format','j','jp2','jbig2','ccitt'],
 'xz':['memory','format','level','depth']}
TARGETS={'gcc':['size','ctime','exec'],'imagemagick':['size','time'],'nodejs':['ops'],'poppler':['size','time'],'xz':['size','time']}
def extract(text,group):
 rows=csv.reader(io.StringIO(text));header=next(rows);names=FEATURES[group]
 if len(set(header))!=len(header) or set(header)!=set(names+TARGETS[group]+([] if group=='nodejs' else ['configurationID'])):raise ValueError('Unapproved schema')
 pos=[header.index(n) for n in names];xs=[]
 for row in rows:
  if len(row)!=len(header):raise ValueError('Wrong row width')
  x=tuple(row[i] for i in pos)
  if any(not v.strip() for v in x):raise ValueError('Missing feature')
  xs.append(x)
 return names,xs
def audit(text,group):
 names,xs=extract(text,group);unique=set(xs)
 result={'rows':len(xs),'unique_configurations':len(unique),'duplicate_feature_rows':len(xs)-len(unique),'feature_names':names,'feature_domain_sizes':{n:len({x[k] for x in xs}) for k,n in enumerate(names)},'minimum_required':40,'raw_coverage_pass':len(unique)>=40,'objective_values_parsed':0}
 if group=='gcc':
  restricted={x for x in unique if x[names.index('optim')]!='-Ofast' and x[names.index('-ffloat-store')]=='1'}
  result['conservative_fp_partition_configurations']=len(restricted);result['conservative_partition_coverage_pass']=len(restricted)>=40
 if group=='imagemagick':
  positions=[names.index(n) for n in ['posterize_r','gaussian-blur','quality']];counts=Counter(tuple(x[k] for k in positions) for x in unique)
  result['output_option_partitions']=len(counts);result['largest_fixed_output_option_partition']=max(counts.values());result['fixed_output_partition_coverage_pass']=max(counts.values())>=40
 return result
def main():
 receipt=json.loads((ROOT/'artifacts/sources/v137/feature_summary.json').read_text());results={}
 for f in receipt['files']:
  path=ROOT/f['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'];g=path.parent.name
  results[g]={'path':f['path'],'sha256':f['sha256'],**audit(path.read_text(),g)}
 dest=ROOT/'artifacts/study_v137/coverage.json';dest.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()

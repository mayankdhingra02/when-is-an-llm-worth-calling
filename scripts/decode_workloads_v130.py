"""Decode fixed licensed source clips; no optimization or encoder call."""
import subprocess,time,wave
from collect_smollm_v47 import ROOT,read,write,sha

def main():
 a=ROOT/'artifacts/study_v130';b=read(a/'build_xcode.json');assert b['status']=='complete';assert sha(ROOT/b['binary'])==b['sha256']
 out=ROOT/'data/native_v130';out.mkdir(exist_ok=True);assert not any(out.iterdir());rows=[]
 for item in read(a/'corpus_selection.json')['clips']:
  src=ROOT/item['path'];assert sha(src)==item['sha256'];dest=out/(src.stem+'.wav');cmd=[str(ROOT/b['binary']),'-d','--silent','-o',str(dest),str(src)];t=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);assert p.returncode==0,p.stderr
  with wave.open(str(dest),'rb') as w:
   assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==16000 and w.getcomptype()=='NONE'
   frames=w.getnframes();samples=w.readframes(frames);assert len(samples)==frames*2
  raw=dest.with_suffix('.raw');raw.write_bytes(samples)
  rows.append({**item,'decode_command':cmd,'decode_seconds':time.monotonic()-t,'decode_stderr':p.stderr,'wav_path':str(dest.relative_to(ROOT)),'wav_sha256':sha(dest),'raw_path':str(raw.relative_to(ROOT)),'raw_sha256':sha(raw),'raw_bytes':len(samples),'frames':frames,'rate':16000,'channels':1,'sample_bits':16})
 write(a/'workloads.json',{'group':'flac','status':'Source decodes only; no optimization target measured','workloads':rows})
 print('Decoded',len(rows),'licensed clips;',sum(r['frames'] for r in rows)/16000,'seconds of audio')
if __name__=='__main__':main()

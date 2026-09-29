"""Fault injection ONLY: fake process outputs under pytest tmp_path, never results/."""
import importlib.util
import json
import sys
from pathlib import Path
import pytest

SCRIPTS=Path(__file__).resolve().parents[2]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('v78_worker_under_test',SCRIPTS/'worker_kanzi_v78.py')
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)

def header(checksum=1):
    # Independently encode a LZ/HUFFMAN,16KiB stream header (not real compression).
    fields=[(0x4B414E5A,32),(1,4),(checksum,1),(1,5),(3<<42,48),(1024,28),(1,6),(0,4)]
    value=0
    for number,width in fields:value=(value<<width)|number
    return value.to_bytes(16,'big')

@pytest.fixture
def harness(tmp_path,monkeypatch):
    monkeypatch.setattr(worker,'ROOT',tmp_path);monkeypatch.setattr(worker,'rss',lambda pid:0)
    folder=tmp_path/'results/v78_kanzi_paired/eval_000';folder.mkdir(parents=True)
    source=tmp_path/'data/generated_v74/workload.bin';source.parent.mkdir(parents=True);source.write_bytes(b'SYNTHETIC-UNIT-TEST-ONLY')
    lock=tmp_path/'configs/runtime_v76.lock.json';lock.parent.mkdir();lock.write_text(json.dumps({'java':'FAKE_JAVA_NEVER_EXECUTED','jar':'FAKE_JAR_NEVER_EXECUTED'}))
    specpath=folder/'spec.json';specpath.write_text(json.dumps({'config_id':0,'config':worker.grid()[0]}))
    calls=[]
    def install(mode):
        def fake_run(command,*,cwd,log_path,wall_cap,monitor,env):
            phase='compression' if '-c' in command else 'decompression';calls.append(phase)
            assert wall_cap==40 and '-Xmx768m' in command
            assert not {'JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH'}&set(env)
            values,reason=monitor(12345)
            log_path.write_text('Block size set to 16384 bytes\nChecksum set to true\nUsing LZ transform (stage 1)\nUsing HUFFMAN entropy codec (stage 2)\nUsing 1 job\n')
            output=Path(command[command.index('-o')+1])
            if phase=='compression':
                output.write_bytes(header(0 if mode=='checksum_missing' else 1)+b'SYNTHETIC')
                if mode=='truncated_header':output.write_bytes(b'bad')
                if mode=='wrong_jobs':log_path.write_text(log_path.read_text().replace('Using 1 job','Using 4 jobs'))
                if mode=='ignored_option':log_path.write_text(log_path.read_text()+'Warning: adjusted option\n')
            else:output.write_bytes(b'CORRUPTED' if mode=='wrong_decoded_bytes' else source.read_bytes())
            exit_code=13 if mode=='compression_exit' and phase=='compression' else 0
            if reason:exit_code=-9
            if mode=='decompression_exit' and phase=='decompression':exit_code=13
            return {'exit_code':exit_code,'termination_reason':reason,'wall_seconds':0.01,'sampled_maxima':values}
        monkeypatch.setattr(worker,'run',fake_run)
    return folder,specpath,calls,install

@pytest.mark.parametrize('mode',['compression_exit','checksum_missing','truncated_header','wrong_jobs','ignored_option'])
def test_reject_before_decompression_and_retain_failure(harness,mode):
    folder,path,calls,install=harness;install(mode);result=worker.collect(path)
    assert result['status']=='failed' and calls==['compression']
    assert (folder/'output.knz').exists() and not (folder/'retention.json').exists()
    assert json.loads((folder/'result.json').read_text())['status']=='failed'

@pytest.mark.parametrize('mode',['decompression_exit','wrong_decoded_bytes'])
def test_decompression_failure_cannot_be_valid(harness,mode):
    folder,path,calls,install=harness;install(mode);result=worker.collect(path)
    assert result['status']=='failed' and calls==['compression','decompression']
    assert (folder/'output.knz').exists() and (folder/'decoded.bin').exists()
    assert not (folder/'retention.json').exists()

def test_abort_guard_reaches_supervisor(harness):
    folder,path,calls,install=harness;install('valid');result=worker.collect(path,lambda:'server_rss_cap')
    assert result['status']=='failed' and calls==['compression']
    assert result['compression']['termination_reason']=='server_rss_cap'

def test_success_removes_only_validated_products(harness,monkeypatch):
    for name in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']:monkeypatch.setenv(name,'SYNTHETIC_INJECTION')
    folder,path,calls,install=harness;install('valid');result=worker.collect(path)
    assert result['status']=='valid' and result['exact_byte_equality']
    assert result['input_sha256']==result['decoded_sha256'] and calls==['compression','decompression']
    assert not (folder/'output.knz').exists() and not (folder/'decoded.bin').exists()
    assert (folder/'spec.json').exists() and (folder/'compression.log').exists() and (folder/'retention.json').exists()

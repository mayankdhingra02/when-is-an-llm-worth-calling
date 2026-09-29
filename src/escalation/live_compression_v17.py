"""Expanded development measurement primitives; no LLM, optimizer, or hidden-label scoring."""
import hashlib
import itertools
import json
import os
import random
import signal
import subprocess
import time
import zlib
from pathlib import Path


def settings():
    grid=[]
    for level,window,check in itertools.product(range(1,13),(17,18,19,20),(False,True)):
        grid.append({'family':'zstd','level':level,'window_log':window,'checksum':check})
    for level,block,dependent in itertools.product(range(1,13),(4,5,6,7),(False,True)):
        grid.append({'family':'lz4','level':level,'block_id':block,'dependent':dependent})
    for level,memory,filtered in itertools.product(range(1,10),(3,5,6,8,9),(False,True)):
        grid.append({'family':'zlib','level':level,'memory_level':memory,'filtered':filtered})
    return [dict(row,config_id=hashlib.sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()[:16]) for row in grid]


def schedule(repetitions=3,seed=20260924):
    rng=random.Random(seed);items=[]
    for repeat in range(repetitions):
        block=settings();rng.shuffle(block)
        offset=len(items)
        items.extend({'trial_id':offset+i,'repetition':repeat,'setting':s} for i,s in enumerate(block))
    return items


def validate_setting(setting):
    if setting not in settings():raise ValueError('Setting outside frozen grid')


def commands(setting,binary):
    validate_setting(setting)
    if setting['family']=='zstd':
        compress=[binary,'-q','-c','--single-thread',f'-{setting["level"]}',f'--zstd=wlog={setting["window_log"]}', '--check' if setting['checksum'] else '--no-check']
        return compress,[binary,'-q','-d','-c']
    if setting['family']=='lz4':
        compress=[binary,'-q','-z','-c','-T1',f'-{setting["level"]}',f'-B{setting["block_id"]}', '-BD' if setting['dependent'] else '-BI']
        return compress,[binary,'-q','-d','-c']
    raise ValueError('zlib uses its Python API')


def exact_roundtrip(original,decoded):
    if decoded!=original:raise ValueError('Decoded bytes differ from original')
    return hashlib.sha256(decoded).hexdigest()


def measure(setting,payload,binary=None):
    validate_setting(setting)
    if setting["family"]!="zlib":compress,decompress=commands(setting,binary)
    start=time.perf_counter_ns()
    if setting['family']=='zlib':
        compressor=zlib.compressobj(level=setting['level'],wbits=15,memLevel=setting['memory_level'],strategy=zlib.Z_FILTERED if setting['filtered'] else zlib.Z_DEFAULT_STRATEGY)
        compressed=compressor.compress(payload)+compressor.flush()
    else:
        compressed=subprocess.run(compress,input=payload,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=.8).stdout
    compression_ns=time.perf_counter_ns()-start
    start=time.perf_counter_ns()
    if setting['family']=='zlib':decoded=zlib.decompress(compressed)
    else:decoded=subprocess.run(decompress,input=compressed,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=.8).stdout
    decompression_ns=time.perf_counter_ns()-start
    digest=exact_roundtrip(payload,decoded)
    return {'compression_ns':compression_ns,'decompression_ns':decompression_ns,
            'compressed_bytes':len(compressed),'original_bytes':len(payload),
            'decoded_sha256':digest,'compressed_sha256':hashlib.sha256(compressed).hexdigest(),
            'roundtrip_equal':True,
            'timing_scope':'Python zlib API' if setting['family']=='zlib' else 'CLI launch, pipes and codec processing'},compressed


def isolated_trial(command,payload,timeout,cwd,env):
    """Own a process group so a timeout also terminates a spawned codec process."""
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env=env,start_new_session=True)
    try:
        stdout,stderr=process.communicate(payload,timeout=timeout)
        return {'returncode':process.returncode,'stdout':stdout.decode('utf-8'),'stderr':stderr.decode('utf-8'),'timed_out':False}
    except subprocess.TimeoutExpired:
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        stdout,stderr=process.communicate()
        return {'returncode':process.returncode,'stdout':stdout.decode('utf-8',errors='replace'),'stderr':stderr.decode('utf-8',errors='replace'),'timed_out':True}

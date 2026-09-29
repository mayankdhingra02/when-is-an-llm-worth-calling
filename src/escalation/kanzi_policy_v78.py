"""Predeclared legal model interface; observations explicitly allowlisted."""
import json
from .kanzi_v75 import SEEDS,TRANSFORMS,CODECS,grid,features,guard
METHODS=['rf_lcb','nn','llm']
def vectors(configs):return [[TRANSFORMS.index(c['transform']),CODECS.index(c['entropy']),c['block_bytes']] for c in configs]
def validate_acquisition(cid,obs,purpose,count):
    guard(cid,obs,purpose,count)
    if count>=150:raise ValueError('150-trial cap')
def messages(configs,observations):
    rows=[{'configuration':vectors(configs)[o['config_id']],'compressed_bytes':o['compressed_bytes']} for o in observations]
    return [{'role':'system','content':'Select one previously unmeasured lossless-compression configuration to minimize compressed output bytes. Return only a JSON integer array [transform_index,entropy_index,block_bytes]. Do not repeat an observed configuration.'},
      {'role':'user','content':'Kanzi 1.9 with documented output-buffer repair. Fixed generated16MiB input: four equal sections of records, repeated text, structured binary and SHA256-derived bytes. Each trial uses checksum and exact decompression validation; jobs1. Primary objective is compressed bytes, lower is better; runtime is tracked separately, not combined into this objective. Transform index mapping: '+json.dumps(dict(enumerate(TRANSFORMS)))+'. Entropy index mapping: '+json.dumps(dict(enumerate(CODECS)))+'. Allowed block bytes: '+json.dumps(sorted({c['block_bytes'] for c in configs}))+'. All listed combinations are candidates; no full-table objective values are available. Observations in acquisition order: '+json.dumps(rows,separators=(',',':'))+'. Select the next unobserved configuration.'}]

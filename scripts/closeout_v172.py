"""V172 closeout: extend V170 cumulative counters with V172's measured ledgers (computed, not typed)."""
import json
from collect_smollm_v47 import ROOT, read, write, now
from common_v172 import A, M, E, STAGES, FAILED_STAGES

def main():
    old = read(ROOT/'artifacts/study_v170/closeout.json'); dl = read(A/'downloads.json'); mm = read(A/'model_manifest.json'); cfg = read(ROOT/'configs/study_v172.json')
    stages = {s: read(M/s/'ledger.json') for s in ['P', *FAILED_STAGES, *STAGES]}
    requests = sum(l['generation_requests'] for l in stages.values()); sci = sum(l['scientific_requests'] for l in stages.values()); comp = sum(l['compatibility_requests'] for l in stages.values())
    acq = read(E/'ledger.json')['acquisitions']; completion = read(E/'completion.json')
    out = {'at': now(), 'stage': 'v172_model_scale_headroom',
           'new_generation_requests': requests, 'new_scientific_requests': sci, 'new_compatibility_requests': comp, 'model_starts_cumulative': old['model_starts_cumulative']+requests,
           'server_launches': {s: l.get('startup_seconds') is not None for s, l in stages.items()}, 'peak_server_rss_bytes': {s: l['peak_server_rss_bytes'] for s, l in stages.items()},
           'allocated_output_tokens': sum(l['allocated_output_tokens'] for l in stages.values()),
           'new_recorded_acquisitions': acq, 'recorded_acquisition_charges_cumulative': 41613+acq, 'historical_incidental_exposures': 2,
           'new_download_bytes': dl['bytes'], 'retained_download_bytes': cfg['download']['previous_retained_download_bytes']+dl['bytes'],
           'retained_download_cap_bytes': cfg['download']['authorized_retained_download_cap_bytes'],
           'download_bytes_remaining': cfg['download']['authorized_retained_download_cap_bytes']-cfg['download']['previous_retained_download_bytes']-dl['bytes'],
           'model_payload_bytes': cfg['download']['previous_model_payload_bytes']+dl['model_bytes'], 'model_payload_cap_bytes': cfg['download']['authorized_model_payload_cap_bytes'],
           'model_file': {'path': mm['path'], 'sha256': mm['sha256'], 'bytes': mm['bytes'], 'revision': mm['revision']},
           'evaluation_complete': completion['complete'], 'external_spend_usd': 0, 'paid_or_cloud_requests': 0,
           'caps_authorized_by': 'artifacts/study_v172/authorization.json', 'failed_stages': FAILED_STAGES}
    write(A/'closeout.json', out); print(json.dumps(out, indent=1))

if __name__ == '__main__': main()

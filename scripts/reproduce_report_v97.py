"""Deterministic rendering wrapper; leaves frozen scientific analysis unchanged."""
import os
from datetime import datetime
from collect_smollm_v47 import ROOT, read

stamp = read(ROOT/'reports/protocol_v97.freeze.json')['at']
os.environ['SOURCE_DATE_EPOCH'] = str(int(datetime.fromisoformat(stamp).timestamp()))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT/'.cache/matplotlib-v97'))
import matplotlib
matplotlib.rcParams['svg.hashsalt'] = 'llm-escalation-v97'
from report_numerical_v97 import main

if __name__=='__main__':
    main()

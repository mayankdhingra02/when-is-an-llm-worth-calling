"""Preserve frozen calculations and attach the disclosed capacity correction."""
from analyze_proposal_v127 import report,ROOT

def main():
 report();p=ROOT/'reports/proposals_v127.md';text=p.read_text();title,rest=text.split('\n\n',1)
 note='**Capacity correction:** The512-token cap cannot emit the required SAC representation (≥520tokens even before nonbinary settings/delimiters). Its six failures and the resulting impossible all-valid screen are design-caused. Raw results remain unchanged. All five families with valid normal outputs still have negative mean gains versus sequential3NN, and even an ideal SAC-only repair cannot make the overall primary means positive. See [capacity correction and repair bound](capacity_correction_v127.md).\n\n'
 p.write_text(title+'\n\n'+note+rest)
if __name__=='__main__':main()

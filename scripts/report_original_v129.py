"""Clearly label the preserved interrupted V128 policy outcome."""
from report_proposal_v128_corrected import main
from collect_smollm_v47 import ROOT
if __name__=='__main__':
    main()
    p=ROOT/'reports/proposals_v128.md'
    notice='> **Interrupted collection, not a completed LLM comparison.** Two requests were attempted: one returned valid, one was interrupted by a resource-monitor subprocess timeout. Ten jobs were unattempted. Nine of the ten normal branches therefore use the declared classical fallback. The table below is the actual interrupted-policy outcome; it does not establish LLM quality on either family. One request has unknown token usage. Original300acquisitions remain charged. Read the separately frozen V129 recovery report for completed responses and its extra costs.\n\n'
    p.write_text(notice+p.read_text())

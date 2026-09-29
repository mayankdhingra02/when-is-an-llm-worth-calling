"""Render a two-page discussion brief from saved results. No inference/analysis.

Presentation dependency: reportlab==4.4.9 (separate from experiment environment).
"""
import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf/llm_escalation_review.pdf'
INK = colors.HexColor('#172C3B')
BLUE = colors.HexColor('#176B93')
LIGHT = colors.HexColor('#EDF3F6')
GRAY = colors.HexColor('#50616A')
STYLES = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=INK, spaceAfter=10),
    'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=12, leading=16, textColor=GRAY, spaceAfter=14),
    'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=BLUE, spaceBefore=12, spaceAfter=6),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14, textColor=INK, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Helvetica', fontSize=8, leading=11, textColor=GRAY, spaceAfter=5),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=9, leading=12, textColor=INK),
}


def p(text, style='body'):
    return Paragraph(text, STYLES[style])


def read(name):
    return json.loads((ROOT / name).read_text())


def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#CFD9DF'))
    canvas.line(44, 39, 568, 39)
    canvas.setFillColor(GRAY)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(44, 25, 'Local pilot | Discussion draft | 24 September 2026 | No publication or novelty claim')
    canvas.drawRightString(568, 25, str(doc.page))


def main():
    with (ROOT / 'results/v6/policies.csv').open() as f:
        policies = {r['policy']: r for r in csv.DictReader(f)}
    accounting = read('artifacts/study_v21/executed_accounting.json')
    latest = read('results/v21_nonmonotone/summary.json')
    if latest['completed'] != 3 or accounting['followup_requests_used'] != 140:
        raise ValueError('Brief is scoped to the completed V21 snapshot')
    story = [p('When Is an LLM Worth Calling?', 'title'),
             p('Cost- and reliability-aware software optimization<br/>A bounded pilot with real local inference', 'subtitle'),
             p('<b>Result:</b> This setup did not demonstrate useful LLM escalation or useful benefit-aware routing. '
               'Always escalating had worse average held-out loss than continuing classically. '
               'The learned controller chose no calls. This is a small negative pilot, not evidence that LLM optimization generally fails.'),
             p('The experiment', 'heading'),
             p('After <b>10 acquired configuration outcomes</b>, save the classical prefix and run paired classical and LLM continuations, '
               'each with 10 further evaluations (20 total per arm). The optimizer and controller see features and acquired labels only; '
               'full-table scoring is confined to the offline evaluator.'),
             p('The expanded V6 pilot used three development and three held-out software families, with five fixed seeds per family. '
               'Preprocessing and thresholds were fitted on development groups and sealed before test collection. '
               'The local model was <b>Qwen2.5-0.5B-Instruct</b>, with pinned weights, CPU float32 and greedy constrained decoding. '
               'The classical method and changed model are adaptations, not a numerical replication of SNAP2.'),
             p('Held-out result: 15 cases from three software families', 'heading')]
    rows = [[p('<b>Policy</b>', 'cell'), p('<b>Mean loss<br/>(lower is better)</b>', 'cell'), p('<b>Escalations</b>', 'cell')]]
    for key, label in [('never', 'Continue classically'), ('always', 'Always escalate'),
                       ('benefit', 'Benefit-aware controller'), ('uncertainty', 'Uncertainty-only controller'),
                       ('hindsight_oracle_diagnostic', 'Hindsight oracle (not deployable)')]:
        row = policies[key]
        rows.append([p(label, 'cell'), f"{float(row['group_mean_loss']):.5f}", f"{row['escalations']} / {row['cases']}"])
    table = Table(rows, colWidths=[286, 132, 106], hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), LIGHT), ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                              ('FONTSIZE', (0, 0), (-1, -1), 10), ('TEXTCOLOR', (0, 0), (-1, -1), INK),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 9),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 9), ('LINEBELOW', (0, 0), (-1, 0), 0.7, BLUE),
                              ('LINEBELOW', (0, 1), (-1, -1), 0.3, colors.HexColor('#DDE5E9'))]))
    story += [table, Spacer(1, 9),
              p('Both random-escalation comparisons also selected zero calls at the matched rate. '
                'That makes the routing comparison uninformative about selection quality at a nonzero rate. '
                'Always escalating yielded two material benefits and three material harms at the frozen 0.02 loss margin. '
                'Repeated seeds do not turn three test families into 15 independent systems.'),
              p('What this supports', 'heading'),
              p('A working, auditable experiment pipeline and an honest failure to establish the proposed routing advantage. '
                'The original question remains open for stronger models and adequately sampled, untouched systems. '
                'All six V6 families are now exposed and cannot serve as fresh test groups in an adaptive follow-up.'),
              p('Evidence: results/v6/policies.csv; router_seal.json; prefixes/; paired/; classical/. '
                'Methods and limitations: reports/pilot_report_v6.md and reports/source_audit.md.', 'small'),
              PageBreak(), p('Why inspect the selections?', 'title'),
              p('A diagnostic finding, with counterexamples retained', 'subtitle'),
              p('V8 produced 15 selections identical to choosing the first ten displayed candidates. '
                'V19 tested nine fresh conditions over three exposed cases: reversing the display replaced all ten selected configurations; '
                'reversing IDs while retaining feature order preserved all ten. However, monotone ID orders left alternative explanations unresolved.'),
              p('V21 fixed interleaved IDs before three new calls. MySQL selected the first ten displayed entries; lrzip and Brotli returned IDs 0-9, '
                'selecting alternating display positions. Neither simple rule explained every case. These are actual model outputs, not rule-generated fixtures.')]
    figure = ROOT / 'results/v21_nonmonotone/interleaved_selection.png'
    width, height = ImageReader(str(figure)).getSize()
    story.append(Image(str(figure), width=496, height=496 * height / width))
    story += [p('One response per exposed case; no fresh original-condition repeats in V21. '
                'The observations do not identify an internal algorithm, establish generalization, or show that changed selections improve optimization.', 'small'),
              p('Costs and reliability', 'heading'),
              p(f"The complete history includes <b>{accounting['historical_attempts_including_initial']} model attempts</b>, "
                f"including failed/superseded stages; the follow-up allowance is exhausted at {accounting['followup_requests_used']}/140. "
                f"Recorded experiment time is {accounting['cumulative_experiment_seconds']:,.2f}/1,800 seconds; external spend is <b>USD 0</b>. "
                'Electricity and hardware cost are unknown. V19/V21 completed all 12 intended calls with no retries or failures.'),
              p(f"Historical collection totals are {accounting['total_recorded_objective_acquisitions']:,} recorded-table objective acquisitions "
                f"and {accounting['total_physical_trials']:,} separate physical compression trials. These are different cost types, "
                'not one pooled evaluation count. Collection includes both branches and failures; modeled deployment counts only the selected branch. '
                'The compression tasks offered under 3% recorded improvement even from their initial references.'),
              p('Decision for discussion', 'heading'),
              p('<b>Review whether this limited methodological finding warrants a larger study.</b> '
                'If it does, prospectively fix formatting controls and repeated original conditions, then evaluate another model independently. '
                'Only proceed to router evaluation on application-grounded tasks with meaningful headroom and untouched system families. '
                'Do not keep changing prompts until a favorable score appears.'),
              p('Review bundle: start with BUNDLE_README.md. It contains selected evidence and all project code, but excludes weights, '
                'downloaded source tables/papers and physical payloads. Full reproduction needs those separately retained inputs. '
                '147 tests passed in the supplied workspace; fresh-machine reconstruction is untested.', 'small'),
              p('Primary starting point: Srinivasan &amp; Menzies, <i>Better Together, in the Right Order</i>, '
                '<link href="https://arxiv.org/abs/2607.02583v1" color="#176B93">arXiv:2607.02583v1</link>. '
                'The exact SNAP2 artifact was not located in the bounded audit. Conditional escalation itself is prior work. '
                'Full evidence paths: reports/review_evidence.md.', 'small')]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=(612, 792), leftMargin=44, rightMargin=44,
                            topMargin=42, bottomMargin=52, title='When Is an LLM Worth Calling? - Pilot review',
                            author='LLM escalation study project')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == '__main__':
    main()

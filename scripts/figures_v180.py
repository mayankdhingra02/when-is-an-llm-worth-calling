"""V180: manuscript figures from the saved case records (no new data). Deterministic PDF output.

    .venv/bin/python scripts/figures_v180.py
writes paper/overleaf_v180/figures/{design,case_gains,draw_variability}.pdf
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from collect_smollm_v47 import ROOT
import revision_v174 as r174

OUT = ROOT/'paper/overleaf_v180/figures'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 8.5, 'axes.linewidth': 0.6, 'pdf.fonttype': 42, 'svg.hashsalt': 'v180'})
SH, OTHER, INK = '#D55E00', '#6E6E6E', '#000000'
META = {'CreationDate': None, 'ModDate': None, 'Producer': None, 'Creator': None}

def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True); fig.savefig(OUT/f'{name}.pdf', bbox_inches='tight', metadata=META); plt.close(fig)

def box(ax, x, y, w, h, text, fc='#FFFFFF', ec=INK, lw=0.7, size=8, weight='normal'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.012,rounding_size=0.02', fc=fc, ec=ec, lw=lw))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=size, weight=weight, linespacing=1.25)

def arrow(ax, x0, y0, x1, y1, style='-|>', ls='-'):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=style, lw=0.7, color=INK, linestyle=ls, shrinkA=0, shrinkB=0))

def design():
    fig, ax = plt.subplots(figsize=(6.4, 3.0)); ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.axis('off')
    box(ax, 0.00, 0.33, 0.20, 0.30, 'Saved prefix:\n10 labelled\nconfigurations,\nshared by all arms', fc='#F2F2F2', size=7.5)
    box(ax, 0.00, 0.80, 0.20, 0.15, 'Controller\n(prefix features)', size=7.5)
    arrow(ax, 0.10, 0.63, 0.10, 0.80); ax.text(0.112, 0.715, 'call the\nLLM?', fontsize=6.8, va='center')
    arms = [('Sequential 3NN (reference)', '#F2F2F2'), ('Random search', '#FFFFFF'), ('Adaptive / fixed neighbour', '#FFFFFF'), ('GP-EI', '#FFFFFF'),
            ('Prefix optimizer continued', '#FFFFFF'), ('LLM, one call: 10 proposals', '#FBE3D6'), ('LLM loop: 5 rounds of 2', '#FBE3D6')]
    ys = np.linspace(0.90, 0.10, len(arms)); h = 0.085
    for (label, fc), y in zip(arms, ys):
        box(ax, 0.30, y-h/2, 0.34, h, label, fc=fc, size=7.3); arrow(ax, 0.205, 0.48, 0.295, y); arrow(ax, 0.645, y, 0.715, y)
    ax.text(0.47, 0.985, 'each arm acquires 10 more charged labels', ha='center', fontsize=6.8, style='italic')
    box(ax, 0.72, 0.05, 0.28, 0.90, 'Result of each arm:\nbest of its 20 labels\n\nrelative gain over\nsequential 3NN,\nper case\n\ncompared across\nall arms', fc='#F2F2F2', size=7.5)
    save(fig, 'design')

ROWS = [('random_full', 'Random search'), ('adaptive_neighbor', 'Adaptive neighbour'), ('gp_ei', 'GP-EI'), ('smollm3_3b', 'SmolLM3-3B'), ('qwen3_8b', 'Qwen3-8B'),
        ('qwen3_14b', 'Qwen3-14B'), ('gptoss_a1', 'gpt-oss-120b, draw 1'), ('gptoss_a2', 'gpt-oss-120b, draw 2'), ('gptoss_b', 'gpt-oss-120b, loop')]

def case_gains(base):
    cs = sorted(base.values(), key=lambda c: c['key']); eco = [c['ecosystem'] for c in cs]
    fig, ax = plt.subplots(figsize=(6.4, 3.6)); rng = np.random.default_rng(180)
    ax.axvspan(-1, 1, color='#EDEDED', lw=0); ax.axvline(0, color=INK, lw=0.6)
    for i, (a, label) in enumerate(ROWS):
        y = len(ROWS)-1-i; g = np.array([100*r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs])
        jit = rng.uniform(-0.22, 0.22, len(g)); sh = np.array([e == 'spark_hadoop' for e in eco])
        ax.scatter(g[~sh], y+jit[~sh], s=9, c=OTHER, alpha=0.75, lw=0, zorder=2)
        ax.scatter(g[sh], y+jit[sh], s=9, c=SH, alpha=0.85, lw=0, zorder=3)
        ax.scatter([g.mean()], [y], marker='o', s=48, facecolor='white', edgecolor=INK, lw=0.9, zorder=4)
        ax.scatter([100*r174.group_mean(list(g/100), eco)], [y], marker='D', s=16, facecolor=INK, edgecolor='white', lw=0.4, zorder=5)
        if i == 2: ax.axhline(y-0.5, color='#BBBBBB', lw=0.5)
    allg = [100*r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for a, _ in ROWS for c in cs]
    assert -62 < min(allg) and max(allg) < 34, (min(allg), max(allg))  # every case must be visible
    ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([l for _, l in ROWS][::-1]); ax.set_xlim(-62, 34)
    ax.set_xlabel('Relative gain over sequential 3NN from the same prefix (%)'); ax.tick_params(length=2.5, width=0.6)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], ls='', marker='o', ms=4, mfc=SH, mec=SH, label='case, Spark/Hadoop'), Line2D([], [], ls='', marker='o', ms=4, mfc=OTHER, mec=OTHER, label='case, other ecosystems'),
          Line2D([], [], ls='', marker='D', ms=4, mfc=INK, mec='white', label='ecosystem-balanced mean'), Line2D([], [], ls='', marker='o', ms=6, mfc='white', mec=INK, label='case-weighted mean')]
    ax.legend(handles=hs, loc='lower left', fontsize=7, frameon=False, ncol=2, bbox_to_anchor=(0.0, 1.0))
    save(fig, 'case_gains')

def draw_variability(base):
    cs = sorted(base.values(), key=lambda c: c['key']); sh = np.array([c['ecosystem'] == 'spark_hadoop' for c in cs])
    g = lambda a: np.array([100*r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs])
    diff = lambda ref, a: np.array([r174.gain(c['raw'][ref], c['raw'][a], c['direction']) for c in cs])
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0))
    for ax, (xa, ya, xl, yl) in zip(axes, [('gptoss_a1', 'gptoss_a2', 'one-shot, draw 1', 'one-shot, draw 2'), ('gptoss_a1', 'gptoss_b', 'one-shot, draw 1', 'iterative loop')]):
        x, y, d = g(xa), g(ya), diff(xa, ya); apart = np.abs(d) > r174.M
        lo = min(x.min(), y.min()); hi = max(x.max(), y.max()); assert lo > -62 and hi < 34, (lo, hi)  # every case must be visible
        lim = (-62, 34); ax.plot(lim, lim, color=INK, lw=0.6, zorder=1)
        for mask, col in [(~sh, OTHER), (sh, SH)]:
            ax.scatter(x[mask & ~apart], y[mask & ~apart], s=12, facecolor='white', edgecolor=col, lw=0.8, zorder=2)
            ax.scatter(x[mask & apart], y[mask & apart], s=12, facecolor=col, edgecolor=col, lw=0.8, zorder=3)
        up, down = int((d > r174.M).sum()), int((d < -r174.M).sum())
        ax.text(0.03, 0.97, f'{int(apart.sum())} of {len(cs)} cases differ by >1%\n({up} higher, {down} lower on the y-axis)', transform=ax.transAxes, va='top', fontsize=7)
        ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_aspect('equal'); ax.set_xlabel(f'gain, {xl} (%)'); ax.set_ylabel(f'gain, {yl} (%)')
        ax.tick_params(length=2.5, width=0.6)
        for s in ['top', 'right']: ax.spines[s].set_visible(False)
    fig.tight_layout(w_pad=2.0); save(fig, 'draw_variability')
    return {'a1_vs_a2_apart': int((np.abs(diff('gptoss_a1', 'gptoss_a2')) > r174.M).sum()), 'loop_vs_a1': (int((diff('gptoss_a1', 'gptoss_b') > r174.M).sum()), int((diff('gptoss_a1', 'gptoss_b') < -r174.M).sum()))}

def main():
    base = r174.load_cases(); design(); case_gains(base); print(draw_variability(base))

if __name__ == '__main__': main()

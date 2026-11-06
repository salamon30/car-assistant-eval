# Draws docs/strategies.svg: bugs found vs. budget for each strategy, in two cost scenarios.
# The lines draw themselves when the page loads (CSS animation), which also works in a GitHub README.
import random

from simulate import REAL_BUGS, STRATEGIES, simulate

REPEATS = 300
SHORT = ["A · only level 2", "B · only level 0", "C · level 0, then 2", "D · level 1, then 2"]
LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
DARK = ["#3987e5", "#d95926", "#199e70", "#c98500"]

PANELS = [
    ("Level 2 costs 3×  (measured)", {0: 1, 1: 1, 2: 3}, list(range(0, 181, 15))),
    ("Level 2 costs 20×  (real car)", {0: 1, 1: 1, 2: 20}, list(range(0, 801, 50))),
]

W, H = 1000, 440
PW, PH = 330, 270          # plot area of one panel
TOP = 80
LEFTS = [60, 560]
YMAX = 20


def average(strategy, budget, cost):
    rng = random.Random(0)
    return sum(simulate(strategy, budget, cost, rng) for _ in range(REPEATS)) / REPEATS


def panel(title, cost, budgets, left):
    out = []
    xmax = budgets[-1]
    sx = lambda b: left + b / xmax * PW
    sy = lambda v: TOP + PH - v / YMAX * PH
    out.append(f'<text class="title" x="{left}" y="{TOP - 30}">{title}</text>')
    for v in range(0, YMAX + 1, 5):
        out.append(f'<line class="grid" x1="{left}" x2="{left + PW}" y1="{sy(v):.1f}" y2="{sy(v):.1f}"/>')
        out.append(f'<text class="tick" x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for b in budgets[:: max(1, len(budgets) // 4)] + ([] if (len(budgets) - 1) % max(1, len(budgets) // 4) == 0 else [budgets[-1]]):
        out.append(f'<text class="tick" x="{sx(b):.1f}" y="{TOP + PH + 20}" text-anchor="middle">{b}</text>')
    out.append(f'<line class="axis" x1="{left}" x2="{left + PW}" y1="{TOP + PH}" y2="{TOP + PH}"/>')
    out.append(f'<text class="axlab" x="{left + PW / 2}" y="{TOP + PH + 42}" text-anchor="middle">budget (cost units)</text>')

    ends = []
    for i, strategy in enumerate(STRATEGIES):
        values = [average(strategy, b, cost) for b in budgets]
        points = " ".join(f"{sx(b):.1f},{sy(v):.1f}" for b, v in zip(budgets, values))
        out.append(f'<polyline class="line s{i} d{i}" pathLength="1" points="{points}"/>')
        out.append(f'<circle class="end s{i}f d{i}e" cx="{sx(budgets[-1]):.1f}" cy="{sy(values[-1]):.1f}" r="4"/>')
        ends.append([sy(values[-1]), i, values])
    # direct labels at the line ends, nudged apart so they do not overlap
    ends.sort()
    last = -99
    for y, i, values in ends:
        y = max(y, last + 15)
        last = y
        out.append(f'<text class="lbl d{i}e" x="{left + PW + 10}" y="{y + 4:.1f}">{SHORT[i][0]}</text>')
    return out, values


def build():
    parts = []
    for title, cost, budgets, left in [(p[0], p[1], p[2], l) for p, l in zip(PANELS, LEFTS)]:
        body, _ = panel(title, cost, budgets, left)
        parts += body

    # headline annotation in the expensive panel, at budget 100
    cost, budgets = PANELS[1][1], PANELS[1][2]
    a, d = average(STRATEGIES[0], 100, cost), average(STRATEGIES[3], 100, cost)
    x = LEFTS[1] + 100 / budgets[-1] * PW
    yd = TOP + PH - d / YMAX * PH
    parts.append(f'<g class="note"><line class="noteline" x1="{x + 5:.1f}" y1="{yd + 4:.1f}" x2="{x + 48:.1f}" y2="{yd + 28:.1f}"/>'
                 f'<text class="notetext" x="{x + 52:.1f}" y="{yd + 34:.1f}">D finds {d / a:.1f}× more bugs</text>'
                 f'<text class="notesub" x="{x + 52:.1f}" y="{yd + 50:.1f}">than A on a small budget</text></g>')

    legend = []
    for i, name in enumerate(SHORT):
        lx = 60 + i * 230
        legend.append(f'<line class="line s{i} static" x1="{lx}" x2="{lx + 22}" y1="{H - 22}" y2="{H - 22}"/>'
                      f'<text class="leg" x="{lx + 30}" y="{H - 18}">{name}</text>')

    css_series = "\n".join(
        f"    .s{i} {{ stroke: {c}; }} .s{i}f {{ fill: {c}; }}" for i, c in enumerate(LIGHT))
    css_dark = "\n".join(
        f"      .s{i} {{ stroke: {c}; }} .s{i}f {{ fill: {c}; }}" for i, c in enumerate(DARK))
    css_delay = "\n".join(
        f"    .d{i} {{ animation-delay: {i * 0.5}s; }} .d{i}e {{ animation-delay: {i * 0.5 + 1.6}s; }}" for i in range(4))

    body = "\n  ".join(parts)
    legend_svg = "\n  ".join(legend)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <title>Bugs found vs. budget for four testing strategies. With cheap audio tests, testing everything at level 2 wins. With expensive audio tests, screening with simulated ASR errors first finds the most bugs on small budgets.</title>
  <style>
    .bg {{ fill: #fcfcfb; }}
    .title {{ fill: #0b0b0b; font-size: 15px; font-weight: 600; }}
    .tick, .axlab {{ fill: #52514e; font-size: 11.5px; }}
    .ylab {{ fill: #52514e; font-size: 11.5px; }}
    .leg, .lbl {{ fill: #0b0b0b; font-size: 12.5px; }}
    .lbl {{ font-weight: 700; }}
    .grid {{ stroke: #e6e5e0; stroke-width: 1; }}
    .axis {{ stroke: #9b9a94; stroke-width: 1; }}
    .line {{ fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
             stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 2s ease-out forwards; }}
    .line.static {{ stroke-dashoffset: 0; animation: none; }}
    .end, .lbl {{ opacity: 0; animation: show .4s ease-out forwards; }}
    .note {{ opacity: 0; animation: show .6s ease-out 3.6s forwards; }}
    .noteline {{ stroke: #52514e; stroke-width: 1; }}
    .notetext {{ fill: #0b0b0b; font-size: 13px; font-weight: 700; }}
    .notesub {{ fill: #52514e; font-size: 11.5px; }}
{css_series}
{css_delay}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes show {{ to {{ opacity: 1; }} }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #1a1a19; }}
      .title, .leg, .lbl, .notetext {{ fill: #f0efec; }}
      .tick, .axlab, .ylab, .notesub {{ fill: #c3c2b7; }}
      .grid {{ stroke: #2e2e2c; }}
      .axis, .noteline {{ stroke: #6b6a64; }}
{css_dark}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .line {{ stroke-dashoffset: 0; animation: none; }}
      .end, .lbl, .note {{ opacity: 1; animation: none; }}
    }}
  </style>
  <rect class="bg" width="{W}" height="{H}" rx="10"/>
  <text class="ylab" x="{LEFTS[0] - 40}" y="{TOP - 10}">real bugs found (of {len(REAL_BUGS)})</text>
  <text class="ylab" x="{LEFTS[1] - 40}" y="{TOP - 10}">real bugs found (of {len(REAL_BUGS)})</text>
  {body}
  {legend_svg}
</svg>
'''


if __name__ == "__main__":
    with open("docs/strategies.svg", "w") as f:
        f.write(build())
    print("Saved docs/strategies.svg")

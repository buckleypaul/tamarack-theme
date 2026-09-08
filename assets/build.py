"""Preview images for Tamarack.

Reads palette.json and writes SVG previews into this directory. Pure standard
library, and deterministic: the same palette always produces byte-identical
files, so the drift check in CI stays quiet.

  python3 assets/build.py
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with open(os.path.join(ROOT, 'palette.json')) as fh:
    PALETTE = json.load(fh)

FLAVORS = sorted(PALETTE.items(), key=lambda kv: kv[1]['order'])

# Token names and their accent/neutral split are shared by every flavor, so the
# first one by order stands in for all of them.
_REF = FLAVORS[0][1]['colors']
ACCENTS = [n for n, c in _REF.items() if c['accent']]
NEUTRALS = [n for n, c in _REF.items() if not c['accent']]

SANS = ('ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", '
        'Helvetica, Arial, sans-serif')
MONO = ('ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, '
        '"Liberation Mono", monospace')

# Monospace advance width at font-size 15. Every mainstream mono face in the
# stack above is exactly 0.6em, so the columns line up without measuring.
FSIZE = 15
ADV = 9
LINE = 24


# ---------- color helpers ----------
def _lum(hexv):
    h = hexv.lstrip('#')
    out = 0.0
    for i, w in ((0, 0.2126), (2, 0.7152), (4, 0.0722)):
        v = int(h[i:i + 2], 16) / 255
        v = v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        out += v * w
    return out


def ratio(a, b):
    l1, l2 = _lum(a), _lum(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def hexv(flavor, token):
    return PALETTE[flavor]['colors'][token]['hex']


def ink(flavor, swatch):
    """The more legible of the flavor's own text and base, over `swatch`."""
    text, base = hexv(flavor, 'text'), hexv(flavor, 'base')
    return text if ratio(swatch, text) >= ratio(swatch, base) else base


def role(flavor, token):
    """How this flavor treats an accent: it leads with one, pushes a family of
    them forward, and pulls the rest back."""
    f = PALETTE[flavor]
    if token == f['hero']:
        return 'hero'
    return 'family' if token in f['family'] else 'muted'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text_el(x, y, s, fill, size=13, family=SANS, weight=None,
            anchor=None, opacity=None, length=None, spacing=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'font-family=\'{family}\'',
             f'font-size="{size}"', f'fill="{fill}"']
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if length:
        attrs.append(f'textLength="{length}" lengthAdjust="spacing"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if opacity:
        attrs.append(f'fill-opacity="{opacity}"')
    return f'  <text {" ".join(attrs)}>{esc(s)}</text>'


def code_line(x0, y, spans, flavor):
    """One line of colored code, positioned column by column.

    SVG trims whitespace at the edges of a <text> run, so each span is placed
    at its own absolute x and its padding is carried in the offset instead.
    Each run is also pinned to `textLength`, which keeps the columns aligned
    even where the viewer substitutes a font of a different advance width.
    """
    out, col = [], 0
    for token, span in spans:
        stripped = span.strip()
        if stripped:
            lead = len(span) - len(span.lstrip())
            out.append(text_el(x0 + (col + lead) * ADV, y, stripped,
                               hexv(flavor, token), size=FSIZE, family=MONO,
                               length=len(stripped) * ADV))
        col += len(span)
    return out


def svg(width, height, body, title):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{esc(title)}">')
    return '\n'.join([head, f'  <title>{esc(title)}</title>'] + body + ['</svg>', ''])


def write(name, content):
    with open(os.path.join(HERE, name), 'w') as fh:
        fh.write(content)
    return name


# ---------- swatch sheet ----------
PAD = 36
SHEET_W = 968
CONTENT = SHEET_W - 2 * PAD          # 896
A_COLS, A_W, A_GAP, A_H = 3, 288, 16, 84
N_COLS, N_W, N_GAP, N_H = 6, 141, 10, 72


def card(x, y, w, h, flavor, token, show_ratio, rank=None):
    """One swatch. A pulled-back accent (`rank` "muted") is inset so its band of
    color sits lower than the ones the flavor pushes forward; the hero wears a
    ring and a tag. Neutrals pass no rank and keep the plain card."""
    fill = hexv(flavor, token)
    label = ink(flavor, fill)
    inset = 9 if rank == 'muted' else 0
    ry, rh = y + inset, h - 2 * inset

    parts = []
    if rank == 'hero':
        parts.append(f'  <rect x="{x - 5}" y="{ry - 5}" width="{w + 10}" '
                     f'height="{rh + 10}" rx="13" fill="none" '
                     f'stroke="{hexv(flavor, "text")}" stroke-width="2"/>')
    parts.append(f'  <rect x="{x}" y="{ry}" width="{w}" height="{rh}" rx="8" '
                 f'fill="{fill}" stroke="{hexv(flavor, "overlay0")}" '
                 f'stroke-opacity="0.35"/>')
    parts.append(text_el(x + 14, ry + (30 if show_ratio else 28), token, label,
                         size=14, family=MONO, weight='600'))
    parts.append(text_el(x + 14, ry + (52 if show_ratio else 48), fill.lower(),
                         label, size=12.5, family=MONO, opacity='0.75'))
    if rank == 'hero':
        parts.append(text_el(x + w - 14, ry + 30, 'HERO', label, size=10.5,
                             weight='700', anchor='end', spacing='1.4'))
    elif rank == 'family':
        parts.append(text_el(x + w - 14, ry + 30, 'FAMILY', label, size=10.5,
                             weight='600', anchor='end', opacity='0.7',
                             spacing='1.4'))
    if show_ratio:
        r = PALETTE[flavor]['colors'][token]['contrastOnBase']
        parts.append(text_el(x + w - 14, ry + 52, f'{r}:1', label, size=12.5,
                             family=MONO, anchor='end', opacity='0.75'))
    return parts


def sheet(flavor):
    f = PALETTE[flavor]
    base, text, sub = hexv(flavor, 'base'), hexv(flavor, 'text'), hexv(flavor, 'subtext0')

    a_top = 138
    a_bottom = a_top + 3 * A_H + 2 * A_GAP          # 422
    n_top = a_bottom + 52                            # 474
    n_bottom = n_top + 2 * N_H + N_GAP               # 628
    height = n_bottom + PAD

    body = [f'  <rect width="{SHEET_W}" height="{height}" fill="{base}"/>']
    body.append(text_el(PAD, 62, f'Tamarack {f["name"]}', text, size=26, weight='600'))
    body.append(text_el(PAD, 86, f'{"dark" if f["dark"] else "light"} season '
                                 f'· base {base.lower()} · contrast measured on base',
                        sub, size=13))

    body.append(text_el(PAD, a_top - 14, 'ACCENTS', sub, size=11,
                        weight='600', opacity='0.85'))
    body.append(text_el(PAD + CONTENT, a_top - 14,
                        f'hero {f["hero"]} · family {", ".join(f["family"])} '
                        f'pushed forward · others pulled back',
                        sub, size=11, anchor='end', opacity='0.85'))
    for i, token in enumerate(ACCENTS):
        x = PAD + (i % A_COLS) * (A_W + A_GAP)
        y = a_top + (i // A_COLS) * (A_H + A_GAP)
        body += card(x, y, A_W, A_H, flavor, token, True, role(flavor, token))

    body.append(text_el(PAD, n_top - 14, 'NEUTRALS', sub, size=11,
                        weight='600', opacity='0.85'))
    for i, token in enumerate(NEUTRALS):
        x = PAD + (i % N_COLS) * (N_W + N_GAP)
        y = n_top + (i // N_COLS) * (N_H + N_GAP)
        body += card(x, y, N_W, N_H, flavor, token, False)

    return svg(SHEET_W, height, body, f'Tamarack {f["name"]} palette swatches')


# ---------- syntax mock ----------
# (token, text) spans, hand-assigned against the Roles → Syntax table.
KW, TYPE, FN, STR, NUM = 'clay', 'juniper', 'ember', 'fern', 'amber'
OP, PROP, CONST, TAG = 'creek', 'slate', 'chokeberry', 'moss'
COM, PUN, ID = 'overlay1', 'subtext0', 'text'

SAMPLE = [
    [(COM, '// Larix laricina — the conifer that goes gold, then bare.')],
    [(KW, 'import'), (PUN, ' { '), (TYPE, 'Season'), (PUN, ' } '), (KW, 'from'),
     (ID, ' '), (STR, '"./almanac"'), (PUN, ';')],
    [],
    [(KW, 'export interface'), (ID, ' '), (TYPE, 'Larch'), (PUN, ' {')],
    [(PROP, '  species'), (PUN, ': '), (TYPE, 'string'), (PUN, ';')],
    [(PROP, '  needles'), (PUN, ': '), (TYPE, 'number'), (PUN, ';')],
    [(PUN, '}')],
    [],
    [(CONST, '@stand'), (PUN, '('), (STR, '"north"'), (PUN, ')')],
    [(KW, 'export class'), (ID, ' '), (TYPE, 'Tamarack'), (ID, ' '),
     (KW, 'implements'), (ID, ' '), (TYPE, 'Larch'), (PUN, ' {')],
    [(PROP, '  species'), (OP, ' = '), (STR, '"Larix laricina"'), (PUN, ';')],
    [(PROP, '  needles'), (OP, ' = '), (NUM, '34'), (PUN, ';')],
    [],
    [(ID, '  '), (FN, 'turns'), (PUN, '('), (PROP, 'season'), (PUN, ': '),
     (TYPE, 'Season'), (PUN, '): '), (TYPE, 'boolean'), (PUN, ' {')],
    [(KW, '    return'), (ID, ' season '), (OP, '==='), (ID, ' '),
     (TYPE, 'Season'), (PUN, '.'), (CONST, 'Autumn'), (OP, ' && '),
     (KW, 'this'), (PUN, '.'), (PROP, 'needles'), (OP, ' > '), (NUM, '0'),
     (PUN, ';')],
    [(PUN, '  }')],
    [(PUN, '}')],
    [],
    [(KW, 'export const'), (ID, ' '), (TYPE, 'Badge'), (OP, ' = '),
     (PUN, '({ '), (PROP, 'label'), (PUN, ' }: '), (TYPE, 'Props'),
     (PUN, ') => ('), ],
    [(PUN, '  <'), (TAG, 'span'), (ID, ' '), (PROP, 'className'), (OP, '='),
     (STR, '"needle"'), (PUN, '>{'), (ID, 'label'), (PUN, '}</'), (TAG, 'span'),
     (PUN, '>')],
    [(PUN, ');')],
]

GUTTER = 52
CODE_X = GUTTER + 16
BAR_H = 40
CODE_PAD = 16


def syntax(flavor):
    f = PALETTE[flavor]
    base, mantle, crust = hexv(flavor, 'base'), hexv(flavor, 'mantle'), hexv(flavor, 'crust')

    cols = max(sum(len(t) for _, t in line) for line in SAMPLE)
    width = CODE_X + cols * ADV + 24
    height = BAR_H + 2 * CODE_PAD + len(SAMPLE) * LINE

    body = [f'  <rect width="{width}" height="{height}" rx="10" fill="{base}"/>',
            f'  <path d="M0 10a10 10 0 0 1 10-10h{width - 20}a10 10 0 0 1 10 10'
            f'v{BAR_H - 10}H0Z" fill="{mantle}"/>',
            f'  <rect x="0" y="{BAR_H}" width="{GUTTER}" '
            f'height="{height - BAR_H - 10}" fill="{mantle}"/>',
            f'  <rect x="0" y="{BAR_H - 1}" width="{width}" height="1" '
            f'fill="{crust}"/>']

    for i, dot in enumerate(['clay', 'amber', 'fern']):
        body.append(f'  <circle cx="{20 + i * 18}" cy="{BAR_H // 2}" r="5" '
                    f'fill="{hexv(flavor, dot)}"/>')
    body.append(text_el(width // 2, BAR_H // 2 + 4, 'tamarack.tsx',
                        hexv(flavor, 'subtext0'), size=12.5, family=MONO,
                        anchor='middle'))
    body.append(text_el(width - 20, BAR_H // 2 + 4, f['name'],
                        hexv(flavor, 'overlay1'), size=11, weight='600',
                        anchor='end'))

    for i, line in enumerate(SAMPLE):
        y = BAR_H + CODE_PAD + 17 + i * LINE
        body.append(text_el(GUTTER - 14, y, str(i + 1), hexv(flavor, 'overlay0'),
                            size=12.5, family=MONO, anchor='end'))
        body += code_line(CODE_X, y, line, flavor)

    return svg(width, height, body, f'Tamarack {f["name"]} syntax preview')


# ---------- hero ----------
HERO_PAD = 40
HERO_CONTENT = 504
PANEL_W = HERO_CONTENT + 2 * HERO_PAD    # 584
HERO_H = 336
SW, SW_GAP = 48, 9
RAMP_H = 26

HERO_CODE = [
    [(COM, '// the larch that turns gold, then drops the lot')],
    [(KW, 'const'), (ID, ' gold '), (OP, '= '), (ID, 'larch'), (PUN, '.'),
     (FN, 'turn'), (PUN, '('), (TYPE, 'Season'), (PUN, '.'), (CONST, 'Autumn'),
     (PUN, ', '), (NUM, '34'), (PUN, ');')],
    [(PUN, '<'), (TAG, 'needle'), (ID, ' '), (PROP, 'name'), (OP, '='),
     (STR, '"tamarack"'), (PUN, ' />')],
]


def panel(flavor, x0, y0):
    f = PALETTE[flavor]
    base, text, sub = hexv(flavor, 'base'), hexv(flavor, 'text'), hexv(flavor, 'subtext0')
    px = x0 + HERO_PAD

    body = [f'  <rect x="{x0}" y="{y0}" width="{PANEL_W}" height="{HERO_H}" '
            f'fill="{base}"/>']
    body.append(text_el(px, y0 + 68, f['name'], text, size=27, weight='600'))
    body.append(text_el(px, y0 + 92, f'{"dark" if f["dark"] else "light"} '
                                    f'· base {base.lower()} '
                                    f'· leads with {f["hero"]}', sub, size=13))

    for i, token in enumerate(ACCENTS):
        x = px + i * (SW + SW_GAP)
        rank = role(flavor, token)
        # Pulled-back accents sit as a shorter band; the hero wears a ring.
        h = 36 if rank == 'muted' else SW
        y = y0 + 112 + (SW - h) // 2
        body.append(f'  <rect x="{x}" y="{y}" width="{SW}" height="{h}" '
                    f'rx="{6 if rank == "muted" else 8}" '
                    f'fill="{hexv(flavor, token)}"/>')
        if rank == 'hero':
            body.append(f'  <rect x="{x - 4}" y="{y - 4}" width="{SW + 8}" '
                        f'height="{h + 8}" rx="12" fill="none" '
                        f'stroke="{text}" stroke-width="2"/>')

    for i, token in enumerate(NEUTRALS):
        a = px + (i * HERO_CONTENT) // len(NEUTRALS)
        b = px + ((i + 1) * HERO_CONTENT) // len(NEUTRALS)
        body.append(f'  <rect x="{a}" y="{y0 + 180}" width="{b - a}" '
                    f'height="{RAMP_H}" fill="{hexv(flavor, token)}"/>')
    body.append(f'  <rect x="{px}" y="{y0 + 180}" width="{HERO_CONTENT}" '
                f'height="{RAMP_H}" fill="none" '
                f'stroke="{hexv(flavor, "overlay0")}" stroke-opacity="0.35"/>')

    for i, line in enumerate(HERO_CODE):
        body += code_line(px, y0 + 244 + i * LINE, line, flavor)
    return body


def hero():
    """Four seasons on a 2x2 grid, in palette order."""
    cols = 2
    rows = (len(FLAVORS) + cols - 1) // cols
    width, height = cols * PANEL_W, rows * HERO_H

    # Rules are drawn in the darkest flavor's crust so they read on every panel.
    rule = hexv(max(FLAVORS, key=lambda kv: kv[1]['dark'])[0], 'crust')

    body = []
    for i, (key, _) in enumerate(FLAVORS):
        body += panel(key, (i % cols) * PANEL_W, (i // cols) * HERO_H)
    for c in range(1, cols):
        body.append(f'  <rect x="{c * PANEL_W - 1}" y="0" width="2" '
                    f'height="{height}" fill="{rule}" fill-opacity="0.5"/>')
    for r in range(1, rows):
        body.append(f'  <rect x="0" y="{r * HERO_H - 1}" width="{width}" '
                    f'height="2" fill="{rule}" fill-opacity="0.5"/>')
    return svg(width, height, body,
               'Tamarack — ' + ', '.join(f['name'] for _, f in FLAVORS))


written = [write('tamarack-hero.svg', hero())]
for key, _ in FLAVORS:
    written.append(write(f'tamarack-{key}-palette.svg', sheet(key)))
    written.append(write(f'tamarack-{key}-syntax.svg', syntax(key)))

print('wrote ' + ', '.join(f'assets/{n}' for n in written))

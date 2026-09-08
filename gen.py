import json, os, colorsys

OUT = os.path.dirname(os.path.abspath(__file__))

ACCENTS  = ['ember','amber','moss','fern','juniper','creek','slate','clay','chokeberry']
NEUTRALS = ['text','subtext1','subtext0','overlay2','overlay1','overlay0',
            'surface2','surface1','surface0','base','mantle','crust']
ANSI     = ['black','red','green','yellow','blue','magenta','cyan','white']

# ---------------------------------------------------------------------------
# Reference flavors
#
# One dark and one light, hand-tuned. Every season is derived from the one that
# matches its mode, so these twelve neutrals and nine accents per mode are the
# only colors in the project chosen by eye.
# ---------------------------------------------------------------------------

REFERENCE = {
  'dark': {
    'ember':'#E9954D','amber':'#DCAE57','moss':'#AFB766','fern':'#8FBE71',
    'juniper':'#5AB99B','creek':'#66B2BA','slate':'#88A6C2','clay':'#D67464','chokeberry':'#B988AA',
    'text':'#DFE5DC','subtext1':'#B8C4BB','subtext0':'#98A69D',
    'overlay2':'#7A8880','overlay1':'#5F6E64','overlay0':'#47564C',
    'surface2':'#313F37','surface1':'#26322B','surface0':'#1C2620',
    'base':'#131A16','mantle':'#0E1411','crust':'#0A0F0C',
  },
  'light': {
    'ember':'#A35514','amber':'#8F6A14','moss':'#6E7524','fern':'#4E7C3A',
    'juniper':'#1F8168','creek':'#2A7B87','slate':'#4A6E8C','clay':'#A8422F','chokeberry':'#9D4382',
    'text':'#2E271E','subtext1':'#554C3E','subtext0':'#6E6454',
    'overlay2':'#877C69','overlay1':'#A0947F','overlay0':'#B8AC95',
    'surface2':'#CFC4AE','surface1':'#E0D7C6','surface0':'#EDE7DB',
    'base':'#FAF7F1','mantle':'#F3EFE6','crust':'#EBE5D9',
  },
}

# ---------------------------------------------------------------------------
# Seasons
#
# `hero`     the token that carries chrome: cursor, links, focus ring, primary.
# `family`   accents the season pushes forward; everything else is pulled back.
# `neutrals` hue and saturation scale for the derived ramp, or None to inherit
#            the reference ramp unchanged.
#
# Saturation is the only dial a season turns on its accents. Hue is locked to
# the reference angle and lightness is solved back to the reference contrast, so
# a season can look completely different without moving a single color off its
# hue or dropping any accent below the ratio it was designed to hit.
# ---------------------------------------------------------------------------

BOOST, DAMP, SAT_CEILING = 1.15, 0.85, 0.90

SEASONS = {
  'spring': {
    'name':'Spring', 'emoji':'🌱', 'order':0, 'dark':False,
    'character':'Green-tinted white, 95°',
    'hero':'fern', 'family':['fern','moss','juniper'],
    'neutrals':{'hue':95, 'sat':0.72},
  },
  'summer': {
    'name':'Summer', 'emoji':'🌻', 'order':1, 'dark':False,
    'character':'Warm white, 40°',
    'hero':'ember', 'family':['ember','amber','moss'],
    'neutrals':None,
  },
  'fall': {
    'name':'Fall', 'emoji':'🍂', 'order':2, 'dark':True,
    'character':'Warm brown-black, 28°',
    'hero':'ember', 'family':['ember','amber','clay'],
    'neutrals':{'hue':28, 'sat':1.15},
  },
  'winter': {
    'name':'Winter', 'emoji':'🌲', 'order':3, 'dark':True,
    'character':'Forest black, 146°',
    'hero':'juniper', 'family':['juniper','fern','moss','creek'],
    'neutrals':None,
  },
}

# The light season the bare :root carries, and the dark one prefers-color-scheme
# swaps to. Also the pair the previews and the port READMEs lead with.
DEFAULT_LIGHT, DEFAULT_DARK = 'spring', 'winter'

# ---------------------------------------------------------------------------
# Color math
# ---------------------------------------------------------------------------

def rgb(h):
    h = h.lstrip('#')
    return {'r': int(h[0:2],16), 'g': int(h[2:4],16), 'b': int(h[4:6],16)}

def hsl(h):
    c = rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(c['r']/255, c['g']/255, c['b']/255)
    return {'h': round(hh*360, 2), 's': round(ss, 4), 'l': round(ll, 4)}

def to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360)/360, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return '#' + ''.join(f'{round(v*255):02X}' for v in (r, g, b))

def lum(h):
    c = rgb(h)
    out = 0.0
    for v, w in zip((c['r'], c['g'], c['b']), (0.2126, 0.7152, 0.0722)):
        v /= 255
        v = v/12.92 if v <= 0.03928 else ((v + 0.055)/1.055) ** 2.4
        out += v * w
    return out

def ratio(a, b):
    l1, l2 = lum(a), lum(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)

def solve_lightness(hue, sat, base, target):
    """The lightness at (hue, sat) whose contrast on `base` lands nearest `target`.

    Contrast is not monotonic in lightness once you cross the base, and the
    search space is one 8-bit channel deep, so a scan is both exact enough and
    instant. Ties resolve to the darker candidate, which keeps a light flavor's
    accents on the ink side of their base rather than flipping to a wash.
    """
    best, best_delta = 0.5, float('inf')
    for step in range(1, 1000):
        l = step / 1000
        delta = abs(ratio(to_hex(hue, sat, l), base) - target)
        if delta < best_delta:
            best, best_delta = l, delta
    return best

# ---------------------------------------------------------------------------
# Derivation
# ---------------------------------------------------------------------------

def derive_neutrals(ref, spec):
    """Rotate a reference ramp onto a new hue, holding every lightness step."""
    if spec is None:
        return {n: ref[n] for n in NEUTRALS}
    return {n: to_hex(spec['hue'], min(hsl(ref[n])['s'] * spec['sat'], 1.0), hsl(ref[n])['l'])
            for n in NEUTRALS}

# The canonical hue angle for each accent, taken from the light reference and
# rounded to the degree. Both references were tuned by eye and drift up to 4°
# from each other on a given token; snapping every season to one angle is what
# lets the hue lock be stated as a fact rather than an approximation. The shift
# it applies to the dark reference is well under a perceptible step.
HUES = {a: round(hsl(REFERENCE['light'][a])['h']) for a in ACCENTS}

def derive_accents(ref, neutrals, family):
    """Re-saturate each accent, holding its hue and its contrast on base."""
    out = {}
    for a in ACCENTS:
        sat = min(hsl(ref[a])['s'] * (BOOST if a in family else DAMP), SAT_CEILING)
        target = ratio(ref[a], ref['base'])
        out[a] = to_hex(HUES[a], sat, solve_lightness(HUES[a], sat, neutrals['base'], target))
    return out

def derive_ansi(colors, dark):
    """Sixteen slots off real tokens. Bright is the normal color, lifted."""
    slots = {
        'black':   'surface1' if dark else 'subtext1',
        'red':     'clay',   'green':   'fern',
        'yellow':  'amber',  'blue':    'slate',
        'magenta': 'chokeberry', 'cyan': 'creek',
        'white':   'subtext1' if dark else 'overlay1',
    }
    # Neutral ends step to the adjacent ramp rung rather than being lifted, so
    # ANSI black and white stay on the ramp the rest of the UI is built from.
    steps = {
        'black': 'surface2' if dark else 'subtext0',
        'white': 'text'     if dark else 'overlay2',
    }
    out = {}
    for slot, token in slots.items():
        normal = colors[token]
        if slot in steps:
            bright = colors[steps[slot]]
        else:
            h = hsl(normal)
            bright = to_hex(h['h'], h['s'], h['l'] + 0.065)
        out[slot] = (normal, bright)
    return out

FLAVORS = {}
for key, season in SEASONS.items():
    ref = REFERENCE['dark' if season['dark'] else 'light']
    neutrals = derive_neutrals(ref, season['neutrals'])
    accents = derive_accents(ref, neutrals, season['family'])
    colors = {**accents, **neutrals}
    FLAVORS[key] = {**season, 'colors': colors, 'ansi': derive_ansi(colors, season['dark'])}

# ---------- palette.json ----------
palette = {}
for key, f in FLAVORS.items():
    colors = {}
    for i, name in enumerate(ACCENTS + NEUTRALS):
        hexv = f['colors'][name]
        colors[name] = {
            'name': name.capitalize(), 'order': i, 'hex': hexv,
            'rgb': rgb(hexv), 'hsl': hsl(hexv),
            'accent': name in ACCENTS,
            'contrastOnBase': ratio(hexv, f['colors']['base']),
        }
    ansi = {}
    for i, name in enumerate(ANSI):
        normal, bright = f['ansi'][name]
        ansi[name] = {
            'name': name.capitalize(), 'order': i,
            'normal': {'hex': normal, 'rgb': rgb(normal), 'hsl': hsl(normal), 'code': i},
            'bright': {'hex': bright, 'rgb': rgb(bright), 'hsl': hsl(bright), 'code': i + 8},
        }
    palette[key] = {'name': f['name'], 'emoji': f['emoji'], 'order': f['order'],
                    'dark': f['dark'], 'character': f['character'],
                    'hero': f['hero'], 'family': f['family'],
                    'colors': colors, 'ansiColors': ansi}

with open(os.path.join(OUT, 'palette.json'), 'w') as fh:
    json.dump(palette, fh, indent=2, ensure_ascii=False)
    fh.write('\n')

ORDERED = sorted(FLAVORS.items(), key=lambda kv: kv[1]['order'])

# ---------- css ----------
def css_vars(f, indent):
    lines = []
    for n in ACCENTS + NEUTRALS:
        hexv = f['colors'][n]
        c = rgb(hexv)
        lines.append(f"{indent}--tm-{n}: {hexv};")
        lines.append(f"{indent}--tm-{n}-rgb: {c['r']} {c['g']} {c['b']};")
    lines.append(f"{indent}--tm-hero: var(--tm-{f['hero']});")
    lines.append(f"{indent}--tm-hero-rgb: var(--tm-{f['hero']}-rgb);")
    return '\n'.join(lines)

LIGHT_KEYS = [k for k, f in ORDERED if not f['dark']]
# Any explicit light stamp has to survive prefers-color-scheme: dark.
light_guard = ''.join(f':not([data-theme="{k}"])' for k in LIGHT_KEYS) + ':not([data-theme="light"])'

blocks = []
for key, f in ORDERED:
    scheme = 'dark' if f['dark'] else 'light'
    alias = ',\n:root[data-theme="dark"]' if key == DEFAULT_DARK else (
            ',\n:root[data-theme="light"]' if key == DEFAULT_LIGHT else '')
    blocks.append(f""":root[data-theme="{key}"]{alias} {{
{css_vars(f, '  ')}
  color-scheme: {scheme};
}}""")

CSS_BLOCKS = '\n\n'.join(blocks)

css = f"""/* Tamarack — {', '.join(f['name'] for _, f in ORDERED)}
 * Generated from gen.py. Do not edit by hand.
 *
 * Accents:  {', '.join(ACCENTS)}
 * Neutrals: {', '.join(NEUTRALS)}
 *
 * Resolves in three states: the bare :root carries {FLAVORS[DEFAULT_LIGHT]['name']},
 * prefers-color-scheme swaps to {FLAVORS[DEFAULT_DARK]['name']} unless a light season is
 * explicitly stamped, and an explicit [data-theme] stamp wins in either direction.
 *
 * --tm-hero aliases whichever accent the season leads with, so chrome written
 * against it re-points on its own when the season changes.
 */

:root {{
{css_vars(FLAVORS[DEFAULT_LIGHT], '  ')}
  color-scheme: light;
}}

@media (prefers-color-scheme: dark) {{
  :root{light_guard} {{
{css_vars(FLAVORS[DEFAULT_DARK], '    ')}
    color-scheme: dark;
  }}
}}

{CSS_BLOCKS}
"""
with open(os.path.join(OUT, 'tamarack.css'), 'w') as fh:
    fh.write(css)

# ---------- scss ----------
def scss_map(key, f):
    body = ',\n'.join(f'  "{n}": {f["colors"][n]}' for n in ACCENTS + NEUTRALS)
    body += f',\n  "hero": {f["colors"][f["hero"]]}'
    return f"${key}: (\n{body}\n);"

SCSS_MAPS = '\n\n'.join(scss_map(k, f) for k, f in ORDERED)
SCSS_INDEX = ',\n'.join(f'  "{k}": ${k}' for k, _ in ORDERED)

scss = f"""// Tamarack — {', '.join(f['name'] for _, f in ORDERED)}
// Generated from gen.py. Do not edit by hand.

$tamarack-accents: ({', '.join(f'"{a}"' for a in ACCENTS)});
$tamarack-neutrals: ({', '.join(f'"{a}"' for a in NEUTRALS)});
$tamarack-seasons: ({', '.join(f'"{k}"' for k, _ in ORDERED)});
$tamarack-light: ({', '.join(f'"{k}"' for k, f in ORDERED if not f['dark'])});
$tamarack-dark: ({', '.join(f'"{k}"' for k, f in ORDERED if f['dark'])});

{SCSS_MAPS}

$tamarack: (
{SCSS_INDEX}
);

@function tm($season, $color) {{
  @return map-get(map-get($tamarack, $season), $color);
}}
"""
with open(os.path.join(OUT, 'tamarack.scss'), 'w') as fh:
    fh.write(scss)


# ---------- README.md ----------

# Syntax roles are identical in all four seasons on purpose: the same file has
# the same shape everywhere, and the season shows up in the colors themselves
# rather than in which token does which job.
SYNTAX_ROLES = [
    ('ember',      'Functions, methods'),
    ('amber',      'Numbers'),
    ('moss',       'Tags, attributes, markup structure'),
    ('fern',       'Strings'),
    ('juniper',    'Types, classes, interfaces'),
    ('creek',      'Operators, builtins, escape sequences'),
    ('slate',      'Properties, parameters, fields, JSON keys'),
    ('clay',       'Keywords, storage'),
    ('chokeberry', 'Constants, enum members, decorators, annotations'),
    ('overlay1',   'Comments, doc blocks'),
    ('subtext0',   'Punctuation, delimiters'),
    ('text',       'Identifiers, everything unclaimed'),
]

# Chrome is the one place the season re-points: `hero` is an alias, not a token.
UI_ROLES = [
    ('hero',       'Primary buttons, links, cursor, focus ring, active tab'),
    ('fern',       'Success, added lines in a diff, passing tests'),
    ('amber',      'Warnings, modified lines, pending state'),
    ('clay',       'Errors, deleted lines, destructive actions'),
    ('creek',      'Selection fill, search highlight, info state'),
    ('slate',      'Secondary links, metadata, breadcrumbs'),
    ('chokeberry', 'Constants and enum members in UI chrome'),
    ('base',       'Editor and page background'),
    ('mantle',     'Sidebar, gutter, status bar'),
    ('crust',      'Window chrome, deepest recess'),
    ('surface0',   'Panels, inline code, hover fill'),
    ('surface2',   'Borders, dividers, inactive tab'),
    ('overlay0',   'Disabled text, placeholder'),
]

ANSI_FROM = {
    'black':'subtext1 (light) / surface1 (dark)', 'red':'clay', 'green':'fern',
    'yellow':'amber', 'blue':'slate', 'magenta':'chokeberry', 'cyan':'creek',
    'white':'overlay1 (light) / subtext1 (dark)',
}

LIGHT = [(k, f) for k, f in ORDERED if not f['dark']]
DARK  = [(k, f) for k, f in ORDERED if f['dark']]
NAMES = [f['name'] for _, f in ORDERED]

def hx(key, token):
    return palette[key]['colors'][token]['hex']

lines = []
w = lines.append

w('# Tamarack')
w('')
w('A warm, nature-derived color palette in four seasons.')
w('')
w('Named for the tamarack — the North American larch, a conifer that turns brilliant')
w('gold-orange every autumn before dropping its needles. A green tree that becomes the')
w('hero color and then goes bare, which is a palette that changes with the season in')
w('one word.')
w('')
w('No purple, no pink, no electric blue. Nine accents named for things that actually')
w('have these colors, over a twelve-step role-named neutral ramp, in two light seasons')
w('and two dark ones.')
w('')
w('![The four seasons](assets/tamarack-hero.svg)')
w('')
w('## Seasons')
w('')
w('| Season | Mode | Base | Text | Leads with | Character |')
w('| --- | --- | --- | --- | --- | --- |')
for k, f in ORDERED:
    w(f"| **{f['name']}** {f['emoji']} | {'dark' if f['dark'] else 'light'} "
      f"| `{hx(k,'base')}` | `{hx(k,'text')}` | `{f['hero']}` | {f['character']} |")
w('')
w('Spring and Summer are the light pair, Fall and Winter the dark one. Within a pair')
w('the split is temperature: Spring and Winter lead green, Summer and Fall lead orange.')
w('So the two axes are mode and warmth, and every combination exists.')
w('')
w('## What a season is allowed to change')
w('')
w('A season turns exactly one dial on the accents: **saturation**. Two things are held')
w('fixed, and holding them is what keeps four palettes from becoming four unrelated')
w('themes.')
w('')
w(f'- **Hue is locked.** A given token sits at one hue angle in all four seasons —')
w(f'  `juniper` is {HUES["juniper"]}° in every one of them. The angles are listed in the')
w('  accent table below and nothing in the derivation is allowed to move them; the')
w('  only spread you can measure back off the hex is under a degree of 8-bit rounding.')
w('- **Contrast is locked.** After saturation moves, lightness is solved back until the')
w("  color lands on its reference ratio against its own season's `base`. A token hits")
w('  the same measured contrast in every season of its mode, so no season is the one')
w('  where the strings got hard to read.')
w('')
w(f'Accents in a season\'s family are pushed to {BOOST}× saturation and everything else is')
w(f'pulled to {DAMP}×, capped at {SAT_CEILING}. That is the whole mechanism. Winter reads green')
w('because its greens are vivid and its warms are muted, not because anything was')
w('recolored or reassigned.')
w('')
w('| Season | Pushed forward | Pulled back |')
w('| --- | --- | --- |')
for k, f in ORDERED:
    fam = ', '.join(f'`{a}`' for a in f['family'])
    rest = ', '.join(f'`{a}`' for a in ACCENTS if a not in f['family'])
    w(f"| {f['name']} | {fam} | {rest} |")
w('')
w('The neutrals move too, but by hue rather than by saturation: Fall rotates the dark')
w('ramp from forest green onto a warm brown, Spring rotates the light ramp from warm')
w('white onto a green-tinted one. Winter and Summer keep their reference ramps unchanged.')
w('Every lightness step is preserved in the rotation, so the ramps stay interchangeable.')
w('')
w('## Accents')
w('')
w('Δ is the reference contrast against `base`. Both seasons of a mode are solved back to')
w('it, so they match to within hex rounding — the per-season measured values are in')
w('`palette.json` as `contrastOnBase`.')
w('')
w('| Token | Hue | Spring | Summer | Δ light | Fall | Winter | Δ dark |')
w('| --- | --- | --- | --- | --- | --- | --- | --- |')
for a in ACCENTS:
    hue = HUES[a]
    dl = ratio(REFERENCE['light'][a], REFERENCE['light']['base'])
    dd = ratio(REFERENCE['dark'][a], REFERENCE['dark']['base'])
    w(f"| `{a}` | {hue}° | `{hx('spring',a)}` | `{hx('summer',a)}` | {dl}:1 "
      f"| `{hx('fall',a)}` | `{hx('winter',a)}` | {dd}:1 |")
w('')
w('## Neutrals')
w('')
w('Role-named rather than color-named, deliberately: `surface0` means the same thing in')
w('every season, whereas a color name would have to be the text in one and the background')
w('in another. The accents carry the identity; the neutrals carry the structure.')
w('')
w('| Token | Spring | Summer | Fall | Winter |')
w('| --- | --- | --- | --- | --- |')
for n in NEUTRALS:
    w(f"| `{n}` | `{hx('spring',n)}` | `{hx('summer',n)}` | `{hx('fall',n)}` | `{hx('winter',n)}` |")
w('')
w('## Roles')
w('')
w('A palette without an assignment is just a list of colors. These maps are written')
w('against token names, so they hold for any season.')
w('')
w('### Syntax')
w('')
w('Identical in all four seasons. The same file has the same shape everywhere; the')
w('season shows up in the colors themselves, not in which token does which job.')
w('')
w('| Token | Applies to |')
w('| --- | --- |')
for t, r in SYNTAX_ROLES:
    w(f'| `{t}` | {r} |')
w('')
w('### Interface')
w('')
w('| Token | Applies to |')
w('| --- | --- |')
for t, r in UI_ROLES:
    w(f'| `{t}` | {r} |')
w('')
w('`hero` is the one entry that is an alias rather than a token. It resolves to')
w(', '.join(f"`{f['hero']}` in {f['name']}" for _, f in ORDERED[:-1]))
w(f"and `{ORDERED[-1][1]['hero']}` in {ORDERED[-1][1]['name']}, which is how chrome follows the")
w('season without every consumer needing a per-season branch.')
w('')
w('## Previews')
w('')
w('Every preview below is an SVG generated from `palette.json` by')
w('`assets/build.py` — nothing here is a screenshot, so the images cannot drift')
w('from the palette they document.')
w('')
w('### Swatches')
w('')
w("Each accent carries its measured contrast against its own season's `base`.")
w('')
for k, f in ORDERED:
    w(f"![{f['name']} swatches](assets/tamarack-{k}-palette.svg)")
    w('')
w('### Syntax')
w('')
w('The same file in all four seasons, colored strictly by the role table above.')
w('')
for k, f in ORDERED:
    w(f"![{f['name']} syntax preview](assets/tamarack-{k}-syntax.svg)")
    w('')
w('## ANSI 16')
w('')
w('All sixteen slots map to real palette tokens. `chokeberry` exists because ANSI')
w('demands a magenta and the original eight accents had no honest answer for it.')
w('')
w('| Slot | Code | Spring | Summer | Fall | Winter | From |')
w('| --- | --- | --- | --- | --- | --- | --- |')
for variant, label in (('normal', ''), ('bright', 'bright ')):
    for i, name in enumerate(ANSI):
        cells = ' | '.join(f"`{palette[k]['ansiColors'][name][variant]['hex']}`" for k, _ in ORDERED)
        w(f"| {label}{name} | {i + (8 if variant == 'bright' else 0)} | {cells} "
          f"| {ANSI_FROM[name] if variant == 'normal' else '—'} |")
w('')
w('Bright is the normal color lifted in lightness, except at the neutral ends, where')
w('black and white step to the adjacent rung of the ramp so they stay on the same')
w('ladder the rest of the UI is built from.')
w('')
w('## Usage')
w('')
w('### CSS')
w('')
w('`tamarack.css` defines every color as a custom property, plus a paired `-rgb`')
w('triplet for alpha composition. It resolves across all three theme states: the bare')
w(f'`:root` carries {FLAVORS[DEFAULT_LIGHT]["name"]}, `prefers-color-scheme` swaps to {FLAVORS[DEFAULT_DARK]["name"]} unless a light')
w('season is explicitly stamped, and an explicit `[data-theme]` stamp wins in either')
w('direction.')
w('')
w('```css')
w('@import "tamarack.css";')
w('')
w('.button {')
w('  background: var(--tm-hero);')
w('  color: var(--tm-base);')
w('}')
w('')
w('.selection {')
w('  background: rgb(var(--tm-creek-rgb) / 0.25);')
w('}')
w('```')
w('')
w('Writing chrome against `--tm-hero` rather than a named accent is what makes it')
w('re-point on its own: the same button is fern in Spring and juniper in Winter.')
w('')
w('Force a season with `<html data-theme="winter">`, and so on for each of')
w(f"{', '.join(f'`{k}`' for k, _ in ORDERED)}. `data-theme=\"dark\"` and `data-theme=\"light\"` are")
w(f'accepted as aliases for {FLAVORS[DEFAULT_DARK]["name"]} and {FLAVORS[DEFAULT_LIGHT]["name"]}.')
w('')
w('### Sass')
w('')
w('```scss')
w('@use "tamarack" as *;')
w('')
w('.button {')
w('  background: tm("winter", "hero");')
w('}')
w('')
w('@each $season in $tamarack-seasons {')
w('  [data-theme="#{$season}"] .button { background: tm($season, "hero"); }')
w('}')
w('```')
w('')
w('`$tamarack-seasons`, `$tamarack-light` and `$tamarack-dark` are exported so you can')
w('loop over the seasons without hardcoding their names.')
w('')
w('### JSON')
w('')
w('The season definitions at the top of `gen.py` are the source of truth.')
w('`palette.json` is generated from them, and is what every port reads — so it is')
w('the stable contract for anything outside this repo. Every color carries `hex`,')
w('`rgb`, `hsl`, `accent`, and `contrastOnBase`; each season also carries `hero`,')
w('`family`, `character`, and a full `ansiColors` block with normal and bright')
w('variants and their codes.')
w('')
w('```json')
w('{')
w('  "winter": {')
w('    "dark": true,')
w('    "hero": "juniper",')
w('    "family": ["juniper", "fern", "moss", "creek"],')
w('    "colors": {')
w('      "juniper": {')
w(f'        "hex": "{hx("winter","juniper")}",')
w(f'        "rgb": {{ "r": {palette["winter"]["colors"]["juniper"]["rgb"]["r"]}, "g": {palette["winter"]["colors"]["juniper"]["rgb"]["g"]}, "b": {palette["winter"]["colors"]["juniper"]["rgb"]["b"]} }},')
w('        "accent": true,')
w(f'        "contrastOnBase": {palette["winter"]["colors"]["juniper"]["contrastOnBase"]}')
w('      }')
w('    }')
w('  }')
w('}')
w('```')
w('')
w('## Regenerating')
w('')
w('`palette.json`, `tamarack.css`, `tamarack.scss` and this README are all generated.')
w('Edit the season definitions at the top of `gen.py`, then:')
w('')
w('```bash')
w('python3 gen.py')
w('python3 assets/build.py')
w('python3 sublime-text/build.py')
w('python3 ghostty/build.py')
w('python3 slack/build.py')
w('```')
w('')
w('`gen.py` runs first because the previews and every port build read the')
w('`palette.json` it writes.')
w('')
w('No dependencies beyond the Python standard library.')
w('')
w('## Notes on the design')
w('')
w('- **Only two flavors were ever chosen by eye.** One dark reference and one light')
w('  reference, twenty-one colors each. All four seasons are derived from those two, so')
w('  a retune is a change to one saturation multiplier rather than to thirty-six hex')
w('  values, and the hue lock cannot quietly break.')
w('- **Contrast is measured, not assumed.** Every accent carries its ratio against its')
w('  own season\'s `base`. The light seasons span roughly 4.5–5.6:1 and the dark ones')
w('  5.5–8.6:1 — light is inherently flatter, which is a property of dark accents on a')
w('  light ground rather than an oversight.')
w('- **Saturation, not reassignment, carries the season.** It would have been easier to')
w('  make Winter green by pointing the string color at `juniper`. That breaks muscle')
w('  memory across seasons for no gain, so the role tables are identical everywhere and')
w('  the palette itself does the work.')
w(f'- **JSON keys map to `slate`, not `moss`.** `moss` and `fern` sit {HUES["fern"] - HUES["moss"]}° apart, which is')
w('  fine in prose and not fine in JSON, where keys and string values alternate on every')
w('  line. Fixed by role assignment rather than by moving hues.')
w('- **`amber` does numbers and warnings only.** Constants moved to `chokeberry` when it')
w('  joined, so no token carries three unrelated meanings.')
w('')
w('## License')
w('')
w('MIT. See [LICENSE](LICENSE).')
w('')

with open(os.path.join(OUT, 'README.md'), 'w') as fh:
    fh.write('\n'.join(lines))


print('wrote palette.json, tamarack.css, tamarack.scss, README.md\n')
for key, f in ORDERED:
    p = palette[key]
    print(f"{f['emoji']}  {f['name']:<7} {'dark ' if f['dark'] else 'light'}  base {f['colors']['base']}  hero {f['hero']}")
    for a in ACCENTS:
        mark = '*' if a in f['family'] else ' '
        print(f"   {mark} {a:<11}{p['colors'][a]['hex']}  {p['colors'][a]['contrastOnBase']:>5}:1  s={p['colors'][a]['hsl']['s']:.2f}")
    for n in ['text','subtext1','overlay1']:
        print(f"     {n:<11}{p['colors'][n]['hex']}  {p['colors'][n]['contrastOnBase']:>5}:1")
    print()

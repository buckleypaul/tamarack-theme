import json, os, colorsys

OUT = '/Users/paulbuckley/Projects/tamarack-theme'
os.makedirs(OUT, exist_ok=True)

ACCENTS  = ['ember','amber','moss','fern','juniper','creek','slate','clay','chokeberry']
NEUTRALS = ['text','subtext1','subtext0','overlay2','overlay1','overlay0',
            'surface2','surface1','surface0','base','mantle','crust']
ANSI     = ['black','red','green','yellow','blue','magenta','cyan','white']

FLAVORS = {
  'clearing': {
    'name':'Clearing', 'emoji':'🌾', 'order':0, 'dark':False,
    'colors': {
      'ember':'#A35514','amber':'#8F6A14','moss':'#6E7524','fern':'#4E7C3A',
      'juniper':'#1F8168','creek':'#2A7B87','slate':'#4A6E8C','clay':'#A8422F','chokeberry':'#9D4382',
      'text':'#2E271E','subtext1':'#554C3E','subtext0':'#6E6454',
      'overlay2':'#877C69','overlay1':'#A0947F','overlay0':'#B8AC95',
      'surface2':'#CFC4AE','surface1':'#E0D7C6','surface0':'#EDE7DB',
      'base':'#FAF7F1','mantle':'#F3EFE6','crust':'#EBE5D9',
    },
    'ansi': {
      'black':('#554C3E','#6E6454'), 'red':('#A8422F','#BC5340'),
      'green':('#4E7C3A','#5C8E45'), 'yellow':('#8F6A14','#A07920'),
      'blue':('#4A6E8C','#587FA0'),  'magenta':('#9D4382','#B25395'),
      'cyan':('#2A7B87','#358995'),  'white':('#B8AC95','#877C69'),
    },
  },
  'thicket': {
    'name':'Thicket', 'emoji':'🌲', 'order':1, 'dark':True,
    'colors': {
      'ember':'#E9954D','amber':'#DCAE57','moss':'#AFB766','fern':'#8FBE71',
      'juniper':'#5AB99B','creek':'#66B2BA','slate':'#88A6C2','clay':'#D67464','chokeberry':'#B988AA',
      'text':'#DFE5DC','subtext1':'#B8C4BB','subtext0':'#98A69D',
      'overlay2':'#7A8880','overlay1':'#5F6E64','overlay0':'#47564C',
      'surface2':'#313F37','surface1':'#26322B','surface0':'#1C2620',
      'base':'#131A16','mantle':'#0E1411','crust':'#0A0F0C',
    },
    'ansi': {
      'black':('#26322B','#313F37'), 'red':('#D67464','#E08A7B'),
      'green':('#8FBE71','#A0CB84'), 'yellow':('#DCAE57','#E6BC6F'),
      'blue':('#88A6C2','#9CB6CE'),  'magenta':('#B988AA','#CB9FBE'),
      'cyan':('#66B2BA','#7BC1C8'),  'white':('#B8C4BB','#DFE5DC'),
    },
  },
}

def rgb(h):
    h = h.lstrip('#')
    return {'r': int(h[0:2],16), 'g': int(h[2:4],16), 'b': int(h[4:6],16)}

def hsl(h):
    c = rgb(h)
    hh, ll, ss = colorsys.rgb_to_hls(c['r']/255, c['g']/255, c['b']/255)
    return {'h': round(hh*360, 2), 's': round(ss, 4), 'l': round(ll, 4)}

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
                    'dark': f['dark'], 'colors': colors, 'ansiColors': ansi}

with open(os.path.join(OUT, 'palette.json'), 'w') as fh:
    json.dump(palette, fh, indent=2, ensure_ascii=False)
    fh.write('\n')

# ---------- css ----------
def css_vars(f, indent):
    lines = []
    for n in ACCENTS + NEUTRALS:
        hexv = f['colors'][n]
        c = rgb(hexv)
        lines.append(f"{indent}--tm-{n}: {hexv};")
        lines.append(f"{indent}--tm-{n}-rgb: {c['r']} {c['g']} {c['b']};")
    return '\n'.join(lines)

css = f"""/* Tamarack — Clearing & Thicket
 * Generated from palette.json. Do not edit by hand.
 *
 * Accents:  {', '.join(ACCENTS)}
 * Neutrals: {', '.join(NEUTRALS)}
 *
 * Resolves in three states: the bare :root carries Clearing (light),
 * prefers-color-scheme swaps to Thicket unless light is explicitly stamped,
 * and an explicit [data-theme] stamp wins in either direction.
 */

:root {{
{css_vars(FLAVORS['clearing'], '  ')}
  color-scheme: light;
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="clearing"]):not([data-theme="light"]) {{
{css_vars(FLAVORS['thicket'], '    ')}
    color-scheme: dark;
  }}
}}

:root[data-theme="thicket"],
:root[data-theme="dark"] {{
{css_vars(FLAVORS['thicket'], '  ')}
  color-scheme: dark;
}}
"""
with open(os.path.join(OUT, 'tamarack.css'), 'w') as fh:
    fh.write(css)

# ---------- scss ----------
def scss_map(key, f):
    body = ',\n'.join(f'  "{n}": {f["colors"][n]}' for n in ACCENTS + NEUTRALS)
    return f"${key}: (\n{body}\n);"

scss = f"""// Tamarack — Clearing & Thicket
// Generated from palette.json. Do not edit by hand.

$tamarack-accents: ({', '.join(f'"{a}"' for a in ACCENTS)});
$tamarack-neutrals: ({', '.join(f'"{a}"' for a in NEUTRALS)});

{scss_map('clearing', FLAVORS['clearing'])}

{scss_map('thicket', FLAVORS['thicket'])}

$tamarack: (
  "clearing": $clearing,
  "thicket": $thicket
);

@function tm($flavor, $color) {{
  @return map-get(map-get($tamarack, $flavor), $color);
}}
"""
with open(os.path.join(OUT, 'tamarack.scss'), 'w') as fh:
    fh.write(scss)

print('wrote palette.json, tamarack.css, tamarack.scss\n')
for key, f in palette.items():
    print(f"{f['name']}  (base {f['colors']['base']['hex']})")
    for a in ACCENTS:
        print(f"   {a:<9}{f['colors'][a]['hex']}  {f['colors'][a]['contrastOnBase']:>5}:1")
    for n in ['text','subtext1','subtext0','overlay1']:
        print(f"   {n:<9}{f['colors'][n]['hex']}  {f['colors'][n]['contrastOnBase']:>5}:1")
    print()

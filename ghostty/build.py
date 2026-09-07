import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PALETTE = os.path.join(HERE, os.pardir, 'palette.json')

# ANSI slot -> code, in ghostty's palette order
SLOTS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

# ---------- chrome ----------
# base=background · text=foreground · ember=cursor · creek=selection
# surface2=split divider · crust=unfocused split fill
#
# Ghostty has no alpha on selection-background, so the creek wash the other ports
# apply is pre-composited over base here — at 0.30 rather than their 0.25, because
# a terminal selection has to read across a whole block at a glance. Everything
# else is a flat token.
CHROME = [
    ('background',           'base'),
    ('foreground',           'text'),
    ('cursor-color',         'ember'),
    ('cursor-text',          'base'),
    ('selection-background', ('creek', 'base', 0.30)),
    ('selection-foreground', 'text'),
    ('split-divider-color',  'surface2'),
    ('unfocused-split-fill', 'crust'),
]


def blend(fg, bg, alpha):
    """Composite fg over bg at the given alpha, both #rrggbb."""
    def parts(h):
        h = h.lstrip('#')
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    f, b = parts(fg), parts(bg)
    return '#' + ''.join(f'{round(x * alpha + y * (1 - alpha)):02X}' for x, y in zip(f, b))


def resolve(value, hexes):
    if isinstance(value, tuple):
        fg, bg, alpha = value
        return blend(hexes[fg], hexes[bg], alpha)
    return hexes[value]


def build(flavor):
    hexes = {n: c['hex'] for n, c in flavor['colors'].items()}
    ansi = flavor['ansiColors']
    mode = 'dark' if flavor.get('dark') else 'light'

    lines = [
        f"# Tamarack {flavor['name']} — {mode}",
        f"# {flavor['emoji']} https://github.com/buckleypaul/tamarack-theme",
        '',
    ]
    codes = {}
    for slot in SLOTS:
        for variant in ('normal', 'bright'):
            entry = ansi[slot][variant]
            codes[entry['code']] = entry['hex'].lower()
    for code in range(16):
        lines.append(f'palette = {code}={codes[code]}')
    lines.append('')
    for key, value in CHROME:
        lines.append(f'{key} = {resolve(value, hexes).lower()}')
    return '\n'.join(lines) + '\n'


def main():
    with open(PALETTE) as fh:
        palette = json.load(fh)

    for key, flavor in sorted(palette.items(), key=lambda kv: kv[1]['order']):
        path = os.path.join(HERE, f'tamarack-{key}.conf')
        with open(path, 'w') as fh:
            fh.write(build(flavor))
        print(f'wrote {os.path.basename(path)}')


if __name__ == '__main__':
    main()

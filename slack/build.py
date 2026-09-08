import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PALETTE = os.path.join(HERE, os.pardir, 'palette.json')

# ---------- the four slots ----------
# Current Slack takes four colors, in this order, and its theme editor names them
# System navigation, Selected items, Presence indication and Notifications. The
# ten-value legacy string is still accepted on import but only slots 1, 3, 7 and 8
# survive it, so there is nothing to be gained by writing one — these files are the
# four values Slack keeps.
#
# All four colors land on the navigation surface: the selected channel is a fill on
# it, and the presence dot and the unread badge sit on top of it. So the rail is not
# free to be any color the season likes. It has to be dark enough for a green dot
# and a red badge to read against it.
#
# A dark season already has that in `mantle`. A light season does not — `mantle` is
# a near-white there, which is the one thing this port cannot use, so the season's
# hero accent is deepened onto the crust of the dark season it shares a temperature
# with (Summer with Fall, Spring with Winter) at half strength. That keeps the hue
# the season leads with — Summer's rail is a deep rust, Spring's a deep forest — and
# buys back the contrast: the selected pill lands near 10:1 and the presence dot
# above 4.8:1, where an undeepened hero rail put the dot at 1.0:1 in Spring, the
# exact same green as the rail behind it.
#
# Because that rail is dark, a light season's other three colors are the dark-mode
# values of those tokens, taken from its partner. Same tokens, mode-appropriate
# variants — the partner's `hero` rather than the season's own, since Spring's hero
# is `fern` and would collide with its own presence dot.
PARTNER = {'spring': 'winter', 'summer': 'fall'}
RAIL_STRENGTH = 0.5

SLOTS = [
    ('System navigation',  'nav'),
    ('Selected items',     'hero'),
    ('Presence indication', 'fern'),
    ('Notifications',      'clay'),
]


def blend(fg, bg, alpha):
    """Composite fg over bg at the given alpha, both #rrggbb."""
    def parts(h):
        h = h.lstrip('#')
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    f, b = parts(fg), parts(bg)
    return '#' + ''.join(f'{round(x * alpha + y * (1 - alpha)):02X}' for x, y in zip(f, b))


def colors_for(key, palette):
    """The four values a season contributes, resolved to hex."""
    flavor = palette[key]
    own = {n: c['hex'] for n, c in flavor['colors'].items()}

    # `source` is the flavor the three accent slots are drawn from: the season
    # itself when it is dark, its dark partner when it is light.
    source_flavor = flavor if flavor.get('dark') else palette[PARTNER[key]]
    source = {n: c['hex'] for n, c in source_flavor['colors'].items()}

    nav = (own['mantle'] if flavor.get('dark')
           else blend(own[flavor['hero']], source['crust'], RAIL_STRENGTH))

    source = dict(source, nav=nav, hero=source[source_flavor['hero']])
    return [source[token] for _, token in SLOTS]


def build(key, palette):
    return ','.join(c.upper() for c in colors_for(key, palette)) + '\n'


def main():
    with open(PALETTE) as fh:
        palette = json.load(fh)

    for key, flavor in sorted(palette.items(), key=lambda kv: kv[1]['order']):
        path = os.path.join(HERE, f'tamarack-{key}.txt')
        with open(path, 'w') as fh:
            fh.write(build(key, palette))
        print(f'wrote {os.path.basename(path)}')


if __name__ == '__main__':
    main()

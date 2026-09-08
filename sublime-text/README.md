# Tamarack for Sublime Text

Four color schemes generated from the palette at the root of this repo — one per
season:

| File | Season | Mode | Leads with |
| --- | --- | --- | --- |
| `Tamarack Spring.sublime-color-scheme` | Spring | light | `fern` |
| `Tamarack Summer.sublime-color-scheme` | Summer | light | `ember` |
| `Tamarack Fall.sublime-color-scheme` | Fall | dark | `ember` |
| `Tamarack Winter.sublime-color-scheme` | Winter | dark | `juniper` |

Winter and Spring are the showcase pair — the default dark and the default
light. Summer and Fall are the warm siblings on either side.

All four are plain JSON. Sublime's format tolerates `//` comments and trailing
commas; these files use neither, so any JSON parser can read them.

## Install

### Manual (any Sublime Text 4 build)

1. **Preferences → Browse Packages…** opens the `Packages` directory.
2. Copy the `.sublime-color-scheme` files you want into `Packages/User/`.
3. **Preferences → Select Color Scheme…** and pick `Tamarack Winter`,
   `Tamarack Spring`, `Tamarack Summer` or `Tamarack Fall`.

Schemes in `Packages/User/` are picked up without a restart.

### As a package

Clone or copy this directory into `Packages/` as `Tamarack`:

```bash
git clone https://github.com/buckleypaul/tamarack-theme.git
cp -R tamarack-theme/sublime-text "$PACKAGES/Tamarack"
```

`$PACKAGES` is the directory that **Preferences → Browse Packages…** opens.

The `.python-version` file pins the plugin host to Python 3.8 so Sublime does not
try to load `build.py` under the legacy 3.3 host. `build.py` defines no plugin
entry points and does nothing on import, but the pin keeps the console quiet.

This is not on Package Control. If it is added later, the Package Control route
is **Command Palette → Package Control: Install Package → Tamarack**.

## Switching with the OS

To follow the system light/dark setting, put this in your user settings:

```json
{
    "color_scheme": "auto",
    "light_color_scheme": "Tamarack Spring.sublime-color-scheme",
    "dark_color_scheme": "Tamarack Winter.sublime-color-scheme"
}
```

Swap in `Tamarack Summer` and `Tamarack Fall` for the warmer pairing.

## Rebuilding

`build.py` reads `../palette.json` and rewrites all four scheme files. Colors
live in the palette; scope assignments live in `build.py`.

```bash
python3 build.py
```

No dependencies beyond the Python standard library. To change a color, edit the
season definitions in the root `gen.py`, run `python3 gen.py` to regenerate
`palette.json`, then run `python3 build.py` here.

## How the files are laid out

Each scheme defines all 21 palette tokens in its own `variables` block and refers
to them as `var(ember)` and so on, so a scheme can be read and edited by hand
without consulting the palette. `globals` covers the editor chrome, `rules` covers
syntax, and `popup_css` styles the hover and autocomplete popups.

Role assignments follow the maps in the root `README.md` — `ember` for functions,
`fern` for strings, `clay` for keywords, `overlay1` for comments, and so on. The
syntax `rules` table is identical across all four seasons on purpose: the seasonal
character comes from the palette values behind the tokens, not from moving scopes
around.

The interface chrome is the one place a season asserts itself. Alongside the 21
tokens, `variables` carries a 22nd entry, `hero`, aliasing whichever accent the
season leads with — `var(juniper)` in Winter, `var(fern)` in Spring, `var(ember)`
in Summer and Fall. The caret, block caret, highlighted gutter number, active
indent guide, `accent` and the popup link color all resolve through `var(hero)`,
so Winter gets a juniper caret where Fall gets an ember one. Roles tied to a
specific token stay put: `fold_marker` is amber, `misspelling` is clay, selection
and find highlighting are creek, `tags_foreground` is moss.

Sublime infers a scheme's light/dark mode from the luminance of its `background`,
which is `var(base)` in every file — so Spring and Summer read as light schemes
and Fall and Winter as dark ones with no extra declaration.

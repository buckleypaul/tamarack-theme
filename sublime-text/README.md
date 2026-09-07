# Tamarack for Sublime Text

Two color schemes generated from the palette at the root of this repo:

| File | Flavor | Mode |
| --- | --- | --- |
| `Tamarack Clearing.sublime-color-scheme` | Clearing | light |
| `Tamarack Thicket.sublime-color-scheme` | Thicket | dark |

Both are plain JSON. Sublime's format tolerates `//` comments and trailing commas;
these files use neither, so any JSON parser can read them.

## Install

### Manual (any Sublime Text 4 build)

1. **Preferences → Browse Packages…** opens the `Packages` directory.
2. Copy both `.sublime-color-scheme` files into `Packages/User/`.
3. **Preferences → Select Color Scheme…** and pick `Tamarack Clearing` or
   `Tamarack Thicket`.

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
    "light_color_scheme": "Tamarack Clearing.sublime-color-scheme",
    "dark_color_scheme": "Tamarack Thicket.sublime-color-scheme"
}
```

## Rebuilding

`build.py` reads `../palette.json` and rewrites both scheme files. Colors live in
the palette; scope assignments live in `build.py`.

```bash
python3 build.py
```

No dependencies beyond the Python standard library. To change a color, edit the
flavor definitions in the root `gen.py`, run `python3 gen.py` to regenerate
`palette.json`, then run `python3 build.py` here.

## How the files are laid out

Each scheme defines all 21 palette tokens in its own `variables` block and refers
to them as `var(ember)` and so on, so a scheme can be read and edited by hand
without consulting the palette. `globals` covers the editor chrome, `rules` covers
syntax, and `popup_css` styles the hover and autocomplete popups.

Role assignments follow the maps in the root `README.md` — `ember` for functions,
`fern` for strings, `clay` for keywords, `overlay1` for comments, and so on for
syntax; `base`/`mantle`/`crust` for backgrounds and `ember` for the caret and
active guide in the interface.

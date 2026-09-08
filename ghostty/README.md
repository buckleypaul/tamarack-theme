# Tamarack for Ghostty

Four themes generated from the palette at the root of this repo:

| File | Season | Mode |
| --- | --- | --- |
| `tamarack-spring.conf` | Spring | light |
| `tamarack-summer.conf` | Summer | light |
| `tamarack-fall.conf` | Fall | dark |
| `tamarack-winter.conf` | Winter | dark |

Winter and Spring are the showcase pair — the default dark and the default light.
Fall is the warmer dark, Summer the warmer light.

Each file is Ghostty config syntax: the sixteen ANSI slots plus the window chrome.
A theme file is loaded by filename, so the `.conf` suffix is part of the name.

## Install

Copy all four files into Ghostty's user theme directory:

```bash
cp tamarack-*.conf ~/.config/ghostty/themes/
```

Then in `~/.config/ghostty/config`:

```
theme = tamarack-winter.conf
```

To follow the system light/dark setting instead:

```
theme = light:tamarack-spring.conf,dark:tamarack-winter.conf
```

Swap in `tamarack-summer.conf` or `tamarack-fall.conf` on either side of that pair
for the warmer run of the year.

Reload with **Cmd+Shift+,** (macOS) or **Ctrl+Shift+,** (Linux). `ghostty
+list-themes` should show all four, marked `(user)`.

## What each file sets

The sixteen `palette` entries come straight from the `ansiColors` block in
`palette.json` — the same mapping the root `README.md` documents.

| Key | Token |
| --- | --- |
| `background` | `base` |
| `foreground` | `text` |
| `cursor-color` | the season's hero accent |
| `cursor-text` | `base` |
| `selection-background` | `creek` at 30% over `base` |
| `selection-foreground` | `text` |
| `split-divider-color` | `surface2` |
| `unfocused-split-fill` | `crust` |

The cursor is the one key that is not a fixed token. Each season declares a `hero`
in `palette.json` — the accent it leads with — and the cursor takes it, so Winter
gets a juniper cursor, Spring a fern one, and Summer and Fall an ember one.

Ghostty takes no alpha on `selection-background`, so the translucent `creek` wash
the other ports use is pre-composited against `base` at build time. It is mixed at
30% rather than the 25% used elsewhere because a terminal selection has to read
across a whole block of text at a glance.

## Rebuilding

`build.py` reads `../palette.json` and rewrites all four files, one per season, in
`order`. Colors live in the palette; the chrome assignments live in `build.py`.

```bash
python3 build.py
```

No dependencies beyond the Python standard library. To change a color, edit the
season definitions in the root `gen.py`, run `python3 gen.py` to regenerate
`palette.json`, then run `python3 build.py` here.

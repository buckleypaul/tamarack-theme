# Tamarack for Ghostty

Two themes generated from the palette at the root of this repo:

| File | Flavor | Mode |
| --- | --- | --- |
| `tamarack-clearing.conf` | Clearing | light |
| `tamarack-thicket.conf` | Thicket | dark |

Each file is Ghostty config syntax: the sixteen ANSI slots plus the window chrome.
A theme file is loaded by filename, so the `.conf` suffix is part of the name.

## Install

Copy both files into Ghostty's user theme directory:

```bash
cp tamarack-*.conf ~/.config/ghostty/themes/
```

Then in `~/.config/ghostty/config`:

```
theme = tamarack-thicket.conf
```

To follow the system light/dark setting instead:

```
theme = light:tamarack-clearing.conf,dark:tamarack-thicket.conf
```

Reload with **Cmd+Shift+,** (macOS) or **Ctrl+Shift+,** (Linux). `ghostty
+list-themes` should show both, marked `(user)`.

## What each file sets

The sixteen `palette` entries come straight from the `ansiColors` block in
`palette.json` — the same mapping the root `README.md` documents.

| Key | Token |
| --- | --- |
| `background` | `base` |
| `foreground` | `text` |
| `cursor-color` | `ember` |
| `cursor-text` | `base` |
| `selection-background` | `creek` at 30% over `base` |
| `selection-foreground` | `text` |
| `split-divider-color` | `surface2` |
| `unfocused-split-fill` | `crust` |

Ghostty takes no alpha on `selection-background`, so the translucent `creek` wash
the other ports use is pre-composited against `base` at build time. It is mixed at
30% rather than the 25% used elsewhere because a terminal selection has to read
across a whole block of text at a glance.

## Rebuilding

`build.py` reads `../palette.json` and rewrites both files. Colors live in the
palette; the chrome assignments live in `build.py`.

```bash
python3 build.py
```

No dependencies beyond the Python standard library. To change a color, edit the
flavor definitions in the root `gen.py`, run `python3 gen.py` to regenerate
`palette.json`, then run `python3 build.py` here.

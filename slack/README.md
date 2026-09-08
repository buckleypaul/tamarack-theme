# Tamarack for Slack

Four themes generated from the palette at the root of this repo:

| File | Season | Rail |
| --- | --- | --- |
| `tamarack-summer.txt` | Summer | deep rust, from `ember` |
| `tamarack-fall.txt` | Fall | warm near-black |
| `tamarack-spring.txt` | Spring | deep forest, from `fern` |
| `tamarack-winter.txt` | Winter | green near-black |

Summer and Fall are the pair to reach for — both leading with `ember`, one as a
saturated rail and one as a quiet one. Spring and Winter are the green run.

Each file is one line: the four comma-separated hex codes Slack wants, and nothing
else, so the whole file is the thing you paste.

## Install

1. Click your profile picture → **Preferences** → **Appearance**.
2. Select **Custom theme**, then click **Import**.
3. Paste the contents of one file and click **Apply**.

`pbcopy < tamarack-summer.txt` puts a season on the clipboard.

Slack notes on that dialog that it will "adapt the colors as best we can to
preserve contrast," so what lands is close to these values rather than exactly
them.

## What each file sets

Four values, in the order Slack's editor lists them:

| # | Slot | Source |
| --- | --- | --- |
| 1 | System navigation | `mantle`, or a deepened hero — see below |
| 2 | Selected items | the hero accent |
| 3 | Presence indication | `fern` |
| 4 | Notifications | `clay` |

Slack used to take ten values — the classic sidebar set, with separate entries for
the column, the hover fills, the text color and the top nav. It still accepts one
on import, but only slots 1, 3, 7 and 8 survive the mapping onto these four, so
there is nothing to be gained by writing one. These files are the four Slack keeps.

Presence and Notifications stay on `fern` and `clay` in every season. Those two
slots mean something — green for online, red for unread — and a season is not
allowed to recolor a signal.

## Why the light seasons have dark rails

All four colors land on the navigation surface: the selected channel is a fill on
it, and the presence dot and the unread badge sit on top of it. The rail is
therefore not free to be whatever the season likes — it has to be dark enough for a
green dot and a red badge to read against.

A dark season has that in `mantle`. A light season does not: `mantle` is a
near-white there, and a near-white rail is the one thing this port cannot use — it
disappears into Slack's own chrome and takes the sidebar's legibility with it.

So a light season's rail is its hero accent deepened onto the `crust` of the dark
season it shares a temperature with — Summer with Fall, Spring with Winter — at
half strength. The hue the season leads with survives: Summer's rail is a deep
rust and Spring's a deep forest, not a neutral. What changes is the room underneath
it.

Because that rail is dark, the other three colors are the dark-mode values of their
tokens, taken from the same partner. Same tokens, mode-appropriate variants. The
hero comes from the partner too rather than from the season itself, since Spring's
hero *is* `fern` and would otherwise be the exact color of its own presence dot.

The measured result, each color against the rail it sits on:

| Season | Rail | Selected | Presence | Notifications |
| --- | --- | --- | --- | --- |
| Spring | `#2A4620` | 4.43:1 | 4.89:1 | 3.28:1 |
| Summer | `#5C2E0A` | 4.71:1 | 5.18:1 | 3.48:1 |
| Fall | `#14110E` | 7.81:1 | 8.59:1 | 5.77:1 |
| Winter | `#0E1411` | 7.85:1 | 8.65:1 | 5.80:1 |

Undeepened, a hero rail put Spring's presence dot at 1.00:1 — the identical green
behind it — and its badge at 1.22:1.

## Rebuilding

`build.py` reads `../palette.json` and rewrites all four files, one per season, in
`order`. Colors live in the palette; the slot assignments, the season pairing and
the rail strength live in `build.py`.

```bash
python3 build.py
```

No dependencies beyond the Python standard library. To change a color, edit the
season definitions in the root `gen.py`, run `python3 gen.py` to regenerate
`palette.json`, then run `python3 build.py` here.

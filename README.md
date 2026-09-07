# Tamarack

A warm, nature-derived color palette in two hue-locked flavors.

Named for the tamarack — the North American larch, a conifer that turns brilliant
gold-orange every autumn before dropping its needles. A green tree that becomes the
hero color, which is the palette in one word.

No purple, no pink, no electric blue. Nine accents named for things that actually
have these colors, over a twelve-step role-named neutral ramp.

## Flavors

| Flavor | Mode | Base | Text | Character |
| --- | --- | --- | --- | --- |
| **Clearing** | light | `#FAF7F1` | `#2E271E` | Warm white, 40° |
| **Thicket** | dark | `#131A16` | `#DFE5DC` | Forest black, 152° |

A clearing is the bright open spot in a dark wood, so the pair explains itself.

## Accents

Both flavors sit at the same hue angle for a given token — only lightness and
saturation move. That hue lock is what makes them read as one palette in two states.

| Token | Hue | Clearing | Δ on base | Thicket | Δ on base |
| --- | --- | --- | --- | --- | --- |
| `ember` | 27° | `#A35514` | 5.08:1 | `#E9954D` | 7.47:1 |
| `amber` | 42° | `#8F6A14` | 4.63:1 | `#DCAE57` | 8.62:1 |
| `moss` | 64° | `#6E7524` | 4.64:1 | `#AFB766` | 8.25:1 |
| `fern` | 112° | `#4E7C3A` | 4.6:1 | `#8FBE71` | 8.23:1 |
| `juniper` | 168° | `#1F8168` | 4.47:1 | `#5AB99B` | 7.45:1 |
| `creek` | 187° | `#2A7B87` | 4.59:1 | `#66B2BA` | 7.28:1 |
| `slate` | 208° | `#4A6E8C` | 5.04:1 | `#88A6C2` | 6.98:1 |
| `clay` | 10° | `#A8422F` | 5.63:1 | `#D67464` | 5.51:1 |
| `chokeberry` | 318° | `#9D4382` | 5.52:1 | `#B988AA` | 6.04:1 |

## Neutrals

Role-named rather than color-named, deliberately: `surface0` means the same thing in
both flavors, whereas a color name would have to be the text in one and the background
in the other. The accents carry the identity; the neutrals carry the structure.

| Token | Clearing | Thicket |
| --- | --- | --- |
| `text` | `#2E271E` | `#DFE5DC` |
| `subtext1` | `#554C3E` | `#B8C4BB` |
| `subtext0` | `#6E6454` | `#98A69D` |
| `overlay2` | `#877C69` | `#7A8880` |
| `overlay1` | `#A0947F` | `#5F6E64` |
| `overlay0` | `#B8AC95` | `#47564C` |
| `surface2` | `#CFC4AE` | `#313F37` |
| `surface1` | `#E0D7C6` | `#26322B` |
| `surface0` | `#EDE7DB` | `#1C2620` |
| `base` | `#FAF7F1` | `#131A16` |
| `mantle` | `#F3EFE6` | `#0E1411` |
| `crust` | `#EBE5D9` | `#0A0F0C` |

## Roles

A palette without an assignment is just a list of colors. These maps are written
against token names, so they hold for either flavor.

### Syntax

| Token | Applies to |
| --- | --- |
| `ember` | Functions, methods |
| `amber` | Numbers |
| `moss` | Tags, attributes, markup structure |
| `fern` | Strings |
| `juniper` | Types, classes, interfaces |
| `creek` | Operators, builtins, escape sequences |
| `slate` | Properties, parameters, fields, JSON keys |
| `clay` | Keywords, storage |
| `chokeberry` | Constants, enum members, decorators, annotations |
| `overlay1` | Comments, doc blocks |
| `subtext0` | Punctuation, delimiters |
| `text` | Identifiers, everything unclaimed |

### Interface

| Token | Applies to |
| --- | --- |
| `ember` | Primary buttons, links, cursor, focus ring, active tab |
| `fern` | Success, added lines in a diff, passing tests |
| `amber` | Warnings, modified lines, pending state |
| `clay` | Errors, deleted lines, destructive actions |
| `creek` | Selection fill, search highlight, info state |
| `slate` | Secondary links, metadata, breadcrumbs |
| `chokeberry` | Constants and enum members in UI chrome |
| `base` | Editor and page background |
| `mantle` | Sidebar, gutter, status bar |
| `crust` | Window chrome, deepest recess |
| `surface0` | Panels, inline code, hover fill |
| `surface2` | Borders, dividers, inactive tab |
| `overlay0` | Disabled text, placeholder |

## ANSI 16

All sixteen slots map to real palette tokens. `chokeberry` exists because ANSI
demands a magenta and the original eight accents had no honest answer for it.

| Slot | Code | Clearing | Thicket | From |
| --- | --- | --- | --- | --- |
| black | 0 | `#554C3E` | `#26322B` | subtext1 (Clearing) / surface1 (Thicket) |
| red | 1 | `#A8422F` | `#D67464` | clay |
| green | 2 | `#4E7C3A` | `#8FBE71` | fern |
| yellow | 3 | `#8F6A14` | `#DCAE57` | amber |
| blue | 4 | `#4A6E8C` | `#88A6C2` | slate |
| magenta | 5 | `#9D4382` | `#B988AA` | chokeberry |
| cyan | 6 | `#2A7B87` | `#66B2BA` | creek |
| white | 7 | `#B8AC95` | `#B8C4BB` | overlay0 (Clearing) / subtext1 (Thicket) |
| bright black | 8 | `#6E6454` | `#313F37` | — |
| bright red | 9 | `#BC5340` | `#E08A7B` | — |
| bright green | 10 | `#5C8E45` | `#A0CB84` | — |
| bright yellow | 11 | `#A07920` | `#E6BC6F` | — |
| bright blue | 12 | `#587FA0` | `#9CB6CE` | — |
| bright magenta | 13 | `#B25395` | `#CB9FBE` | — |
| bright cyan | 14 | `#358995` | `#7BC1C8` | — |
| bright white | 15 | `#877C69` | `#DFE5DC` | — |

## Usage

### CSS

`tamarack.css` defines every color as a custom property, plus a paired `-rgb`
triplet for alpha composition. It resolves across all three theme states: the bare
`:root` carries Clearing, `prefers-color-scheme` swaps to Thicket unless light is
explicitly stamped, and an explicit `[data-theme]` stamp wins in either direction.

```css
@import "tamarack.css";

.button {
  background: var(--tm-ember);
  color: var(--tm-base);
}

.selection {
  background: rgb(var(--tm-creek-rgb) / 0.25);
}
```

Force a flavor with `<html data-theme="thicket">` or `data-theme="clearing"`.

### Sass

```scss
@use "tamarack" as *;

.button {
  background: tm("thicket", "ember");
}
```

### JSON

`palette.json` is the source of truth. Every color carries `hex`, `rgb`, `hsl`,
`accent`, and `contrastOnBase`; each flavor also carries a full `ansiColors` block
with normal and bright variants and their codes.

```json
{
  "thicket": {
    "colors": {
      "ember": {
        "hex": "#E9954D",
        "rgb": { "r": 233, "g": 149, "b": 77 },
        "accent": true,
        "contrastOnBase": 7.47
      }
    }
  }
}
```

## Regenerating

`palette.json`, `tamarack.css`, `tamarack.scss` and this README are all generated.
Edit the flavor definitions at the top of `gen.py`, then:

```bash
python3 gen.py
```

No dependencies beyond the Python standard library.

## Notes on the design

- **Contrast is measured, not assumed.** Every accent carries its ratio against its
  own flavor's `base`. Clearing spans roughly 4.5–5.6:1 and Thicket 5.5–8.6:1 — the
  light flavor is inherently flatter, which is a property of dark accents on a light
  ground rather than an oversight.
- **JSON keys map to `slate`, not `moss`.** `moss` and `fern` sit 48° apart, which is
  fine in prose and not fine in JSON, where keys and string values alternate on every
  line. Fixed by role assignment rather than by moving hues.
- **`amber` does numbers and warnings only.** Constants moved to `chokeberry` when it
  joined, so no token carries three unrelated meanings.

## License

MIT. See [LICENSE](LICENSE).

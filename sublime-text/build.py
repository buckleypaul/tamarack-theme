import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PALETTE = os.path.join(HERE, os.pardir, 'palette.json')

ACCENTS  = ['ember','amber','moss','fern','juniper','creek','slate','clay','chokeberry']
NEUTRALS = ['text','subtext1','subtext0','overlay2','overlay1','overlay0',
            'surface2','surface1','surface0','base','mantle','crust']

# ---------- globals ----------
# base=background · mantle=gutter · surface2=guides · overlay0=disabled
# hero=caret/active/primary · creek=selection/find · clay=error · crust=shadow
# `hero` is a per-season alias emitted into `variables`: the accent the season
# leads with (fern for Spring, ember for Summer and Fall, juniper for Winter).
GLOBALS = {
    'background':                 'var(base)',
    'foreground':                 'var(text)',
    'caret':                      'var(hero)',
    'block_caret':                'var(hero)',
    'invisibles':                 'color(var(overlay0) alpha(0.4))',
    'line_highlight':             'color(var(surface2) alpha(0.4))',
    'selection':                  'color(var(creek) alpha(0.25))',
    'selection_border':           'color(var(creek) alpha(0.6))',
    'selection_border_width':     '1',
    'inactive_selection':         'color(var(creek) alpha(0.12))',
    'inactive_selection_foreground': 'var(text)',
    'misspelling':                'var(clay)',
    'gutter':                     'var(mantle)',
    'gutter_foreground':          'var(overlay0)',
    'gutter_foreground_highlight':'var(hero)',
    'find_highlight':             'var(creek)',
    'find_highlight_foreground':  'var(base)',
    'highlight':                  'color(var(creek) alpha(0.5))',
    'guide':                      'color(var(surface2) alpha(0.6))',
    'active_guide':               'var(hero)',
    'stack_guide':                'color(var(surface2) alpha(0.9))',
    'shadow':                     'var(crust)',
    'shadow_width':               '8',
    'accent':                     'var(hero)',
    'fold_marker':                'var(amber)',
    'brackets_options':           'underline',
    'brackets_foreground':        'var(overlay2)',
    'bracket_contents_options':   'underline',
    'bracket_contents_foreground':'var(overlay2)',
    'tags_options':               'stippled_underline',
    'tags_foreground':            'var(moss)',
}

# ---------- rules ----------
# (name, scope, foreground, background, font_style)
RULES = [
    # comments — overlay1
    ('Comment', 'comment', 'overlay1', None, 'italic'),
    ('Documentation comment', 'comment.block.documentation', 'overlay1', None, 'italic'),
    ('Shebang', 'comment.line.shebang', 'overlay1', None, 'italic'),

    # punctuation — subtext0
    ('Punctuation', 'punctuation', 'subtext0', None, None),
    ('Punctuation separator', 'punctuation.separator', 'subtext0', None, None),
    ('Punctuation terminator', 'punctuation.terminator', 'subtext0', None, None),
    ('Punctuation section', 'punctuation.section', 'subtext0', None, None),
    ('Punctuation definition of a string', 'punctuation.definition.string', 'fern', None, None),

    # strings — fern
    ('String', 'string', 'fern', None, None),
    ('String regexp', 'string.regexp', 'creek', None, None),
    ('Character escape', 'constant.character.escape', 'creek', None, None),
    ('Regexp character class', 'constant.other.character-class.regexp', 'creek', None, None),

    # numbers — amber
    ('Number', 'constant.numeric', 'amber', None, None),
    ('Numeric unit suffix', 'constant.numeric.suffix, keyword.other.unit', 'creek', None, None),

    # constants — chokeberry
    ('Built-in constant', 'constant.language', 'chokeberry', None, None),
    ('Other constant', 'constant.other', 'chokeberry', None, None),
    ('User-defined constant', 'variable.other.constant, entity.name.constant', 'chokeberry', None, None),
    ('Library constant', 'support.constant', 'chokeberry', None, None),
    ('Enum member', 'entity.name.enum-member, meta.enum entity.name.constant', 'chokeberry', None, None),

    # decorators and annotations — chokeberry
    ('Annotation', 'meta.annotation, variable.annotation, entity.name.decorator', 'chokeberry', None, None),
    ('Annotation punctuation', 'punctuation.definition.annotation', 'chokeberry', None, None),

    # keywords and storage — clay
    ('Keyword', 'keyword', 'clay', None, None),
    ('Word operator', 'keyword.operator.word', 'clay', None, None),
    ('Storage', 'storage', 'clay', None, None),
    ('Storage type', 'storage.type', 'clay', None, None),
    ('Storage modifier', 'storage.modifier', 'clay', None, None),

    # operators and builtins — creek
    ('Operator', 'keyword.operator', 'creek', None, None),
    ('Accessor', 'punctuation.accessor', 'creek', None, None),
    ('Built-in function', 'support.function.builtin', 'creek', None, None),
    ('Built-in variable', 'variable.language', 'creek', None, None),
    ('Built-in type', 'support.type.primitive, storage.type.primitive', 'creek', None, None),

    # functions — ember
    ('Function name', 'entity.name.function', 'ember', None, None),
    ('Function call', 'variable.function', 'ember', None, None),
    ('Library function', 'support.function', 'ember', None, None),
    ('Macro', 'support.macro, entity.name.function.preprocessor', 'ember', None, None),

    # types and classes — juniper
    ('Class name', 'entity.name.class, entity.name.struct, entity.name.union, entity.name.impl',
     'juniper', None, None),
    ('Type name', 'entity.name.type, entity.name.trait, entity.name.enum, entity.name.interface',
     'juniper', None, None),
    ('Namespace', 'entity.name.namespace', 'juniper', None, None),
    ('Inherited class', 'entity.other.inherited-class', 'juniper', None, 'italic'),
    ('Library class/type', 'support.class, support.type', 'juniper', None, None),
    ('Generic parameter brackets', 'punctuation.definition.generic', 'juniper', None, None),

    # properties, parameters, fields — slate
    ('Parameter', 'variable.parameter', 'slate', None, 'italic'),
    ('Member/field', 'variable.other.member', 'slate', None, None),
    ('Label', 'entity.name.label', 'slate', None, None),
    ('Mapping key', 'meta.mapping.key string, meta.mapping.key string.unquoted', 'slate', None, None),
    ('Mapping key quotes', 'meta.mapping.key punctuation.definition.string', 'subtext0', None, None),
    ('YAML anchor/alias', 'entity.name.other.anchor, variable.other.alias', 'slate', None, 'italic'),

    # tags and attributes — moss
    ('Tag name', 'entity.name.tag', 'moss', None, None),
    ('Tag attribute', 'entity.other.attribute-name', 'moss', None, 'italic'),
    ('Tag punctuation', 'punctuation.definition.tag', 'subtext0', None, None),

    # identifiers — text
    ('Variable', 'variable', 'text', None, None),
    ('Other variable', 'variable.other', 'text', None, None),
    ('Generic name', 'meta.generic-name', 'text', None, None),

    # CSS
    ('CSS property name', 'support.type.property-name, meta.property-name entity.other.custom-property',
     'slate', None, None),
    ('CSS property value', 'support.constant.property-value', 'text', None, None),
    ('CSS selector tag', 'entity.name.tag.css', 'moss', None, None),
    ('CSS variable use', 'variable.other.custom-property', 'chokeberry', None, None),
    ('Sass/SCSS variable', 'variable.other.sass, variable.other.scss', 'slate', None, None),
    ('SCSS mixin', 'entity.name.mixin.scss, variable.other.mixin.scss', 'ember', None, None),

    # markup
    ('Markup heading', 'markup.heading', 'ember', None, 'bold'),
    ('Markup heading punctuation', 'markup.heading punctuation.definition.heading', 'subtext0', None, 'bold'),
    ('Markup bold', 'markup.bold', 'moss', None, 'bold'),
    ('Markup italic', 'markup.italic', 'moss', None, 'italic'),
    ('Markup link', 'markup.underline.link', 'slate', None, 'underline'),
    ('Markup link description', 'meta.link.inline.description, meta.image.inline.description',
     'chokeberry', None, None),
    ('Markup raw', 'markup.raw', 'fern', None, None),
    ('Markup inline code', 'markup.raw.inline', 'fern', None, None),
    ('Markup code fence info string', 'meta.code-fence.definition, constant.other.language-name',
     'overlay1', None, 'italic'),
    ('Markup quote', 'markup.quote', 'overlay1', None, 'italic'),
    ('Markup list punctuation', 'markup.list punctuation.definition.list_item', 'subtext0', None, None),

    # diffs
    ('Diff header', 'meta.diff, meta.diff.header, meta.diff.range', 'slate', None, None),
    ('Diff inserted', 'markup.inserted', 'fern', None, None),
    ('Diff deleted', 'markup.deleted', 'clay', None, None),
    ('Diff changed', 'markup.changed', 'amber', None, None),

    # diagnostics
    ('Invalid', 'invalid', 'base', 'clay', None),
    ('Invalid deprecated', 'invalid.deprecated', 'base', 'amber', None),
    ('Error message', 'message.error', 'clay', None, None),
]

POPUP_CSS = """html {{
    background-color: {surface0};
    color: {text};
}}
a {{
    color: {hero};
}}
code, .code {{
    background-color: {surface1};
    color: {text};
}}
.error {{
    color: {clay};
}}
.warning {{
    color: {amber};
}}
.success {{
    color: {fern};
}}
"""


def build(key, flavor):
    hexes = {n: flavor['colors'][n]['hex'] for n in ACCENTS + NEUTRALS}
    # chrome roles follow the season's lead accent rather than a fixed token
    variables = dict(hexes, hero=f"var({flavor['hero']})")

    rules = []
    for name, scope, fg, bg, style in RULES:
        rule = {'name': name, 'scope': scope}
        if fg:
            rule['foreground'] = f'var({fg})'
        if bg:
            rule['background'] = f'var({bg})'
        if style:
            rule['font_style'] = style
        rules.append(rule)

    return {
        'name': f"Tamarack {flavor['name']}",
        'author': 'Tamarack',
        'variables': variables,
        'globals': GLOBALS,
        'rules': rules,
        'popup_css': POPUP_CSS.format(hero=hexes[flavor['hero']], **hexes),
    }


def main():
    with open(PALETTE) as fh:
        palette = json.load(fh)

    for key, flavor in sorted(palette.items(), key=lambda kv: kv[1]['order']):
        scheme = build(key, flavor)
        path = os.path.join(HERE, f"Tamarack {flavor['name']}.sublime-color-scheme")
        with open(path, 'w') as fh:
            json.dump(scheme, fh, indent=4, ensure_ascii=False)
            fh.write('\n')
        print(f'wrote {os.path.basename(path)}  ({len(scheme["rules"])} rules)')


if __name__ == '__main__':
    main()

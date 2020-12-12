import fontforge
import psMat
from sys import stderr, argv
from compat_map import compat_map
from glyph_filter import ranges as filter_ranges
from os2_weights import os2_weights

weight = "Regular" if len(argv) == 1 else argv[1]
version = "1.00"

if not os2_weights.has_key(weight):
    raise Exception("Unknown weight: {}".format(weight))

latin = fontforge.open("./resources/SourceCodePro-{}.ttf".format(weight))
hans = fontforge.open("./resources/NotoSansJP-{}.otf".format(weight))

filters = [range(x[0], x[1]) for x in filter_ranges]

def sfnt_find_first(key_name):
    return [t for t in list(latin.sfnt_names) if t[1] == key_name][0]

def is_halfwidth(codepoint):
    return 0xFF61 <= codepoint <= 0xFFDC or 0xFFE8 <= codepoint <= 0xFFEE

def do_paste(glyph):
    hans.selection.select(glyph.glyphname)
    hans.copy()

    code = compat_map.get(glyph.unicode)
    if code is None: code = glyph.unicode

    latin.selection.select(code)
    latin.paste()

    try:
        latin[code].transform(psMat.scale(0.87))
        latin[code].transform(psMat.translate(77, 0))

        if is_halfwidth(code):
            latin[code].width = 512
        else:
            latin[code].width = 1024
    except Exception as err:
        stderr.write("E: {}\n".format(hex(code)))
        print(err)

    hans.selection.none()
    latin.selection.none()
    

def do_merge(cid_number):
    hans.cidsubfont = cid_number

    for g in hans.glyphs():
        if any([g.unicode in x for x in filters]):
            do_paste(g)

latin.em = 1024
latin.selection.all()
latin.transform(psMat.scale(0.8338762215))
for g in latin.glyphs():
    g.width = 512

latin.selection.none()

for n in range(1, 17):
    do_merge(n)

latin.fontname = "RelaxedTypingMono-{}".format(weight)
latin.familyname = "Relaxed Typing Mono"
latin.fullname = "Relaxed Typing Mono-{}".format(weight)
latin.os2_weight = os2_weights[weight]
latin.os2_vendor = "MSHD"
latin.sfntRevision = float(version)
latin.version = version
latin.copyright = """Source Code Pro:
{}

Noto Sans JP:
Copyright -2020 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'.
""".format(sfnt_find_first("Copyright")[2])
latin.sfnt_names = ()

latin.generate("RelaxedTypingMono-{}.ttf".format(weight))

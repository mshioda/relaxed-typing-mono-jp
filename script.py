import fontforge
import psMat
from sys import stderr, argv
from os import path, system
from compat_map import compat_map
from glyph_filter import ranges as filter_ranges
from os2_weights import os2_weights
from version import version

weight = "Regular" if len(argv) == 1 else argv[1]

if weight not in os2_weights:
    raise Exception(f"Unknown weight: {weight}")

if not path.exists(f"./resources/NotoSansJP-{weight}.ttf"):
    system("bash ./conv-ttf.sh")

latin = fontforge.open(f"./resources/SourceCodePro-{weight}.ttf")
han = fontforge.open(f"./resources/NotoSansJP-{weight}.ttf")

filters = [range(x[0], x[1]) for x in filter_ranges]

def sfnt_find_first(key_name):
    return [t for t in list(latin.sfnt_names) if t[1] == key_name][0]

def is_halfwidth(codepoint):
    return 0xFF61 <= codepoint <= 0xFFDC or 0xFFE8 <= codepoint <= 0xFFEE

def do_paste(glyph):
    han.selection.select(glyph.glyphname)
    han.copy()

    code = compat_map.get(glyph.unicode) or glyph.unicode
    if code in latin: code = glyph.unicode

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
        stderr.write(f"E: {hex(code)}\n")
        print(err)

    han.selection.none()
    latin.selection.none()
    

def do_merge():
    for g in han.glyphs():
        if any([g.unicode in x for x in filters]):
            do_paste(g)

latin.em = 1024
latin.selection.all()
latin.transform(psMat.scale(0.8338762215))
for g in latin.glyphs():
    g.width = 512

latin.selection.none()

do_merge()

latin.fontname = f"RelaxedTypingMonoJP-{weight}"
latin.familyname = "Relaxed Typing Mono JP"
latin.fullname = f"Relaxed Typing Mono JP-{weight}"
latin.os2_weight = os2_weights[weight]
latin.os2_vendor = "MSHD"
latin.sfntRevision = float(version)
latin.version = version
latin.copyright = f"""Source Code Pro:
{sfnt_find_first("Copyright")[2]}

Noto Sans JP:
Copyright -2020 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'.

Relaxed Typing Mono JP:
Copyright 2020 SHIODA Masaharu, with Reserved Font Name 'Relaxed Typing Mono'.
"""
latin.sfnt_names = ()

latin.generate(f"RelaxedTypingMonoJP-{weight}.ttf")

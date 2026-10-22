"""Convert TeX Live's Bitstream Charter Type 1 fonts (used by mathdesign in the
paper) to OpenType so matplotlib can use them. Run once; outputs sit next to
this script.

Charter has no Greek, so the italic font also gets the lowercase Greek from
mathdesign's Charter math italic, matching how the paper typesets e.g. delta."""
import os
from fontTools.t1Lib import T1Font
from fontTools.afmLib import AFM
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
from fontTools.ttLib import newTable
from fontTools.agl import toUnicode

TL = "/usr/local/texlive/2026/texmf-dist/fonts"
STYLES = {"bchr8a": "Regular", "bchri8a": "Italic", "bchb8a": "Bold", "bchbi8a": "Bold Italic"}
OUT = os.path.dirname(os.path.abspath(__file__))
# Lowercase Greek glyph names in the mathdesign font -> Unicode (skipping final sigma).
# Charter already uses "mu" for the micro sign, so the Greek glyphs get uniXXXX names.
GREEK = dict(zip(
    ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi "
     "omicron pi rho sigma tau upsilon phi chi psi omega").split(),
    [c for c in range(0x03B1, 0x03CA) if c != 0x03C2],
))

math_it = T1Font(f"{TL}/type1/public/mathdesign/mdbch/md-chri7m.pfb")
math_it.parse()
math_it_gs = math_it.getGlyphSet()

for base, style in STYLES.items():
    t1 = T1Font(f"{TL}/type1/bitstrea/charter/{base}.pfb")
    t1.parse()
    afm = AFM(f"{TL}/afm/bitstrea/charter/{base}.afm")
    gs = t1.getGlyphSet()
    names = [".notdef"] + sorted(n for n in gs.keys() if n != ".notdef")
    # Glyph name -> glyph set it is drawn from.
    source = {n: (gs, n) for n in names}
    greek_cmap = {}
    if style == "Italic":
        for n, code in GREEK.items():
            if n not in math_it_gs:  # e.g. no omicron; TeX uses a plain o
                continue
            name = f"uni{code:04X}"
            names.append(name)
            source[name] = (math_it_gs, n)
            greek_cmap[code] = name

    charstrings, widths, cmap = {}, {}, {}
    for n in names:
        src_gs, src_name = source[n]
        g = src_gs[src_name]
        rec = RecordingPen()
        g.draw(rec)  # executing the charstring sets g.width
        pen = T2CharStringPen(g.width, src_gs)
        rec.replay(pen)
        charstrings[n] = pen.getCharString()
        widths[n] = g.width
        u = toUnicode(n)
        if len(u) == 1:
            cmap[ord(u)] = n
    cmap.update(greek_cmap)

    family = "Charter"
    full = f"{family} {style}"
    ps = f"{family}-{style.replace(' ', '')}"
    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap(cmap)
    fb.setupCFF(ps, {"FullName": full}, charstrings, {})
    lsb = {}
    for n in names:
        src_gs, src_name = source[n]
        bp = BoundsPen(src_gs)
        src_gs[src_name].draw(bp)
        lsb[n] = bp.bounds[0] if bp.bounds else 0
    fb.setupHorizontalMetrics({n: (widths[n], lsb[n]) for n in names})
    asc, desc = afm.Ascender, afm.Descender
    fb.setupHorizontalHeader(ascent=asc, descent=desc)
    fb.setupNameTable({"familyName": family, "styleName": style, "psName": ps})
    bold, italic = "Bold" in style, "Italic" in style
    fb.setupOS2(sTypoAscender=asc, sTypoDescender=desc, usWinAscent=asc, usWinDescent=-desc,
                usWeightClass=700 if bold else 400,
                fsSelection=(0x20 if bold else 0) | (0x01 if italic else 0) | (0x40 if not (bold or italic) else 0))
    fb.setupPost(italicAngle=float(afm.ItalicAngle))
    fb.font["head"].macStyle = (1 if bold else 0) | (2 if italic else 0)

    kern = newTable("kern")
    kern.version = 0
    sub = KernTable_format_0()
    sub.version, sub.coverage, sub.format = 0, 1, 0
    sub.kernTable = {k: v for k, v in afm._kerning.items() if k[0] in gs and k[1] in gs}
    kern.kernTables = [sub]
    fb.font["kern"] = kern

    fb.save(os.path.join(OUT, f"{ps}.otf"))
    print("wrote", ps)

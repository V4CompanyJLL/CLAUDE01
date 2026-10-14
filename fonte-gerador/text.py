"""Shape text with HarfBuzz and emit outlined SVG glyph groups (same format as the original brandbook)."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import os

FONT_DIR = os.environ['SORA_DIR']
WEIGHTS = {300: 'Light', 400: 'Regular', 600: 'SemiBold', 700: 'Bold', 200: 'ExtraLight'}
_cache = {}

def font(w):
    if w not in _cache:
        p = os.path.join(FONT_DIR, f'Sora-{WEIGHTS[w]}.ttf')
        blob = hb.Blob.from_file_path(p)
        face = hb.Face(blob)
        hbf = hb.Font(face)
        tt = TTFont(p)
        _cache[w] = (hbf, tt, tt.getGlyphSet(), tt['head'].unitsPerEm, {})
    return _cache[w]

def glyph_d(w, name):
    hbf, tt, gs, upem, dc = font(w)
    if name not in dc:
        pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        gs[name].draw(pen)
        dc[name] = pen.getCommands()
    return dc[name]

def shape(s, w, tracking=0.0):
    """returns list of (glyphname, x_units) and total advance in units"""
    hbf, tt, gs, upem, dc = font(w)
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
    hb.shape(hbf, buf, {'kern': True, 'liga': True})
    order = tt.getGlyphOrder()
    x = 0; out = []
    tr = tracking * upem
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((order[info.codepoint], x + pos.x_offset))
        x += pos.x_advance + tr
    if out: x -= tr
    return out, x, upem

def width(s, size, w=400, tracking=0.0):
    _, adv, upem = shape(s, w, tracking)
    return adv * size / upem

def svg_text(s, x, y, size, fill, w=400, tracking=0.0, anchor='start'):
    glyphs, adv, upem = shape(s, w, tracking)
    k = size / upem
    if anchor == 'middle': x -= adv * k / 2
    elif anchor == 'end': x -= adv * k
    parts = []
    for name, gx in glyphs:
        d = glyph_d(w, name)
        if d:
            parts.append(f'<path d="{d}" transform="translate({gx:g} 0)"/>')
    return (f'<g fill="{fill}" transform="translate({x:g} {y:g}) scale({k:g} -{k:g})">' + ''.join(parts) + '</g>')

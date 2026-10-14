"""New page 10: graphic pattern built from the official symbol (paths reused untouched)."""
import os, re
from text import svg_text

IMP, VIN, ROS, CAR, CRE = "#EA382A", "#431B20", "#FFB5A6", "#231C20", "#F5EFE5"
SX, SY, SW = 129.7, 226.9, 62.3   # symbol origin/width in the source coordinate space

def symbol_paths(src):
    s = open(os.path.join(src, "..", "assets", "GEREVENDAS-symbol-principal.svg")).read()
    return re.findall(r'd="([^"]*)"', s)

def sym(D, x, y, size, fill):
    k = size / SW
    return (f'<g fill="{fill}" transform="translate({x:g} {y:g}) scale({k:g}) translate(-{SX} -{SY})">' +
            ''.join(f'<path fill-rule="evenodd" d="{d}"/>' for d in D) + '</g>')

def label(t, x, y, fill):
    return svg_text(t, x, y, 18 * 0.86, fill, w=400, tracking=0.14)

def brick(D, x0, y0, w, h, pitch, size, color, top=0):
    """Symbols on a staggered grid (each row shifted half a step) clipped to the panel."""
    out = []
    rows = int((h - top) / pitch) + 2
    for r in range(rows):
        off = (pitch / 2) if r % 2 else 0
        cy = y0 + top + r * pitch
        c = -1
        while True:
            cx = x0 + off + c * pitch + (pitch - size) / 2
            if cx > x0 + w: break
            col = color(cx - x0 + size / 2, cy - y0 + size / 2, w, h)
            if col: out.append(sym(D, cx, cy, size, col))
            c += 1
    return out

def build(src, outdir):
    D = symbol_paths(src)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',
         '<defs><clipPath id="pa"><rect x="0" y="340" width="1100" height="664"/></clipPath>'
         '<clipPath id="pb"><rect x="1100" y="340" width="820" height="332"/></clipPath>'
         '<clipPath id="pc"><rect x="1100" y="672" width="820" height="332"/></clipPath></defs>',
         f'<rect x="0" y="0" width="1920" height="1080" fill="{CRE}"/>',
         label("GEREVENDAS / IDENTIDADE VISUAL", 64, 49, CAR),
         label("10 / PADRÃO GRÁFICO", 1230, 49, CAR),
         f'<rect x="64" y="76" width="1792" height="1" fill="{CAR}"/>',
         svg_text("Um padrão em movimento.", 64, 200, 64 * 0.9, VIN, w=600, tracking=-0.025),
         svg_text("O símbolo se repete em grade deslocada, criando ritmo e direção: a progressão do funil.", 64, 262, 27 * 0.9, CAR, w=300),
         svg_text("Use em capas, fundos e peças de apoio. A assinatura permanece íntegra e separada do padrão.", 64, 298, 27 * 0.9, CAR, w=300)]

    # A: principal — tonal grid with a rising area of Impulso (growth / progression)
    def grow(cx, cy, w, h):
        line = h * (1.02 - 0.95 * max(cx / w, 0) ** 1.25)   # rises from left to right
        d = cy - line
        if d > 40: return IMP
        if d > -40: return ROS
        return CAR
    o += [f'<rect x="0" y="340" width="1100" height="664" fill="{VIN}"/>', '<g clip-path="url(#pa)">']
    o += brick(D, 0, 340, 1100, 664, 110, 70, grow, top=96)
    o += ['</g>', label("PADRÃO PRINCIPAL / PROGRESSÃO", 38, 386, CRE)]

    # B: base clara — monochrome
    o += [f'<rect x="1100" y="340" width="820" height="332" fill="{ROS}"/>', '<g clip-path="url(#pb)">']
    o += brick(D, 1100, 340, 820, 332, 92, 58, lambda *a: VIN, top=86)
    o += ['</g>', label("VARIAÇÃO / BASE CLARA", 1138, 386, VIN)]

    # C: ampliação — enlarged symbol cropped by the panel
    o += [f'<rect x="1100" y="672" width="820" height="332" fill="{IMP}"/>', '<g clip-path="url(#pc)">',
          sym(D, 1420, 580, 640, CRE), '</g>', label("AMPLIAÇÃO / RECORTE", 1138, 718, CRE)]

    o += [svg_text("Mais controle. Mais vendas.", 64, 1039, 18 * 0.9, CAR),
          svg_text("GEREVENDAS  /  10", 1851, 1039, 17 * 0.9, CAR, tracking=0.02, anchor="end"), '</svg>']
    open(os.path.join(outdir, "10-padrao.svg"), "w").write(''.join(o))

def export_patterns(src, outdir):
    """Standalone 1920x1080 pattern backgrounds for the asset folder."""
    D = symbol_paths(src)
    def grow(cx, cy, w, h):
        d = cy - h * (1.02 - 0.95 * max(cx / w, 0) ** 1.25)
        return IMP if d > 40 else ROS if d > -40 else CAR
    sets = {
        "GEREVENDAS-padrao-progressao": (VIN, grow),
        "GEREVENDAS-padrao-vinho": (VIN, lambda *a: CAR),
        "GEREVENDAS-padrao-rosado": (ROS, lambda *a: VIN),
        "GEREVENDAS-padrao-impulso": (IMP, lambda *a: CRE),
    }
    for name, (bg, col) in sets.items():
        o = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',
             '<defs><clipPath id="c"><rect width="1920" height="1080"/></clipPath></defs>',
             f'<rect width="1920" height="1080" fill="{bg}"/><g clip-path="url(#c)">']
        o += brick(D, 0, 0, 1920, 1080, 110, 70, col, top=20)
        o += ['</g></svg>']
        open(os.path.join(outdir, name + ".svg"), "w").write(''.join(o))

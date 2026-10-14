import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from text import svg_text, width
from content import PAGES
import page10

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
G = re.compile(r'<g fill="(#\w+)" transform="translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+) -[\d.]+\)">(?:<path d="[^"]*" transform="translate\([\d.-]+ 0\)"/>)*</g>')

def is_label(t):
    letters = [c for c in t if c.isalpha()]
    return len(letters) > 1 and all(c.isupper() for c in letters)

def render(entry, fill, x, y, sc):
    e = {"t": entry} if isinstance(entry, str) else dict(entry)
    t = e["t"]
    a = sc * 2048
    display = abs(a - round(a)) > 0.01
    orig = sc * 1000 if display else round(a)
    if display:
        st = dict(w=600, size=orig * 0.9, tr=-0.025)
    elif is_label(t) and orig <= 20:
        st = dict(w=400, size=orig * 0.86, tr=0.14)
    else:
        st = dict(w=300 if orig >= 23 else 400, size=orig * 0.9, tr=-0.005)
    st.update({k: v for k, v in e.items() if k in ("w", "size", "tr")})
    return svg_text(t, e.get("x", x), e.get("y", y), st["size"], e.get("fill", fill),
                    w=st["w"], tracking=st["tr"], anchor=e.get("anchor", "start")), st

for name, texts in PAGES.items():
    s = open(os.path.join(SRC, name + ".svg")).read()
    groups = list(G.finditer(s))
    assert len(groups) == len(texts), (name, len(groups), len(texts))
    out, last = [], 0
    for m, entry in zip(groups, texts):
        fill, x, y, sc = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4))
        out.append(s[last:m.start()])
        if entry is not None:
            g, st = render(entry, fill, x, y, sc)
            out.append(g)
        last = m.end()
    out.append(s[last:])
    open(os.path.join(OUT, name + ".svg"), "w").write("".join(out))

page10.build(SRC, OUT)
print("ok")

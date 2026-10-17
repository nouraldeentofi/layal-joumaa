#!/usr/bin/env python3
"""Draws assets/img/og.jpg (1200×630), the link-preview card: a typographic card with her name,
her LinkedIn headline and the hero's map of where her clients work. No photo.

Needs Playwright for Python and Chrome:  python3 og.py"""
import html, os, pathlib, tempfile
import build as B

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / B.OG_IMG


def card():
    data = B._map()
    P = data["places"]
    x0, y0, vw, vh = B.FLIGHT_VB
    sy = tuple(P["sy"])
    land = "".join(f"M{x} {y}h0" for x, y in data["dots"] if x >= x0 - 12)
    arcs, pins = "", ""
    for key, bend, *_ in B.FLIGHT_DEST:
        E = tuple(P[key])
        mx, my = B._arc(sy, E, bend)
        arcs += f'<path class="trail" d="M{sy[0]} {sy[1]}Q{mx:.1f} {my:.1f} {E[0]} {E[1]}"/>'
        pins += f'<circle class="pin" cx="{E[0]}" cy="{E[1]}" r="9"/>'
    font = lambda n: (HERE / "assets" / "fonts" / n).as_uri()
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Readex;font-weight:160 700;src:url({font("readex-pro-arabic-full-normal.woff2")}) format("woff2");unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}}
@font-face{{font-family:Readex;font-weight:160 700;src:url({font("readex-pro-latin-full-normal.woff2")}) format("woff2");unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:Ruqaa;font-weight:700;src:url({font("aref-ruqaa-arabic-700-normal.woff2")}) format("woff2");unicode-range:U+0600-06FF,U+FB50-FDFF,U+FE70-FEFC}}
@font-face{{font-family:Ruqaa;font-weight:700;src:url({font("aref-ruqaa-latin-700-normal.woff2")}) format("woff2");unicode-range:U+0000-00FF}}
*{{box-sizing:border-box}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{position:relative;font-family:Readex,sans-serif;color:#242327;
  background:radial-gradient(60% 70% at 88% 18%,rgba(244,221,217,.85),transparent 70%),radial-gradient(50% 60% at 6% 100%,rgba(249,204,168,.45),transparent 70%),#F6F5F3}}
body::before{{content:"";position:absolute;inset:0 0 auto;height:10px;background:#EE7F2D}}
.map{{position:absolute;right:26px;top:84px;width:700px;opacity:.95}}
.land{{fill:none;stroke:rgba(36,35,39,.2);stroke-width:4.8;stroke-linecap:round}}
.trail{{fill:none;stroke:#EE7F2D;stroke-width:5.5;stroke-linecap:round;stroke-dasharray:0 11}}
.pin{{fill:#EE7F2D;stroke:#fff;stroke-width:4}}
.origin{{fill:#242327;stroke:#fff;stroke-width:4}}
.copy{{position:absolute;left:72px;top:96px;width:640px}}
.ar{{margin:0;font-size:92px;font-weight:600;line-height:1.15;direction:rtl;text-align:left}}
.en{{margin:2px 0 0;font-size:60px;font-weight:560;letter-spacing:-.02em;font-variation-settings:"HEXP" 24;line-height:1.05}}
.role{{margin:26px 0 0;font-size:26px;color:#5D5B61;line-height:1.45}}
.role b{{color:#B4521A;font-weight:500}}
.hl{{position:absolute;left:72px;bottom:74px;max-width:640px;padding:16px 22px;background:#fff;border-left:5px solid #EE7F2D;border-radius:6px;
  font-size:27px;font-weight:560;box-shadow:0 20px 40px -24px rgba(60,40,30,.45)}}
.sig{{position:absolute;right:70px;bottom:58px;display:flex;align-items:center;gap:16px;font-family:Ruqaa,serif;font-weight:700;font-size:64px;color:#B4521A;line-height:1}}
.sig span{{width:78px;height:78px;border-radius:22px;background:#F4DDD9;display:grid;place-items:center}}
.sig svg{{width:52px;height:52px}}
.nib .nib-ink{{fill:none;stroke:#EE7F2D;stroke-width:2.6;stroke-linecap:round}}.nib .nib-body{{fill:#242327}}
.nib .nib-slit{{fill:none;stroke:#fff;stroke-width:1.3;stroke-linecap:round}}.nib .nib-hole{{fill:#fff}}
</style></head><body>
<svg class="map" viewBox="{x0} {y0} {vw} {vh}"><path class="land" d="{land}"/>{arcs}{pins}<circle class="origin" cx="{sy[0]}" cy="{sy[1]}" r="9"/></svg>
<div class="copy">
  <p class="ar">{B.NAME_AR}</p>
  <p class="en">{B.NAME_EN}</p>
  <p class="role">CV &amp; resume writer · LinkedIn optimisation · Personal branding<br><b>Syria · the Gulf · Europe · the US</b></p>
</div>
<p class="hl">“{html.escape(B.HEADLINE_LI.split(" || ")[-1])}”</p>
<div class="sig">ليال<span>{B.NIB}</span></div>
</body></html>'''


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as tmp:
        page_file = pathlib.Path(tmp) / "og.html"
        page_file.write_text(card(), encoding="utf-8")
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            pg.goto(page_file.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(OUT), type="jpeg", quality=88)
            b.close()
    print("wrote", OUT.relative_to(HERE), os.path.getsize(OUT), "bytes")

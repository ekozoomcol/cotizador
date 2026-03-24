import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace all relevant rules for `#previewGrid`, `#orderPreviewGrid`, `.previewItem`, `.previewSvg` and its SVG.
# Since we don't know the exact current state, it's safer to append a strong `<style>` block at the end of `<head>` 
# to override whatever was there, or cleanly do a `re.sub`.
# Let's cleanly inject a style block before `</head>`.

override_css = """
/* --- INJECTED SCALING FIXES FOR MULTIPLE BAGS --- */
#previewGrid, #orderPreviewGrid {
  display: flex;
  gap: 16px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  align-items: center;
  justify-content: center;
}
.previewItem {
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  max-width: 100%;
  overflow: hidden;
}
.previewItem > span, .previewItem > div:not(.previewSvg) {
  display: none; /* Hide any extra text/dims if they exist inside Item */
}
.previewSvg {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
#previewGrid .previewSvg svg, #orderPreviewGrid .previewSvg svg, .previewSvg svg {
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 100% !important;
  object-fit: contain;
  filter: drop-shadow(0 15px 25px rgba(0,0,0,0.08));
}
/* Ensure the wraps are constrained heavily */
#previewWrap, #orderPreviewWrap {
  flex: 1 1 auto;
  min-height: 0 !important;
  max-height: 450px !important;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
}
"""

if "/* --- INJECTED SCALING FIXES FOR MULTIPLE BAGS --- */" in html:
    html = re.sub(r'/\* --- INJECTED SCALING FIXES.*?</style>', override_css + "\n</style>", html, flags=re.DOTALL)
else:
    html = html.replace("</head>", f"<style>{override_css}</style>\n</head>")

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

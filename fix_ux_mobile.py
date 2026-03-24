import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Increase font sizes back to a better middle ground for mobile legibility.
css_replacements = {
    r'\.priceHighlight\s*{[^}]+}': """.priceHighlight {
    margin: 0 auto 12px;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #ffffff;
    font-size: clamp(34px, 3.2vw, 56px);
    font-weight: 800;
    border-radius: var(--radius-lg);
    padding: 12px 16px;
    line-height: 1.1;
    box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
    font-family: 'Outfit', sans-serif;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }""",
    r'\.posterTitle\s*{[^}]+}': """.posterTitle {
    text-align: center;
    font-size: clamp(26px, 2.5vw, 40px);
    letter-spacing: -0.5px;
    margin: 0 0 6px;
    color: #0f172a;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    text-transform: uppercase;
  }""",
    r'\.posterSub\s*{[^}]+}': """.posterSub {
    text-align: center;
    color: #475569;
    font-size: clamp(15px, 1.2vw, 19px);
    margin-bottom: 12px;
    font-weight: 500;
  }""",
    r'\.miniList\s*{[^}]+}': """.miniList {
    width: 100%;
    margin: 0 auto 8px;
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 8px 0;
    font-size: clamp(16px, 1.4vw, 22px);
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
  }""",
    r'\.miniRow\s*{[^}]+}': """.miniRow {
    display:flex;
    justify-content: space-between;
    gap: 16px;
    margin: 6px 0;
    padding: 4px 12px;
    border-radius: 8px;
    transition: background 0.2s;
  }""",
    # 2. Fix the SVG sizing so it actually takes all the flex space allocated, ensuring minimum 20%
    r'#previewGrid \.previewSvg svg, #orderPreviewGrid \.previewSvg svg, \.previewSvg svg\s*{[^}]+}': """#previewGrid .previewSvg svg, #orderPreviewGrid .previewSvg svg, .previewSvg svg {
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  max-height: 100% !important;
  object-fit: contain;
  filter: drop-shadow(0 15px 25px rgba(0,0,0,0.08));
}""",
    r'#previewWrap, #orderPreviewWrap\s*{[^}]+}': """#previewWrap, #orderPreviewWrap {
  flex: 1 1 20%;
  min-height: 20% !important;
  max-height: 50vh !important;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
}"""
}

# The overrides are in a style block at the bottom, so doing a clean search and replace
for pattern, repl in css_replacements.items():
    html = re.sub(pattern, repl, html, flags=re.DOTALL)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

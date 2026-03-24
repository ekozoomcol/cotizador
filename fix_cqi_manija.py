import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update separacionInternaCm = 7.5 to 8
html = html.replace('const separacionInternaCm = 7.5;', 'const separacionInternaCm = 8;')

# 2. Add container-type to .board > .card and update .priceHighlight
# We can use cqi (container query inline length) to scale text relative to the card width!
css_card = r'(\.board\s*>\s*\.card\s*{)'
html = re.sub(css_card, r'\1\n  container-type: inline-size;', html)

# Replace .priceHighlight
old_pricehighlight = r'\.priceHighlight\s*{[^}]+}'
new_pricehighlight = """.priceHighlight {
    margin: 0 auto 12px;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #ffffff;
    font-size: clamp(16px, 8.5cqi, 44px);
    font-weight: 800;
    border-radius: var(--radius-lg);
    padding: 12px 0px;
    line-height: 1.1;
    box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
    font-family: 'Outfit', sans-serif;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    white-space: nowrap;
    overflow: hidden;
  }"""

html = re.sub(old_pricehighlight, new_pricehighlight, html)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

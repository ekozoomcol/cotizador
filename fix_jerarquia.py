import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# CSS adjustments
css_replacements = {
    r'\.priceHighlight\s*{[^}]+}': """.priceHighlight {
    margin: 0 auto 12px;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #ffffff;
    font-size: clamp(28px, 2.5vw, 38px);
    font-weight: 800;
    border-radius: var(--radius-lg);
    padding: 10px 16px;
    line-height: 1.1;
    box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
    font-family: 'Outfit', sans-serif;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }""",
    r'\.posterTitle\s*{[^}]+}': """.posterTitle {
    text-align: center;
    font-size: clamp(22px, 2vw, 32px);
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
    font-size: clamp(14px, 1.1vw, 17px);
    margin-bottom: 12px;
    font-weight: 500;
  }""",
    r'\.miniList\s*{[^}]+}': """.miniList {
    width: 100%;
    margin: 0 auto 8px;
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 6px 0;
    font-size: clamp(15px, 1.3vw, 18px);
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
  }""",
    r'\.miniRow\s*{[^}]+}': """.miniRow {
    display:flex;
    justify-content: space-between;
    gap: 16px;
    margin: 4px 0;
    padding: 4px 12px;
    border-radius: 8px;
    transition: background 0.2s;
  }""",
    # Update injected CSS for #previewWrap
    r'min-height:\s*0\s*!important;': "min-height: 25% !important;"
}

for pattern, repl in css_replacements.items():
    html = re.sub(pattern, repl, html, flags=re.DOTALL)


# JS adjustments to change `.orderTitle` text inside `renderDesignSummary`
js_target = r'(document\.getElementById\("posterTitle"\)\.textContent\s*=\s*bagTypeLabel;)'
js_repl = r'\1\n  const orderTitle = document.querySelector(".orderTitle");\n  if (orderTitle) orderTitle.textContent = bagTypeLabel;'
html = re.sub(js_target, js_repl, html)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

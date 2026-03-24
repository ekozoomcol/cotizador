import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Hide Manija 1 and Manija 2, and add Largo Arco Manija (Visual)
html = re.sub(
    r'<div class="row"\s*id="row_manijas">.*?</div>\s*</div>',
    """<div class="row" id="row_manijas">
        <div style="display:none;"><label>Manija 1 (cm)</label><input id="manija1_cm" type="number" value="60"></div>
        <div style="display:none;"><label>Manija 2 (cm)</label><input id="manija2_cm" type="number" value="60"></div>
        <div><label>Largo arco visual</label><input id="largo_arco_visual" type="number" value="55" min="10" max="150"></div>
        <div><label>Ancho manijas (cm)</label><input id="ancho_manijas_cm" type="number" value="5"></div>
      </div>""",
    html,
    flags=re.DOTALL
)

# 2. Add `largo_arco_visual` to `generateModernBagSVG` arguments and logic
html = html.replace(
    'function generateModernBagSVG(fabricHex, logoColors, bagType, anchoCm, altoCm, showMeasures=true) {',
    'function generateModernBagSVG(fabricHex, logoColors, bagType, anchoCm, altoCm, showMeasures=true, archVisualCm=55) {'
)

html = re.sub(
    r'const archH\s*=\s*archW\s*\*\s*1\.5\s*;',
    'const archH = archW * (Number(archVisualCm) / 36.666);',
    html
)

# 3. Pass `n("largo_arco_visual") || 55` into the render preview inside `makeItem`
html = re.sub(
    r'svgBox\.innerHTML\s*=\s*generateModernBagSVG\(fabricHex,\s*logoColors,\s*bagType,\s*ancho,\s*alto,\s*showMeasures\);',
    'svgBox.innerHTML = generateModernBagSVG(fabricHex, logoColors, bagType, ancho, alto, showMeasures, document.getElementById("largo_arco_visual") ? Number(document.getElementById("largo_arco_visual").value) : 55);',
    html
)

# 4. Add `largo_arco_visual` to the preview instant listeners array
html = re.sub(
    r'("color_hex",\s*"caras",\s*"logo_colors_count",\s*"logo_c1_a",\s*"logo_c1_b",\s*"logo_c2_a",\s*"logo_c2_b")',
    r'\1, "largo_arco_visual"',
    html
)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

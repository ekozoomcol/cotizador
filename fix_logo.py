import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove old `logo_colors_count` block from the main row
html = re.sub(
    r'<div>\s*<label>Colores del logo</label>\s*<select id="logo_colors_count">.*?</select>\s*<div class="inlineHint">[^<]*</div>\s*</div>',
    '',
    html,
    flags=re.DOTALL
)

# 2. Re-write the `<details class="adv">` Logo area
new_logo_html = """
        <div class="subTitle">Logo por cara (Hasta 4 colores)</div>

        <div class="row" id="row_tintas_c1">
          <div>
            <label>Tintas Cara Frente</label>
            <select id="tintas_c1">
              <option value="1">1 color</option>
              <option value="2">2 colores</option>
              <option value="3">3 colores</option>
              <option value="4">4 colores</option>
            </select>
          </div>
          <div id="wrap_c1_1"><label>C1</label><input type="color" id="logo_c1_1" value="#059669"></div>
          <div id="wrap_c1_2"><label>C2</label><input type="color" id="logo_c1_2" value="#000000"></div>
          <div id="wrap_c1_3"><label>C3</label><input type="color" id="logo_c1_3" value="#FFFFFF"></div>
          <div id="wrap_c1_4"><label>C4</label><input type="color" id="logo_c1_4" value="#FF7A00"></div>
        </div>

        <div class="row" id="row_tintas_c2">
          <div>
            <label>Tintas Cara Trasera</label>
            <select id="tintas_c2">
              <option value="1">1 color</option>
              <option value="2">2 colores</option>
              <option value="3">3 colores</option>
              <option value="4">4 colores</option>
            </select>
          </div>
          <div id="wrap_c2_1"><label>C1</label><input type="color" id="logo_c2_1" value="#059669"></div>
          <div id="wrap_c2_2"><label>C2</label><input type="color" id="logo_c2_2" value="#000000"></div>
          <div id="wrap_c2_3"><label>C3</label><input type="color" id="logo_c2_3" value="#FFFFFF"></div>
          <div id="wrap_c2_4"><label>C4</label><input type="color" id="logo_c2_4" value="#FF7A00"></div>
        </div>
"""
# Replace the old rows from Cara 1 - Color 1 up to end of row_logo_cara2
html = re.sub(
    r'<div class="subTitle">Logo por cara</div>\s*<div class="row">.*?<div class="row" id="row_logo_cara2">.*?</div>\s*</div>',
    new_logo_html.strip(),
    html,
    flags=re.DOTALL
)

# 3. Update syncLogoControlsUI
new_sync_js = """
function syncLogoControlsUI(){
  const caras = Math.max(1, Math.min(2, n("caras") || 1));
  const t1 = n("tintas_c1") || 1;
  const t2 = n("tintas_c2") || 1;

  document.getElementById("row_tintas_c2").style.display = (caras === 2) ? "flex" : "none";

  for(let i=1; i<=4; i++){
    document.getElementById(`wrap_c1_${i}`).style.display = (i <= t1) ? "block" : "none";
    document.getElementById(`wrap_c2_${i}`).style.display = (i <= t2 && caras === 2) ? "block" : "none";
  }
}
"""
html = re.sub(
    r'function syncLogoControlsUI\(\)\{.*?(?=function buildLogoSVGBlock|function cleanAndStyleSVG|function cleanAndStyleSVG)',
    new_sync_js,
    html,
    flags=re.DOTALL
)

# 4. Update array of events
html = re.sub(
    r'\[\s*"color_hex",\s*"caras",\s*"logo_colors_count",\s*"logo_c1_a",\s*"logo_c1_b",\s*"logo_c2_a",\s*"logo_c2_b",\s*"largo_arco_visual"\s*\]',
    '["color_hex","caras","tintas_c1","tintas_c2","logo_c1_1","logo_c1_2","logo_c1_3","logo_c1_4","logo_c2_1","logo_c2_2","logo_c2_3","logo_c2_4","largo_arco_visual"]',
    html
)
html = re.sub(
    r'\[\s*"color_hex",\s*"logo_c1_a",\s*"logo_c1_b",\s*"logo_c2_a",\s*"logo_c2_b"\s*\]',
    '["color_hex"]', # Swatches logic is removed since we use native color inputs for simplicity and speed
    html
)

# 5. Fix `getLogoColors` and `makeItem` inside `renderPreviewInstant`
new_get_colors = """
  const getLogoColors = (caraIdx) => {
    const t = caraIdx === 1 ? (n("tintas_c1") || 1) : (n("tintas_c2") || 1);
    let arr = [];
    for(let i=1; i<=t; i++){
      arr.push(document.getElementById(`logo_c${caraIdx}_${i}`)?.value || "#000");
    }
    return arr;
  };
"""
html = re.sub(
    r'const getLogoColors = \(caraIdx\) => \{.*?\};',
    new_get_colors.strip(),
    html,
    flags=re.DOTALL
)

# Remove `const k = Math.max(...)`
html = re.sub(r'const k = Math\.max\(1, Math\.min\(2, Number\(v\("logo_colors_count"\)\) \|\| 1\)\);', '', html)

# 6. Update `cotizarAuto` payload to send `tintas: max(t1, t2)`
html = re.sub(
    r'tintas:\s*n\("tintas"\)',
    'tintas: Math.max(n("tintas_c1")||1, n("tintas_c2")||1)',
    html
)

# 7. Update `renderDesignSummary` legend
new_legend_js = """
  const caras = Math.max(1, Math.min(2, n("caras") || 1));
  const t1 = n("tintas_c1") || 1;
  const t2 = n("tintas_c2") || 1;
  let legend = "";
  if (caras === 1) {
    legend = `INCLUYE LOGO 1 CARA (${t1} TINTA${t1>1?'S':''})`;
  } else {
    legend = `LOGO FRENTE (${t1} TINTA${t1>1?'S':''}) · POSTERIOR (${t2} TINTA${t2>1?'S':''})`;
  }
"""
html = re.sub(
    r'const caras = Math\.max\(1, Math\.min\(2, n\("caras"\)\s*\|\|\s*1\)\);\s*const tintas = Math\.max\(1, n\("tintas"\)\s*\|\|\s*1\);\s*const txtCara[^`]+`INCLUYE LOGO A \$\{caras\}[^`]+`\s*;',
    new_legend_js.strip(),
    html,
    flags=re.DOTALL
)

# 8. Update SVG logo generator in `generateModernBagSVG`
# We replace the textWithHalo and logoSVG assignment...
new_logo_svg_logic = """
  let logoSVG = "";
  const tx = w / 2;
  const ty = h / 2;
  
  const c1 = logoColors[0] || "#0833a2";
  const c2 = logoColors.length > 1 ? logoColors[1] : c1;
  const c3 = logoColors.length > 2 ? logoColors[2] : c1;
  const c4 = logoColors.length > 3 ? logoColors[3] : c2;

  const dropShadow = `<filter id="logoShdw-${tx}"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.12"/></filter>`;
  
  // Isotipo (Hoja geometrica)
  const pieceA = `
    <path d="M ${tx} ${ty-40} C ${tx+35} ${ty-40}, ${tx+35} ${ty-5}, ${tx} ${ty-5} C ${tx-35} ${ty-5}, ${tx-35} ${ty-40}, ${tx} ${ty-40} Z" 
          fill="${c1}" filter="url(#logoShdw-${tx})"/>
  `;
  // Detalle Isotipo (Lenteja central)
  const pieceB = `
    <circle cx="${tx}" cy="${ty-22.5}" r="7" fill="${c2}" />
  `;
  // Texto Supremo
  const pieceC = `
    <text x="${tx}" y="${ty + 18}" text-anchor="middle" font-size="16" font-family="Plus Jakarta Sans, sans-serif" font-weight="900" fill="${c3}" letter-spacing="0.5px">TU LOGO</text>
  `;
  // Texto Inferior
  const pieceD = `
    <text x="${tx}" y="${ty + 36}" text-anchor="middle" font-size="14" font-family="Plus Jakarta Sans, sans-serif" font-weight="700" fill="${c4}" opacity="0.8">AQUÍ</text>
  `;

  logoSVG = `<defs>${dropShadow}</defs>${pieceA}${pieceB}${pieceC}${pieceD}`;
"""
html = re.sub(
    r'const textWithHalo =.*?\} else \{.*?textWithHalo\("TU LOGO", ty, c1, 26\);\s*\}',
    new_logo_svg_logic.strip(),
    html,
    flags=re.DOTALL
)


with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

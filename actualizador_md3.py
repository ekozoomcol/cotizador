import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS specifically for .board and .card
css_replacements = {
    r'\.card\s*{[^}]+}': """.card {
    border: 1px solid var(--card-border);
    border-radius: 28px; /* Google MD3 typical large shape */
    background: var(--card-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    padding: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.08); /* MD3 elevation 1 */
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
  }""",
    r'\.board\s*{\s*display:\s*grid;[^}]+}': """.board {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    margin-bottom: 32px;
    align-items: center;
  }""",
    r'\.board\s*>\s*\.card\s*{[^}]+}': """.board > .card {
    aspect-ratio: 3 / 4.4;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 24px;
    /* Make it essentially a standalone poster */
  }""",
    r'#previewWrap\s*{[^}]+}': """#previewWrap {
    border-radius: 20px;
    border: none;
    background: transparent;
    padding: 0;
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
    margin: 0;
    width: 100%;
    /* Let the image be giant */
  }""",
    r'#orderPreviewWrap\s*{[^}]+}': """#orderPreviewWrap {
    margin-top: 0;
    margin-bottom: 24px;
    border: none;
    border-radius: 20px;
    background: transparent;
    padding: 0;
    width: 100%;
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: visible;
  }"""
}

# 2. Update the JS `buildLogoSVGBlock` and `cleanAndStyleSVG` into a new `generateModernBagSVG` function
js_new_function = """function generateModernBagSVG(fabricHex, logoColors, bagType, anchoCm, altoCm, showMeasures=true) {
  const isTroquel = /TROQUEL/i.test(String(bagType || ""));
  const w = 240;
  const ratio = (altoCm && anchoCm) ? (Number(altoCm) / Number(anchoCm)) : 1.25;
  const h = w * Math.min(Math.max(ratio, 0.8), 1.8);

  const isWhite = normalizeHex(fabricHex) === "#FFFFFF";
  const strokeColor = isWhite ? "rgba(0,0,0,0.12)" : "rgba(0,0,0,0.15)";
  const shadowColor = isWhite ? "rgba(0,0,0,0.06)" : "rgba(0,0,0,0.15)";
  const highlightColor = "rgba(255,255,255,0.12)";

  // Logo Text Setup
  let logoSVG = "";
  const tx = w / 2;
  const ty = h / 2;
  
  const textWithHalo = (text, yPos, fill, textSize) => `
    <text x="${tx}" y="${yPos}" text-anchor="middle"
      font-size="${textSize}" font-family="Plus Jakarta Sans, sans-serif" font-weight="800"
      fill="${fill}" fill-opacity="1"
      style="letter-spacing:-0.5px"
      stroke="rgba(255,255,255,0.4)" stroke-width="2" paint-order="stroke">
      ${text}
    </text>
  `;

  if (Array.isArray(logoColors) && logoColors.length >= 2) {
    logoSVG += textWithHalo("COLOR 1", ty - 8, logoColors[0] || "#000", 22);
    logoSVG += textWithHalo("COLOR 2", ty + 20, logoColors[1] || "#000", 22);
  } else {
    const c1 = (Array.isArray(logoColors) && logoColors.length) ? logoColors[0] : "#000000";
    logoSVG += textWithHalo("TU LOGO", ty, c1, 26);
  }

  // Handle (Manija vs Troquel)
  let manijaSVG = "";
  if (isTroquel) {
    const holeW = w * 0.28;
    const holeH = holeW * 0.35;
    const holeX = (w - holeW) / 2;
    const holeY = h * 0.08;
    manijaSVG = `<rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH/2}" fill="#ffffff" stroke="${strokeColor}" stroke-width="1.5" />`;
  } else {
    // Manija de tela estilo arco suave
    const archW = w * 0.45;
    const archH = archW * 0.6;
    const archX = (w - archW) / 2;
    const yAnchor = 20; // extends above the bag
    manijaSVG = `
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="12" stroke-linecap="round" />
      <!-- Shadow/inner edge of handle -->
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${strokeColor}" stroke-width="14" stroke-linecap="round" stroke-dasharray="0" opacity="0.3" style="mix-blend-mode: multiply;" />
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="12" stroke-linecap="round" />
    `;
  }

  // Modern Flat Bag Design
  // Viewbox padded to account for handles
  const vbX = -20;
  const vbY = isTroquel ? -20 : -100; // room for top handle
  const vbW = w + 40;
  const vbH = h + (isTroquel ? 40 : 120);

  // Soft reflection/creases to make it look premium
  const creases = `
    <!-- Left seam reflection -->
    <rect x="0" y="0" width="10" height="${h}" fill="${highlightColor}" rx="4"/>
    <!-- Bottom seam shadow -->
    <rect x="0" y="${h - 10}" width="${w}" height="10" fill="${shadowColor}" rx="4"/>
  `;

  return `
    <svg viewBox="${vbX} ${vbY} ${vbW} ${vbH}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 15px 25px rgba(0,0,0,0.08));">
      <defs>
        <linearGradient id="bagGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${fabricHex}" />
          <stop offset="100%" stop-color="${fabricHex}" stop-opacity="0.9" />
        </linearGradient>
      </defs>
      ${manijaSVG}
      <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="url(#bagGrad)" stroke="${strokeColor}" stroke-width="1.5" />
      ${creases}
      ${logoSVG}
    </svg>
  `;
}"""

for pattern, repl in css_replacements.items():
    html = re.sub(pattern, repl, html, flags=re.DOTALL)

# Insert the new JS function before `renderPreviewInstant`
html = re.sub(r'(function renderPreviewInstant\(\)\{)', r'\n' + js_new_function + r'\n\n\1', html, flags=re.DOTALL)

# Now, modify `renderPreviewInstant` to call `generateModernBagSVG` instead of `cleanAndStyleSVG`
# We need to replace `cleanAndStyleSVG(lastRawSVG, fabricHex, logoColors, bagType, ancho, alto, showMeasures)`
# With `generateModernBagSVG(fabricHex, logoColors, bagType, ancho, alto, showMeasures)`
# Also, remove the `if (!lastRawSVG) return;` since we don't need backend SVG anymore.
html = re.sub(r'if\s*\(!lastRawSVG\)\s*return;', '', html)
html = re.sub(r'cleanAndStyleSVG\(lastRawSVG,\s*fabricHex,\s*logoColors,\s*bagType,\s*ancho,\s*alto,\s*showMeasures\)', r'generateModernBagSVG(fabricHex, logoColors, bagType, ancho, alto, showMeasures)', html)

# Extra details for images: 
# #previewGrid .previewSvg svg and #orderPreviewGrid .previewSvg svg sizes.
# Make them immense.
css_image_sizes = {
  r'#previewGrid .previewSvg svg{[^}]+}': """#previewGrid .previewSvg svg{
    width: 100%;
    height: 100%;
    margin-bottom: auto;
    filter: drop-shadow(0 20px 25px rgba(0,0,0,0.1));
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  }""",
  r'#orderPreviewGrid .previewSvg svg{[^}]+}': """#orderPreviewGrid .previewSvg svg{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 15px 20px rgba(0,0,0,0.1));
  }"""
}
for pattern, repl in css_image_sizes.items():
    html = re.sub(pattern, repl, html, flags=re.DOTALL)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

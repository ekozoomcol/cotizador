import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix CSS overflow issues in Wraps
css_fixes = {
    r'#previewWrap\s*{[^}]+overflow:\s*visible;[^}]+}': """#previewWrap {
    border-radius: 20px;
    border: none;
    background: transparent;
    padding: 0;
    flex: 1;
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin: 0;
    width: 100%;
  }""",
    r'#orderPreviewWrap\s*{[^}]+overflow:\s*visible;[^}]+}': """#orderPreviewWrap {
    margin-top: 0;
    margin-bottom: 24px;
    border: none;
    border-radius: 20px;
    background: transparent;
    padding: 0;
    width: 100%;
    flex: 1;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }"""
}
for pattern, repl in css_fixes.items():
    # If the regex doesn't match because of spacing, we'll use a broader one:
    html = re.sub(r'#(previewWrap|orderPreviewWrap)\s*{[^}]+}', 
      lambda m: repl if m.group(1) == 'orderPreviewWrap' else css_fixes[list(css_fixes.keys())[0]], 
      html)

# Also fix the specific replace mapping manually if the regex logic above doesn't work perfectly.
# Let's just replace them directly.
html = re.sub(r'#previewWrap\s*\{[^\}]+\}', """#previewWrap {
    border-radius: 20px;
    border: none;
    background: transparent;
    padding: 0;
    flex: 1 1 auto;
    min-height: 250px;
    max-height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin: 0;
    width: 100%;
  }""", html)

html = re.sub(r'#orderPreviewWrap\s*\{[^\}]+\}', """#orderPreviewWrap {
    margin-top: 0;
    margin-bottom: 24px;
    border: none;
    border-radius: 20px;
    background: transparent;
    padding: 0;
    width: 100%;
    flex: 1 1 auto;
    min-height: 200px;
    max-height: 350px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }""", html)


# 2. Re-write the `generateModernBagSVG` function to have a mask and taller handles
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
  let maskSVG = "";
  if (isTroquel) {
    const holeW = w * 0.28;
    const holeH = holeW * 0.35;
    const holeX = (w - holeW) / 2;
    const holeY = h * 0.08;
    // We create a mask that is entirely white (opaque), except for a black hole (transparent)
    maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
        <rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH/2}" fill="black" />
      </mask>
    `;
    // Add an inner stroke for the hole
    manijaSVG = `<rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH/2}" fill="none" stroke="${strokeColor}" stroke-width="1.5" />`;
  } else {
    // Manija de tela estilo arco suave, MÁS LARGA
    const archW = w * 0.50;
    const archH = archW * 1.5; // MUCHO MÁS LARGA (55 equivalentes)
    const archX = (w - archW) / 2;
    const yAnchor = 25; // extends above the bag
    manijaSVG = `
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="12" stroke-linecap="round" />
      <!-- Shadow/inner edge of handle -->
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${strokeColor}" stroke-width="14" stroke-linecap="round" stroke-dasharray="0" opacity="0.3" style="mix-blend-mode: multiply;" />
      <path d="M ${archX} ${yAnchor} C ${archX} ${-archH}, ${archX + archW} ${-archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="12" stroke-linecap="round" />
    `;
    maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
      </mask>
    `
  }

  // Modern Flat Bag Design
  const vbX = -30;
  const vbY = isTroquel ? -20 : -140; // room for *much taller* top handle
  const vbW = w + 60;
  const vbH = h + (isTroquel ? 40 : 160);

  // Soft reflection/creases to make it look premium
  const creases = `
    <!-- Left seam reflection -->
    <rect x="0" y="0" width="10" height="${h}" fill="${highlightColor}" rx="4" mask="url(#bagMask-${tx})"/>
    <!-- Bottom seam shadow -->
    <rect x="0" y="${h - 10}" width="${w}" height="10" fill="${shadowColor}" rx="4" mask="url(#bagMask-${tx})"/>
  `;

  return `
    <svg viewBox="${vbX} ${vbY} ${vbW} ${vbH}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 15px 25px rgba(0,0,0,0.08)); max-height: 100%;">
      <defs>
        ${maskSVG}
        <linearGradient id="bagGrad-${tx}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${fabricHex}" />
          <stop offset="100%" stop-color="${fabricHex}" stop-opacity="0.9" />
        </linearGradient>
      </defs>
      ${!isTroquel ? manijaSVG : ''}
      <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="url(#bagGrad-${tx})" mask="url(#bagMask-${tx})" stroke="${strokeColor}" stroke-width="1.5" />
      ${isTroquel ? manijaSVG : ''}
      ${creases}
      ${logoSVG}
    </svg>
  `;
}"""

# Replace the whole generateModernBagSVG function
html = re.sub(r'function generateModernBagSVG\(.*?\)\s*\{.*?</svg>\s*`;\s*\}', js_new_function, html, flags=re.DOTALL)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

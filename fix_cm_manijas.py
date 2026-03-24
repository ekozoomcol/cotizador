import re

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update the label and default value of the new input field
html = re.sub(
    r'<label>Largo arco visual</label>\s*<input id="largo_arco_visual" type="number" value="[^"]+" min="10" max="150">',
    '<label>Largo Manija</label><input id="largo_arco_visual" type="number" value="46" min="10" max="300">',
    html
)

# 2. Update `generateModernBagSVG` logic for precise parametric handles
def handle_replacement(m):
    return """
    // Manija de tela parametrizada por dimensiones reales (cm)
    const cmToSvg = w / (Number(anchoCm) || 30);
    const gruesoCm = 2.5;
    const separacionInternaCm = 7.5;
    // La distancia entre centros de las manijas es la separacion interna + el grosor de 1 pata (2 medias patas)
    const archW = (separacionInternaCm + gruesoCm) * cmToSvg; 
    const archX = (w - archW) / 2;
    
    // Largo de manija total en cm, lo dividimos por 2 para el alto visual aproximado
    const visualH = (Number(archVisualCm) / 2) * cmToSvg;
    const archH = visualH * 1.33; // factor de control para bezier cúbica
    
    const strokeWidthSVG = gruesoCm * cmToSvg;
    const yAnchor = 25; // extends above the bag
    
    // Calcular altura maxima de la manija para ajustar el viewBox
    const peakY = yAnchor - visualH;
"""

# Let's replace the block in generateModernBagSVG where `isTroquel == false`
# We need to replace these specific lines:
# const archW = w * 0.50;
# const archH = archW * (Number(archVisualCm) / 36.666);
# const archX = (w - archW) / 2;
# const yAnchor = 25; // extends above the bag

# And replace the SVG string parts relying on stroke-width="12" inside manijaSVG

# It's cleaner to replace the entire `if (isTroquel) { ... } else { ... }` up to `// Modern Flat Bag Design`
pattern = r'(if\s*\(\s*isTroquel\s*\)\s*\{)(.*?)(// Modern Flat Bag Design\s*)const vbX = -30;\s*const vbY = isTroquel \? -20 :[^;]+;\s*const vbW = w \+ 60;\s*const vbH = h \+ [^;]+;'
# Wait, my regex might fail. Let's write a targeted function to apply this properly.

def replace_bag_logic():
    # Because making a python script with regex is dangerous for large javascript logic blocks, 
    pass

import sys

target = """  if (isTroquel) {
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
    const archH = archW * (Number(archVisualCm) / 36.666); // MUCHO MÁS LARGA (55 equivalentes)
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
  const vbH = h + (isTroquel ? 40 : 160);"""

replacement = """  let peakY = 0;
  if (isTroquel) {
    const holeW = w * 0.28;
    const holeH = holeW * 0.35;
    const holeX = (w - holeW) / 2;
    const holeY = h * 0.08;
    maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
        <rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH/2}" fill="black" />
      </mask>
    `;
    manijaSVG = `<rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH/2}" fill="none" stroke="${strokeColor}" stroke-width="1.5" />`;
    peakY = 0;
  } else {
    // Manija calculada por proporciones exactas en cm
    const cmToSvg = w / (Number(anchoCm) || 30);
    const gruesoCm = 2.5;
    const separacionInternaCm = 7.5;
    const archW = (separacionInternaCm + gruesoCm) * cmToSvg; 
    const archX = (w - archW) / 2;
    
    const visualH = (Number(archVisualCm) / 2) * cmToSvg;
    const archH = visualH * 1.33; 
    const strokeWidthSVG = gruesoCm * cmToSvg;
    const yAnchor = 25; 
    
    peakY = yAnchor - visualH;
    
    manijaSVG = `
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="${strokeWidthSVG}" stroke-linecap="round" />
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${strokeColor}" stroke-width="${strokeWidthSVG + 3}" stroke-linecap="round" stroke-dasharray="0" opacity="0.3" style="mix-blend-mode: multiply;" />
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${fabricHex}" stroke-width="${strokeWidthSVG}" stroke-linecap="round" />
    `;
    maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
      </mask>
    `
  }

  // Modern Flat Bag Design - Responsive ViewBox
  const vbX = -30;
  const vbY = isTroquel ? -20 : (peakY - 20); 
  const vbW = w + 60;
  // Alto del viewbox es el fondo de la bolsa (h + pad) menos el inicio (vbY)
  const vbH = h + 40 - vbY;"""


import textwrap
if target.strip() in html.strip() or True:
    # Use re to just match and replace it loosely in case of spacing
    p = re.compile(r'if \(\s*isTroquel\s*\)\s*\{.*?const vbH = h \+ \(isTroquel \? 40 : 160\);', re.DOTALL)
    html = p.sub(replacement, html)
else:
    print("Warning: could not match target.")

# 3. Re-inject default parameter 46 in makeItem instead of 55
html = re.sub(
    r'Number\(document\.getElementById\("largo_arco_visual"\)\.value\) : 55',
    'Number(document.getElementById("largo_arco_visual").value) : 46',
    html
)
html = html.replace('function generateModernBagSVG(fabricHex, logoColors, bagType, anchoCm, altoCm, showMeasures=true, archVisualCm=55)', 
                    'function generateModernBagSVG(fabricHex, logoColors, bagType, anchoCm, altoCm, showMeasures=true, archVisualCm=46)')

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)


import os
import re

filepath = r"c:\Users\ekozo\OneDrive\Desktop\cotizador\static\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new highly realistic version of generateModernBagSVG
new_func = """function generateModernBagSVG(fabricHex, manualLogoList = [], bagType, anchoCm, altoCm, showMeasures = true, handleArcoLogico = 46, handleHex = null) {
      const isTroquel = (bagType === "PLANA_TROQUEL");
      const realHandleHex = handleHex || fabricHex;
      const w = 240;
      const ratio = (altoCm && anchoCm) ? (Number(altoCm) / Number(anchoCm)) : 1.25;
      const h = w * Math.min(Math.max(ratio, 0.8), 1.8);

      const isWhite = normalizeHex(fabricHex) === "#FFFFFF";
      const strokeColor = isWhite ? "rgba(0,0,0,0.12)" : "rgba(0,0,0,0.15)";
      const shadowColor = isWhite ? "rgba(0,0,0,0.06)" : "rgba(0,0,0,0.15)";
      const highlightColor = "rgba(255,255,255,0.12)";
      
      const tx = w / 2;
      const ty = h / 2;
      let logosGroup = "";
      
      const cmToSvg = w / (Number(anchoCm) || 30);
      
      const isSide2 = manualLogoList.length > 0 && manualLogoList[0] && !manualLogoList[0].showMeasures;

      const hasSeri = manualLogoList.some(l => l.type === 'serigrafia');
      const dtfLogo = manualLogoList.find(l => l.type === 'dtf');
      const hasDtf = !!dtfLogo;
      const seriScale = (hasSeri && hasDtf) ? 0.75 : 1.3;
      const gap = 30;

      const dtfW_cm = dtfLogo ? Math.min(dtfLogo.width || 15, anchoCm * 0.85) : 0;
      const dtfH_cm = dtfLogo ? Math.min(dtfLogo.height || 15, altoCm * 0.6) : 0;
      const dtfW_svg = dtfW_cm * cmToSvg;
      const dtfH_svg = dtfH_cm * cmToSvg;
      
      const seriH_svg = hasSeri ? (80 * seriScale) : 0;
      let totalH = seriH_svg + (hasSeri && hasDtf ? gap : 0) + dtfH_svg;
      
      let safetyScale = 1.0;
      const maxHAllowed = h * 0.75;
      if (totalH > maxHAllowed) {
        safetyScale = maxHAllowed / totalH;
        totalH = maxHAllowed;
      }

      const startY = ty - (totalH / 2);

      if (hasSeri) {
        const seriColors = manualLogoList.filter(l => l.type === 'serigrafia').map(l => l.color);
        const c1 = seriColors[0] || "#0833a2";
        const c2 = seriColors.length > 1 ? seriColors[1] : c1;
        const c3 = seriColors.length > 2 ? seriColors[2] : c1;
        const c4 = seriColors.length > 3 ? seriColors[3] : c2;

        const seriY = startY + (seriH_svg * safetyScale / 2);
        
        logosGroup += `
          <g transform="translate(0, ${seriY - ty}) scale(${seriScale * safetyScale})" transform-origin="${tx} ${ty}">
            <path d="M ${tx} ${ty - 40} C ${tx + 35} ${ty - 40}, ${tx + 35} ${ty - 5}, ${tx} ${ty - 5} C ${tx - 35} ${ty - 5}, ${tx - 35} ${ty - 40}, ${tx} ${ty - 40} Z" fill="${c1}"/>
            <circle cx="${tx}" cy="${ty - 22.5}" r="7" fill="${c2}" />
            <text x="${tx}" y="${ty + 18}" text-anchor="middle" font-size="16" font-family="Plus Jakarta Sans, sans-serif" font-weight="900" fill="${c3}" letter-spacing="0.5px">TU LOGO</text>
            <text x="${tx}" y="${ty + 36}" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" font-weight="700" fill="${c4}" opacity="0.8">AQUÍ</text>
          </g>
        `;
      }

      if (hasDtf) {
        const dtfY = startY + (hasSeri ? (seriH_svg + gap) * safetyScale : 0) + (dtfH_svg * safetyScale / 2);
        const fontSize1 = Math.min(dtfW_svg * 0.18, 14);
        const fontSize2 = Math.min(dtfW_svg * 0.12, 10);
        const textY1 = ty + (dtfH_svg * 0.05);
        const textY2 = ty + (dtfH_svg * 0.25);
        
        logosGroup += `
          <g transform="translate(0, ${dtfY - ty}) scale(${safetyScale})" transform-origin="${tx} ${ty}">
            <rect x="${tx - dtfW_svg / 2}" y="${ty - dtfH_svg / 2}" width="${dtfW_svg}" height="${dtfH_svg}" rx="8" fill="url(#dtfGrad)" filter="drop-shadow(0 4px 5px rgba(0,0,0,0.25))" />
            <defs>
              <linearGradient id="dtfGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ff0000" /><stop offset="50%" stop-color="#00ff00" /><stop offset="100%" stop-color="#0000ff" />
              </linearGradient>
            </defs>
            <text x="${tx}" y="${textY1}" text-anchor="middle" font-size="${fontSize1}" font-weight="900" fill="white" font-family="Outfit">FULL COLOR</text>
            <text x="${tx}" y="${textY2}" text-anchor="middle" font-size="${fontSize2}" font-weight="600" fill="white" opacity="0.8">DTF ${dtfW_cm}x${dtfH_cm}cm</text>
          </g>
        `;
      }
      const gruesoCm = 2.5;
      const separacionInternaCm = 8;
      const archW = (separacionInternaCm + gruesoCm) * cmToSvg;
      const archX = (w - archW) / 2;

      const archVisualCm = manualLogoList.some(l => l.showMeasures) ? (document.getElementById("largo_arco_visual") ? Number(document.getElementById("largo_arco_visual").value) : 46) : 46;
      const visualH = (Number(archVisualCm) / 2) * cmToSvg;
      const archH = visualH * 1.33;
      const strokeWidthSVG = gruesoCm * cmToSvg;
      const yAnchor = 25;

      const peakY = yAnchor - visualH;

      let manijaSVG = "";
      let handleStitchesSVG = "";
      let maskSVG = "";
      
      const texturePatternID = \`cambrelNoise-\${Math.round(tx)}\`;
      
      // ULTRA REALISTIC CAMBREL 70G TEXTURE (Organic Fiber Network)
      const texturePattern = `
        <pattern id="\${texturePatternID}" width="16" height="16" patternUnits="userSpaceOnUse">
          <path d="M1,1 L5,9 M11,3 L4,10 M2,11 L10,6 M7,1 L9,8" stroke="rgba(0,0,0,0.06)" stroke-width="0.7" fill="none" opacity="0.85"/>
          <path d="M0,6 L12,4 M6,0 L8,12 M3,12 L12,2" stroke="rgba(255,255,255,0.18)" stroke-width="0.9" fill="none" opacity="0.7"/>
          <path d="M14,14 L10,6 M16,10 L8,16" stroke="rgba(0,0,0,0.08)" stroke-width="0.6" fill="none"/>
          <ellipse cx="4" cy="4" rx="1.5" ry="1.0" fill="rgba(0,0,0,0.04)" />
          <ellipse cx="12" cy="12" rx="1.2" ry="1.6" fill="rgba(0,0,0,0.05)" />
          <ellipse cx="10" cy="4" rx="1.6" ry="1.2" fill="rgba(255,255,255,0.08)" />
          <ellipse cx="4" cy="12" rx="1.0" ry="1.5" fill="rgba(255,255,255,0.06)" />
        </pattern>
      `;
      
      if (isTroquel) {
        const holeW = 7.5 * cmToSvg;
        const holeH = 2.4 * cmToSvg;
        const holeX = (w - holeW) / 2;
        const holeY = 1.7 * cmToSvg;
        maskSVG = `
      <mask id="bagMask-\${tx}">
        <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="white" />
        <rect x="\${holeX}" y="\${holeY}" width="\${holeW}" height="\${holeH}" rx="\${holeH / 2}" fill="black" />
      </mask>
      <!-- Troquel Hole Inner Shadow -->
      <mask id="troquelHole-\${tx}">
        <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="black" />
        <rect x="\${holeX}" y="\${holeY}" width="\${holeW}" height="\${holeH}" rx="\${holeH / 2}" fill="white" />
      </mask>
      <rect x="0" y="0" width="\${w}" height="\${h}" fill="rgba(0,0,0,0.4)" mask="url(#troquelHole-\${tx})" filter="blur(3px)" transform="translate(0, 2)" style="mix-blend-mode: multiply;" />
    `;
        manijaSVG = `<rect x="\${holeX}" y="\${holeY}" width="\${holeW}" height="\${holeH}" rx="\${holeH / 2}" fill="none" stroke="\${strokeColor}" stroke-width="1.5" />`;
      } else {
        // MANIJA 3D COMPUESTA
        manijaSVG = `
      <!-- 1. Drop shadow base difuminada (efecto volumen a la bolsa) -->
      <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="rgba(0,0,0,0.18)" stroke-width="\${strokeWidthSVG}" stroke-linecap="round" filter="blur(4px)" transform="translate(0, 5) scale(0.98)" style="mix-blend-mode: multiply; transform-origin: \${w/2} \${yAnchor - archH};"/>
      <!-- 2. Sombra de contacto profunda -->
      <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="rgba(0,0,0,0.22)" stroke-width="\${strokeWidthSVG}" stroke-linecap="round" filter="blur(1.5px)" transform="translate(0, 1) scale(0.99)" style="transform-origin: \${w/2} \${yAnchor - archH};"/>
      
      <g>
        <!-- Cuerpo Manija principal -->
        <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="\${realHandleHex}" stroke-width="\${strokeWidthSVG}" stroke-linecap="round" />
        <!-- Cambrel Texture on Handle -->
        <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="url(#\${texturePatternID})" stroke-width="\${strokeWidthSVG}" stroke-linecap="round" style="mix-blend-mode: multiply; opacity:0.9" />
        <!-- 3D Interior Shadow (Bottom curve) -->
        <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="\${strokeWidthSVG}" stroke-linecap="round" style="mix-blend-mode: multiply;" transform="translate(0, -1)" />
        <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="\${realHandleHex}" stroke-width="\${strokeWidthSVG-1.5}" stroke-linecap="round" transform="translate(0, -1.8)" />
        <!-- 3D Outer Light (Top Curve) -->
        <path d="M \${archX} \${yAnchor} C \${archX} \${yAnchor - archH}, \${archX + archW} \${yAnchor - archH}, \${archX + archW} \${yAnchor}" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="\${strokeWidthSVG - 3.5}" stroke-linecap="round" filter="blur(0.5px)" />
      </g>
    `;
    
        const stitchW = 2.2 * cmToSvg;
        const stitchH = 2.2 * cmToSvg;
        const scX = stitchW / 71.93;
        const scY = stitchH / 76.03;
        const leftX = archX - stitchW / 2;
        const rightX = archX + archW - stitchW / 2;
        const stitchY = (3.0 * cmToSvg) - (stitchH / 2);

        handleStitchesSVG = `
          <!-- Left Handle Stitch (shadow + stitch) -->
          <g transform="translate(\${leftX}, \${stitchY + 1}) scale(\${scX}, \${scY})" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.4)" stroke-width="1.2" stroke-linejoin="round" opacity="0.8">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/>
            <rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/>
            <rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/>
            <rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/>
            <rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/>
            <rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/>
            <rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/>
            <rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/>
            <rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/>
            <rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/>
            <rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/>
            <rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/>
            <rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/>
            <rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/>
            <rect x="40.92" y="60.69" width="2.83" height="8.5"/>
            <rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/>
            <rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/>
            <rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/>
            <rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/>
            <rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/>
            <rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/>
            <rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/>
            <rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/>
            <rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/>
            <rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/>
            <rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
          <g transform="translate(\${leftX}, \${stitchY}) scale(\${scX}, \${scY})" fill="\${shadowColor}" stroke="\${shadowColor}" stroke-width="0.8" stroke-linejoin="round" opacity="0.8">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/>
            <rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/>
            <rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/>
            <rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/>
            <rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/>
            <rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/>
            <rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/>
            <rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/>
            <rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/>
            <rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/>
            <rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/>
            <rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/>
            <rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/>
            <rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/>
            <rect x="40.92" y="60.69" width="2.83" height="8.5"/>
            <rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/>
            <rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/>
            <rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/>
            <rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/>
            <rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/>
            <rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/>
            <rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/>
            <rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/>
            <rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/>
            <rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/>
            <rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
          
          <!-- Right Handle Stitch (shadow + stitch) -->
          <g transform="translate(\${rightX}, \${stitchY + 1}) scale(\${scX}, \${scY})" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.4)" stroke-width="1.2" stroke-linejoin="round" opacity="0.8">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/>
            <rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/>
            <rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/>
            <rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/>
            <rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/>
            <rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/>
            <rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/>
            <rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/>
            <rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/>
            <rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/>
            <rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/>
            <rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/>
            <rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/>
            <rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/>
            <rect x="40.92" y="60.69" width="2.83" height="8.5"/>
            <rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/>
            <rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/>
            <rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/>
            <rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/>
            <rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/>
            <rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/>
            <rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/>
            <rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/>
            <rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/>
            <rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/>
            <rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
          <g transform="translate(\${rightX}, \${stitchY}) scale(\${scX}, \${scY})" fill="\${shadowColor}" stroke="\${shadowColor}" stroke-width="0.8" stroke-linejoin="round" opacity="0.8">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/>
            <rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/>
            <rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/>
            <rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/>
            <rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/>
            <rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/>
            <rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/>
            <rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/>
            <rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/>
            <rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/>
            <rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/>
            <rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/>
            <rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/>
            <rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/>
            <rect x="40.92" y="60.69" width="2.83" height="8.5"/>
            <rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/>
            <rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/>
            <rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/>
            <rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/>
            <rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/>
            <rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/>
            <rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/>
            <rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/>
            <rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/>
            <rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/>
            <rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
        `;
        maskSVG = `
      <mask id="bagMask-\${tx}">
        <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="white" />
      </mask>
    `;
      }

      const vbX = -30;
      const vbY = peakY - 20; 
      const vbW = w + 60;
      const vbH = h + 40 - vbY;

      // TERMOSELLADOS (EMBOSSED EFFECT 3D: Dark groove + Bright highlight)
      const topSealStyleH = `stroke="rgba(0,0,0,0.22)" stroke-width="2.5" stroke-dasharray="2, 3" stroke-linecap="butt"`;
      const topSealStyleL = `stroke="rgba(255,255,255,0.4)" stroke-width="2.5" stroke-dasharray="2, 3" stroke-linecap="butt" transform="translate(0, 1.5)"`;
      const sideSealStyleH = `stroke="rgba(0,0,0,0.22)" stroke-width="1.2" stroke-dasharray="4, 1.5" stroke-linecap="butt"`;
      const sideSealStyleL = `stroke="rgba(255,255,255,0.4)" stroke-width="1.2" stroke-dasharray="4, 1.5" stroke-linecap="butt" transform="translate(1, 0)"`;
      
      const _cmToSvg = w / (Number(anchoCm) || 30);
      const top1 = 1.5 * _cmToSvg;
      const top2 = top1 + (2.5 * _cmToSvg);

      const sealedEdges = `
        <g mask="url(#bagMask-\${tx})">
          <!-- Left Sealing -->
          <line x1="3" y1="0" x2="3" y2="\${h}" \${sideSealStyleL} />
          <line x1="3" y1="0" x2="3" y2="\${h}" \${sideSealStyleH} />
          <line x1="5.5" y1="0" x2="5.5" y2="\${h}" \${sideSealStyleL} stroke-dashoffset="-2.75" />
          <line x1="5.5" y1="0" x2="5.5" y2="\${h}" \${sideSealStyleH} stroke-dashoffset="-2.75" />
          
          <!-- Right Sealing -->
          <line x1="\${w - 3}" y1="0" x2="\${w - 3}" y2="\${h}" \${sideSealStyleL} />
          <line x1="\${w - 3}" y1="0" x2="\${w - 3}" y2="\${h}" \${sideSealStyleH} />
          <line x1="\${w - 5.5}" y1="0" x2="\${w - 5.5}" y2="\${h}" \${sideSealStyleL} stroke-dashoffset="-2.75" />
          <line x1="\${w - 5.5}" y1="0" x2="\${w - 5.5}" y2="\${h}" \${sideSealStyleH} stroke-dashoffset="-2.75" />
          
          <!-- Top Sealing -->
          <line x1="0" y1="\${top1}" x2="\${w}" y2="\${top1}" \${topSealStyleL} />
          <line x1="0" y1="\${top1}" x2="\${w}" y2="\${top1}" \${topSealStyleH} />
          <line x1="0" y1="\${top2}" x2="\${w}" y2="\${top2}" \${topSealStyleL} />
          <line x1="0" y1="\${top2}" x2="\${w}" y2="\${top2}" \${topSealStyleH} />
        </g>
      `;

      // HYPER REALISTIC VOLUME, CREASES & PILLOWING
      const bagRadiusH = h * 0.45;
      const bagRadiusW = w * 0.45;
      const creases = `
        <defs>
          <radialGradient id="volumeMask-\${tx}" cx="50%" cy="50%" r="50%">
            <stop offset="35%" stop-color="rgba(0,0,0,0)" />
            <stop offset="90%" stop-color="rgba(0,0,0,0.18)" />
            <stop offset="100%" stop-color="rgba(0,0,0,0.5)" />
          </radialGradient>
          <radialGradient id="highlightMask-\${tx}" cx="45%" cy="30%" r="55%">
            <stop offset="0%" stop-color="rgba(255,255,255,0.25)" />
            <stop offset="100%" stop-color="rgba(255,255,255,0)" />
          </radialGradient>
        </defs>
        
        <!-- Center Pillowing / Bag curve volume -->
        <rect x="0" y="0" width="\${w}" height="\${h}" fill="url(#volumeMask-\${tx})" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;" />
        <rect x="0" y="0" width="\${w}" height="\${h}" fill="url(#highlightMask-\${tx})" mask="url(#bagMask-\${tx})" style="mix-blend-mode: screen;" />
        
        <!-- Seam shadows/reflections to give it physical edges -->
        <rect x="0" y="0" width="10" height="\${h}" fill="rgba(255,255,255,0.3)" filter="blur(2px)" mask="url(#bagMask-\${tx})"/>
        <rect x="\${w-9}" y="0" width="9" height="\${h}" fill="rgba(0,0,0,0.25)" filter="blur(1.5px)" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;" />
        <!-- Base Gusset/Fold volume -->
        <rect x="0" y="\${h - 22}" width="\${w}" height="22" fill="rgba(0,0,0,0.2)" filter="blur(4px)" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;"/>
        <line x1="0" y1="\${h - 18}" x2="\${w}" y2="\${h - 18}" stroke="rgba(255,255,255,0.15)" stroke-width="1.5" mask="url(#bagMask-\${tx})" />
        
        <!-- Natural organic wrinkles & tension lines (blur makes them soft) -->
        <path d="M \${w * 0.22} 0 Q \${w * 0.28} \${h * 0.12} \${w * 0.15} \${h * 0.28}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="3" filter="blur(2px)" mask="url(#bagMask-\${tx})"/>
        <path d="M \${w * 0.22} 0 Q \${w * 0.25} \${h * 0.14} \${w * 0.12} \${h * 0.28}" fill="none" stroke="rgba(0,0,0,0.15)" stroke-width="4" filter="blur(3px)" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;"/>
        
        <path d="M \${w * 0.78} 0 Q \${w * 0.72} \${h * 0.12} \${w * 0.85} \${h * 0.28}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="3" filter="blur(2px)" mask="url(#bagMask-\${tx})"/>
        <path d="M \${w * 0.78} 0 Q \${w * 0.75} \${h * 0.14} \${w * 0.88} \${h * 0.28}" fill="none" stroke="rgba(0,0,0,0.15)" stroke-width="4" filter="blur(3px)" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;"/>
        
        <path d="M \${w * 0.3} \${h} Q \${w * 0.45} \${h * 0.85} \${w * 0.4} \${h * 0.7}" fill="none" stroke="rgba(0,0,0,0.08)" stroke-width="6" filter="blur(4px)" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;"/>
      `;

      return `
    <svg viewBox="\${vbX} \${vbY} \${vbW} \${vbH}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 18px 28px rgba(0,0,0,0.16)) drop-shadow(0 4px 8px rgba(0,0,0,0.06)); max-height: 100%;">
      <defs>
        \${maskSVG}
        \${texturePattern}
        <linearGradient id="bagGrad-\${tx}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="\${fabricHex}" />
          <stop offset="100%" stop-color="\${fabricHex}" stop-opacity="0.94" />
        </linearGradient>
      </defs>

      \${!isTroquel ? manijaSVG : ''}

      <!-- MAIN FABRIC BODY -->
      <g>
        <!-- Base body shape -->
        <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="url(#bagGrad-\${tx})" mask="url(#bagMask-\${tx})" />
        
        <!-- Pores & Non-Woven Texture Overlay -->
        <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="url(#\${texturePatternID})" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply; opacity: 0.8;" />
      </g>
      
      <!-- THERMOSELLADO AND WRINKLES / VOLUME -->
      \${sealedEdges}
      \${!isTroquel ? handleStitchesSVG : ''}
      \${creases}

      <!-- LOGOS -->
      <g style="opacity: 0.95; filter: contrast(1.08) brightness(1.02) drop-shadow(0 1px 1px rgba(0,0,0,0.1));">
        \${logosGroup}
      </g>

      <!-- Gloss & Edge Highlights on entire object -->
      <rect x="0.5" y="0.5" width="\${w-1}" height="\${h-1}" rx="5.5" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" mask="url(#bagMask-\${tx})" style="mix-blend-mode: screen;" opacity="0.6" />
      <rect x="0" y="0" width="\${w}" height="\${h}" rx="6" fill="none" stroke="rgba(0,0,0,0.2)" stroke-width="1.5" mask="url(#bagMask-\${tx})" style="mix-blend-mode: multiply;" />
    </svg>
  `;
    }"""

pattern = re.compile(r"function generateModernBagSVG\(.*?return `\n    <svg viewBox=\".*?</svg>\n  `;\n    \}", re.DOTALL)
match = pattern.search(content)

if match:
    new_content = content[:match.start()] + new_func + content[match.end():]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced the function. Length of new string inside file:", len(new_func))
else:
    print("Function not found, try tweaking the Regex!")

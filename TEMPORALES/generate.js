function generateModernBagSVG(fabricHex, manualLogoList = [], bagType, anchoCm, altoCm, showMeasures = true, handleArcoLogico = 46, handleHex = null) {
      const isTroquel = (bagType === "PLANA_TROQUEL");
      const realHandleHex = handleHex || fabricHex;
      const w = 240;
      const ratio = (altoCm && anchoCm) ? (Number(altoCm) / Number(anchoCm)) : 1.25;
      const h = w * Math.min(Math.max(ratio, 0.8), 1.8);

      const isWhite = normalizeHex(fabricHex) === "#FFFFFF";
      const strokeColor = isWhite ? "rgba(0,0,0,0.12)" : "rgba(0,0,0,0.15)";
      const shadowColor = isWhite ? "rgba(0,0,0,0.06)" : "rgba(0,0,0,0.15)";
      
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
      let troquelInsideSVG = "";
      
      if (isTroquel) {
        const holeW = 7.5 * cmToSvg;
        const holeH = 2.4 * cmToSvg;
        const holeX = (w - holeW) / 2;
        const holeY = 1.7 * cmToSvg;
        
        maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
        <rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH / 2}" fill="black" />
      </mask>
    `;
        // Draw the inside of the hole (back fabric showing through with shadow)
        troquelInsideSVG = `
      <rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH / 2}" fill="${fabricHex}" style="filter: brightness(0.7) drop-shadow(0 3px 2px rgba(0,0,0,0.5))" />
      <rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH / 2}" fill="url(#cambrelNoise-${Math.round(tx)})" style="mix-blend-mode: multiply;" />
    `;
        manijaSVG = `<rect x="${holeX}" y="${holeY}" width="${holeW}" height="${holeH}" rx="${holeH / 2}" fill="none" stroke="${strokeColor}" stroke-width="1.5" />`;
      } else {
        manijaSVG = `
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="${realHandleHex}" stroke-width="${strokeWidthSVG}" stroke-linecap="round" />
      <!-- Textura Cambrel para la Manija -->
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="url(#cambrelNoise-${Math.round(tx)})" stroke-width="${strokeWidthSVG}" stroke-linecap="round" style="mix-blend-mode: multiply; opacity: 0.8" />
      <!-- Subtle edge highlight on handle -->
      <path d="M ${archX} ${yAnchor} C ${archX} ${yAnchor - archH}, ${archX + archW} ${yAnchor - archH}, ${archX + archW} ${yAnchor}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="${strokeWidthSVG * 0.9}" stroke-linecap="round" filter="blur(0.5px)" transform="translate(0, -1)" />
    `;
    
        const stitchW = 2.2 * cmToSvg;
        const stitchH = 2.2 * cmToSvg;
        const scX = stitchW / 71.93;
        const scY = stitchH / 76.03;
        const leftX = archX - stitchW / 2;
        const rightX = archX + archW - stitchW / 2;
        const stitchY = (3.0 * cmToSvg) - (stitchH / 2);

        // Termofijado Sónico pattern base (clean geometric weave)
        handleStitchesSVG = `
          <!-- Sombra de la manija proyectada sutilmente en la bolsa -->
          <rect x="${leftX}" y="${yAnchor}" width="${stitchW}" height="${stitchH*1.5}" fill="rgba(0,0,0,0.15)" filter="blur(2px)" style="mix-blend-mode: multiply;" rx="2" />
          <rect x="${rightX}" y="${yAnchor}" width="${stitchW}" height="${stitchH*1.5}" fill="rgba(0,0,0,0.15)" filter="blur(2px)" style="mix-blend-mode: multiply;" rx="2" />

          <!-- Stitch Left -->
          <g transform="translate(${leftX}, ${stitchY}) scale(${scX}, ${scY})" fill="${shadowColor}" stroke="${shadowColor}" stroke-width="0.6" stroke-linejoin="round" opacity="0.6">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/><rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/><rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/><rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/><rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/><rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/><rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/><rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/><rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/><rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/><rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/><rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/><rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/><rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/><rect x="40.92" y="60.69" width="2.83" height="8.5"/><rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/><rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/><rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/><rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/><rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/><rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/><rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/><rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/><rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/><rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/><rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
          <!-- Stitch Right -->
          <g transform="translate(${rightX}, ${stitchY}) scale(${scX}, ${scY})" fill="${shadowColor}" stroke="${shadowColor}" stroke-width="0.6" stroke-linejoin="round" opacity="0.6">
            <rect x="40.92" y="6.83" width="2.83" height="8.5"/><rect x="58.64" y="20.97" width="2.83" height="8.5" transform="translate(85.27 -34.84) rotate(90)"/><rect x="59.67" y="7.54" width="2.27" height="7.09" transform="translate(25.65 -39.75) rotate(45)"/><rect x="50.67" y="16.54" width="2.27" height="7.09" transform="translate(29.38 -30.75) rotate(45)"/><rect x="41.67" y="25.54" width="2.27" height="7.09" transform="translate(33.1 -21.75) rotate(45)"/><rect x="58.64" y="33.76" width="2.83" height="8.5" transform="translate(98.07 -22.04) rotate(90)"/><rect x="58.64" y="27.36" width="2.83" height="8.5" transform="translate(91.67 -28.44) rotate(90)"/><rect x="28.17" y="6.83" width="2.83" height="8.5" transform="translate(59.17 22.17) rotate(180)"/><rect x="10.45" y="20.97" width="2.83" height="8.5" transform="translate(37.09 13.35) rotate(90)"/><rect x="9.99" y="7.54" width="2.27" height="7.09" transform="translate(26.83 11.06) rotate(135)"/><rect x="18.99" y="16.54" width="2.27" height="7.09" transform="translate(48.56 20.06) rotate(135)"/><rect x="27.99" y="25.54" width="2.27" height="7.09" transform="translate(70.27 29.06) rotate(135)"/><rect x="10.45" y="33.76" width="2.83" height="8.5" transform="translate(49.88 26.15) rotate(90)"/><rect x="10.45" y="27.36" width="2.83" height="8.5" transform="translate(43.49 19.75) rotate(90)"/><rect x="40.92" y="60.69" width="2.83" height="8.5"/><rect x="58.64" y="46.56" width="2.83" height="8.5" transform="translate(9.24 110.87) rotate(-90)"/><rect x="59.67" y="61.4" width="2.27" height="7.09" transform="translate(-28.11 62.02) rotate(-45)"/><rect x="50.67" y="52.4" width="2.27" height="7.09" transform="translate(-24.39 53.02) rotate(-45)"/><rect x="41.67" y="43.41" width="2.27" height="7.09" transform="translate(-20.66 44.02) rotate(-45)"/><rect x="58.64" y="40.16" width="2.83" height="8.5" transform="translate(15.64 104.47) rotate(-90)"/><rect x="28.17" y="60.69" width="2.83" height="8.5" transform="translate(59.17 129.89) rotate(180)"/><rect x="10.45" y="46.56" width="2.83" height="8.5" transform="translate(-38.95 62.68) rotate(-90)"/><rect x="9.99" y="61.4" width="2.27" height="7.09" transform="translate(-26.93 118.73) rotate(-135)"/><rect x="18.99" y="52.4" width="2.27" height="7.09" transform="translate(-5.2 109.73) rotate(-135)"/><rect x="27.99" y="43.41" width="2.27" height="7.09" transform="translate(16.51 100.74) rotate(-135)"/><rect x="10.45" y="40.16" width="2.83" height="8.5" transform="translate(-32.55 56.28) rotate(-90)"/>
          </g>
        `;
        maskSVG = `
      <mask id="bagMask-${tx}">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="white" />
      </mask>
    `;
      }

      const vbX = -30;
      const vbY = peakY - 20;
      const vbW = w + 60;
      const vbH = h + 40 - vbY;

      // Pure SVG Geometric Cambrel Texture (Semillitas / Honeycomb)
      const texturePattern = `
        <pattern id="cambrelNoise-${Math.round(tx)}" width="3.8" height="3.4" patternUnits="userSpaceOnUse">
          <ellipse cx="0.95" cy="0.85" rx="0.45" ry="0.35" fill="rgba(0,0,0,0.15)" />
          <ellipse cx="2.85" cy="2.55" rx="0.45" ry="0.35" fill="rgba(0,0,0,0.15)" />
        </pattern>
      `;

      // Termosellado Embossing (shadow + specular)
      const topSealStyle = `stroke="${shadowColor}" stroke-width="3" stroke-dasharray="1, 2" stroke-linecap="butt"`;
      const sideSealStyle = `stroke="${shadowColor}" stroke-width="1.5" stroke-dasharray="4, 1.5" stroke-linecap="butt"`;
      const topSealStyleLight = `stroke="rgba(255,255,255,0.4)" stroke-width="3" stroke-dasharray="1, 2" stroke-linecap="butt" transform="translate(0, 1)"`;
      const sideSealStyleLight = `stroke="rgba(255,255,255,0.4)" stroke-width="1.5" stroke-dasharray="4, 1.5" stroke-linecap="butt" transform="translate(1, 0)"`;
      
      const _cmToSvg = w / (Number(anchoCm) || 30);
      const top1 = 1.5 * _cmToSvg;
      const top2 = top1 + (2.5 * _cmToSvg);

      const sealedEdges = `
        <g mask="url(#bagMask-${tx})">
          <!-- Left Sealing Shadows -->
          <line x1="2.5" y1="0" x2="2.5" y2="${h}" ${sideSealStyle} />
          <line x1="5.0" y1="0" x2="5.0" y2="${h}" ${sideSealStyle} stroke-dashoffset="-2.75" />
          <!-- Left Sealing Lights (Bajo relieve) -->
          <line x1="2.5" y1="0" x2="2.5" y2="${h}" ${sideSealStyleLight} />
          <line x1="5.0" y1="0" x2="5.0" y2="${h}" ${sideSealStyleLight} stroke-dashoffset="-2.75" />
          
          <!-- Right Sealing Shadows -->
          <line x1="${w - 2.5}" y1="0" x2="${w - 2.5}" y2="${h}" ${sideSealStyle} />
          <line x1="${w - 5.0}" y1="0" x2="${w - 5.0}" y2="${h}" ${sideSealStyle} stroke-dashoffset="-2.75" />
          <!-- Right Sealing Lights -->
          <line x1="${w - 2.5}" y1="0" x2="${w - 2.5}" y2="${h}" ${sideSealStyleLight} />
          <line x1="${w - 5.0}" y1="0" x2="${w - 5.0}" y2="${h}" ${sideSealStyleLight} stroke-dashoffset="-2.75" />
          
          <!-- Top Sealing Shadows -->
          <line x1="0" y1="${top1}" x2="${w}" y2="${top1}" ${topSealStyle} />
          <line x1="0" y1="${top2}" x2="${w}" y2="${top2}" ${topSealStyle} />
          <!-- Top Sealing Lights -->
          <line x1="0" y1="${top1}" x2="${w}" y2="${top1}" ${topSealStyleLight} />
          <line x1="0" y1="${top2}" x2="${w}" y2="${top2}" ${topSealStyleLight} />
        </g>
      `;

      // Soft reflection/creases to make it look premium
      const creases = `
    <!-- Subtle left edge light highlight -->
    <rect x="0" y="0" width="8" height="${h}" fill="rgba(255,255,255,0.2)" rx="3" filter="blur(1px)" mask="url(#bagMask-${tx})"/>
    <!-- Subtle right edge shadow -->
    <rect x="${w-6}" y="0" width="6" height="${h}" fill="rgba(0,0,0,0.15)" rx="3" filter="blur(1px)" mask="url(#bagMask-${tx})" style="mix-blend-mode: multiply;" />
    <!-- Bottom seam thick gusset shadow -->
    <rect x="0" y="${h - 12}" width="${w}" height="12" fill="rgba(0,0,0,0.25)" rx="2" filter="blur(2px)" mask="url(#bagMask-${tx})" style="mix-blend-mode: multiply;" />
  `;

      return `
    <svg viewBox="${vbX} ${vbY} ${vbW} ${vbH}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.18)); max-height: 100%;">
      <defs>
        ${maskSVG}
        ${texturePattern}
        <linearGradient id="bagGrad-${tx}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${fabricHex}" />
          <stop offset="100%" stop-color="${fabricHex}" stop-opacity="0.9" />
        </linearGradient>
      </defs>
      
      <!-- Troquel Hole Inner Background -->
      ${isTroquel ? troquelInsideSVG : ''}

      ${!isTroquel ? manijaSVG : ''}
      
      <!-- Main Fabric with texture -->
      <g stroke="${strokeColor}" stroke-width="1.5">
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="url(#bagGrad-${tx})" mask="url(#bagMask-${tx})" />
        <!-- Geometric Seeds Overlay (Pores) -->
        <rect x="0" y="0" width="${w}" height="${h}" rx="6" fill="url(#cambrelNoise-${Math.round(tx)})" mask="url(#bagMask-${tx})" style="mix-blend-mode: multiply;" />
      </g>
      
      ${sealedEdges}
      ${!isTroquel ? handleStitchesSVG : ''}
      ${creases}
      
      <!-- Printed Logo Effect -->
      <g style="opacity: 0.95; filter: contrast(1.02) brightness(1.02) drop-shadow(0 1px 1px rgba(0,0,0,0.08));">
        ${logosGroup}
      </g>
    </svg>
  `;
    }

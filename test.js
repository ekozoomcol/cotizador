
function v(id){ return document.getElementById(id).value; }
function n(id){ return Number(v(id)); }
function setStatus(html){ document.getElementById("status").innerHTML = html; }
function money(value){
  return new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 }).format(Number(value || 0));
}
function parseTramoMin(label){
  const m = String(label || "").match(/(\d[\d\.\,]*)/);
  if (!m) return null;
  return Number(m[1].replace(/\./g,"").replace(",","."));
}

function hexToRgb(hex){
  const h = (hex || "").replace("#","").trim();
  if (h.length !== 6) return {r:0,g:0,b:0};
  return { r: parseInt(h.slice(0,2),16), g: parseInt(h.slice(2,4),16), b: parseInt(h.slice(4,6),16) };
}
function rgbToHex(r,g,b){
  const to2 = (x)=> Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2,"0");
  return "#" + to2(r) + to2(g) + to2(b);
}
function normalizeHex(hex){
  const raw = String(hex || "").trim().toUpperCase();
  return raw.startsWith("#") ? raw : `#${raw}`;
}
function isLightHex(hex){
  const {r,g,b} = hexToRgb(normalizeHex(hex));
  const luma = (0.299 * r) + (0.587 * g) + (0.114 * b);
  return luma > 205;
}
function darken(hex, factor=0.60){
  const {r,g,b} = hexToRgb(hex);
  return rgbToHex(r*factor, g*factor, b*factor);
}

/** Fondo oscuro SOLO para tela blanca */
function updatePreviewBackground(colorHex){
  const wrap = document.getElementById("previewWrap");
  if ((colorHex || "").toUpperCase() === "#FFFFFF") {
    wrap.style.background = "#f1f5f9";
    wrap.style.borderColor = "#d7e0ea";
  } else {
    wrap.style.background = "#ffffff";
    wrap.style.borderColor = "#eee";
  }
}

function syncFuelleField(){
  const bagSel = document.getElementById("bag_type");
  const fuelleInput = document.getElementById("fuelle_cm");
  const row = fuelleInput?.closest("div");
  if (!bagSel || !fuelleInput || !row) return;

  const optionText = bagSel.selectedOptions[0]?.textContent || "";
  const optionVal = bagSel.value || "";
  const hasFuelle = /fuelle/i.test(`${optionText} ${optionVal}`);

  fuelleInput.disabled = !hasFuelle;
  row.classList.toggle("is-disabled", !hasFuelle);
  if (!hasFuelle && Number(fuelleInput.value || 0) !== 0){
    fuelleInput.value = "0";
  }
}

function initColorSwatches(selectId){
  const select = document.getElementById(selectId);
  if (!select) return;
  select.classList.add("color-select");

  let swatchWrap = select.parentElement.querySelector(".swatchGroup");
  if (!swatchWrap){
    swatchWrap = document.createElement("div");
    swatchWrap.className = "swatchGroup";
    select.parentElement.appendChild(swatchWrap);
  }
  swatchWrap.innerHTML = "";

  const setActive = (valueHex) => {
    [...swatchWrap.querySelectorAll(".swatchBtn")].forEach(btn => {
      btn.classList.toggle("active", btn.dataset.value === valueHex);
    });
  };

  [...select.options].forEach(opt => {
    const color = normalizeHex(opt.value);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "swatchBtn";
    btn.title = opt.textContent || color;
    btn.dataset.value = color;
    btn.style.background = color;
    if (isLightHex(color)){
      btn.style.borderColor = "rgba(0,0,0,0.4)";
    }
    btn.addEventListener("click", () => {
      select.value = color;
      setActive(color);
      select.dispatchEvent(new Event("input", { bubbles: true }));
      select.dispatchEvent(new Event("change", { bubbles: true }));
    });
    swatchWrap.appendChild(btn);
  });

  setActive(normalizeHex(select.value));
  select.addEventListener("change", () => setActive(normalizeHex(select.value)));
}

/** Mostrar/ocultar selectores según Caras y #colores */

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
function buildLogoSVGBlock(x, y, w, h, logoColors){
  const tx = x + w/2;

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

  // Handle (Manija vs Troquel)
  let manijaSVG = "";
  let maskSVG = "";
    let peakY = 0;
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
    const separacionInternaCm = 8;
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
  const vbH = h + 40 - vbY;

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
}

function renderPreviewInstant(){
  const fabricHex = v("color_hex");
  updatePreviewBackground(fabricHex);
  syncFuelleField();
  syncLogoControlsUI();

  const grid = document.getElementById("previewGrid");
  const orderGrid = document.getElementById("orderPreviewGrid");
  grid.innerHTML = "";
  if (orderGrid) orderGrid.innerHTML = "";

  

  const ancho = n("ancho_cm");
  const alto = n("alto_cm");
  const fuelle = n("fuelle_cm");
  const bagType = v("bag_type");
  const caras = Math.max(1, Math.min(2, n("caras") || 1));
  grid.classList.toggle("is-one-face", caras === 1);
  grid.classList.toggle("two-faces", caras === 2);
  if (orderGrid) orderGrid.classList.toggle("is-one-face", caras === 1);
  if (orderGrid) orderGrid.classList.toggle("two-faces", caras === 2);

  

  const dimsTextCara1_2Caras = `ANCHO ${ancho} cm · ALTO ${alto} cm`;
  const dimsText1Cara = `ANCHO ${ancho} cm · ALTO ${alto} cm · FUELLE ${fuelle} cm`;

  const getLogoColors = (caraIdx) => {
    const t = caraIdx === 1 ? (n("tintas_c1") || 1) : (n("tintas_c2") || 1);
    let arr = [];
    for(let i=1; i<=t; i++){
      arr.push(document.getElementById(`logo_c${caraIdx}_${i}`)?.value || "#000");
    }
    return arr;
  };

  const makeItem = (_label, _showDims, _dimsText, logoColors, showMeasures=true) => {
    const wrap = document.createElement("div");
    wrap.className = "previewItem";

    const svgBox = document.createElement("div");
    svgBox.className = "previewSvg";
    svgBox.innerHTML = generateModernBagSVG(fabricHex, logoColors, bagType, ancho, alto, showMeasures, document.getElementById("largo_arco_visual") ? Number(document.getElementById("largo_arco_visual").value) : 46);

    wrap.appendChild(svgBox);
    return wrap;
  };

  const appendToBoards = (itemMain) => {
    grid.appendChild(itemMain);
    if (orderGrid) orderGrid.appendChild(itemMain.cloneNode(true));
  };

  if (caras === 1){
    appendToBoards(makeItem("Cara 1", true, dimsText1Cara, getLogoColors(1), true));
  } else {
    appendToBoards(makeItem("Cara 1", true, dimsTextCara1_2Caras, getLogoColors(1), true));
    // Cara 2 no muestra medidas para evitar redundancia visual.
    appendToBoards(makeItem("Cara 2", false, "", getLogoColors(2), false));
  }
}

function pickBandForCantidad(beforeObj, cantidad){
  const arr = Object.keys(beforeObj || {}).map((code) => {
    const row = beforeObj[code] || {};
    return {
      code,
      label: row.label || "",
      minQty: parseTramoMin(row.label),
      sinIva: Number(row.precio_unitario_sin_iva || 0),
    };
  }).filter(x => Number.isFinite(x.minQty));

  arr.sort((a,b) => a.minQty - b.minQty);
  if (!arr.length) return null;

  let chosen = arr[0];
  for (const it of arr){
    if (cantidad >= it.minQty) chosen = it;
  }
  return { chosen, all: arr };
}

function renderDesignSummary(data){
  if (!data) return;

  const bagTypeLabel = v("bag_type") === "PLANA_MANIJA" ? "BOLSA PLANA MANIJA" : "BOLSA PLANA TROQUEL";
  const materialText = document.getElementById("material_code").selectedOptions[0]?.textContent || "";
  const ancho = n("ancho_cm") || 0;
  const alto = n("alto_cm") || 0;
  const cantidad = Math.max(1, n("cantidad") || 1);
  const caras = Math.max(1, Math.min(2, n("caras") || 1));
  const t1 = n("tintas_c1") || 1;
  const t2 = n("tintas_c2") || 1;
  let legend = "";
  if (caras === 1) {
    legend = `INCLUYE LOGO 1 CARA (${t1} TINTA${t1>1?'S':''})`;
  } else {
    legend = `LOGO FRENTE (${t1} TINTA${t1>1?'S':''}) · POSTERIOR (${t2} TINTA${t2>1?'S':''})`;
  }

  document.getElementById("posterTitle").textContent = bagTypeLabel;
  const orderTitle = document.querySelector(".orderTitle");
  if (orderTitle) orderTitle.textContent = bagTypeLabel;
  document.getElementById("posterSub").textContent = `Tamaño: ${ancho} cm Ancho x ${alto} Alto · Material: ${materialText}`;
  document.getElementById("posterLegend").textContent = legend;
  document.getElementById("orderLegend").textContent = legend;
  document.getElementById("sumCantidad").textContent = `${cantidad} bolsas`;
  document.getElementById("sumMedidas").textContent = `${ancho} cm Ancho x ${alto} Alto`;

  const before = data.prices_by_band_before_iva || {};
  const selection = pickBandForCantidad(before, cantidad);
  if (!selection){
    document.getElementById("priceDesde").textContent = "DESDE $0 + IVA";
    document.getElementById("miniBands").innerHTML = "";
    return;
  }

  const minPrice = Math.min(...selection.all.map(x => x.sinIva));
  document.getElementById("priceDesde").textContent = `DESDE ${money(minPrice)} + IVA`;

  const mini = selection.all.slice(0, 5).map((it) => {
    return `<div class="miniRow"><span>${it.label}:</span><span>${money(it.sinIva)}</span></div>`;
  }).join("");
  document.getElementById("miniBands").innerHTML = mini;

  const unit = Number(selection.chosen.sinIva || 0);
  const subtotal = unit * cantidad;
  const iva = subtotal * 0.19;
  const total = subtotal + iva;
  document.getElementById("sumPrecioBolsa").textContent = money(unit);
  document.getElementById("sumSubtotal").textContent = money(subtotal);
  document.getElementById("sumIva").textContent = money(iva);
  document.getElementById("sumTotal").textContent = money(total);
}

async function cotizarAuto(){
  const bagType = v("bag_type");
  syncFuelleField();
  document.getElementById("row_manijas").style.display = (bagType === "PLANA_TROQUEL") ? "none" : "flex";

  const ancho = n("ancho_cm");
  const alto = n("alto_cm");
  if (!ancho || !alto || ancho <= 0 || alto <= 0){
    setStatus("<span class='warn'>Faltan medidas</span>");
    return;
  }

  const payload = {
    bag_type: bagType,
    inputs: {
      ancho_cm: ancho,
      alto_cm: alto,
      fuelle_cm: n("fuelle_cm"),
      manija1_cm: n("manija1_cm"),
      manija2_cm: n("manija2_cm"),
      ancho_manijas_cm: n("ancho_manijas_cm"),
      dobles_cm: n("dobles_cm"),
      caras: n("caras"),
      tintas: Math.max(n("tintas_c1")||1, n("tintas_c2")||1),
      cola_produccion: n("cola_produccion"),
      material_code: v("material_code")
    }
  };
  payload.material = v("material_code");

  const payloadKey = JSON.stringify(payload);
  if (payloadKey === lastPayloadKey) return;
  lastPayloadKey = payloadKey;

  setStatus("Calculando...");

  let res;
  try{
    res = await fetch("/quote", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: payloadKey
    });
  }catch(err){
    setStatus("<span class='warn'>Error</span> No se pudo conectar al backend.");
    return;
  }

  if(!res.ok){
    const t = await res.text();
    setStatus("<span class='warn'>Error</span> " + t);
    return;
  }

  const data = await res.json();
  lastQuoteData = data;
  setStatus("<span class='ok'>OK</span> Cotización actualizada");

  lastRawSVG = data.svg_preview || "";
  renderPreviewInstant();

  const tbody = null;
  const before = data.prices_by_band_before_iva || {};
  const withIva = data.prices_by_band_with_iva || {};

  Object.keys(before).forEach(code=>{
    const r1 = before[code];
    const r2 = withIva[code] || {};
    if (tbody){
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r1.label ?? ""}</td>
        <td>${r1.margen_base_pct ?? ""}%</td>
        <td>${r1.dto_L49_pct ?? ""}%</td>
        <td>${r1.margen_real_pct ?? ""}%</td>
        <td>${r1.precio_unitario_sin_iva ?? ""}</td>
        <td>${r2.precio_unitario_con_iva ?? ""}</td>
      `;
      tbody.appendChild(tr);
    }
  });
  renderDesignSummary(data);
}

function scheduleAutoQuote(){
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(cotizarAuto, 250);
}

// Inputs que disparan backend (debounced)
const backendIds = [
  "bag_type","material_code",
  "ancho_cm","alto_cm","fuelle_cm",
  "manija1_cm","manija2_cm","ancho_manijas_cm",
  "dobles_cm","caras","tintas","cola_produccion"
];
backendIds.forEach(id=>{
  const el = document.getElementById(id);
  el.addEventListener("input", scheduleAutoQuote);
  el.addEventListener("change", scheduleAutoQuote);
});

// Preview instantáneo (sin backend): tela, caras, colores
["color_hex","caras","tintas_c1","tintas_c2","logo_c1_1","logo_c1_2","logo_c1_3","logo_c1_4","logo_c2_1","logo_c2_2","logo_c2_3","logo_c2_4","largo_arco_visual"].forEach(id=>{
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("input", renderPreviewInstant);
  el.addEventListener("change", renderPreviewInstant);
});
[
  "cantidad","bag_type","material_code","ancho_cm","alto_cm"
].forEach(id=>{
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("input", () => renderDesignSummary(lastQuoteData));
  el.addEventListener("change", () => renderDesignSummary(lastQuoteData));
});

window.addEventListener("load", () => {
  ["color_hex"].forEach(initColorSwatches);
  syncFuelleField();
  syncLogoControlsUI();
  updatePreviewBackground(v("color_hex"));
  cotizarAuto();
});

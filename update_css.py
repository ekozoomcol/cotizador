import re

css = """
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

  :root {
    --bg-color: #f8fafc;
    --card-bg: rgba(255, 255, 255, 0.85);
    --card-border: rgba(255, 255, 255, 0.6);
    --ink: #0f172a;
    --muted: #64748b;
    --brand: #4f46e5;
    --brand-dark: #3730a3;
    --brand-light: #e0e7ff;
    --accent: #10b981;
    --line: #e2e8f0;
    --ok: #059669;
    --warn: #ea580c;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
  }
  * { box-sizing: border-box; }
  body {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    margin: 0;
    color: var(--ink);
    min-height: 100vh;
    background-color: var(--bg-color);
    background-image: 
      radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.15) 0px, transparent 50%),
      radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),
      radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
      radial-gradient(at 0% 100%, rgba(56, 189, 248, 0.15) 0px, transparent 50%);
    background-attachment: fixed;
  }
  .app {
    max-width: 1220px;
    margin: 0 auto;
    padding: 32px 20px;
  }
  h1 {
    margin: 0 0 28px;
    font-size: clamp(36px, 5vw, 56px);
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(135deg, #1e1b4b 0%, #4f46e5 50%, #d946ef 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: -1px;
    line-height: 1.1;
    filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1));
  }
  /* Agregando un badge de conexion elegante */
  .connectionBanner {
    display: none; /* el original dice que es banner, pero lo omitimos si no es importante, la v actual no lo tiene */
  }
  .card {
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    background: var(--card-bg);
    backdrop-filter: blur(24px);
    padding: 24px;
    box-shadow: var(--shadow-xl);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
  }
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 25px 30px -5px rgb(0 0 0 / 0.15);
  }
  .topForm { 
    margin-bottom: 32px; 
    padding: 28px; 
    border-radius: var(--radius-xl); 
    border-top: 2px solid rgba(255,255,255,0.8);
    border-left: 2px solid rgba(255,255,255,0.8);
  }
  .topForm h3 { 
    margin: 0 0 24px; 
    font-size: 20px; 
    font-family: 'Outfit', sans-serif; 
    color: #1e293b; 
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .topForm h3::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 20px;
    background: var(--brand);
    border-radius: 4px;
  }
  .row { display:flex; gap: 16px; align-items: flex-end; flex-wrap: wrap; margin-bottom: 20px; }
  .row:last-child { margin-bottom: 0; }
  .row > div { flex: 1; min-width: 160px; position: relative; }
  .topForm .row > div { min-width: 140px; }
  label { 
    display:block; 
    font-size: 13px; 
    color: #334155; 
    margin-bottom: 6px; 
    font-weight: 600; 
  }
  input, select {
    width: 100%;
    padding: 10px 14px;
    border: 2px solid #cbd5e1;
    border-radius: var(--radius-md);
    background: #ffffff;
    font-size: 14px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 500;
    color: var(--ink);
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
  }
  input:hover, select:hover {
    border-color: #94a3b8;
  }
  input:focus, select:focus {
    outline: none;
    border-color: var(--brand);
    box-shadow: 0 0 0 4px var(--brand-light);
  }
  .subTitle { font-weight: 700; font-size: 14px; color:#1e293b; margin: 16px 0 8px; font-family: 'Outfit', sans-serif;}
  .inlineHint { font-size: 12px; color:#64748b; margin-top: 6px; font-weight: 500;}
  .muted { color: var(--muted); font-size: 14px; font-weight: 500;}
  #status { margin-top: 16px; padding: 12px 16px; border-radius: 8px; background: rgba(255,255,255,0.7); border: 1px solid var(--line); display: inline-block; font-weight:600;}
  .ok { color: var(--ok); font-weight: 800; padding-right: 4px;}
  .warn { color: var(--warn); font-weight: 800; padding-right: 4px;}
  
  .board {
    display: grid;
    grid-template-columns: 1.3fr 1fr;
    gap: 24px;
    margin-bottom: 16px;
    align-items: stretch;
  }
  .board > .card{
    aspect-ratio: auto;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 32px;
  }
  .posterTitle {
    text-align: center;
    font-size: clamp(28px, 2.5vw, 42px);
    letter-spacing: -0.5px;
    margin: 0 0 8px;
    color: #0f172a;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    text-transform: uppercase;
  }
  .posterSub {
    text-align: center;
    color: #475569;
    font-size: clamp(16px, 1.2vw, 20px);
    margin-bottom: 16px;
    font-weight: 500;
  }
  .logoLegend {
    text-align: center;
    background: linear-gradient(to right, #e0e7ff, #f3e8ff);
    color: var(--brand-dark);
    border: 1px solid #c7d2fe;
    border-radius: var(--radius-md);
    font-size: clamp(14px, 1.1vw, 18px);
    font-weight: 700;
    padding: 8px 16px;
    margin: 0 auto 16px;
    display: inline-block;
    width: auto;
    align-self: center;
    box-shadow: var(--shadow-sm);
  }
  .priceHighlight {
    margin: 0 auto 20px;
    width: 100%;
    text-align: center;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #ffffff;
    font-size: clamp(42px, 3.5vw, 64px);
    font-weight: 800;
    border-radius: var(--radius-lg);
    padding: 16px;
    line-height: 1.1;
    box-shadow: 0 10px 20px -5px rgba(16, 185, 129, 0.4);
    font-family: 'Outfit', sans-serif;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .miniList {
    width: 100%;
    margin: 0 auto 16px;
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 12px 0;
    font-size: clamp(18px, 1.5vw, 24px);
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
  }
  .miniRow {
    display:flex;
    justify-content: space-between;
    gap: 16px;
    margin: 8px 0;
    padding: 6px 12px;
    border-radius: 8px;
    transition: background 0.2s;
  }
  .miniRow:hover {
    background: rgba(79, 70, 229, 0.05);
  }
  .miniRow span:last-child { color: var(--brand); font-weight: 800;}
  
  #previewWrap {
    border-radius: var(--radius-lg);
    border: 2px solid var(--line);
    background: #ffffff;
    padding: 16px;
    flex: 1;
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin: 8px auto 0;
    width: 100%;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.02);
    transition: background 0.3s ease, border-color 0.3s ease;
  }
  #previewGrid{
    width: 100%;
    height: 100%;
    display: flex;
    gap: 16px;
    align-items: center;
    justify-content: center;
  }
  #previewGrid.two-faces{ gap: 8px; }
  .previewItem{
    width: 100%;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    animation: fadeIn 0.4s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .previewSvg{
    width: 100%;
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0 0;
  }
  #previewGrid .previewItem{ width: 50%; }
  #previewGrid.is-one-face .previewItem{ width: 90%; }
  #previewGrid .previewSvg svg{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 10px 15px rgba(0,0,0,0.08));
    transition: transform 0.3s ease;
  }
  #previewGrid .previewSvg svg:hover {
    transform: scale(1.02);
  }
  .previewSvg svg{ width: 100%; height: 100%; display: block; }
  .previewLabel{ font-weight: 800; font-size: 16px; font-family: 'Outfit', sans-serif; color: #1e293b; background: #e2e8f0; padding: 4px 12px; border-radius: 999px;}
  .previewDims{ font-size: 13px; color: #64748b; text-align: center; font-weight: 600; margin-top: 4px;}
  
  .orderTitle {
    text-align: center;
    font-size: clamp(32px, 2.8vw, 42px);
    margin: 0 0 16px;
    color: #1e293b;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.5px;
  }
  .orderPanel {
    background: rgba(255,255,255,0.7);
    border: 2px solid var(--line);
    border-radius: var(--radius-lg);
    padding: 24px;
    font-size: clamp(16px, 1.4vw, 20px);
    line-height: 1.6;
    margin-top: auto;
  }
  .orderPanel div {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dashed var(--line);
    padding: 8px 0;
  }
  .orderPanel div:last-of-type, .orderPanel .total, .orderPanel .totalNote {
    border-bottom: none;
  }
  .orderPanel strong { color: #334155; font-weight: 600;}
  .orderPanel span { font-weight: 700; color: #0f172a;}
  .total {
    margin-top: 16px;
    border-top: 2px solid var(--brand);
    padding-top: 16px !important;
    color: var(--brand);
    font-size: clamp(38px, 3.2vw, 52px);
    line-height: 1.1;
    font-weight: 900;
    text-align: center;
    font-family: 'Outfit', sans-serif;
    display: block !important;
  }
  .totalNote {
    text-align: center;
    color: #64748b;
    font-size: clamp(14px, 1.1vw, 16px);
    font-weight: 600;
    display: block !important;
    padding-top: 4px !important;
  }
  
  #orderPreviewWrap{
    margin-top: 8px;
    margin-bottom: 24px;
    border: 2px dashed #cbd5e1;
    border-radius: var(--radius-md);
    background: rgba(248, 250, 252, 0.5);
    padding: 8px;
    width: 100%;
    flex: 1;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  #orderPreviewGrid{
    width: 100%;
    height: 100%;
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: center;
  }
  #orderPreviewGrid .previewItem{
    max-width: none;
    width: 50%;
    gap: 4px;
  }
  #orderPreviewGrid .previewSvg{
    height: auto;
    flex: 1;
    min-height: 0;
    padding: 0;
  }
  #orderPreviewGrid.is-one-face .previewItem{ width: 90%; }
  #orderPreviewGrid .previewSvg svg{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.05));
  }
  #orderPreviewGrid .previewLabel{
    font-size: 12px;
    padding: 2px 8px;
  }
  #orderPreviewGrid .previewDims{
    display: none;
  }
  
  .is-disabled {
    opacity: 0.4;
    filter: grayscale(1);
    pointer-events: none;
  }
  .color-select {
    display: none;
  }
  .swatchGroup {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    min-height: 32px;
    padding-top: 8px;
  }
  .swatchBtn {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid rgba(0,0,0,0.1);
    cursor: pointer;
    outline: none;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }
  .swatchBtn:hover { transform: scale(1.15) translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
  .swatchBtn.active {
    box-shadow: 0 0 0 3px #fff, 0 0 0 5px var(--brand);
    border-color: transparent;
    transform: scale(1.1);
  }
  .adv {
    margin-top: 16px;
    background: rgba(241, 245, 249, 0.5);
    border: 1px solid var(--line);
    border-radius: var(--radius-md);
    padding: 16px;
    transition: all 0.3s ease;
  }
  .adv[open] {
    background: #ffffff;
    box-shadow: var(--shadow-md);
  }
  .adv summary {
    cursor: pointer;
    font-weight: 700;
    color: var(--brand);
    font-size: 14px;
    list-style: none;
    font-family: 'Outfit', sans-serif;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .adv summary::-webkit-details-marker { display: none; }
  .adv summary::before { 
    content: ""; 
    display: inline-block;
    width: 20px;
    height: 20px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234f46e5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M9 18l6-6-6-6'/%3E%3C/svg%3E");
    background-size: cover;
    transition: transform 0.3s ease;
  }
  .adv[open] summary::before { transform: rotate(90deg); }
  
  table { width:100%; border-collapse: collapse; background: #fff; margin-top: 20px; border-radius: 8px; overflow: hidden; box-shadow: var(--shadow-sm);}
  th, td { border-bottom: 1px solid #edf2f7; padding: 12px; text-align:left; font-size: 14px; }
  th { background: #f1f5f9; font-weight: 700; color: #334155; }
  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas; font-size: 12px; white-space: pre-wrap; }
  
  @media (max-width: 980px){
    .board { grid-template-columns: 1fr; }
    .board > .card { aspect-ratio: auto; }
    #previewWrap { min-height: 350px; }
    #orderPreviewWrap { min-height: 250px; }
  }
"""

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
new_html = re.sub(r'<style>.*?</style>', f'<style>\n{css}\n  </style>', html, flags=re.DOTALL)

with open("c:/Users/jppo0/OneDrive/Desktop/cotizador/static/index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

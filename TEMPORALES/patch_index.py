import re
import sys

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the block 5 Hero section
    old_hero = '''        <!-- BLOQUE 5: IMAGEN HERO -->
        <div class="commercial-block image-block" style="flex: 1 1 auto; min-height: 150px; padding: 0;">
          <div id="previewWrap">
            <div id="previewGrid"></div>
          </div>
        </div>'''
        
    new_hero = '''        <!-- BLOQUE 5: IMAGEN HERO -->
        <div class="commercial-block image-block" style="flex: 1 1 auto; min-height: 150px; padding: 0; position: relative;">
          <!-- Botón de toggle flotante -->
          <button id="togglePresentationBtn" onclick="togglePresentationImage()" style="position: absolute; top: 10px; right: 10px; z-index: 10; padding: 6px 12px; background: rgba(255,255,255,0.9); border: 1px solid #ccc; border-radius: 20px; font-weight: bold; cursor: pointer; color: #333; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 6px; font-family: 'Plus Jakarta Sans', sans-serif;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <span>Ver Foto</span>
          </button>
          
          <div id="previewWrap">
            <div id="previewGrid"></div>
          </div>
          
          <!-- Contenedor para la imagen de presentación, inicialmente oculto -->
          <div id="presentationWrap" style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center; padding: 10px; box-sizing: border-box;">
            <img id="presentationImage" src="/static/foto_manija.png" alt="Presentación de la bolsa" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px;">
          </div>
        </div>'''
        
    if old_hero not in content:
        print("Hero section not found!")
        return
        
    content = content.replace(old_hero, new_hero)

    # 2. Add the JS functions right before the "Inputs que disparan backend" comment
    js_marker = '    // Inputs que disparan backend (debounced)'
    if js_marker not in content:
        print("JS marker not found!")
        return
        
    js_functions = '''    let showingPresentation = false;
    
    function togglePresentationImage() {
      showingPresentation = !showingPresentation;
      const wrapSvg = document.getElementById("previewWrap");
      const wrapImg = document.getElementById("presentationWrap");
      const btn = document.getElementById("togglePresentationBtn");
      
      if (showingPresentation) {
        wrapSvg.style.setProperty("display", "none", "important");
        wrapImg.style.setProperty("display", "flex", "important");
        updatePresentationImage();
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg><span>Ver Gráfico</span>';
        btn.style.color = "#4f46e5";
      } else {
        wrapSvg.style.setProperty("display", "flex", "important");
        wrapImg.style.setProperty("display", "none", "important");
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg><span>Ver Foto</span>';
        btn.style.color = "#333";
      }
    }
    
    function updatePresentationImage() {
      const bagType = v("bag_type");
      const imgEl = document.getElementById("presentationImage");
      if (!imgEl) return;
      
      if (bagType === "PLANA_TROQUEL") {
         imgEl.src = "/static/foto_troquel.png"; 
      } else {
         imgEl.src = "/static/foto_manija.png";
      }
    }

    // Inputs que disparan backend (debounced)'''
    content = content.replace(js_marker, js_functions)

    # 3. Add to the input listeners
    old_listener = '''    [
      "cantidad", "bag_type", "material_code", "ancho_cm", "alto_cm", "caras", "tintas_c1", "tintas_c2"
    ].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("input", () => renderDesignSummary(lastQuoteData));
      el.addEventListener("change", () => renderDesignSummary(lastQuoteData));
    });'''
    new_listener = '''    [
      "cantidad", "bag_type", "material_code", "ancho_cm", "alto_cm", "caras", "tintas_c1", "tintas_c2"
    ].forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      el.addEventListener("input", () => { renderDesignSummary(lastQuoteData); if(showingPresentation) updatePresentationImage(); });
      el.addEventListener("change", () => { renderDesignSummary(lastQuoteData); if(showingPresentation) updatePresentationImage(); });
    });'''
    
    if old_listener not in content:
        print("Listener block not found!")
        return
        
    content = content.replace(old_listener, new_listener)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Patch applied successfully.")

if __name__ == "__main__":
    patch_file('static/index.html')

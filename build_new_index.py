# -*- coding: utf-8 -*-
"""
Builder for QAZAQSTAN GEO-ECONOMIC DOSSIER 2.0 with True 3D Interactive Map,
23 National Parks & Nature Reserves, and 3D Animal Hologram Showcase.
"""
import json
import os

with open("dossier_db.json", "r", encoding="utf-8") as f:
    dossier_db = json.load(f)

with open("nature_reserves_db.json", "r", encoding="utf-8") as f:
    parks_db = json.load(f)

# Build SVG markup for regions
svg_regions_markup = []
for rid, rdata in dossier_db.items():
    path_d = rdata.get("svg_path", "")
    name = rdata.get("name", "")
    tags_str = " ".join(rdata.get("filterTags", []))
    svg_regions_markup.append(f'''    <path class="geo-region" id="region-{rid}" data-id="{rid}" data-tags="{tags_str}" d="{path_d}">
      <title>{name}</title>
    </path>''')

# Build SVG markup for cities
svg_city_markers = []
for rid, rdata in dossier_db.items():
    if rdata.get("type") == "city":
        name = rdata.get("name", "")
        lx = rdata.get("label_x", 500)
        ly = rdata.get("label_y", 300)
        tags_str = " ".join(rdata.get("filterTags", []))
        svg_city_markers.append(f'''    <g class="city-pin" id="pin-{rid}" data-id="{rid}" data-tags="{tags_str}" transform="translate({lx:.1f}, {ly:.1f})">
      <circle class="pin-hitbox" r="22" />
      <circle class="pin-radar" r="14" />
      <rect class="pin-diamond" x="-6" y="-6" width="12" height="12" rx="2" transform="rotate(45)" />
      <circle class="pin-center" r="3" />
      <g class="pin-tag" transform="translate(14, -10)">
        <rect class="pin-tag-bg" x="0" y="0" width="{len(name)*7.5 + 16}" height="20" rx="4" />
        <text class="pin-tag-text" x="8" y="14">{name}</text>
      </g>
    </g>''')

# Build SVG markup for National Parks and Nature Reserves (23 total)
svg_park_markers = []
for p in parks_db:
    pid = p["id"]
    pname = p["name"]
    ptype = p["type"]
    px = p["x"]
    py = p["y"]
    animal_name = p["animal"]["name"]
    is_park = (ptype == "park")
    color = "#10b981" if is_park else "#f59e0b"
    
    # SVG Leaf / Mountain Icon
    icon_path = "M0 -7 L5 2 L-5 2 Z M0 0 L0 5" if is_park else "M-6 4 L0 -6 L6 4 Z"
    
    svg_park_markers.append(f'''    <g class="nature-pin {ptype}" id="park-{pid}" data-park-id="{pid}" transform="translate({px:.1f}, {py:.1f})">
      <circle class="nature-hitbox" r="20" />
      <circle class="nature-radar" r="13" stroke="{color}" />
      <circle class="nature-core-bg" r="8" fill="#06090e" stroke="{color}" stroke-width="1.8" />
      <path class="nature-symbol" d="{icon_path}" stroke="{color}" stroke-width="1.4" fill="none" />
      <circle class="nature-center-dot" r="2.2" fill="{color}" />
    </g>''')

svg_regions_html = "\n".join(svg_regions_markup)
svg_cities_html = "\n".join(svg_city_markers)
svg_parks_html = "\n".join(svg_park_markers)

db_json_embedded = json.dumps(dossier_db, ensure_ascii=False)
parks_json_embedded = json.dumps(parks_db, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>QAZAQSTAN 3D // НАЦИОНАЛЬНЫЙ ГЕОЭКОНОМИЧЕСКИЙ РЕЕСТР И АТЛАС</title>
  
  <!-- Fonts: Space Grotesk (tech/headings) & Manrope (editorial body) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

  <!-- Three.js for 3D procedural animal models -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <style>
    /* ==========================================================================
       DESIGN SYSTEM: OBSIDIAN & GOLD 3D OBSERVATORY
       ========================================================================== */
    :root {{
      --bg-black: #05080e;
      --bg-surface: #0b111c;
      --bg-surface-elevated: #111a2c;
      --bg-card: rgba(17, 26, 44, 0.75);
      --border-subtle: rgba(229, 195, 100, 0.15);
      --border-bright: rgba(229, 195, 100, 0.45);
      --gold-primary: #e5c364;
      --gold-bright: #ffd977;
      --gold-dim: #a68936;
      --gold-glow: rgba(229, 195, 100, 0.28);
      --text-main: #f3f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-emerald: #10b981;
      --accent-emerald-bright: #34d399;
      --accent-ruby: #f43f5e;
      --accent-amber: #f59e0b;
      --accent-cyan: #06b6d4;
      --font-display: 'Space Grotesk', -apple-system, sans-serif;
      --font-body: 'Manrope', -apple-system, sans-serif;
      --shadow-lux: 0 20px 45px -10px rgba(0, 0, 0, 0.7), 0 0 30px rgba(229, 195, 100, 0.08);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      height: 100%;
      background-color: var(--bg-black);
      color: var(--text-main);
      font-family: var(--font-body);
      font-size: 14px;
      line-height: 1.5;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(229, 195, 100, 0.07) 0%, transparent 65%),
        linear-gradient(rgba(229, 195, 100, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(229, 195, 100, 0.02) 1px, transparent 1px);
      background-size: 100% 100%, 48px 48px, 48px 48px;
      pointer-events: none;
      z-index: 0;
    }}

    .app-viewport {{
      position: relative;
      z-index: 1;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}

    /* HEADER & TICKER */
    .top-dossier-bar {{
      background: rgba(11, 17, 28, 0.9);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      position: sticky;
      top: 0;
      z-index: 60;
    }}

    .ticker-ribbon {{
      background: rgba(5, 8, 14, 0.98);
      border-bottom: 1px solid rgba(229, 195, 100, 0.08);
      font-family: var(--font-display);
      font-size: 11px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--text-muted);
      overflow-x: auto;
      white-space: nowrap;
    }}

    .ticker-items {{
      display: flex;
      gap: 20px;
      align-items: center;
    }}

    .ticker-item {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .ticker-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald);
      display: inline-block;
    }}

    .ticker-val {{
      color: var(--gold-primary);
      font-weight: 600;
    }}

    .header-main {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 24px;
      gap: 20px;
      flex-wrap: wrap;
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .brand-crest {{
      width: 44px;
      height: 44px;
      border: 1px solid var(--border-bright);
      background: linear-gradient(135deg, rgba(229, 195, 100, 0.15), rgba(11, 17, 28, 0.9));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--gold-primary);
      box-shadow: 0 0 16px var(--gold-glow);
    }}

    .brand-titles h1 {{
      font-family: var(--font-display);
      font-size: 19px;
      font-weight: 700;
      letter-spacing: 0.04em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-titles h1 span {{
      color: var(--gold-primary);
    }}

    .brand-titles p {{
      font-size: 11px;
      color: var(--text-muted);
      letter-spacing: 0.02em;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex: 1;
      max-width: 600px;
      justify-content: flex-end;
    }}

    .search-box-wrapper {{
      position: relative;
      flex: 1;
      max-width: 340px;
    }}

    .search-input {{
      width: 100%;
      height: 38px;
      background: rgba(17, 26, 44, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0 36px 0 14px;
      font-family: var(--font-body);
      font-size: 13px;
      color: var(--text-main);
      outline: none;
      transition: var(--transition);
    }}

    .search-input:focus {{
      border-color: var(--gold-primary);
      box-shadow: 0 0 12px var(--gold-glow);
      background: rgba(17, 26, 44, 0.95);
    }}

    .search-badge {{
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 10px;
      color: var(--gold-dim);
      border: 1px solid rgba(229, 195, 100, 0.2);
      border-radius: 4px;
      padding: 2px 5px;
      pointer-events: none;
      font-family: var(--font-display);
    }}

    .search-dropdown {{
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      right: 0;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-bright);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lux);
      max-height: 280px;
      overflow-y: auto;
      display: none;
      z-index: 100;
    }}

    .search-item {{
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      transition: background 0.15s;
    }}

    .search-item:hover {{
      background: rgba(229, 195, 100, 0.1);
    }}

    .search-item-title {{
      font-weight: 600;
      color: #ffffff;
    }}

    .search-item-sub {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .view-toggle-btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      height: 38px;
      padding: 0 14px;
      background: rgba(229, 195, 100, 0.08);
      border: 1px solid var(--border-bright);
      color: var(--gold-primary);
      border-radius: var(--radius-md);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.03em;
      cursor: pointer;
      transition: var(--transition);
      white-space: nowrap;
    }}

    .view-toggle-btn:hover {{
      background: var(--gold-primary);
      color: #05080e;
      box-shadow: 0 0 15px var(--gold-glow);
    }}

    /* FILTER TABS */
    .filter-ribbon-bar {{
      padding: 8px 24px;
      background: rgba(8, 12, 20, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
    }}

    .filter-ribbon-bar::-webkit-scrollbar {{
      display: none;
    }}

    .sector-tab {{
      background: rgba(17, 26, 44, 0.5);
      border: 1px solid rgba(229, 195, 100, 0.12);
      border-radius: var(--radius-sm);
      color: var(--text-muted);
      padding: 6px 14px;
      font-family: var(--font-display);
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: var(--transition);
      white-space: nowrap;
    }}

    .sector-tab:hover {{
      border-color: var(--gold-primary);
      color: var(--text-main);
      background: rgba(229, 195, 100, 0.08);
    }}

    .sector-tab.active {{
      background: linear-gradient(135deg, rgba(229, 195, 100, 0.2), rgba(11, 17, 28, 0.8));
      border-color: var(--gold-primary);
      color: var(--gold-bright);
      box-shadow: 0 0 12px var(--gold-glow);
      font-weight: 600;
    }}

    .sector-count {{
      background: rgba(0, 0, 0, 0.4);
      padding: 1px 6px;
      border-radius: 10px;
      font-size: 10px;
      border: 1px solid rgba(229, 195, 100, 0.2);
    }}

    /* ==========================================================================
       TRUE 3D MAP WORKSPACE
       ========================================================================== */
    .workspace-container {{
      flex: 1;
      display: flex;
      flex-direction: column;
      position: relative;
    }}

    .map-stage-3d-wrapper {{
      position: relative;
      flex: 1;
      min-height: calc(100vh - 120px);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      perspective: 1400px; /* 3D PERSPECTIVE */
      cursor: grab;
      user-select: none;
      padding: 20px;
    }}

    .map-stage-3d-wrapper:active {{
      cursor: grabbing;
    }}

    /* 3D Depth Floor Plate */
    .map-3d-plane {{
      position: relative;
      width: 1000px;
      max-width: 95vw;
      height: 650px;
      max-height: 80vh;
      transform-style: preserve-3d;
      transition: transform 0.12s cubic-bezier(0.1, 0.9, 0.2, 1);
      will-change: transform;
    }}

    /* Ambient Base Grid on 3D Floor */
    .map-3d-plane::before {{
      content: "";
      position: absolute;
      inset: -40px;
      border: 1px dashed rgba(229, 195, 100, 0.2);
      border-radius: 20px;
      background: radial-gradient(circle at 50% 50%, rgba(229, 195, 100, 0.04) 0%, transparent 75%);
      transform: translateZ(-25px);
      pointer-events: none;
      box-shadow: 0 35px 70px rgba(0,0,0,0.85);
    }}

    .svg-atlas-viewport {{
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 25px 40px rgba(0, 0, 0, 0.9));
      transform: translateZ(15px);
      transform-style: preserve-3d;
    }}

    /* MAP REGIONS */
    .geo-region {{
      fill: #0d1524;
      stroke: var(--gold-primary);
      stroke-width: 1.15;
      stroke-opacity: 0.45;
      vector-effect: non-scaling-stroke;
      cursor: pointer;
      transition: fill 0.25s ease, stroke 0.25s ease, stroke-width 0.25s ease, filter 0.25s ease;
    }}

    .geo-region:hover {{
      fill: rgba(229, 195, 100, 0.32);
      stroke: var(--gold-bright);
      stroke-width: 2.2;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 14px rgba(229, 195, 100, 0.7));
    }}

    .geo-region.dimmed {{
      opacity: 0.2;
      fill: #060a12;
      stroke-opacity: 0.15;
    }}

    .geo-region.highlighted {{
      fill: rgba(229, 195, 100, 0.4);
      stroke: var(--gold-bright);
      stroke-width: 2.4;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 16px rgba(229, 195, 100, 0.8));
    }}

    /* CITY MARKERS */
    .city-pin {{
      cursor: pointer;
    }}
    .pin-hitbox {{
      fill: transparent;
      pointer-events: all;
    }}
    .pin-radar {{
      fill: none;
      stroke: var(--gold-primary);
      stroke-width: 1.2;
      opacity: 0.6;
      animation: radarPulse 2.8s infinite ease-out;
      pointer-events: none;
    }}
    @keyframes radarPulse {{
      0% {{ transform: scale(0.6); opacity: 0.9; }}
      100% {{ transform: scale(2.0); opacity: 0; }}
    }}
    .pin-diamond {{
      fill: var(--bg-black);
      stroke: var(--gold-primary);
      stroke-width: 2;
      pointer-events: none;
      transition: stroke 0.2s, fill 0.2s;
    }}
    .pin-center {{
      fill: var(--gold-bright);
      pointer-events: none;
    }}
    .pin-tag {{
      pointer-events: none;
    }}
    .pin-tag-bg {{
      fill: rgba(8, 12, 20, 0.9);
      stroke: var(--border-bright);
      stroke-width: 1;
    }}
    .pin-tag-text {{
      fill: #ffffff;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 600;
    }}
    .city-pin:hover .pin-diamond {{
      stroke: #ffffff;
      fill: var(--gold-primary);
    }}
    .city-pin:hover .pin-tag-bg {{
      fill: var(--gold-primary);
    }}
    .city-pin:hover .pin-tag-text {{
      fill: #05080e;
    }}

    /* ==========================================================================
       3D NATURE PINS: NATIONAL PARKS & RESERVES (23 TOTAL)
       ========================================================================== */
    .nature-pin {{
      cursor: pointer;
    }}
    .nature-hitbox {{
      fill: transparent;
      pointer-events: all;
    }}
    .nature-radar {{
      fill: none;
      stroke-width: 1.2;
      opacity: 0.7;
      animation: naturePulse 2.6s infinite ease-out;
      pointer-events: none;
    }}
    @keyframes naturePulse {{
      0% {{ transform: scale(0.5); opacity: 1; }}
      100% {{ transform: scale(2.2); opacity: 0; }}
    }}
    .nature-core-bg {{
      pointer-events: none;
      transition: transform 0.2s, fill 0.2s;
      filter: drop-shadow(0 2px 6px rgba(0,0,0,0.8));
    }}
    .nature-symbol {{
      pointer-events: none;
    }}
    .nature-center-dot {{
      pointer-events: none;
    }}
    .nature-pin:hover .nature-core-bg {{
      fill: var(--gold-primary);
      stroke: #ffffff;
    }}
    .nature-pin:hover .nature-symbol {{
      stroke: #05080e;
    }}

    /* FLOATING 3D MAP CONTROLS & HUD */
    .map-3d-toolbar {{
      position: absolute;
      top: 20px;
      right: 24px;
      display: flex;
      gap: 8px;
      background: rgba(11, 17, 28, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 6px;
      box-shadow: var(--shadow-lux);
      z-index: 20;
    }}

    .map-3d-btn {{
      background: rgba(17, 26, 44, 0.6);
      border: 1px solid rgba(229, 195, 100, 0.15);
      color: var(--text-muted);
      border-radius: var(--radius-sm);
      padding: 6px 12px;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: var(--transition);
      white-space: nowrap;
    }}

    .map-3d-btn:hover {{
      color: var(--gold-bright);
      border-color: var(--gold-primary);
      background: rgba(229, 195, 100, 0.12);
    }}

    .map-3d-btn.active {{
      background: var(--gold-primary);
      color: #05080e;
      border-color: var(--gold-primary);
      box-shadow: 0 0 10px var(--gold-glow);
    }}

    /* TELEMETRY HUD */
    .map-telemetry-hud {{
      position: absolute;
      bottom: 24px;
      left: 24px;
      width: 320px;
      background: rgba(11, 17, 28, 0.88);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px;
      box-shadow: var(--shadow-lux);
      pointer-events: none;
      transition: opacity 0.2s ease;
      z-index: 10;
    }}

    .hud-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }}

    .hud-title {{
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      color: #ffffff;
    }}

    .hud-rating {{
      font-family: var(--font-display);
      font-size: 11px;
      color: var(--accent-emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.1);
    }}

    .hud-metric-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid rgba(229, 195, 100, 0.1);
    }}

    .hud-metric-label {{
      font-size: 10px;
      color: var(--text-dim);
      text-transform: uppercase;
    }}

    .hud-metric-val {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--gold-primary);
    }}

    /* ZOOM CONTROLS */
    .map-controls-panel {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 10;
    }}

    .map-btn {{
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      background: rgba(17, 26, 44, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-bright);
      color: var(--gold-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}

    .map-btn:hover {{
      background: var(--gold-primary);
      color: #05080e;
      box-shadow: 0 0 12px var(--gold-glow);
    }}

    /* ==========================================================================
       3D ANIMAL SHOWCASE & HOLOGRAPHIC INSPECTOR (CARD ON HOVER / CLICK)
       ========================================================================== */
    .animal-hologram-card {{
      position: fixed;
      pointer-events: none;
      background: rgba(9, 14, 24, 0.94);
      backdrop-filter: blur(20px);
      border: 1px solid var(--gold-primary);
      border-radius: var(--radius-lg);
      padding: 16px;
      width: 360px;
      box-shadow: 0 25px 50px rgba(0,0,0,0.85), 0 0 35px var(--gold-glow);
      z-index: 1200;
      opacity: 0;
      transform: translate(-50%, -105%) scale(0.95);
      transition: opacity 0.25s ease, transform 0.25s ease;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .animal-hologram-card.visible {{
      opacity: 1;
      transform: translate(-50%, -105%) scale(1);
      pointer-events: all;
    }}

    .animal-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      border-bottom: 1px solid rgba(229, 195, 100, 0.15);
      padding-bottom: 10px;
    }}

    .animal-park-name {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      color: var(--gold-bright);
    }}

    .animal-park-region {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .animal-type-badge {{
      font-size: 9.5px;
      font-family: var(--font-display);
      text-transform: uppercase;
      padding: 3px 7px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: var(--accent-emerald);
      white-space: nowrap;
    }}

    /* 3D Model & Photo Split Visual View */
    .animal-visual-stage {{
      position: relative;
      width: 100%;
      height: 190px;
      border-radius: var(--radius-md);
      overflow: hidden;
      background: radial-gradient(circle at 50% 50%, rgba(17, 26, 44, 0.9), #05080e);
      border: 1px solid var(--border-subtle);
    }}

    .animal-3d-canvas-wrap {{
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      cursor: grab;
    }}

    .animal-photo-view {{
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      object-fit: cover;
      display: none;
      transition: opacity 0.3s;
    }}

    .visual-toggle-bar {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      display: flex;
      gap: 4px;
      z-index: 10;
    }}

    .visual-toggle-btn {{
      background: rgba(5, 8, 14, 0.85);
      border: 1px solid var(--border-bright);
      color: var(--gold-primary);
      font-size: 10px;
      font-family: var(--font-display);
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      transition: var(--transition);
    }}

    .visual-toggle-btn.active {{
      background: var(--gold-primary);
      color: #05080e;
      font-weight: 700;
    }}

    .animal-bio-info {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .animal-name-title {{
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .animal-latin {{
      font-size: 11px;
      font-style: italic;
      color: var(--gold-dim);
    }}

    .animal-redbook {{
      font-size: 11px;
      color: #f87171;
      font-weight: 600;
      background: rgba(248, 113, 113, 0.1);
      border: 1px solid rgba(248, 113, 113, 0.25);
      padding: 3px 8px;
      border-radius: 4px;
      margin-top: 4px;
    }}

    .animal-fact {{
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-top: 4px;
    }}

    .animal-card-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .animal-link-btn {{
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 600;
      color: var(--gold-primary);
      background: none;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 0;
    }}

    .animal-link-btn:hover {{
      text-decoration: underline;
      color: var(--gold-bright);
    }}

    /* MATRIX GRID VIEW */
    .matrix-grid-view {{
      display: none;
      padding: 28px 24px;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      max-width: 1440px;
      margin: 0 auto;
      width: 100%;
    }}

    .matrix-card {{
      background: linear-gradient(145deg, rgba(17, 26, 44, 0.85), rgba(9, 13, 22, 0.95));
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 20px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--transition);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .matrix-card:hover {{
      border-color: var(--gold-primary);
      transform: translateY(-4px);
      box-shadow: var(--shadow-lux);
    }}

    .matrix-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 12px;
    }}

    .matrix-card-title {{
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
    }}

    .matrix-card-kz {{
      font-size: 11px;
      color: var(--text-dim);
    }}

    .matrix-card-rating {{
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      color: var(--gold-bright);
      background: rgba(229, 195, 100, 0.12);
      border: 1px solid rgba(229, 195, 100, 0.25);
      padding: 3px 8px;
      border-radius: var(--radius-sm);
    }}

    .matrix-card-focus {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.4;
      flex: 1;
    }}

    .matrix-card-stats {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      margin-bottom: 14px;
    }}

    .matrix-stat-name {{
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-dim);
    }}

    .matrix-stat-val {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--gold-primary);
    }}

    .matrix-card-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-dim);
    }}

    /* EXECUTIVE DOSSIER MODAL */
    .dossier-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(4, 6, 10, 0.82);
      backdrop-filter: blur(16px);
      z-index: 1500;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}

    .dossier-overlay.active {{
      opacity: 1;
      pointer-events: all;
    }}

    .dossier-modal-window {{
      background: linear-gradient(175deg, #0d1422 0%, #080c14 100%);
      border: 1px solid var(--border-bright);
      box-shadow: var(--shadow-lux), 0 0 50px rgba(229, 195, 100, 0.08);
      border-radius: var(--radius-xl);
      width: 100%;
      max-width: 1180px;
      height: 92vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transform: translateY(20px) scale(0.98);
      transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .dossier-overlay.active .dossier-modal-window {{
      transform: translateY(0) scale(1);
    }}

    .dossier-modal-top {{
      padding: 16px 28px;
      background: rgba(11, 17, 28, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .dossier-breadcrumbs {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-display);
      font-size: 11px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--text-dim);
    }}

    .dossier-code-badge {{
      background: rgba(229, 195, 100, 0.12);
      border: 1px solid rgba(229, 195, 100, 0.3);
      color: var(--gold-bright);
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      font-weight: 600;
    }}

    .dossier-close-btn {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      transition: var(--transition);
    }}

    .dossier-close-btn:hover {{
      background: rgba(244, 63, 94, 0.15);
      border-color: var(--accent-ruby);
      color: #ffffff;
      transform: rotate(90deg);
    }}

    .dossier-scroll-body {{
      flex: 1;
      overflow-y: auto;
      padding: 32px 36px;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}

    .dossier-scroll-body::-webkit-scrollbar {{
      width: 6px;
    }}
    .dossier-scroll-body::-webkit-scrollbar-thumb {{
      background: rgba(229, 195, 100, 0.25);
      border-radius: 3px;
    }}

    .dossier-hero {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 24px;
      flex-wrap: wrap;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .dossier-titles h2 {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.2;
    }}

    .dossier-titles .dossier-kz-title {{
      font-size: 14px;
      color: var(--gold-primary);
      margin-top: 4px;
    }}

    .dossier-titles .dossier-center-info {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 8px;
    }}

    .dossier-hero-badges {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 8px;
    }}

    .dossier-inv-tier {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 6px 14px;
      border-radius: var(--radius-md);
      box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
    }}

    .dossier-type-tag {{
      font-family: var(--font-display);
      font-size: 11px;
      text-transform: uppercase;
      color: var(--gold-bright);
      background: rgba(229, 195, 100, 0.08);
      border: 1px solid rgba(229, 195, 100, 0.2);
      padding: 4px 10px;
      border-radius: var(--radius-sm);
    }}

    .dossier-macro-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
    }}

    .macro-tile {{
      background: rgba(17, 26, 44, 0.65);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 16px 20px;
    }}

    .macro-tile-label {{
      font-size: 11px;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 6px;
    }}

    .macro-tile-val {{
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      color: #ffffff;
    }}

    .macro-tile-sub {{
      font-size: 11px;
      color: var(--gold-primary);
      margin-top: 4px;
    }}

    .dossier-executive-summary {{
      background: linear-gradient(135deg, rgba(229, 195, 100, 0.05), rgba(11, 17, 28, 0.6));
      border-left: 3px solid var(--gold-primary);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 18px 24px;
      font-size: 14px;
      line-height: 1.7;
    }}

    .dossier-section {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    .dossier-section-title {{
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 8px;
    }}

    .dossier-section-title span {{
      color: var(--gold-primary);
    }}

    .enterprises-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }}

    .enterprise-card {{
      background: rgba(17, 26, 44, 0.55);
      border: 1px solid rgba(229, 195, 100, 0.12);
      border-radius: var(--radius-md);
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      transition: var(--transition);
    }}

    .enterprise-card:hover {{
      border-color: var(--gold-primary);
      background: rgba(17, 26, 44, 0.85);
      transform: translateY(-2px);
    }}

    .enterprise-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }}

    .enterprise-title {{
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      color: #ffffff;
    }}

    .enterprise-tag {{
      font-size: 10px;
      font-family: var(--font-display);
      color: var(--gold-primary);
      background: rgba(229, 195, 100, 0.12);
      border: 1px solid rgba(229, 195, 100, 0.25);
      padding: 2px 7px;
      border-radius: 4px;
    }}

    .enterprise-role {{
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .enterprise-badge {{
      font-size: 11px;
      color: var(--gold-dim);
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 8px;
      font-family: var(--font-display);
    }}

    /* NATURE 3-COLUMN */
    .nature-pillars {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}

    .nature-pillar-card {{
      background: rgba(11, 17, 28, 0.7);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 18px;
    }}

    .nature-pillar-head {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      color: var(--gold-primary);
      text-transform: uppercase;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .nature-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .nature-list-item {{
      font-size: 12.5px;
      color: var(--text-main);
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }}

    .nature-list-item::before {{
      content: "◆";
      color: var(--gold-dim);
      font-size: 9px;
      margin-top: 4px;
    }}

    /* GALLERY */
    .gallery-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 16px;
    }}

    .gallery-tile {{
      position: relative;
      border-radius: var(--radius-md);
      overflow: hidden;
      aspect-ratio: 16 / 10;
      background: rgba(17, 26, 44, 0.8);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: var(--transition);
    }}

    .gallery-tile:hover {{
      border-color: var(--gold-primary);
      transform: scale(1.02);
      box-shadow: 0 10px 25px rgba(0,0,0,0.7);
    }}

    .gallery-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }}

    .gallery-tile:hover .gallery-img {{
      transform: scale(1.06);
    }}

    .gallery-caption {{
      position: absolute;
      inset: auto 0 0 0;
      background: linear-gradient(transparent, rgba(5, 8, 14, 0.95) 75%);
      padding: 24px 12px 10px;
      font-size: 11.5px;
      color: #ffffff;
      font-family: var(--font-display);
    }}

    /* TOOLTIP */
    .geo-tooltip {{
      position: fixed;
      pointer-events: none;
      background: rgba(11, 17, 28, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-bright);
      border-radius: var(--radius-md);
      padding: 10px 16px;
      box-shadow: var(--shadow-lux);
      z-index: 500;
      opacity: 0;
      transform: translate(-50%, -120%);
      transition: opacity 0.15s ease, transform 0.15s ease;
      white-space: nowrap;
    }}

    .geo-tooltip.visible {{
      opacity: 1;
    }}

    .tooltip-name {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      color: #ffffff;
    }}

    .tooltip-center {{
      font-size: 11px;
      color: var(--text-muted);
    }}

    .tooltip-focus {{
      font-size: 11px;
      color: var(--gold-primary);
      margin-top: 2px;
      font-weight: 600;
    }}

    /* LIGHTBOX */
    .lightbox-modal {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.94);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 30px;
    }}

    .lightbox-modal.active {{
      display: flex;
    }}

    .lightbox-content {{
      max-width: 90vw;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 14px;
    }}

    .lightbox-img {{
      max-width: 100%;
      max-height: 78vh;
      object-fit: contain;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-bright);
    }}

    .lightbox-caption {{
      font-family: var(--font-display);
      color: var(--text-main);
      font-size: 14px;
    }}

    .lightbox-close {{
      position: absolute;
      top: 24px;
      right: 28px;
      color: #ffffff;
      font-size: 32px;
      cursor: pointer;
    }}

    /* RESPONSIVE */
    @media (max-width: 900px) {{
      .header-main {{
        flex-direction: column;
        align-items: stretch;
      }}
      .header-actions {{
        max-width: 100%;
      }}
      .map-3d-toolbar {{
        top: 10px;
        right: 10px;
        flex-wrap: wrap;
        max-width: 240px;
      }}
      .dossier-modal-window {{
        height: 98vh;
        width: 98vw;
      }}
      .dossier-scroll-body {{
        padding: 20px;
      }}
      .map-telemetry-hud {{
        display: none;
      }}
      .animal-hologram-card {{
        width: 320px;
      }}
    }}
  </style>
</head>
<body>
  <div class="app-viewport">
    <!-- TOP EXECUTIVE BAR -->
    <header class="top-dossier-bar">
      <!-- MACRO TICKER RIBBON -->
      <div class="ticker-ribbon">
        <div class="ticker-items">
          <div class="ticker-item">
            <span class="ticker-dot"></span>
            <span>СУВЕРЕННЫЙ 3D АТЛАС:</span>
            <span class="ticker-val">20 СУБЪЕКТОВ • 23 НАЦПАРКА И ЗАПОВЕДНИКА</span>
          </div>
          <div class="ticker-item">
            <span>ВВП РК:</span>
            <span class="ticker-val">\$265+ МЛРД (EST. 2024-2026)</span>
          </div>
          <div class="ticker-item">
            <span>ФАУНА:</span>
            <span class="ticker-val">3D МОДЕЛИРОВАНИЕ И РЕАЛЬНЫЕ АРХИВЫ РК</span>
          </div>
          <div class="ticker-item">
            <span>ИНТЕРАКТИВНОСТЬ:</span>
            <span class="ticker-val">3D ORBIT • ПЕРСПЕКТИВА • ГОЛОГРАММЫ</span>
          </div>
        </div>
        <div class="ticker-item">
          <span>РЕЖИМ:</span>
          <span class="ticker-val">TRUE 3D VIEWPORT v2.8</span>
        </div>
      </div>

      <!-- MAIN HEADER CONTENT -->
      <div class="header-main">
        <div class="brand-section">
          <div class="brand-crest">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"></polygon>
              <line x1="12" y1="22" x2="12" y2="12"></line>
              <polyline points="2 8.5 12 12 22 8.5"></polyline>
            </svg>
          </div>
          <div class="brand-titles">
            <h1>QAZAQSTAN <span>// 3D GEO-ECONOMIC DOSSIER</span></h1>
            <p>Суверенный реестр промышленных мощностей, 23 нацпарков и заповедников с 3D фауной</p>
          </div>
        </div>

        <div class="header-actions">
          <div class="search-box-wrapper">
            <input type="text" id="subjectSearch" class="search-input" placeholder="Поиск области, города или нацпарка..." autocomplete="off">
            <span class="search-badge">ESC</span>
            <div id="searchDropdown" class="search-dropdown"></div>
          </div>
          <button id="viewToggleBtn" class="view-toggle-btn">
            <span id="viewToggleIcon">⊞</span>
            <span id="viewToggleText">Сводная матрица</span>
          </button>
        </div>
      </div>

      <!-- SECTOR FILTER TABS -->
      <nav class="filter-ribbon-bar">
        <button class="sector-tab active" data-filter="all">Все субъекты <span class="sector-count">20</span></button>
        <button class="sector-tab" data-filter="parks">🌲 Заповедники & Нацпарки <span class="sector-count">23</span></button>
        <button class="sector-tab" data-filter="oilgas">Нефтегазовый сектор <span class="sector-count">5</span></button>
        <button class="sector-tab" data-filter="metallurgy">Металлургия & Горнорудный <span class="sector-count">7</span></button>
        <button class="sector-tab" data-filter="uranium">Уран & Атомпром <span class="sector-count">3</span></button>
        <button class="sector-tab" data-filter="agro">Агропромышленный пояс <span class="sector-count">6</span></button>
        <button class="sector-tab" data-filter="coal">Уголь & Энергетика <span class="sector-count">4</span></button>
        <button class="sector-tab" data-filter="machinery">Машиностроение <span class="sector-count">4</span></button>
      </nav>
    </header>

    <!-- WORKSPACE CONTAINER -->
    <main class="workspace-container">
      <!-- 1. TRUE 3D MAP VIEWPORT -->
      <div id="mapStageWrapper" class="map-stage-3d-wrapper">
        <!-- 3D TOOLBAR PRESETS -->
        <div class="map-3d-toolbar">
          <button id="btn3DPerspective" class="map-3d-btn active" title="3D Перспектива">⟲ 3D Перспектива</button>
          <button id="btn3DIsometric" class="map-3d-btn" title="3D Изометрия">◰ Изометрия</button>
          <button id="btn3DTopDown" class="map-3d-btn" title="2D Вид сверху">⧈ 2D План</button>
          <button id="btn3DAutoOrbit" class="map-3d-btn" title="Автовращение 3D">✦ Авто-облёт</button>
          <button id="btnToggleParks" class="map-3d-btn" style="color: var(--accent-emerald);" title="Переключить заповедники">🌲 Фауна (23)</button>
        </div>

        <!-- 3D PLANE CONTAINER -->
        <div id="map3DPlane" class="map-3d-plane">
          <svg id="svgAtlas" class="svg-atlas-viewport" viewBox="0 0 1000 650">
            <!-- REGION PATHS -->
            <g id="regionsLayer">
{svg_regions_html}
            </g>

            <!-- REPUBLICAN CITY RETICLE PINS -->
            <g id="citiesLayer">
{svg_cities_html}
            </g>

            <!-- 23 NATIONAL PARKS & RESERVES PINS -->
            <g id="parksLayer">
{svg_parks_html}
            </g>
          </svg>
        </div>

        <!-- FLOATING TELEMETRY HUD -->
        <div id="telemetryHud" class="map-telemetry-hud">
          <div class="hud-header">
            <div id="hudTitle" class="hud-title">Карагандинская область</div>
            <div id="hudRating" class="hud-rating">AAA PRIME</div>
          </div>
          <div id="hudFocus" style="font-size: 11.5px; color: var(--text-muted);">Чёрная металлургия и угольный бассейн</div>
          <div class="hud-metric-row">
            <div>
              <div class="hud-metric-label">Центр</div>
              <div id="hudCenter" class="hud-metric-val">г. Караганда</div>
            </div>
            <div>
              <div class="hud-metric-label">Доля в пром. РК</div>
              <div id="hudShare" class="hud-metric-val">~9.5%</div>
            </div>
          </div>
        </div>

        <!-- ZOOM & RECENTER CONTROLS -->
        <div class="map-controls-panel">
          <button id="zoomInBtn" class="map-btn" title="Приблизить">+</button>
          <button id="zoomOutBtn" class="map-btn" title="Отдалить">−</button>
          <button id="zoomResetBtn" class="map-btn" title="Сбросить 3D вид" style="font-size: 11px;">100%</button>
        </div>
      </div>

      <!-- 2. MATRIX GRID VIEW (TOGGLEABLE) -->
      <div id="matrixStage" class="matrix-grid-view"></div>
    </main>
  </div>

  <!-- FLOATING MAP TOOLTIP -->
  <div id="geoTooltip" class="geo-tooltip">
    <div id="tooltipName" class="tooltip-name"></div>
    <div id="tooltipCenter" class="tooltip-center"></div>
    <div id="tooltipFocus" class="tooltip-focus"></div>
  </div>

  <!-- 3D ANIMAL SHOWCASE & HOLOGRAPHIC INSPECTOR -->
  <div id="animalHologramCard" class="animal-hologram-card">
    <div class="animal-card-header">
      <div>
        <div id="animalParkName" class="animal-park-name">Иле-Алатауский национальный парк</div>
        <div id="animalParkRegion" class="animal-park-region">Алматинская область • Основан в 1996 г.</div>
      </div>
      <div id="animalTypeBadge" class="animal-type-badge">ГНПП</div>
    </div>

    <!-- 3D Canvas / Photo Viewer -->
    <div class="animal-visual-stage" id="animalVisualStage">
      <div id="animal3DCanvasWrap" class="animal-3d-canvas-wrap"></div>
      <img id="animalPhotoView" class="animal-photo-view" src="" alt="Fauna photograph" referrerpolicy="no-referrer">
      <div class="visual-toggle-bar">
        <button id="btnView3D" class="visual-toggle-btn active">3D Модель</button>
        <button id="btnViewPhoto" class="visual-toggle-btn">Фото</button>
      </div>
    </div>

    <!-- Biological Data -->
    <div class="animal-bio-info">
      <div class="animal-name-title">
        <span id="animalName">Снежный барс (Ирбис)</span>
      </div>
      <div id="animalLatin" class="animal-latin">Panthera uncia</div>
      <div id="animalRedBook" class="animal-redbook">Красная книга РК: I категория (исчезающий вид)</div>
      <div id="animalFact" class="animal-fact">Обитает на альпийских скалах Заилийского Алатау...</div>
    </div>

    <div class="animal-card-actions">
      <button id="animalOpenRegionBtn" class="animal-link-btn">Открыть досье региона →</button>
      <span style="font-size: 10px; color: var(--text-dim); font-family: var(--font-display);">3D WEBLAB // РК</span>
    </div>
  </div>

  <!-- EXECUTIVE DOSSIER MODAL -->
  <div id="dossierOverlay" class="dossier-overlay">
    <div class="dossier-modal-window">
      <div class="dossier-modal-top">
        <div class="dossier-breadcrumbs">
          <span>ҚАЗАҚСТАН</span>
          <span>/</span>
          <span>РЕГИОНАЛЬНЫЙ РЕЕСТР</span>
          <span>/</span>
          <span id="dossierCodeBadge" class="dossier-code-badge">KZ-KAR</span>
        </div>
        <div class="dossier-top-actions">
          <button id="closeDossierBtn" class="dossier-close-btn" title="Закрыть [Esc]">&times;</button>
        </div>
      </div>

      <div class="dossier-scroll-body">
        <div class="dossier-hero">
          <div class="dossier-titles">
            <h2 id="dossierName">Карагандинская область</h2>
            <div id="dossierKzName" class="dossier-kz-title">Qaraǵandy oblysy</div>
            <div id="dossierCenter" class="dossier-center-info">Административный центр: г. Караганда</div>
          </div>
          <div class="dossier-hero-badges">
            <div id="dossierInvRating" class="dossier-inv-tier">INVESTMENT GRADE: AAA PRIME</div>
            <div id="dossierTypeTag" class="dossier-type-tag">Индустриальный субъект РК</div>
          </div>
        </div>

        <div class="dossier-macro-strip">
          <div class="macro-tile">
            <div class="macro-tile-label">Территория</div>
            <div id="macroArea" class="macro-tile-val">239 045 км²</div>
            <div id="macroAreaCmp" class="macro-tile-sub">Крупнейший центр страны</div>
          </div>
          <div class="macro-tile">
            <div class="macro-tile-label">Население</div>
            <div id="macroPopulation" class="macro-tile-val">1 134 000 чел.</div>
            <div id="macroDensity" class="macro-tile-sub">Плотность: 4.7 чел/км²</div>
          </div>
          <div class="macro-tile">
            <div class="macro-tile-label">Урбанизация</div>
            <div id="macroUrbanRate" class="macro-tile-val">81.5%</div>
            <div class="macro-tile-sub">Высокий уровень индустриализации</div>
          </div>
          <div class="macro-tile">
            <div class="macro-tile-label">Вклад в пром. РК</div>
            <div id="macroIndShare" class="macro-tile-val">9.5%</div>
            <div class="macro-tile-sub">Системообразующий регион</div>
          </div>
        </div>

        <div id="dossierSummary" class="dossier-executive-summary"></div>

        <section class="dossier-section">
          <div class="dossier-section-title">
            <span>01 //</span> Системообразующие индустриальные гиганты
          </div>
          <div id="enterprisesContainer" class="enterprises-grid"></div>
        </section>

        <section class="dossier-section">
          <div class="dossier-section-title">
            <span>02 //</span> Природный каркас и биоразнообразие
          </div>
          <div class="nature-pillars">
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">Заповедники и ГНПП</div>
              <ul id="reservesList" class="nature-list"></ul>
            </div>
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">Краснокнижная фауна</div>
              <ul id="faunaList" class="nature-list"></ul>
            </div>
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">Ландшафты & Памятники</div>
              <ul id="landscapesList" class="nature-list"></ul>
            </div>
          </div>
        </section>

        <section class="dossier-section">
          <div class="dossier-section-title">
            <span>03 //</span> Фотографический фонд (Wikimedia Commons Verified)
          </div>
          <div id="galleryContainer" class="gallery-grid"></div>
        </section>
      </div>
    </div>
  </div>

  <!-- LIGHTBOX -->
  <div id="lightboxModal" class="lightbox-modal">
    <span id="lightboxClose" class="lightbox-close">&times;</span>
    <div class="lightbox-content">
      <img id="lightboxImg" class="lightbox-img" src="" alt="Dossier photograph" referrerpolicy="no-referrer">
      <div id="lightboxCaption" class="lightbox-caption"></div>
    </div>
  </div>

  <!-- EMBEDDED DATA & LOGIC -->
  <script>
    const DOSSIER_DATABASE = {db_json_embedded};
    const PARKS_DATABASE = {parks_json_embedded};

    class GeoEconomicAtlas3D {{
      constructor() {{
        this.db = DOSSIER_DATABASE;
        this.parks = PARKS_DATABASE;
        this.currentFilter = 'all';
        this.activeView = 'map';
        this.currentRegionId = 'karaganda';
        this.parksVisible = true;

        // 3D Orbit State
        this.rotX = 36;
        this.rotZ = -10;
        this.zoom = 1;
        this.isDragging = false;
        this.startX = 0;
        this.startY = 0;
        this.autoOrbit = false;
        this.autoOrbitAngle = -10;

        // Three.js State for Animal 3D Model
        this.threeScene = null;
        this.threeCamera = null;
        this.threeRenderer = null;
        this.threeCurrentMesh = null;
        this.activeAnimal = null;
        this.activeVisualTab = '3d';

        this.initDOMElements();
        this.init3DOrbitControls();
        this.initThreeJSViewer();
        this.initEventListeners();
        this.renderMatrixGrid();
        this.updateHUD('karaganda');
        this.apply3DTransform();
      }}

      initDOMElements() {{
        this.mapStageWrapper = document.getElementById('mapStageWrapper');
        this.map3DPlane = document.getElementById('map3DPlane');
        this.svgAtlas = document.getElementById('svgAtlas');
        this.tooltip = document.getElementById('geoTooltip');
        this.tooltipName = document.getElementById('tooltipName');
        this.tooltipCenter = document.getElementById('tooltipCenter');
        this.tooltipFocus = document.getElementById('tooltipFocus');

        this.hudTitle = document.getElementById('hudTitle');
        this.hudRating = document.getElementById('hudRating');
        this.hudFocus = document.getElementById('hudFocus');
        this.hudCenter = document.getElementById('hudCenter');
        this.hudShare = document.getElementById('hudShare');

        this.matrixStage = document.getElementById('matrixStage');
        this.viewToggleBtn = document.getElementById('viewToggleBtn');
        this.viewToggleText = document.getElementById('viewToggleText');
        this.viewToggleIcon = document.getElementById('viewToggleIcon');

        this.dossierOverlay = document.getElementById('dossierOverlay');
        this.closeDossierBtn = document.getElementById('closeDossierBtn');
        this.subjectSearch = document.getElementById('subjectSearch');
        this.searchDropdown = document.getElementById('searchDropdown');

        // Animal 3D Card Elements
        this.animalCard = document.getElementById('animalHologramCard');
        this.animalParkName = document.getElementById('animalParkName');
        this.animalParkRegion = document.getElementById('animalParkRegion');
        this.animalTypeBadge = document.getElementById('animalTypeBadge');
        this.animalName = document.getElementById('animalName');
        this.animalLatin = document.getElementById('animalLatin');
        this.animalRedBook = document.getElementById('animalRedBook');
        this.animalFact = document.getElementById('animalFact');
        this.animalPhotoView = document.getElementById('animalPhotoView');
        this.animal3DCanvasWrap = document.getElementById('animal3DCanvasWrap');
        this.btnView3D = document.getElementById('btnView3D');
        this.btnViewPhoto = document.getElementById('btnViewPhoto');
        this.animalOpenRegionBtn = document.getElementById('animalOpenRegionBtn');

        this.lightboxModal = document.getElementById('lightboxModal');
        this.lightboxImg = document.getElementById('lightboxImg');
        this.lightboxCaption = document.getElementById('lightboxCaption');
        this.lightboxClose = document.getElementById('lightboxClose');
      }}

      init3DOrbitControls() {{
        const wrapper = this.mapStageWrapper;

        wrapper.addEventListener('pointerdown', (e) => {{
          // Do not drag if clicking buttons or dropdowns
          if (e.target.closest('.map-3d-toolbar, .map-controls-panel, .map-telemetry-hud, .animal-hologram-card')) return;
          this.isDragging = true;
          this.startX = e.clientX;
          this.startY = e.clientY;
          wrapper.setPointerCapture(e.pointerId);
        }});

        wrapper.addEventListener('pointermove', (e) => {{
          if (!this.isDragging) return;
          const deltaX = e.clientX - this.startX;
          const deltaY = e.clientY - this.startY;
          this.startX = e.clientX;
          this.startY = e.clientY;

          this.rotZ += deltaX * 0.28;
          this.rotX = Math.max(0, Math.min(65, this.rotX - deltaY * 0.28));
          this.autoOrbit = false;
          this.update3DButtonState(null);
          this.apply3DTransform();
        }});

        const endDrag = (e) => {{
          if (this.isDragging) {{
            this.isDragging = false;
            try {{ wrapper.releasePointerCapture(e.pointerId); }} catch(_) {{}}
          }}
        }};
        wrapper.addEventListener('pointerup', endDrag);
        wrapper.addEventListener('pointercancel', endDrag);

        // Wheel Zoom
        wrapper.addEventListener('wheel', (e) => {{
          e.preventDefault();
          const delta = e.deltaY > 0 ? -0.1 : 0.1;
          this.zoom = Math.max(0.7, Math.min(2.2, this.zoom + delta));
          this.apply3DTransform();
        }}, {{ passive: false }});

        // Preset 3D Buttons
        document.getElementById('btn3DPerspective').addEventListener('click', () => {{
          this.rotX = 36; this.rotZ = -10; this.autoOrbit = false;
          this.update3DButtonState('btn3DPerspective');
          this.apply3DTransform();
        }});

        document.getElementById('btn3DIsometric').addEventListener('click', () => {{
          this.rotX = 55; this.rotZ = -28; this.autoOrbit = false;
          this.update3DButtonState('btn3DIsometric');
          this.apply3DTransform();
        }});

        document.getElementById('btn3DTopDown').addEventListener('click', () => {{
          this.rotX = 0; this.rotZ = 0; this.autoOrbit = false;
          this.update3DButtonState('btn3DTopDown');
          this.apply3DTransform();
        }});

        document.getElementById('btn3DAutoOrbit').addEventListener('click', () => {{
          this.autoOrbit = !this.autoOrbit;
          this.update3DButtonState(this.autoOrbit ? 'btn3DAutoOrbit' : null);
          if (this.autoOrbit) this.runAutoOrbit();
        }});

        document.getElementById('btnToggleParks').addEventListener('click', (e) => {{
          this.parksVisible = !this.parksVisible;
          document.getElementById('parksLayer').style.display = this.parksVisible ? 'block' : 'none';
          e.currentTarget.style.opacity = this.parksVisible ? '1' : '0.4';
        }});
      }}

      update3DButtonState(activeId) {{
        document.querySelectorAll('.map-3d-btn').forEach(btn => {{
          if (btn.id === 'btnToggleParks') return;
          btn.classList.toggle('active', btn.id === activeId);
        }});
      }}

      runAutoOrbit() {{
        if (!this.autoOrbit) return;
        this.rotZ += 0.15;
        this.apply3DTransform();
        requestAnimationFrame(() => this.runAutoOrbit());
      }}

      apply3DTransform() {{
        this.map3DPlane.style.transform = `rotateX(${{this.rotX.toFixed(1)}}deg) rotateZ(${{this.rotZ.toFixed(1)}}deg) scale(${{this.zoom.toFixed(2)}})`;
      }}

      /* ==========================================================================
         THREE.JS 3D ANIMAL PROCEDURAL ENGINE
         ========================================================================== */
      initThreeJSViewer() {{
        if (typeof THREE === 'undefined') return;
        const container = this.animal3DCanvasWrap;
        const width = 328;
        const height = 190;

        this.threeScene = new THREE.Scene();
        this.threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
        this.threeCamera.position.set(0, 1.2, 3.8);

        this.threeRenderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        this.threeRenderer.setSize(width, height);
        this.threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(this.threeRenderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        this.threeScene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xe5c364, 1.8, 20);
        pointLight.position.set(2, 4, 3);
        this.threeScene.add(pointLight);

        const fillLight = new THREE.PointLight(0x10b981, 1.2, 20);
        fillLight.position.set(-3, -1, -2);
        this.threeScene.add(fillLight);

        // User drag rotation inside animal canvas
        let isModelDragging = false;
        let prevX = 0;
        this.threeRenderer.domElement.addEventListener('pointerdown', (e) => {{
          isModelDragging = true;
          prevX = e.clientX;
        }});
        window.addEventListener('pointermove', (e) => {{
          if (!isModelDragging || !this.threeCurrentMesh) return;
          const dx = e.clientX - prevX;
          prevX = e.clientX;
          this.threeCurrentMesh.rotation.y += dx * 0.02;
        }});
        window.addEventListener('pointerup', () => isModelDragging = false);

        // Continuous render loop
        const animate = () => {{
          requestAnimationFrame(animate);
          if (this.threeCurrentMesh) {{
            if (!isModelDragging) {{
              this.threeCurrentMesh.rotation.y += 0.012;
            }}
          }}
          this.threeRenderer.render(this.threeScene, this.threeCamera);
        }};
        animate();
      }}

      buildAnimalProceduralGeometry(modelType, colorHex) {{
        if (!THREE) return new THREE.Group();
        const root = new THREE.Group();
        const color = new THREE.Color(colorHex || 0x10b981);

        const mat = new THREE.MeshStandardMaterial({{
          color: color,
          metalness: 0.65,
          roughness: 0.25,
          flatShading: true
        }});

        const wireMat = new THREE.MeshBasicMaterial({{
          color: 0xffffff,
          wireframe: true,
          transparent: true,
          opacity: 0.25
        }});

        const addPart = (geom, x=0, y=0, z=0, rx=0, ry=0, rz=0) => {{
          const m1 = new THREE.Mesh(geom, mat);
          const m2 = new THREE.Mesh(geom, wireMat);
          const g = new THREE.Group();
          g.add(m1); g.add(m2);
          g.position.set(x, y, z);
          g.rotation.set(rx, ry, rz);
          root.add(g);
          return g;
        }};

        if (modelType === 'feline') {{
          // SNOW LEOPARD / LYNX
          addPart(new THREE.CylinderGeometry(0.35, 0.45, 1.4, 8), 0, 0, 0, 1.57); // Torso
          addPart(new THREE.ConeGeometry(0.3, 0.5, 6), 0, 0.35, 0.75, 0.4); // Neck
          addPart(new THREE.DodecahedronGeometry(0.38), 0, 0.6, 0.95); // Head
          addPart(new THREE.ConeGeometry(0.12, 0.25, 4), -0.22, 0.95, 0.95, 0, 0, -0.3); // Left Ear
          addPart(new THREE.ConeGeometry(0.12, 0.25, 4), 0.22, 0.95, 0.95, 0, 0, 0.3); // Right Ear
          // 4 Legs
          addPart(new THREE.CylinderGeometry(0.1, 0.08, 0.8, 6), -0.28, -0.5, 0.5);
          addPart(new THREE.CylinderGeometry(0.1, 0.08, 0.8, 6), 0.28, -0.5, 0.5);
          addPart(new THREE.CylinderGeometry(0.12, 0.09, 0.8, 6), -0.3, -0.5, -0.5);
          addPart(new THREE.CylinderGeometry(0.12, 0.09, 0.8, 6), 0.3, -0.5, -0.5);
          // Long curled tail
          addPart(new THREE.CylinderGeometry(0.08, 0.05, 1.2, 6), 0, 0.2, -0.9, -0.8);
        }} else if (modelType === 'bird') {{
          // FLAMINGO / EAGLE / GULL
          addPart(new THREE.SphereGeometry(0.4, 8, 6), 0, 0, 0); // Torso
          addPart(new THREE.CylinderGeometry(0.08, 0.12, 0.8, 6), 0, 0.45, 0.25, 0.3); // Neck
          addPart(new THREE.ConeGeometry(0.18, 0.45, 6), 0, 0.85, 0.45, -1.4); // Head & Beak
          // Outstretched Wings
          addPart(new THREE.BoxGeometry(1.6, 0.06, 0.5), -0.9, 0.1, 0, 0, 0, 0.15); // Left Wing
          addPart(new THREE.BoxGeometry(1.6, 0.06, 0.5), 0.9, 0.1, 0, 0, 0, -0.15); // Right Wing
          addPart(new THREE.CylinderGeometry(0.04, 0.03, 0.9, 4), -0.12, -0.6, 0); // Leg 1
          addPart(new THREE.CylinderGeometry(0.04, 0.03, 0.9, 4), 0.12, -0.6, 0); // Leg 2
        }} else if (modelType === 'ungulate') {{
          // KULAN / SAIGA / ARGALI / MARAL / IBEX
          addPart(new THREE.CylinderGeometry(0.4, 0.45, 1.5, 8), 0, 0, 0, 1.57); // Torso
          addPart(new THREE.CylinderGeometry(0.18, 0.25, 0.75, 6), 0, 0.45, 0.65, 0.5); // Neck
          addPart(new THREE.BoxGeometry(0.35, 0.4, 0.55), 0, 0.85, 0.85); // Head
          // Majestic Horns
          addPart(new THREE.TorusGeometry(0.45, 0.08, 6, 12, Math.PI), -0.3, 1.15, 0.7, 0, 1.2, 0.8); // Left Horn
          addPart(new THREE.TorusGeometry(0.45, 0.08, 6, 12, Math.PI), 0.3, 1.15, 0.7, 0, -1.2, -0.8); // Right Horn
          // 4 Legs
          addPart(new THREE.CylinderGeometry(0.09, 0.07, 1.0, 6), -0.25, -0.6, 0.55);
          addPart(new THREE.CylinderGeometry(0.09, 0.07, 1.0, 6), 0.25, -0.6, 0.55);
          addPart(new THREE.CylinderGeometry(0.1, 0.08, 1.0, 6), -0.27, -0.6, -0.55);
          addPart(new THREE.CylinderGeometry(0.1, 0.08, 1.0, 6), 0.27, -0.6, -0.55);
        }} else if (modelType === 'bear') {{
          // BROWN BEAR
          addPart(new THREE.SphereGeometry(0.65, 8, 8), 0, 0, 0); // Body
          addPart(new THREE.SphereGeometry(0.55, 8, 8), 0, 0.25, 0.55); // Shoulders
          addPart(new THREE.DodecahedronGeometry(0.4), 0, 0.45, 0.95); // Broad Head
          addPart(new THREE.SphereGeometry(0.12, 6, 6), -0.3, 0.75, 0.95); // Left Ear
          addPart(new THREE.SphereGeometry(0.12, 6, 6), 0.3, 0.75, 0.95); // Right Ear
          // 4 Heavy Paws
          addPart(new THREE.CylinderGeometry(0.2, 0.16, 0.75, 6), -0.35, -0.45, 0.45);
          addPart(new THREE.CylinderGeometry(0.2, 0.16, 0.75, 6), 0.35, -0.45, 0.45);
          addPart(new THREE.CylinderGeometry(0.22, 0.17, 0.75, 6), -0.38, -0.45, -0.45);
          addPart(new THREE.CylinderGeometry(0.22, 0.17, 0.75, 6), 0.38, -0.45, -0.45);
        }} else {{
          // RODENT / MARMOT (Sitting upright)
          addPart(new THREE.CylinderGeometry(0.35, 0.5, 0.9, 8), 0, 0, 0); // Torso upright
          addPart(new THREE.SphereGeometry(0.32, 8, 8), 0, 0.55, 0.05); // Head
          addPart(new THREE.BoxGeometry(0.15, 0.35, 0.12), -0.25, 0.2, 0.25, -0.6); // Front Left Paw
          addPart(new THREE.BoxGeometry(0.15, 0.35, 0.12), 0.25, 0.2, 0.25, -0.6); // Front Right Paw
          addPart(new THREE.SphereGeometry(0.22, 6, 6), -0.3, -0.4, 0); // Hind leg
          addPart(new THREE.SphereGeometry(0.22, 6, 6), 0.3, -0.4, 0); // Hind leg
        }}

        root.position.y = -0.2;
        return root;
      }}

      showAnimalShowcase(parkId, event) {{
        const park = this.parks.find(p => p.id === parkId);
        if (!park) return;
        this.activeAnimal = park;

        // Populate Card Data
        this.animalParkName.textContent = park.name;
        this.animalParkRegion.textContent = park.regionName + ' • ' + park.areaKm2;
        this.animalTypeBadge.textContent = park.type === 'park' ? 'ГНПП' : 'ЗАПОВЕДНИК';
        this.animalTypeBadge.style.color = park.type === 'park' ? '#34d399' : '#f59e0b';

        const a = park.animal;
        this.animalName.textContent = a.name;
        this.animalLatin.textContent = a.latin;
        this.animalRedBook.textContent = a.category;
        this.animalFact.textContent = a.population;
        this.animalPhotoView.src = a.imageUrl;

        // Build 3D Model in Three.js Scene
        if (this.threeScene) {{
          if (this.threeCurrentMesh) {{
            this.threeScene.remove(this.threeCurrentMesh);
          }}
          this.threeCurrentMesh = this.buildAnimalProceduralGeometry(a.modelType, a.modelColor);
          this.threeScene.add(this.threeCurrentMesh);
        }}

        // Position Card beside event or pin
        let x = event ? event.clientX : window.innerWidth / 2;
        let y = event ? event.clientY : window.innerHeight / 2;
        // Clamp card to screen boundaries
        x = Math.max(190, Math.min(window.innerWidth - 190, x));
        y = Math.max(340, Math.min(window.innerHeight - 30, y));

        this.animalCard.style.left = x + 'px';
        this.animalCard.style.top = y + 'px';
        this.animalCard.classList.add('visible');

        this.setVisualTab('3d');
      }}

      hideAnimalShowcase() {{
        this.animalCard.classList.remove('visible');
      }}

      setVisualTab(tab) {{
        this.activeVisualTab = tab;
        if (tab === '3d') {{
          this.animal3DCanvasWrap.style.display = 'block';
          this.animalPhotoView.style.display = 'none';
          this.btnView3D.classList.add('active');
          this.btnViewPhoto.classList.remove('active');
        }} else {{
          this.animal3DCanvasWrap.style.display = 'none';
          this.animalPhotoView.style.display = 'block';
          this.btnViewPhoto.classList.add('active');
          this.btnView3D.classList.remove('active');
        }}
      }}

      /* ==========================================================================
         STANDARD ATLAS CONTROLS & LISTENERS
         ========================================================================== */
      initEventListeners() {{
        // Region Hover & Click
        document.querySelectorAll('.geo-region').forEach(el => {{
          el.addEventListener('mouseenter', (e) => this.onRegionHover(e, el.dataset.id));
          el.addEventListener('mousemove', (e) => this.moveTooltip(e));
          el.addEventListener('mouseleave', () => this.hideTooltip());
          el.addEventListener('click', () => this.openDossier(el.dataset.id));
        }});

        // City Pins Hover & Click
        document.querySelectorAll('.city-pin').forEach(pin => {{
          pin.addEventListener('mouseenter', (e) => this.onRegionHover(e, pin.dataset.id));
          pin.addEventListener('mousemove', (e) => this.moveTooltip(e));
          pin.addEventListener('mouseleave', () => this.hideTooltip());
          pin.addEventListener('click', () => this.openDossier(pin.dataset.id));
        }});

        // 23 Nature Pins: Hover & Click -> Trigger 3D Animal Showcase
        document.querySelectorAll('.nature-pin').forEach(np => {{
          np.addEventListener('mouseenter', (e) => {{
            this.showAnimalShowcase(np.dataset.parkId, e);
          }});
          np.addEventListener('click', (e) => {{
            e.stopPropagation();
            this.showAnimalShowcase(np.dataset.parkId, e);
          }});
        }});

        // Close animal card when clicking outside
        document.addEventListener('click', (e) => {{
          if (!this.animalCard.contains(e.target) && !e.target.closest('.nature-pin')) {{
            this.hideAnimalShowcase();
          }}
        }});

        // Animal Visual Switcher (3D vs Photo)
        this.btnView3D.addEventListener('click', (e) => {{
          e.stopPropagation();
          this.setVisualTab('3d');
        }});
        this.btnViewPhoto.addEventListener('click', (e) => {{
          e.stopPropagation();
          this.setVisualTab('photo');
        }});

        // Animal Card -> Open Region Dossier
        this.animalOpenRegionBtn.addEventListener('click', () => {{
          if (this.activeAnimal) {{
            this.hideAnimalShowcase();
            this.openDossier(this.activeAnimal.regionId);
          }}
        }});

        // Filter Tabs
        document.querySelectorAll('.sector-tab').forEach(tab => {{
          tab.addEventListener('click', () => {{
            document.querySelectorAll('.sector-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            this.applyFilter(tab.dataset.filter);
          }});
        }});

        // View Mode Toggle
        this.viewToggleBtn.addEventListener('click', () => this.toggleViewMode());

        // Modal Close Events
        this.closeDossierBtn.addEventListener('click', () => this.closeDossier());
        this.dossierOverlay.addEventListener('click', (e) => {{
          if (e.target === this.dossierOverlay) this.closeDossier();
        }});
        window.addEventListener('keydown', (e) => {{
          if (e.key === 'Escape') {{
            this.closeDossier();
            this.closeLightbox();
            this.hideAnimalShowcase();
            this.searchDropdown.style.display = 'none';
          }}
        }});

        // Search Input
        this.subjectSearch.addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.addEventListener('click', (e) => {{
          if (!this.subjectSearch.contains(e.target) && !this.searchDropdown.contains(e.target)) {{
            this.searchDropdown.style.display = 'none';
          }}
        }});

        // Zoom Controls
        document.getElementById('zoomInBtn').addEventListener('click', () => {{
          this.zoom = Math.min(2.2, this.zoom + 0.15);
          this.apply3DTransform();
        }});
        document.getElementById('zoomOutBtn').addEventListener('click', () => {{
          this.zoom = Math.max(0.7, this.zoom - 0.15);
          this.apply3DTransform();
        }});
        document.getElementById('zoomResetBtn').addEventListener('click', () => {{
          this.zoom = 1; this.rotX = 36; this.rotZ = -10; this.autoOrbit = false;
          this.update3DButtonState('btn3DPerspective');
          this.apply3DTransform();
        }});

        // Lightbox
        this.lightboxClose.addEventListener('click', () => this.closeLightbox());
        this.lightboxModal.addEventListener('click', (e) => {{
          if (e.target === this.lightboxModal) this.closeLightbox();
        }});
      }}

      onRegionHover(e, id) {{
        const data = this.db[id];
        if (!data) return;
        this.tooltipName.textContent = data.name;
        this.tooltipCenter.textContent = 'Центр: ' + data.center;
        this.tooltipFocus.textContent = data.focus;
        this.tooltip.classList.add('visible');
        this.moveTooltip(e);
        this.updateHUD(id);
      }}

      moveTooltip(e) {{
        this.tooltip.style.left = e.clientX + 'px';
        this.tooltip.style.top = (e.clientY - 12) + 'px';
      }}

      hideTooltip() {{
        this.tooltip.classList.remove('visible');
      }}

      updateHUD(id) {{
        const d = this.db[id];
        if (!d) return;
        this.hudTitle.textContent = d.name;
        this.hudRating.textContent = d.invRating || 'AAA PRIME';
        this.hudFocus.textContent = d.focus;
        this.hudCenter.textContent = 'г. ' + d.center;
        this.hudShare.textContent = d.indShare || '—';
      }}

      applyFilter(category) {{
        this.currentFilter = category;
        const regions = document.querySelectorAll('.geo-region');
        const pins = document.querySelectorAll('.city-pin');
        const parksLayer = document.getElementById('parksLayer');

        if (category === 'parks') {{
          parksLayer.style.display = 'block';
          regions.forEach(r => r.classList.remove('dimmed', 'highlighted'));
          pins.forEach(p => p.style.opacity = '0.3');
          return;
        }}

        if (category === 'all') {{
          regions.forEach(r => r.classList.remove('dimmed', 'highlighted'));
          pins.forEach(p => p.style.opacity = '1');
        }} else {{
          regions.forEach(r => {{
            const tags = (r.dataset.tags || '').split(' ');
            if (tags.includes(category)) {{
              r.classList.remove('dimmed');
              r.classList.add('highlighted');
            }} else {{
              r.classList.remove('highlighted');
              r.classList.add('dimmed');
            }}
          }});
          pins.forEach(p => {{
            const tags = (p.dataset.tags || '').split(' ');
            p.style.opacity = tags.includes(category) ? '1' : '0.2';
          }});
        }}
      }}

      toggleViewMode() {{
        if (this.activeView === 'map') {{
          this.activeView = 'matrix';
          this.mapStageWrapper.style.display = 'none';
          this.matrixStage.style.display = 'grid';
          this.viewToggleText.textContent = '3D Карта';
          this.viewToggleIcon.textContent = '◰';
        }} else {{
          this.activeView = 'map';
          this.mapStageWrapper.style.display = 'flex';
          this.matrixStage.style.display = 'none';
          this.viewToggleText.textContent = 'Сводная матрица';
          this.viewToggleIcon.textContent = '⊞';
          this.apply3DTransform();
        }}
      }}

      renderMatrixGrid() {{
        this.matrixStage.innerHTML = '';
        Object.values(this.db).forEach(item => {{
          const card = document.createElement('div');
          card.className = 'matrix-card';
          card.dataset.tags = item.filterTags.join(' ');
          card.onclick = () => this.openDossier(item.id);

          card.innerHTML = `
            <div>
              <div class="matrix-card-header">
                <div>
                  <div class="matrix-card-title">${{item.name}}</div>
                  <div class="matrix-card-kz">${{item.nameKz}}</div>
                </div>
                <div class="matrix-card-rating">${{item.invRating}}</div>
              </div>
              <div class="matrix-card-focus">${{item.focus}}</div>
            </div>
            <div>
              <div class="matrix-card-stats">
                <div class="matrix-stat-item">
                  <span class="matrix-stat-name">Центр</span>
                  <span class="matrix-stat-val">г. ${{item.center}}</span>
                </div>
                <div class="matrix-stat-item">
                  <span class="matrix-stat-name">Вклад в пром.</span>
                  <span class="matrix-stat-val">${{item.indShare}}</span>
                </div>
                <div class="matrix-stat-item">
                  <span class="matrix-stat-name">Население</span>
                  <span class="matrix-stat-val">${{item.population}}</span>
                </div>
                <div class="matrix-stat-item">
                  <span class="matrix-stat-name">Площадь</span>
                  <span class="matrix-stat-val">${{item.area}}</span>
                </div>
              </div>
              <div class="matrix-card-footer">
                <span>Код: KZ-${{item.id.slice(0,3).toUpperCase()}}</span>
                <span style="color: var(--gold-primary); font-family: var(--font-display); font-weight: 600;">Открыть досье →</span>
              </div>
            </div>
          `;
          this.matrixStage.appendChild(card);
        }});
      }}

      handleSearch(q) {{
        q = q.trim().toLowerCase();
        if (!q) {{
          this.searchDropdown.style.display = 'none';
          return;
        }}

        // Search in regions and national parks
        const regionMatches = Object.values(this.db).filter(item => 
          item.name.toLowerCase().includes(q) ||
          item.nameKz.toLowerCase().includes(q) ||
          item.center.toLowerCase().includes(q)
        ).slice(0, 4);

        const parkMatches = this.parks.filter(p =>
          p.name.toLowerCase().includes(q) ||
          p.animal.name.toLowerCase().includes(q)
        ).slice(0, 3);

        let html = '';
        regionMatches.forEach(m => {{
          html += `
            <div class="search-item" onclick="atlasApp.openDossier('${{m.id}}')">
              <div>
                <div class="search-item-title">${{m.name}}</div>
                <div class="search-item-sub">Центр: г. ${{m.center}} • ${{m.focus}}</div>
              </div>
              <div class="search-item-badge" style="color: var(--gold-primary); font-size: 11px;">${{m.invRating}}</div>
            </div>
          `;
        }});

        parkMatches.forEach(p => {{
          html += `
            <div class="search-item" onclick="atlasApp.showAnimalShowcase('${{p.id}}')">
              <div>
                <div class="search-item-title" style="color: var(--accent-emerald);">🌲 ${{p.name}}</div>
                <div class="search-item-sub">Фауна: ${{p.animal.name}} (${{p.regionName}})</div>
              </div>
              <div class="search-item-badge" style="color: var(--accent-emerald); font-size: 11px;">3D ФАУНА</div>
            </div>
          `;
        }});

        if (!html) {{
          html = '<div style="padding: 12px; color: var(--text-dim); text-align: center;">Совпадений не обнаружено</div>';
        }}
        this.searchDropdown.innerHTML = html;
        this.searchDropdown.style.display = 'block';
      }}

      openDossier(id) {{
        const item = this.db[id];
        if (!item) return;

        this.currentRegionId = id;
        this.searchDropdown.style.display = 'none';
        this.hideAnimalShowcase();

        document.getElementById('dossierCodeBadge').textContent = 'KZ-' + id.slice(0,3).toUpperCase();
        document.getElementById('dossierName').textContent = item.name;
        document.getElementById('dossierKzName').textContent = item.nameKz;
        document.getElementById('dossierCenter').textContent = 'Административный центр: г. ' + item.center;
        document.getElementById('dossierInvRating').textContent = 'INVESTMENT GRADE: ' + item.invRating;
        document.getElementById('dossierTypeTag').textContent = item.typeLabel;

        document.getElementById('macroArea').textContent = item.area;
        document.getElementById('macroAreaCmp').textContent = item.areaCmp;
        document.getElementById('macroPopulation').textContent = item.population;
        document.getElementById('macroDensity').textContent = 'Плотность: ' + item.density;
        document.getElementById('macroUrbanRate').textContent = item.urbanRate;
        document.getElementById('macroIndShare').textContent = item.indShare;

        document.getElementById('dossierSummary').textContent = item.summary;

        // Enterprises
        const entContainer = document.getElementById('enterprisesContainer');
        entContainer.innerHTML = item.enterprises.map(e => `
          <div class="enterprise-card">
            <div>
              <div class="enterprise-top">
                <div class="enterprise-title">${{e.title}}</div>
                <div class="enterprise-tag">${{e.tag}}</div>
              </div>
              <div class="enterprise-role" style="margin-top: 8px;">${{e.role}}</div>
            </div>
            <div class="enterprise-badge">${{e.badge}}</div>
          </div>
        `).join('');

        // Nature Pillars
        document.getElementById('reservesList').innerHTML = item.nature.reserves.map(r => `<li class="nature-list-item">${{r}}</li>`).join('');
        document.getElementById('faunaList').innerHTML = item.nature.fauna.map(f => `<li class="nature-list-item">${{f}}</li>`).join('');
        document.getElementById('landscapesList').innerHTML = item.nature.landscapes.map(l => `<li class="nature-list-item">${{l}}</li>`).join('');

        // Gallery
        this.renderGallery(item);

        this.dossierOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      }}

      closeDossier() {{
        this.dossierOverlay.classList.remove('active');
        document.body.style.overflow = '';
      }}

      renderGallery(item) {{
        const gallery = document.getElementById('galleryContainer');
        gallery.innerHTML = '';
        (item.images || []).forEach(img => {{
          const tile = document.createElement('div');
          tile.className = 'gallery-tile';
          tile.onclick = () => this.openLightbox(img.url, img.caption);
          tile.innerHTML = `
            <img class="gallery-img" src="${{img.url}}" alt="${{img.caption}}" loading="lazy" referrerpolicy="no-referrer">
            <div class="gallery-caption">
              <div>${{img.caption}}</div>
              <div style="font-size: 9.5px; color: var(--gold-primary);">Wikimedia Commons</div>
            </div>
          `;
          gallery.appendChild(tile);
        }});
      }}

      openLightbox(src, caption) {{
        this.lightboxImg.src = src;
        this.lightboxCaption.textContent = caption;
        this.lightboxModal.classList.add('active');
      }}

      closeLightbox() {{
        this.lightboxModal.classList.remove('active');
        this.lightboxImg.src = '';
      }}
    }}

    let atlasApp;
    window.addEventListener('DOMContentLoaded', () => {{
      atlasApp = new GeoEconomicAtlas3D();
    }});
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Site 2 (Qazaqstan 3D Geo-Economic Dossier) index.html updated successfully! Size:", os.path.getsize("index.html"), "bytes")

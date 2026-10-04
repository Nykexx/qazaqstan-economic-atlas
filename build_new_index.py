# -*- coding: utf-8 -*-
"""
Generator for QAZAQSTAN GEO-ECONOMIC DOSSIER (index.html)
Standalone single-file application with gold/obsidian theme, Space Grotesk + Manrope fonts,
dual view (Interactive SVG Map + Executive Matrix), and rich verified Wikimedia photo gallery.
"""
import json
import os

with open("dossier_db.json", "r", encoding="utf-8") as f:
    dossier_db = json.load(f)

# Build SVG markup for all regions and city markers
svg_regions_markup = []
svg_city_markers = []

for rid, rdata in dossier_db.items():
    path_d = rdata.get("svg_path", "")
    cx = rdata.get("center_x", 500)
    cy = rdata.get("center_y", 300)
    lx = rdata.get("label_x", cx)
    ly = rdata.get("label_y", cy)
    name = rdata.get("name", "")
    rtype = rdata.get("type", "region")
    tags_str = " ".join(rdata.get("filterTags", []))
    
    # Path element
    svg_regions_markup.append(f'''    <path class="geo-region" id="region-{rid}" data-id="{rid}" data-tags="{tags_str}" d="{path_d}">
      <title>{name}</title>
    </path>''')
    
    # If city or has custom label
    if rtype == "city":
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

svg_regions_html = "\n".join(svg_regions_markup)
svg_cities_html = "\n".join(svg_city_markers)
db_json_embedded = json.dumps(dossier_db, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>QAZAQSTAN // НАЦИОНАЛЬНЫЙ ГЕОЭКОНОМИЧЕСКИЙ РЕЕСТР И АТЛАС</title>
  
  <!-- Fonts: Space Grotesk (headings & tech badges) & Manrope (editorial body) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

  <style>
    /* ==========================================================================
       DESIGN SYSTEM: OBSIDIAN & CHAMPAGNE GOLD (EXECUTIVE OBSERVATORY)
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
      --gold-glow: rgba(229, 195, 100, 0.25);
      --text-main: #f3f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-emerald: #10b981;
      --accent-ruby: #f43f5e;
      --accent-amber: #f59e0b;
      --font-display: 'Space Grotesk', -apple-system, sans-serif;
      --font-body: 'Manrope', -apple-system, sans-serif;
      --shadow-lux: 0 20px 45px -10px rgba(0, 0, 0, 0.7), 0 0 30px rgba(229, 195, 100, 0.08);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
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

    /* Subtle background grid pattern */
    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(229, 195, 100, 0.06) 0%, transparent 60%),
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

    /* ==========================================================================
       1. TOP EXECUTIVE HEADER & TICKER
       ========================================================================== */
    .top-dossier-bar {{
      background: rgba(11, 17, 28, 0.85);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      position: sticky;
      top: 0;
      z-index: 50;
    }}

    .ticker-ribbon {{
      background: rgba(5, 8, 14, 0.95);
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
      max-width: 580px;
      justify-content: flex-end;
    }}

    .search-box-wrapper {{
      position: relative;
      flex: 1;
      max-width: 360px;
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

    .search-item-badge {{
      font-size: 11px;
      color: var(--gold-primary);
      font-family: var(--font-display);
    }}

    .view-toggle-btn {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      height: 38px;
      padding: 0 16px;
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

    /* ==========================================================================
       2. SECTOR FILTER LEDGER
       ========================================================================== */
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
       3. WORKSPACE / DUAL VIEW (MAP & MATRIX)
       ========================================================================== */
    .workspace-container {{
      flex: 1;
      display: flex;
      flex-direction: column;
      position: relative;
    }}

    /* MAP VIEW */
    .map-stage-wrapper {{
      position: relative;
      flex: 1;
      min-height: calc(100vh - 120px);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      padding: 16px;
    }}

    .svg-atlas-viewport {{
      width: 100%;
      height: 100%;
      max-height: 82vh;
      filter: drop-shadow(0 15px 35px rgba(0, 0, 0, 0.8));
      user-select: none;
    }}

    /* Map Regions */
    .geo-region {{
      fill: #0d1524;
      stroke: var(--gold-primary);
      stroke-width: 1.15;
      stroke-opacity: 0.4;
      vector-effect: non-scaling-stroke;
      cursor: pointer;
      transition: fill 0.22s ease, stroke 0.22s ease, stroke-width 0.22s ease, filter 0.22s ease;
    }}

    .geo-region:hover {{
      fill: rgba(229, 195, 100, 0.28);
      stroke: var(--gold-bright);
      stroke-width: 2.2;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 12px rgba(229, 195, 100, 0.6));
    }}

    .geo-region.dimmed {{
      opacity: 0.22;
      fill: #060a12;
      stroke-opacity: 0.15;
    }}

    .geo-region.highlighted {{
      fill: rgba(229, 195, 100, 0.35);
      stroke: var(--gold-bright);
      stroke-width: 2.4;
      stroke-opacity: 1;
      filter: drop-shadow(0 0 14px rgba(229, 195, 100, 0.7));
    }}

    /* City Markers - STABLE HITBOXES, ZERO JITTER */
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
      box-shadow: 0 0 10px var(--gold-bright);
    }}

    .pin-tag {{
      pointer-events: none;
      transition: opacity 0.2s, transform 0.2s;
    }}

    .pin-tag-bg {{
      fill: rgba(8, 12, 20, 0.88);
      stroke: var(--border-bright);
      stroke-width: 1;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.6));
    }}

    .pin-tag-text {{
      fill: #ffffff;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}

    .city-pin:hover .pin-diamond {{
      stroke: #ffffff;
      fill: var(--gold-primary);
    }}

    .city-pin:hover .pin-tag-bg {{
      fill: var(--gold-primary);
      stroke: #ffffff;
    }}

    .city-pin:hover .pin-tag-text {{
      fill: #05080e;
    }}

    /* FLOATING TELEMETRY HUD (BOTTOM-LEFT) */
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
      transition: opacity 0.2s ease, transform 0.2s ease;
      z-index: 10;
    }}

    .hud-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
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
      letter-spacing: 0.04em;
    }}

    .hud-metric-val {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--gold-primary);
    }}

    /* FLOATING MAP CONTROLS */
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

    /* MATRIX GRID VIEW (ALTERNATIVE VIEW) */
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

    .matrix-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
      opacity: 0;
      transition: opacity 0.25s;
    }}

    .matrix-card:hover {{
      border-color: var(--gold-primary);
      transform: translateY(-4px);
      box-shadow: var(--shadow-lux);
    }}

    .matrix-card:hover::before {{
      opacity: 1;
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
      line-height: 1.3;
    }}

    .matrix-card-kz {{
      font-size: 11px;
      color: var(--text-dim);
      margin-top: 2px;
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
      white-space: nowrap;
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

    .matrix-stat-item {{
      display: flex;
      flex-direction: column;
    }}

    .matrix-stat-name {{
      font-size: 10px;
      text-transform: uppercase;
      color: var(--text-dim);
      letter-spacing: 0.03em;
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

    .matrix-action-link {{
      color: var(--gold-primary);
      font-family: var(--font-display);
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}

    /* ==========================================================================
       4. EXECUTIVE DOSSIER MODAL (SLIDE-OVER / FULLSCREEN)
       ========================================================================== */
    .dossier-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(4, 6, 10, 0.82);
      backdrop-filter: blur(16px);
      z-index: 1000;
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

    /* Modal Header Bar */
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

    .dossier-top-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
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

    /* Modal Scrollable Body */
    .dossier-scroll-body {{
      flex: 1;
      overflow-y: auto;
      padding: 32px 36px;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}

    /* Custom Scrollbar */
    .dossier-scroll-body::-webkit-scrollbar {{
      width: 6px;
    }}
    .dossier-scroll-body::-webkit-scrollbar-track {{
      background: rgba(0, 0, 0, 0.2);
    }}
    .dossier-scroll-body::-webkit-scrollbar-thumb {{
      background: rgba(229, 195, 100, 0.25);
      border-radius: 3px;
    }}
    .dossier-scroll-body::-webkit-scrollbar-thumb:hover {{
      background: var(--gold-primary);
    }}

    /* Hero Banner of Subject */
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
      letter-spacing: 0.02em;
    }}

    .dossier-titles .dossier-center-info {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
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
      letter-spacing: 0.04em;
    }}

    .dossier-type-tag {{
      font-family: var(--font-display);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--gold-bright);
      background: rgba(229, 195, 100, 0.08);
      border: 1px solid rgba(229, 195, 100, 0.2);
      padding: 4px 10px;
      border-radius: var(--radius-sm);
    }}

    /* Key Macroeconomic Strip */
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
      position: relative;
    }}

    .macro-tile-label {{
      font-size: 11px;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.04em;
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

    /* Dossier Summary Box */
    .dossier-executive-summary {{
      background: linear-gradient(135deg, rgba(229, 195, 100, 0.05), rgba(11, 17, 28, 0.6));
      border-left: 3px solid var(--gold-primary);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 18px 24px;
      font-size: 14px;
      line-height: 1.7;
      color: var(--text-main);
    }}

    /* Section Headings */
    .dossier-section {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}

    .dossier-section-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 8px;
    }}

    .dossier-section-title {{
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 700;
      letter-spacing: 0.03em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .dossier-section-title span {{
      color: var(--gold-primary);
      font-size: 14px;
    }}

    /* Enterprise Cards Grid */
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
      line-height: 1.35;
    }}

    .enterprise-tag {{
      font-size: 10px;
      font-family: var(--font-display);
      color: var(--gold-primary);
      background: rgba(229, 195, 100, 0.12);
      border: 1px solid rgba(229, 195, 100, 0.25);
      padding: 2px 7px;
      border-radius: 4px;
      white-space: nowrap;
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

    /* Nature & Ecology 3-Column Layout */
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
      letter-spacing: 0.04em;
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
      line-height: 1.45;
    }}

    .nature-list-item::before {{
      content: "◆";
      color: var(--gold-dim);
      font-size: 9px;
      margin-top: 4px;
    }}

    /* Photographic Archive & Gallery */
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
      text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }}

    .gallery-source {{
      font-size: 9.5px;
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    /* Lightbox Modal */
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
      box-shadow: 0 0 40px rgba(0,0,0,0.9);
    }}

    .lightbox-caption {{
      font-family: var(--font-display);
      color: var(--text-main);
      font-size: 14px;
      text-align: center;
    }}

    .lightbox-close {{
      position: absolute;
      top: 24px;
      right: 28px;
      color: #ffffff;
      font-size: 32px;
      cursor: pointer;
      line-height: 1;
      transition: color 0.2s;
    }}

    .lightbox-close:hover {{
      color: var(--gold-primary);
    }}

    /* Tooltip */
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

    /* Responsive */
    @media (max-width: 900px) {{
      .header-main {{
        flex-direction: column;
        align-items: stretch;
      }}
      .header-actions {{
        max-width: 100%;
      }}
      .dossier-modal-window {{
        height: 98vh;
        width: 98vw;
      }}
      .dossier-scroll-body {{
        padding: 20px;
      }}
      .dossier-hero {{
        flex-direction: column;
      }}
      .dossier-hero-badges {{
        align-items: flex-start;
      }}
      .map-telemetry-hud {{
        display: none;
      }}
    }}
  </style>
</head>
<body>
  <div class="app-viewport">
    <!-- TOP EXECUTIVE DOSSIER BAR -->
    <header class="top-dossier-bar">
      <!-- MACRO TICKER RIBBON -->
      <div class="ticker-ribbon">
        <div class="ticker-items">
          <div class="ticker-item">
            <span class="ticker-dot"></span>
            <span>СУВЕРЕННЫЙ СТАТУС:</span>
            <span class="ticker-val">РЕСПУБЛИКА КАЗАХСТАН // 20 СУБЪЕКТОВ</span>
          </div>
          <div class="ticker-item">
            <span>ВВП:</span>
            <span class="ticker-val">\$265+ МЛРД (EST. 2024-2026)</span>
          </div>
          <div class="ticker-item">
            <span>ЛИДЕРЫ ЭКСПОРТА:</span>
            <span class="ticker-val">АТЫРАУ • АЛМАТЫ • КАРАГАНДА • МАНГИСТАУ</span>
          </div>
          <div class="ticker-item">
            <span>ГРАНИЦЫ:</span>
            <span class="ticker-val">100% АДМИНИСТРАТИВНАЯ СЕТКА 2023+ (УЛЫТАУ, АБАЙ, ЖЕТЫСУ)</span>
          </div>
        </div>
        <div class="ticker-item">
          <span>СИСТЕМА:</span>
          <span class="ticker-val">QAZAQSTAN OBS-GEO v2.6</span>
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
            <h1>QAZAQSTAN <span>// GEO-ECONOMIC DOSSIER</span></h1>
            <p>Национальный свод промышленных мощностей, природных экосистем и инвестиционных профилей</p>
          </div>
        </div>

        <div class="header-actions">
          <div class="search-box-wrapper">
            <input type="text" id="subjectSearch" class="search-input" placeholder="Поиск области, города или сектора..." autocomplete="off">
            <span class="search-badge">ESC</span>
            <div id="searchDropdown" class="search-dropdown"></div>
          </div>
          <button id="viewToggleBtn" class="view-toggle-btn">
            <span id="viewToggleIcon">⊞</span>
            <span id="viewToggleText">Сводная матрица</span>
          </button>
        </div>
      </div>

      <!-- SECTOR LEDGER FILTER TABS -->
      <nav class="filter-ribbon-bar">
        <button class="sector-tab active" data-filter="all">Все субъекты <span class="sector-count">20</span></button>
        <button class="sector-tab" data-filter="oilgas">Нефтегазовый комплекс <span class="sector-count">5</span></button>
        <button class="sector-tab" data-filter="metallurgy">Металлургия & Добыча <span class="sector-count">7</span></button>
        <button class="sector-tab" data-filter="uranium">Уран & Атомпром <span class="sector-count">3</span></button>
        <button class="sector-tab" data-filter="agro">Агропромышленный пояс <span class="sector-count">6</span></button>
        <button class="sector-tab" data-filter="coal">Уголь & Энергетика <span class="sector-count">4</span></button>
        <button class="sector-tab" data-filter="machinery">Машиностроение <span class="sector-count">4</span></button>
        <button class="sector-tab" data-filter="chem">Химическая отрасль <span class="sector-count">3</span></button>
      </nav>
    </header>

    <!-- WORKSPACE (MAP & MATRIX CONTAINER) -->
    <main class="workspace-container">
      <!-- 1. MAP VIEW -->
      <div id="mapStage" class="map-stage-wrapper">
        <svg id="svgAtlas" class="svg-atlas-viewport" viewBox="0 0 1000 650">
          <defs>
            <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>
          
          <!-- REGION PATHS -->
          <g id="regionsLayer">
{svg_regions_html}
          </g>

          <!-- REPUBLICAN CITY RETICLE PINS -->
          <g id="citiesLayer">
{svg_cities_html}
          </g>
        </svg>

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

        <!-- MAP ZOOM & POSITION CONTROLS -->
        <div class="map-controls-panel">
          <button id="zoomInBtn" class="map-btn" title="Приблизить">+</button>
          <button id="zoomOutBtn" class="map-btn" title="Отдалить">−</button>
          <button id="zoomResetBtn" class="map-btn" title="Сбросить масштаб" style="font-size: 11px;">100%</button>
        </div>
      </div>

      <!-- 2. MATRIX GRID VIEW (TOGGLEABLE) -->
      <div id="matrixStage" class="matrix-grid-view">
        <!-- Rendered by JS -->
      </div>
    </main>
  </div>

  <!-- FLOATING MAP TOOLTIP -->
  <div id="geoTooltip" class="geo-tooltip">
    <div id="tooltipName" class="tooltip-name"></div>
    <div id="tooltipCenter" class="tooltip-center"></div>
    <div id="tooltipFocus" class="tooltip-focus"></div>
  </div>

  <!-- EXECUTIVE DOSSIER MODAL -->
  <div id="dossierOverlay" class="dossier-overlay">
    <div class="dossier-modal-window">
      <!-- Modal Top Bar -->
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

      <!-- Scrollable Dossier Content -->
      <div class="dossier-scroll-body">
        <!-- Hero Header -->
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

        <!-- Key Macroeconomic Indicators -->
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

        <!-- Executive Narrative Summary -->
        <div id="dossierSummary" class="dossier-executive-summary">
          <!-- Summary content -->
        </div>

        <!-- SECTION I: ENTERPRISES -->
        <section class="dossier-section">
          <div class="dossier-section-header">
            <h3 class="dossier-section-title">
              <span>01 //</span> Системообразующие индустриальные гиганты
            </h3>
          </div>
          <div id="enterprisesContainer" class="enterprises-grid">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- SECTION II: NATURE & ECOLOGY -->
        <section class="dossier-section">
          <div class="dossier-section-header">
            <h3 class="dossier-section-title">
              <span>02 //</span> Природный каркас и биоразнообразие
            </h3>
          </div>
          <div class="nature-pillars">
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 22h20L12 2z"></path>
                </svg>
                Заповедники и ГНПП
              </div>
              <ul id="reservesList" class="nature-list"></ul>
            </div>
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Краснокнижная фауна
              </div>
              <ul id="faunaList" class="nature-list"></ul>
            </div>
            <div class="nature-pillar-card">
              <div class="nature-pillar-head">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Ландшафты & Памятники
              </div>
              <ul id="landscapesList" class="nature-list"></ul>
            </div>
          </div>
        </section>

        <!-- SECTION III: MULTIMEDIA ARCHIVE -->
        <section class="dossier-section">
          <div class="dossier-section-header">
            <h3 class="dossier-section-title">
              <span>03 //</span> Фотографический фонд (Wikimedia Commons Verified)
            </h3>
          </div>
          <div id="galleryContainer" class="gallery-grid">
            <!-- Rendered by JS -->
          </div>
        </section>
      </div>
    </div>
  </div>

  <!-- LIGHTBOX VIEWER -->
  <div id="lightboxModal" class="lightbox-modal">
    <span id="lightboxClose" class="lightbox-close">&times;</span>
    <div class="lightbox-content">
      <img id="lightboxImg" class="lightbox-img" src="" alt="Dossier photograph" referrerpolicy="no-referrer">
      <div id="lightboxCaption" class="lightbox-caption"></div>
    </div>
  </div>

  <!-- DATA & LOGIC -->
  <script>
    const DOSSIER_DATABASE = {db_json_embedded};

    class GeoEconomicAtlas {{
      constructor() {{
        this.db = DOSSIER_DATABASE;
        this.currentFilter = 'all';
        this.activeView = 'map'; // 'map' or 'matrix'
        this.currentRegionId = 'karaganda';
        this.zoomLevel = 1;
        
        this.initDOMElements();
        this.initEventListeners();
        this.renderMatrixGrid();
        this.updateHUD('karaganda');
      }}

      initDOMElements() {{
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

        this.mapStage = document.getElementById('mapStage');
        this.matrixStage = document.getElementById('matrixStage');
        this.viewToggleBtn = document.getElementById('viewToggleBtn');
        this.viewToggleText = document.getElementById('viewToggleText');
        this.viewToggleIcon = document.getElementById('viewToggleIcon');

        this.dossierOverlay = document.getElementById('dossierOverlay');
        this.closeDossierBtn = document.getElementById('closeDossierBtn');
        this.subjectSearch = document.getElementById('subjectSearch');
        this.searchDropdown = document.getElementById('searchDropdown');

        this.lightboxModal = document.getElementById('lightboxModal');
        this.lightboxImg = document.getElementById('lightboxImg');
        this.lightboxCaption = document.getElementById('lightboxCaption');
        this.lightboxClose = document.getElementById('lightboxClose');
      }}

      initEventListeners() {{
        // Map Region Hover & Click
        document.querySelectorAll('.geo-region').forEach(el => {{
          el.addEventListener('mouseenter', (e) => this.onRegionHover(e, el.dataset.id));
          el.addEventListener('mousemove', (e) => this.moveTooltip(e));
          el.addEventListener('mouseleave', () => this.hideTooltip());
          el.addEventListener('click', () => this.openDossier(el.dataset.id));
        }});

        // City Pins Hover & Click (STATIC HITBOX PREVENTS JITTER)
        document.querySelectorAll('.city-pin').forEach(pin => {{
          pin.addEventListener('mouseenter', (e) => this.onRegionHover(e, pin.dataset.id));
          pin.addEventListener('mousemove', (e) => this.moveTooltip(e));
          pin.addEventListener('mouseleave', () => this.hideTooltip());
          pin.addEventListener('click', () => this.openDossier(pin.dataset.id));
        }});

        // Filter Tabs
        document.querySelectorAll('.sector-tab').forEach(tab => {{
          tab.addEventListener('click', () => {{
            document.querySelectorAll('.sector-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            this.applyFilter(tab.dataset.filter);
          }});
        }});

        // View Mode Toggle (Map vs Matrix)
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
            this.searchDropdown.style.display = 'none';
          }}
          if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {{
            e.preventDefault();
            this.subjectSearch.focus();
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
        document.getElementById('zoomInBtn').addEventListener('click', () => this.changeZoom(0.2));
        document.getElementById('zoomOutBtn').addEventListener('click', () => this.changeZoom(-0.2));
        document.getElementById('zoomResetBtn').addEventListener('click', () => this.resetZoom());

        // Lightbox Close
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

      changeZoom(delta) {{
        this.zoomLevel = Math.max(0.8, Math.min(2.2, this.zoomLevel + delta));
        this.svgAtlas.style.transform = `scale(${{this.zoomLevel}})`;
        this.svgAtlas.style.transition = 'transform 0.25s ease';
      }}

      resetZoom() {{
        this.zoomLevel = 1;
        this.svgAtlas.style.transform = 'scale(1)';
      }}

      applyFilter(category) {{
        this.currentFilter = category;
        const regions = document.querySelectorAll('.geo-region');
        const pins = document.querySelectorAll('.city-pin');

        if (category === 'all') {{
          regions.forEach(r => {{
            r.classList.remove('dimmed', 'highlighted');
          }});
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

        // Also filter matrix cards if matrix view is open
        document.querySelectorAll('.matrix-card').forEach(card => {{
          const tags = (card.dataset.tags || '').split(' ');
          if (category === 'all' || tags.includes(category)) {{
            card.style.display = 'flex';
          }} else {{
            card.style.display = 'none';
          }}
        }});
      }}

      toggleViewMode() {{
        if (this.activeView === 'map') {{
          this.activeView = 'matrix';
          this.mapStage.style.display = 'none';
          this.matrixStage.style.display = 'grid';
          this.viewToggleText.textContent = 'Интерактивная карта';
          this.viewToggleIcon.textContent = '◰';
        }} else {{
          this.activeView = 'map';
          this.mapStage.style.display = 'flex';
          this.matrixStage.style.display = 'none';
          this.viewToggleText.textContent = 'Сводная матрица';
          this.viewToggleIcon.textContent = '⊞';
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
                <span class="matrix-action-link">Открыть досье →</span>
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

        const matches = Object.values(this.db).filter(item => 
          item.name.toLowerCase().includes(q) ||
          item.nameKz.toLowerCase().includes(q) ||
          item.center.toLowerCase().includes(q) ||
          item.focus.toLowerCase().includes(q)
        ).slice(0, 6);

        if (matches.length === 0) {{
          this.searchDropdown.innerHTML = '<div style="padding: 12px; color: var(--text-dim); text-align: center;">Совпадений не обнаружено</div>';
        }} else {{
          this.searchDropdown.innerHTML = matches.map(m => `
            <div class="search-item" onclick="atlasApp.openDossier('${{m.id}}')">
              <div>
                <div class="search-item-title">${{m.name}}</div>
                <div class="search-item-sub">Центр: г. ${{m.center}} • ${{m.focus}}</div>
              </div>
              <div class="search-item-badge">${{m.invRating}}</div>
            </div>
          `).join('');
        }}
        this.searchDropdown.style.display = 'block';
      }}

      openDossier(id) {{
        const item = this.db[id];
        if (!item) return;

        this.currentRegionId = id;
        this.searchDropdown.style.display = 'none';

        // Fill Hero & Meta
        document.getElementById('dossierCodeBadge').textContent = 'KZ-' + id.slice(0,3).toUpperCase();
        document.getElementById('dossierName').textContent = item.name;
        document.getElementById('dossierKzName').textContent = item.nameKz;
        document.getElementById('dossierCenter').textContent = 'Административный центр: г. ' + item.center;
        document.getElementById('dossierInvRating').textContent = 'INVESTMENT GRADE: ' + item.invRating;
        document.getElementById('dossierTypeTag').textContent = item.typeLabel;

        // Fill Macro Metrics
        document.getElementById('macroArea').textContent = item.area;
        document.getElementById('macroAreaCmp').textContent = item.areaCmp;
        document.getElementById('macroPopulation').textContent = item.population;
        document.getElementById('macroDensity').textContent = 'Плотность: ' + item.density;
        document.getElementById('macroUrbanRate').textContent = item.urbanRate;
        document.getElementById('macroIndShare').textContent = item.indShare;

        // Fill Summary
        document.getElementById('dossierSummary').textContent = item.summary;

        // Fill Enterprises
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

        // Fill Nature Pillars
        const resList = document.getElementById('reservesList');
        resList.innerHTML = item.nature.reserves.map(r => `<li class="nature-list-item">${{r}}</li>`).join('');

        const fauList = document.getElementById('faunaList');
        fauList.innerHTML = item.nature.fauna.map(f => `<li class="nature-list-item">${{f}}</li>`).join('');

        const lndList = document.getElementById('landscapesList');
        lndList.innerHTML = item.nature.landscapes.map(l => `<li class="nature-list-item">${{l}}</li>`).join('');

        // Fill Verified Wikimedia Gallery + Dynamic Wikipedia Query
        this.renderGallery(item);

        // Show Modal
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

        // Verified Wikimedia Commons Images embedded in database
        const images = item.images || [];

        images.forEach(img => {{
          const tile = document.createElement('div');
          tile.className = 'gallery-tile';
          tile.onclick = () => this.openLightbox(img.url, img.caption);

          tile.innerHTML = `
            <img class="gallery-img" src="${{img.url}}" alt="${{img.caption}}" loading="lazy" referrerpolicy="no-referrer">
            <div class="gallery-caption">
              <div>${{img.caption}}</div>
              <div class="gallery-source">Wikimedia Commons</div>
            </div>
          `;
          gallery.appendChild(tile);
        }});

        // Dynamically fetch extra real high-res images from Wikipedia API if available
        if (item.wikiTitles && item.wikiTitles.length > 0) {{
          const titlesParam = encodeURIComponent(item.wikiTitles.join('|'));
          const apiUrl = `https://ru.wikipedia.org/w/api.php?action=query&titles=${{titlesParam}}&prop=pageimages&format=json&pithumbsize=800&origin=*`;
          
          fetch(apiUrl)
            .then(res => res.json())
            .then(data => {{
              if (data && data.query && data.query.pages) {{
                Object.values(data.query.pages).forEach(page => {{
                  if (page.thumbnail && page.thumbnail.source) {{
                    const tile = document.createElement('div');
                    tile.className = 'gallery-tile';
                    const caption = page.title;
                    tile.onclick = () => this.openLightbox(page.thumbnail.source, caption);
                    tile.innerHTML = `
                      <img class="gallery-img" src="${{page.thumbnail.source}}" alt="${{caption}}" loading="lazy" referrerpolicy="no-referrer">
                      <div class="gallery-caption">
                        <div>${{caption}}</div>
                        <div class="gallery-source">Wikipedia Public API</div>
                      </div>
                    `;
                    gallery.appendChild(tile);
                  }}
                }});
              }}
            }})
            .catch(err => console.log('Wiki API extra fetch deferred:', err));
        }}
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

    // Global application initialization
    let atlasApp;
    window.addEventListener('DOMContentLoaded', () => {{
      atlasApp = new GeoEconomicAtlas();
    }});
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated index.html successfully! Size:", os.path.getsize("index.html"), "bytes")

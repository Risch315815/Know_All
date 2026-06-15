#!/usr/bin/env python3
"""Wrap Self-Paid Medical Tx.html (EN) into Know_All domain page."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "自費醫療" / "Self-Paid Medical Tx.html"
OUT = ROOT / "domains" / "Self-Paid Medical Tx_TW" / "en.html"
TW_INDEX = ROOT / "domains" / "Self-Paid Medical Tx_TW" / "index.html"

TOC_LINKS = [
    ("cardiology", "Cardiology"),
    ("pulmonology", "Pulmonology"),
    ("gi", "Gastroenterology"),
    ("hepatobiliary", "Hepatobiliary"),
    ("metabolism", "Endocrinology & Metabolism"),
    ("rheumatology", "Rheumatology"),
    ("hematology", "Hematology"),
    ("oncology", "Oncology"),
    ("neurology", "Neurology"),
    ("surgery", "Surgery"),
    ("urology", "Urology"),
    ("orthopedics", "Orthopedics"),
    ("ophthalmology", "Ophthalmology"),
    ("ent", "ENT"),
    ("dermatology", "Dermatology"),
    ("psychiatry", "Psychiatry"),
    ("family-medicine", "Family Medicine"),
    ("hospital", "Hospital & Surgery Fees"),
    ("priority", "High-Priority Overview"),
    ("ltc", "Long-Term Care"),
    ("sources", "Data Sources"),
]

PAGE_STYLES = """
    .sub-title {
      font-size: 15px; font-weight: 600; color: var(--accent);
      margin: 20px 0 12px; padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }
    .note {
      background: rgba(124, 158, 248, 0.08);
      border-left: 3px solid var(--accent);
      padding: 12px 16px; margin-bottom: 16px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 13px; color: var(--text-muted);
    }
    .note p { margin: 4px 0; }
    .note ul { margin: 6px 0 0 1.2rem; }
    .note strong { color: var(--text); }
    .fx-banner {
      font-size: 12px; color: var(--text-dim); margin-top: 6px;
    }
    .table-wrap { overflow-x: auto; margin: 12px 0 20px; }
    .med-table {
      width: 100%; border-collapse: collapse; font-size: 12px;
      table-layout: fixed;
    }
    .med-table.cost th:nth-child(1), .med-table.cost td:nth-child(1) { width: 26%; line-height: 1.35; }
    .med-table.cost th:nth-child(2), .med-table.cost td:nth-child(2) { width: 9%; }
    .med-table.cost th:nth-child(3), .med-table.cost td:nth-child(3) { width: 7%; }
    .med-table.cost th:nth-child(4), .med-table.cost td:nth-child(4) { width: 7%; }
    .med-table.cost th:nth-child(5), .med-table.cost td:nth-child(5) { width: 9%; }
    .med-table.cost th:nth-child(6), .med-table.cost td:nth-child(6) { width: 42%; line-height: 1.35; font-size: 11px; }
    .med-table.cost td:nth-child(2), .med-table.cost td:nth-child(3),
    .med-table.cost td:nth-child(4), .med-table.cost td:nth-child(5) { white-space: nowrap; font-size: 11px; }
    #priority .med-table.cost th:nth-child(1), #priority .med-table.cost td:nth-child(1) { width: 7%; white-space: nowrap; }
    #priority .med-table.cost th:nth-child(2), #priority .med-table.cost td:nth-child(2) { width: 13%; }
    #priority .med-table.cost th:nth-child(3), #priority .med-table.cost td:nth-child(3) { width: 30%; }
    #priority .med-table.cost th:nth-child(4), #priority .med-table.cost td:nth-child(4) { width: 17%; }
    #priority .med-table.cost th:nth-child(5), #priority .med-table.cost td:nth-child(5) { width: 16%; }
    #priority .med-table.cost th:nth-child(6), #priority .med-table.cost td:nth-child(6) { width: 17%; }
    .med-table th, .med-table td {
      border: 1px solid var(--border); padding: 8px 10px;
      text-align: left; vertical-align: top;
    }
    .med-table th {
      background: var(--bg-surface); font-weight: 600;
      color: var(--text); white-space: nowrap;
    }
    .med-table tr:nth-child(even) td { background: rgba(255,255,255,0.02); }
    .med-table td.num { white-space: nowrap; font-variant-numeric: tabular-nums; }
    .summary-box {
      background: rgba(230, 168, 23, 0.1);
      border-left: 3px solid #e6a817;
      padding: 12px 16px; margin-bottom: 16px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 13px; color: var(--text-muted);
    }
    .page-footer-note {
      font-size: 12px; color: var(--text-dim); margin-top: 24px;
      padding-top: 16px; border-top: 1px solid var(--border);
    }
"""

SIDEBAR_TOC = "\n".join(
    f'          <a href="#{sid}" class="sidebar-link">{label}</a>'
    for sid, label in TOC_LINKS
)


def transform_content(html: str) -> str:
    m = re.search(r"<main>(.*)</main>", html, re.DOTALL)
    if not m:
        raise ValueError("Could not find <main> in source HTML")
    body = m.group(1)

    # drop standalone footer inside main
    body = re.sub(r"<footer>.*?</footer>", "", body, flags=re.DOTALL)

    # meta block
    body = body.replace('<div class="meta">', '<div class="note">')
    body = re.sub(r"<nav class=\"toc\">.*?</nav>", "", body, flags=re.DOTALL)

    # sections
    body = body.replace("<section ", '<section class="map-section" ')
    body = body.replace('class="map-section" id=', 'id=')
    body = body.replace('class="map-section" class="map-section"', 'class="map-section"')
    body = re.sub(
        r'<section id="([^"]+)">',
        r'<section class="map-section" id="\1">',
        body,
    )
    body = body.replace("<h2>", '<h2 class="map-title">')
    body = body.replace("<h3>", '<h3 class="sub-title">')
    body = body.replace('class="map-title" class="map-title"', 'class="map-title"')
    body = body.replace('class="sub-title" class="sub-title"', 'class="sub-title"')

    # tables
    body = body.replace('table class="data cost"', 'table class="med-table cost"')
    body = body.replace('table class="data"', 'table class="med-table"')
    body = re.sub(
        r"(<table class=\"med-table[^\"]*\">)",
        r'<div class="table-wrap">\1',
        body,
    )
    body = body.replace("</table>", "</table></div>")

    # blockquote
    body = body.replace('blockquote class="summary"', 'blockquote class="summary-box"')

    # fix untranslated cell
    body = body.replace("完全自費為多", "Mostly fully self-pay")

    return body.strip()


def build_page(content: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Self-Paid Medical Items for a 65-Year-Old Father · Know All</title>
  <link rel="stylesheet" href="../../css/style.css" />
  <style>{PAGE_STYLES}</style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <div class="logo">
        <a href="../../index.html" style="display:flex;align-items:center;gap:10px;color:inherit;text-decoration:none;">
          <span class="logo-icon">◈</span>
          <span class="logo-text">Know All</span>
        </a>
      </div>
      <nav class="site-nav">
        <a href="../../index.html" class="nav-link">Map</a>
        <a href="index.html" class="nav-link">自費醫療 (TW)</a>
        <a href="en.html" class="nav-link active">Self-Paid (EN)</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="domain-page-header">
      <span class="domain-page-icon">🏥</span>
      <h1 class="domain-page-title">Self-Paid Medical Items for a 65-Year-Old Father</h1>
      <p class="domain-page-desc">Taiwan Medical Center Fee Reference — English Edition</p>
      <p class="fx-banner">Exchange: NT$30 = US$1 &nbsp;|&nbsp; NT$22 = A$1 &nbsp;|&nbsp; USD/AUD rounded to nearest $100</p>
    </div>

    <div class="domain-content">
      <aside class="domain-sidebar">
        <div class="sidebar-section">
          <div class="sidebar-title">Sections</div>
{SIDEBAR_TOC}
        </div>
        <div class="sidebar-section">
          <div class="sidebar-title">Language</div>
          <a href="index.html" class="sidebar-link">繁體中文 (TW)</a>
          <a href="en.html" class="sidebar-link active">English (EN)</a>
        </div>
      </aside>

      <div class="domain-main-content">
        {content}
        <p class="page-footer-note">Compiled: May 2026 · For financial planning reference only. Actual fees per hospital bulletin at time of service.</p>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <p>Know All · <a href="https://github.com/Risch315815/Know_All" target="_blank">GitHub</a></p>
  </footer>

</body>
</html>
"""


def patch_tw_index():
    text = TW_INDEX.read_text(encoding="utf-8")
    if 'href="en.html"' not in text:
        text = text.replace(
            '<span class="sidebar-link" style="opacity:.5">English — 待上架</span>',
            '<a href="en.html" class="sidebar-link">English (EN)</a>',
        )
    if 'nav-link">Self-Paid (EN)</a>' not in text:
        text = text.replace(
            '<a href="index.html" class="nav-link active">自費醫療 (TW)</a>\n      </nav>',
            '<a href="index.html" class="nav-link active">自費醫療 (TW)</a>\n        <a href="en.html" class="nav-link">Self-Paid (EN)</a>\n      </nav>',
            1,
        )
    TW_INDEX.write_text(text, encoding="utf-8")


def main():
    src = SRC.read_text(encoding="utf-8")
    content = transform_content(src)
    OUT.write_text(build_page(content), encoding="utf-8")
    patch_tw_index()
    print(f"Built: {OUT} ({OUT.stat().st_size:,} bytes)")
    print(f"Updated: {TW_INDEX}")


if __name__ == "__main__":
    main()

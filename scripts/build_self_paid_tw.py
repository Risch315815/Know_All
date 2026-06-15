#!/usr/bin/env python3
"""Build Self-Paid Medical Tx_TW domain page from markdown."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT.parent / "自費醫療" / "Self-Paid Medical Tx.md"
OUT_DIR = ROOT / "domains" / "Self-Paid Medical Tx_TW"
OUT_PATH = OUT_DIR / "index.html"

SECTION_ICONS = {
    "心臟": "❤️", "胸腔": "🫁", "腸胃": "🫃", "肝膽": "🫀",
    "新陳代謝": "⚗️", "免疫": "🦴", "血液": "🩸", "腫瘤": "🎗️",
    "神經": "🧠", "外科": "🔪", "泌尿": "💧", "骨科": "🦵",
    "眼科": "👁️", "耳鼻喉": "👂", "皮膚": "🧴", "精神": "🧩",
    "家庭": "🏠", "住院": "🏥", "高頻": "⭐", "長期": "🛏️", "附錄": "📎",
}


def slugify_heading(text: str) -> str:
    m = re.match(r"^[一二三四五六七八九十]+、(.+)$", text)
    if m:
        return re.sub(r"[^\w\u4e00-\u9fff]+", "", m.group(1))[:20]
    return re.sub(r"[^\w\u4e00-\u9fff]+", "-", text).strip("-")[:30]


def parse_table(lines: list[str]) -> str:
    if len(lines) < 2:
        return ""
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header, sep, body = rows[0], rows[1], rows[2:]
    if not all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in sep):
        body = rows[1:]
        header = rows[0]
    out = ['<div class="table-wrap"><table class="med-table"><thead><tr>']
    for h in header:
        out.append(f"<th>{inline_md(h)}</th>")
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{inline_md(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def parse_md(content: str) -> tuple[str, str, str]:
    lines = content.splitlines()
    title = "65 歲父親自費醫療項目整理"
    toc_items: list[tuple[str, str]] = []
    body_parts: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("# "):
            title = line[2:].strip()
            i += 1
            continue

        if line.startswith("## "):
            heading = line[3:].strip()
            sid = slugify_heading(heading)
            toc_items.append((heading, sid))
            body_parts.append(f'<section class="map-section" id="{sid}">')
            body_parts.append(f'<h2 class="map-title">{html.escape(heading)}</h2>')
            i += 1
            continue

        if line.startswith("### "):
            sub = line[4:].strip()
            body_parts.append(f'<h3 class="sub-title">{html.escape(sub)}</h3>')
            i += 1
            continue

        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            body_parts.append('<blockquote class="note">')
            for ql in quote_lines:
                if ql:
                    body_parts.append(f"<p>{inline_md(ql)}</p>")
            body_parts.append("</blockquote>")
            continue

        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            body_parts.append(parse_table(table_lines))
            continue

        if line.strip() == "---":
            if body_parts and body_parts[-1] != "</section>":
                body_parts.append("</section>")
            i += 1
            continue

        if line.strip():
            body_parts.append(f"<p>{inline_md(line.strip())}</p>")
        i += 1

    if body_parts and body_parts[-1] != "</section>":
        body_parts.append("</section>")

    toc_html = "\n".join(
        f'<a href="#{sid}" class="sidebar-link">{html.escape(h)}</a>'
        for h, sid in toc_items
    )
    return title, toc_html, "\n".join(body_parts)


def build_page(title: str, toc_html: str, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} · 全知專案</title>
  <link rel="stylesheet" href="../../css/style.css" />
  <style>
    .sub-title {{
      font-size: 15px; font-weight: 600; color: var(--accent);
      margin: 20px 0 12px; padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }}
    .note {{
      background: rgba(124, 158, 248, 0.08);
      border-left: 3px solid var(--accent);
      padding: 12px 16px; margin-bottom: 16px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 13px; color: var(--text-muted);
    }}
    .note p {{ margin: 4px 0; }}
    .table-wrap {{ overflow-x: auto; margin: 12px 0 20px; }}
    .med-table {{
      width: 100%; border-collapse: collapse; font-size: 13px;
    }}
    .med-table th, .med-table td {{
      border: 1px solid var(--border); padding: 8px 10px;
      text-align: left; vertical-align: top;
    }}
    .med-table th {{
      background: var(--bg-surface); font-weight: 600;
      white-space: nowrap; color: var(--text);
    }}
    .med-table tr:nth-child(even) td {{ background: rgba(255,255,255,0.02); }}
    .med-table td:nth-child(2) {{ white-space: nowrap; font-variant-numeric: tabular-nums; }}
    .page-footer-note {{
      font-size: 12px; color: var(--text-dim); margin-top: 24px;
      padding-top: 16px; border-top: 1px solid var(--border);
    }}
  </style>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <div class="logo">
        <a href="../../index.html" style="display:flex;align-items:center;gap:10px;color:inherit;text-decoration:none;">
          <span class="logo-icon">◈</span>
          <span class="logo-text">全知專案</span>
        </a>
      </div>
      <nav class="site-nav">
        <a href="../../index.html" class="nav-link">地圖</a>
        <a href="index.html" class="nav-link active">自費醫療 (TW)</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="domain-page-header">
      <span class="domain-page-icon">🏥</span>
      <h1 class="domain-page-title">{html.escape(title)}</h1>
      <p class="domain-page-desc">台灣醫學中心自費／自付差額項目參考 · 65 歲男性財務規劃用</p>
    </div>

    <div class="domain-content">
      <aside class="domain-sidebar">
        <div class="sidebar-section">
          <div class="sidebar-title">章節目錄</div>
          {toc_html}
        </div>
        <div class="sidebar-section">
          <div class="sidebar-title">版本</div>
          <a href="index.html" class="sidebar-link active">繁體中文 (TW)</a>
          <span class="sidebar-link" style="opacity:.5">English — 待上架</span>
        </div>
      </aside>

      <div class="domain-main-content">
        {body_html}
        <p class="page-footer-note">整理日期：2026 年 5 月 · 本文僅供財務規劃參考，實際費用以就醫當日各院公告為準</p>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <p>全知專案 · <a href="https://github.com/Risch315815/Know_All" target="_blank">GitHub</a></p>
  </footer>

</body>
</html>
"""


def main():
    content = MD_PATH.read_text(encoding="utf-8")
    title, toc, body = parse_md(content)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(build_page(title, toc, body), encoding="utf-8")
    print(f"Built: {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

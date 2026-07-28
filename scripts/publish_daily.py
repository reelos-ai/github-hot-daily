#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date, datetime, timedelta
from html import escape, unescape
from pathlib import Path

from restyle_report_pages import restyle_report_html


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://gh.reelos.ai"
REPORT_WINDOWS_DAYS = {
    "daily": 15,
    "weekly": 30,
    "monthly": 50,
}
REPORT_CATEGORIES = {
    "daily": "日报",
    "weekly": "周报",
    "monthly": "月报",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_report_entries(reports: list[dict]) -> list[dict]:
    for report in reports:
        report["category"] = REPORT_CATEGORIES.get(report.get("type"), "其他")
    return reports


def report_period_date(report: dict) -> date | None:
    period = report.get("period", "")
    for pattern in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(period, pattern).date()
        except ValueError:
            continue
    return None


def visible_reports(
    reports: list[dict],
    report_type: str,
    reference_date: date | None = None,
) -> list[dict]:
    window_days = REPORT_WINDOWS_DAYS[report_type]
    today = reference_date or date.today()
    cutoff = today - timedelta(days=window_days)
    return [
        report
        for report in normalize_report_entries(reports)
        if report.get("type") == report_type
        and (period_date := report_period_date(report)) is not None
        and cutoff <= period_date <= today
    ]


def load_report_stats(period: str) -> dict:
    top10 = read_json(ROOT / f"top10-{period}.json")
    data = read_json(ROOT / f"trending-data-{period}.json")
    return {
        "top10": top10,
        "data": data,
        "top_count": len(top10),
        "candidate_count": len(data),
        "readme_coverage": sum(1 for item in data if item.get("readme_content")),
        "api_failures": sum(1 for item in data if item.get("metadata_error")),
        "top_signal": top10[0]["full_name"] if top10 else "N/A",
    }


def upsert_report_entry(period: str, stats: dict) -> list[dict]:
    reports_path = ROOT / "reports.json"
    if reports_path.exists():
        payload = read_json(reports_path)
        reports = payload.get("reports", [])
    else:
        reports = []
    entry = {
        "type": "daily",
        "category": REPORT_CATEGORIES["daily"],
        "period": period,
        "title": f"GitHub 热榜情报日报 · {period}",
        "html": f"/daily/{period}/",
        "top10": f"/top10-{period}.json",
        "raw_data": f"/trending-data-{period}.json",
        "top_count": stats["top_count"],
        "candidate_count": stats["candidate_count"],
        "readme_coverage": stats["readme_coverage"],
        "api_failures": stats["api_failures"],
    }
    reports = [item for item in reports if not (item.get("type") == "daily" and item.get("period") == period)]
    reports.insert(0, entry)
    reports = normalize_report_entries(reports)
    reports.sort(key=lambda item: (item.get("period", ""), item.get("type", "")), reverse=True)
    payload = {
        "updated_at": datetime.now().astimezone().isoformat(timespec="minutes"),
        "site": SITE,
        "reports": reports,
    }
    write_text(reports_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return reports


def sync_daily_report_dir(period: str) -> None:
    src = ROOT / f"github-trending-daily-{period.replace('-', '')}.html"
    dst = ROOT / "daily" / period / "index.html"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    dst.write_text(restyle_report_html(dst.read_text(encoding="utf-8")), encoding="utf-8")


def latest_report(reports: list[dict], report_type: str) -> dict | None:
    for item in reports:
        if item.get("type") == report_type:
            return item
    return None


def load_report_repositories(report: dict | None, fallback: list[dict] | None = None) -> list[dict]:
    if not report:
        return fallback or []
    top10_path = report.get("top10", "").lstrip("/")
    if top10_path and (ROOT / top10_path).exists():
        return read_json(ROOT / top10_path)
    return fallback or []


def load_report_summaries(report: dict | None) -> dict[str, str]:
    if not report:
        return {}
    report_path = ROOT / report.get("html", "").strip("/") / "index.html"
    if not report_path.exists():
        return {}
    source = report_path.read_text(encoding="utf-8")
    summaries = {}
    for name, summary in re.findall(
        r'<article class="project-row">.*?<h3>(.*?)</h3>.*?<p>(.*?)</p>',
        source,
        flags=re.DOTALL,
    ):
        clean_name = unescape(re.sub(r"<[^>]+>", "", name)).strip()
        clean_summary = unescape(re.sub(r"<[^>]+>", "", summary)).strip()
        summaries[clean_name] = clean_summary
    return summaries


def render_home_report_panel(
    report_type: str,
    period: str,
    report: dict | None,
    repositories: list[dict],
    briefs: dict,
    active: bool = False,
) -> str:
    labels = {
        "daily": ("今日日报", "今日", "/daily/"),
        "weekly": ("最新周报", "本周", "/weekly/"),
        "monthly": ("最新月报", "本月", "/monthly/"),
    }
    title, growth_label, archive_link = labels[report_type]
    summaries = load_report_summaries(report)
    rows = []
    for rank, repo in enumerate(repositories[:10], start=1):
        name = repo.get("full_name", "未命名项目")
        summary = (
            briefs.get(name, {}).get("summary")
            or summaries.get(name)
            or repo.get("description")
            or "项目说明暂缺。"
        )
        growth = repo.get("stars_this_period") or 0
        rows.append(
            f"""<article class="home-project-row">
          <span class="home-project-rank mono">{rank:02d}</span>
          <div class="home-project-main">
            <h2>{escape(name)}</h2>
            <p>{escape(summary)}</p>
          </div>
          <div class="home-project-signal">
            <strong>{growth_label} +{growth}</strong>
            <a href="{escape(repo.get("url", "#"))}" target="_blank" rel="noopener noreferrer">原文 ↗</a>
          </div>
        </article>"""
        )
    hidden = "" if active else " hidden"
    return f"""<section class="home-report-panel" id="home-{report_type}" data-report-panel="{report_type}"{hidden}>
      <header class="home-report-head">
        <div>
          <span class="mono">{escape(period)}</span>
          <h1>{title}</h1>
          <p>{len(rows)} 个项目，一句话看懂</p>
        </div>
        <div class="home-report-links">
          <a href="{archive_link}">查看往期{title[-2:]}</a>
        </div>
      </header>
      <div class="home-project-list">{"".join(rows)}</div>
    </section>"""


def nav_links(active: str) -> str:
    items = [
        ("overview", "/", "首页"),
        ("daily", "/daily/", "日报"),
        ("weekly", "/weekly/", "周报"),
        ("monthly", "/monthly/", "月报"),
        ("archive", "/archive/", "归档"),
    ]
    links = []
    for key, href, label in items:
        cls = "active" if key == active else ""
        links.append(f'<a class="{cls}" href="{href}">{label}</a>')
    return "".join(links)


def reelos_brand_css() -> str:
    return """
    .reelos-lockup{
      display:inline-flex;
      align-items:center;
      gap:10px;
      width:max-content;
      color:var(--text,#111722);
      font-family:"Space Grotesk","IBM Plex Sans","PingFang SC","Microsoft YaHei",ui-sans-serif,system-ui,sans-serif;
      text-decoration:none;
      text-transform:none;
      letter-spacing:0;
    }
    .reelos-mark{
      position:relative;
      display:grid;
      flex:0 0 auto;
      width:30px;
      height:30px;
      place-items:center;
      border-radius:50%;
      background:#111722;
    }
    .reelos-mark::before,
    .reelos-mark::after,
    .reelos-mark > span{
      content:"";
      position:absolute;
      border:1.5px solid #fff7ed;
      border-radius:50%;
    }
    .reelos-mark::before{
      width:18px;
      height:18px;
    }
    .reelos-mark::after{
      width:8px;
      height:8px;
      border-color:#f97316;
    }
    .reelos-mark > span{
      width:24px;
      height:24px;
      border-top-color:transparent;
      transform:rotate(-25deg);
      transition:transform .62s cubic-bezier(.2,.8,.2,1);
    }
    .reelos-lockup:hover .reelos-mark > span{
      transform:rotate(295deg);
    }
    .reelos-lockup-copy{
      display:grid;
      gap:2px;
      min-width:0;
    }
    .reelos-wordmark{
      color:var(--text,#111722);
      font-size:16px;
      font-weight:650;
      line-height:1.2;
      letter-spacing:0;
      white-space:nowrap;
    }
    .reelos-logo-os{
      color:#f97316;
    }
    .reelos-lockup-subtitle{
      color:var(--muted,#6c788d);
      font-size:10px;
      font-weight:500;
      line-height:1.3;
      letter-spacing:.14em;
      text-transform:uppercase;
      white-space:nowrap;
    }
    .reelos-lockup:focus-visible{
      border-radius:3px;
      outline:2px solid #f97316;
      outline-offset:4px;
    }
    @media (max-width:680px){
      .reelos-mark{
        width:26px;
        height:26px;
      }
      .reelos-mark::before{
        width:16px;
        height:16px;
      }
      .reelos-mark > span{
        width:21px;
        height:21px;
      }
      .reelos-wordmark{
        font-size:14px;
      }
    }
    @media (prefers-reduced-motion:reduce){
      .reelos-mark > span{
        transition:none;
      }
    }
    """.strip()


def render_reelos_brand(
    href: str = "/",
    subtitle: str = "GitHub 热榜情报",
    extra_class: str = "",
) -> str:
    classes = " ".join(filter(None, ("reelos-lockup", extra_class)))
    return f"""<a class="{classes}" href="{escape(href)}" aria-label="ReelOS.ai">
      <span class="reelos-mark" aria-hidden="true"><span></span></span>
      <span class="reelos-lockup-copy">
        <span class="reelos-wordmark">Reel<span class="reelos-logo-os">OS</span>.ai</span>
        <span class="reelos-lockup-subtitle">{escape(subtitle)}</span>
      </span>
    </a>"""


def render_site_footer() -> str:
    return """<footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="https://www.reelos.ai/">ReelOS.ai</a>
        <p>AI Native Builder Lab</p>
      </div>
      <nav class="footer-column" aria-label="ReelOS">
        <h2>ReelOS</h2>
        <a href="https://www.reelos.ai/about/">关于</a>
        <a href="https://www.reelos.ai/principles/">原则</a>
        <a href="https://www.reelos.ai/faq/">FAQ</a>
        <a href="https://github.com/reelos-ai">GitHub</a>
      </nav>
      <nav class="footer-column" aria-label="Projects">
        <h2>Projects</h2>
        <a href="https://daoyin.reelos.ai/">DaoYin</a>
        <a href="https://yi.reelos.ai/">Yi</a>
        <a href="https://macro.reelos.ai/">MacroFlow</a>
      </nav>
      <nav class="footer-column" aria-label="Channels">
        <h2>Channels</h2>
        <a href="https://www.reelos.ai/feed.xml">RSS Feed</a>
        <a href="https://infra.reelos.ai/">AI Infra</a>
        <a href="https://ainews.reelos.ai/">AI News</a>
        <a href="https://gh.reelos.ai/">GitHub Radar</a>
        <a href="https://www.reelos.ai/daily/">Daily Research</a>
      </nav>
    </div>
  </footer>"""


def shell_css() -> str:
    return """
    :root{
      color-scheme:light;
      --bg:#fcfaf6;
      --bg-2:#fffdf8;
      --surface:rgba(255,255,255,.74);
      --surface-2:rgba(255,255,255,.58);
      --surface-3:rgba(255,250,241,.8);
      --line:rgba(228,228,225,.92);
      --line-strong:rgba(232,178,126,.72);
      --text:#111111;
      --muted:rgba(48,45,40,.68);
      --soft:rgba(48,45,40,.82);
      --blue:#8ea3e8;
      --cyan:#a9b7ea;
      --amber:#f97316;
      --amber-soft:rgba(249,115,22,.14);
      --rail:rgba(177,164,148,.34);
      --ok:#4c8b66;
      --shadow:0 20px 70px rgba(17,17,17,.07);
      --radius:14px;
      --radius-sm:8px;
    }
    *{box-sizing:border-box}
    html{color-scheme:light}
    body{
      margin:0;
      color:var(--text);
      font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC",sans-serif;
      line-height:1.7;
      -webkit-font-smoothing:antialiased;
      text-rendering:optimizeLegibility;
      background:
        radial-gradient(circle at 18% 0%, rgba(176,192,255,.18), transparent 30%),
        radial-gradient(circle at 84% 16%, rgba(249,115,22,.12), transparent 22%),
        linear-gradient(rgba(196,203,230,.18) 1px, transparent 1px),
        linear-gradient(90deg, rgba(196,203,230,.18) 1px, transparent 1px),
        linear-gradient(180deg, var(--bg), var(--bg-2));
      background-size:auto,auto,72px 72px,72px 72px,auto;
      background-attachment:fixed;
    }
    a{color:inherit;text-decoration:none}
    a:hover{color:var(--amber)}
    .mono{
      font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;
      letter-spacing:.08em;
    }
    .wrap{max-width:1180px;margin:0 auto;padding:28px 20px 96px}
    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:16px;
      padding:10px 0 18px;
      border-bottom:1px solid var(--line);
    }
    .brand{
      display:flex;
      align-items:center;
      gap:12px;
      min-width:0;
    }
    .brand-mark{
      width:10px;
      height:10px;
      border-radius:999px;
      background:linear-gradient(180deg,#ff9f54,#f97316);
      box-shadow:0 0 14px rgba(249,115,22,.22);
    }
    .brand-copy{min-width:0}
    .brand-kicker{
      color:var(--muted);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.18em;
    }
    .brand-title{
      font-size:14px;
      color:var(--text);
      white-space:nowrap;
    }
    .nav{
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      justify-content:flex-end;
    }
    .nav a{
      padding:8px 12px;
      border:1px solid var(--line);
      border-radius:999px;
      background:rgba(255,255,255,.6);
      color:var(--muted);
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.12em;
      backdrop-filter:blur(12px);
    }
    .nav a.active,.nav a:hover{
      color:var(--text);
      border-color:var(--line-strong);
      background:rgba(255,244,232,.92);
    }
    .hero{
      display:grid;
      grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr);
      gap:18px;
      margin-top:22px;
      align-items:stretch;
    }
    .hero-main,.hero-side,.panel,.list,.quote{
      border:1px solid var(--line);
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,253,248,.72));
      box-shadow:var(--shadow);
      backdrop-filter:blur(20px);
    }
    .hero-main{
      border-radius:22px;
      padding:24px;
      position:relative;
      overflow:hidden;
    }
    .hero-main::before{
      content:"";
      position:absolute;
      inset:auto -10% -35% 30%;
      height:260px;
      background:radial-gradient(circle, rgba(249,115,22,.14), transparent 60%);
      pointer-events:none;
    }
    .hero-main::after{
      content:"";
      position:absolute;
      inset:0;
      background:
        repeating-linear-gradient(90deg, rgba(120,130,170,0) 0 47px, rgba(120,130,170,.08) 47px 48px),
        repeating-linear-gradient(180deg, rgba(249,115,22,0) 0 13px, rgba(249,115,22,.02) 13px 14px);
      opacity:.42;
      pointer-events:none;
      mask-image:linear-gradient(180deg, rgba(0,0,0,.38), transparent 76%);
    }
    .eyebrow{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:6px 10px;
      border:1px solid var(--line);
      border-radius:999px;
      color:var(--soft);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.16em;
      background:rgba(255,255,255,.46);
    }
    .eyebrow::before{
      content:"";
      width:6px;
      height:6px;
      border-radius:999px;
      background:var(--amber);
      box-shadow:0 0 10px rgba(249,115,22,.3);
    }
    h1{
      margin:16px 0 10px;
      font-size:clamp(42px,8vw,86px);
      line-height:.94;
      letter-spacing:-.045em;
      font-weight:650;
      font-family:Sora,"Space Grotesk","IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
    }
    .headline{
      display:block;
      max-width:9ch;
    }
    .headline-line{display:block}
    .ghost-word,
    .texture-word{
      display:inline-block;
      position:relative;
      font-weight:700;
      letter-spacing:-.06em;
    }
    .ghost-word{color:rgba(17,17,17,.96)}
    .texture-word{
      color:transparent;
      background-image:
        linear-gradient(180deg, rgba(255,171,97,.98), rgba(249,115,22,.96)),
        repeating-linear-gradient(90deg, rgba(255,250,241,0) 0 14px, rgba(255,250,241,.18) 14px 15px),
        repeating-linear-gradient(180deg, rgba(17,17,17,0) 0 9px, rgba(17,17,17,.16) 9px 10px);
      background-blend-mode:normal,screen,multiply;
      -webkit-background-clip:text;
      background-clip:text;
      text-shadow:0 8px 26px rgba(249,115,22,.16);
    }
    .texture-word::after{
      content:"";
      position:absolute;
      inset:10% 3% 8% 3%;
      background:
        repeating-linear-gradient(180deg, rgba(255,250,241,0) 0 8px, rgba(255,250,241,.18) 8px 9px),
        repeating-linear-gradient(90deg, rgba(120,90,40,0) 0 12px, rgba(120,90,40,.12) 12px 13px);
      opacity:.38;
      mix-blend-mode:soft-light;
      pointer-events:none;
      border-radius:12px;
    }
    .lead{
      max-width:62ch;
      margin:0;
      color:var(--soft);
      font-size:16px;
    }
    .hero-actions{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      margin-top:22px;
    }
    .btn{
      display:inline-flex;
      align-items:center;
      gap:9px;
      padding:11px 15px;
      border-radius:999px;
      border:1px solid var(--line);
      background:rgba(255,255,255,.7);
      color:var(--text);
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.14em;
    }
    .btn.primary{
      border-color:rgba(249,115,22,.3);
      background:linear-gradient(180deg, rgba(255,166,84,.95), rgba(249,115,22,.9));
      color:#fffaf1;
    }
    .hero-side{
      border-radius:22px;
      padding:18px;
      display:grid;
      gap:12px;
      align-content:start;
    }
    .hero-side.compact{
      background:rgba(255,252,246,.72);
      gap:14px;
    }
    .side-label{
      color:var(--muted);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.16em;
    }
    .signal-title{
      font-size:24px;
      line-height:1.15;
      margin:0;
    }
    .signal-copy{
      margin:0;
      color:var(--soft);
      font-size:14px;
    }
    .hero-side .signal-copy{max-width:34ch}
    .status-grid{
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:10px;
      padding-top:4px;
    }
    .status-item{
      border-top:1px solid var(--line);
      padding-top:10px;
      min-width:0;
    }
    .status-item.wide{grid-column:1 / -1}
    .status-label{
      display:block;
      margin-bottom:6px;
      color:var(--muted);
      font-size:10px;
      text-transform:uppercase;
      letter-spacing:.16em;
    }
    .status-value{
      display:block;
      color:var(--text);
      font-size:15px;
      line-height:1.35;
      word-break:break-word;
    }
    .stat-grid,.card-grid{
      display:grid;
      grid-template-columns:repeat(4,minmax(0,1fr));
      gap:12px;
      margin-top:18px;
    }
    .card-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
    .metric,.card{
      border:1px solid var(--line);
      border-radius:var(--radius);
      background:var(--surface-2);
      padding:14px;
      min-width:0;
    }
    .metric b{
      display:block;
      font-size:28px;
      line-height:1;
      color:var(--text);
      margin-bottom:6px;
    }
    .metric span,.card p{
      color:var(--muted);
      font-size:13px;
    }
    .card b{
      display:block;
      margin-bottom:8px;
      color:var(--blue);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.14em;
    }
    .section{
      display:grid;
      grid-template-columns:96px minmax(0,1fr);
      gap:16px;
      margin-top:18px;
      align-items:start;
    }
    .section-rail{
      padding-top:8px;
      color:var(--muted);
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.18em;
      position:relative;
    }
    .section-rail::after{
      content:"";
      position:absolute;
      left:8px;
      top:34px;
      bottom:-24px;
      width:1px;
      background:linear-gradient(180deg,var(--rail),transparent);
    }
    .panel{
      border-radius:20px;
      padding:18px;
    }
    .panel h2{
      margin:0;
      font-size:26px;
      line-height:1.15;
      letter-spacing:-.03em;
    }
    .panel > p{
      margin:8px 0 0;
      color:var(--muted);
      font-size:14px;
      max-width:68ch;
    }
    .list{
      border-radius:20px;
      margin-top:14px;
      overflow:hidden;
    }
    .row{
      display:grid;
      grid-template-columns:90px minmax(0,1fr) 104px;
      gap:12px;
      align-items:center;
      padding:15px 18px;
      border-bottom:1px solid var(--line);
      transition:background .2s ease, transform .2s ease, border-color .2s ease;
    }
    .row:last-child{border-bottom:0}
    .row:hover{
      background:rgba(255,247,239,.88);
      transform:translateX(2px);
      border-color:rgba(232,178,126,.72);
    }
    .row .type{
      color:var(--amber);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.16em;
    }
    .row .title{
      font-size:15px;
      color:var(--text);
    }
    .row .meta{
      text-align:right;
      color:var(--muted);
      font-size:11px;
    }
    .quote{
      border-radius:20px;
      margin-top:22px;
      padding:18px 20px;
      position:relative;
    }
    .quote::before{
      content:"Conclusion";
      display:block;
      margin-bottom:8px;
      color:var(--amber);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.18em;
    }
    .quote p{
      margin:0;
      color:var(--text);
      font-size:18px;
      line-height:1.6;
    }
    .mini-list{
      display:grid;
      gap:10px;
    }
    .mini-item{
      display:flex;
      justify-content:space-between;
      gap:12px;
      align-items:flex-start;
      padding:12px 0;
      border-top:1px solid var(--line);
    }
    .mini-item:first-child{border-top:0;padding-top:0}
    .mini-item b{
      display:block;
      margin-bottom:4px;
      font-size:13px;
    }
    .mini-item span{
      color:var(--muted);
      font-size:12px;
    }
    .flow-intro{
      display:flex;
      justify-content:space-between;
      gap:14px;
      align-items:flex-end;
      margin-bottom:12px;
    }
    .flow-intro h2{
      margin:0;
      font-size:26px;
      line-height:1.12;
      letter-spacing:-.03em;
    }
    .flow-intro p{
      margin:6px 0 0;
      max-width:54ch;
      color:var(--muted);
      font-size:14px;
    }
    .flow-meta{
      color:var(--amber);
      font-size:11px;
      text-transform:uppercase;
      letter-spacing:.18em;
      white-space:nowrap;
    }
    .list.open{
      margin-top:0;
      border:none;
      border-radius:0;
      background:transparent;
      box-shadow:none;
      backdrop-filter:none;
    }
    .list.open .row{
      padding:17px 0;
      border-bottom:1px solid rgba(223,219,210,.92);
    }
    .list.open .row:hover{
      background:transparent;
      transform:translateX(4px);
      border-color:rgba(232,178,126,.72);
    }
    .home-main{
      margin-top:18px;
    }
    .home-page{
      --bg:#edf1f6;
      --bg-2:#edf1f6;
      --surface:#fff;
      --surface-2:#fff;
      --surface-3:#f7f9fc;
      --line:#d7dce5;
      --line-strong:#bcc5d2;
      --text:#0d1424;
      --muted:#6c788d;
      --soft:#344159;
      --blue:#315fc8;
      --amber:#315fc8;
      --amber-soft:#eef3ff;
      background:#edf1f6;
      background-attachment:scroll;
    }
    .home-page .wrap{
      padding-bottom:56px;
    }
    .home-page .topbar{
      padding-top:4px;
    }
    .home-page .nav a{
      border-radius:0;
      background:transparent;
      backdrop-filter:none;
    }
    .home-page .nav a.active,
    .home-page .nav a:hover{
      color:#315fc8;
      border-color:#bcc5d2;
      background:#fff;
    }
    .home-page .btn.primary{
      color:#fff;
      border-color:#315fc8;
      background:#315fc8;
      box-shadow:none;
    }
    .home-masthead{
      padding:10px 0 34px;
      border-bottom:1px solid var(--line);
    }
    .home-masthead-top{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:24px;
    }
    .home-masthead-brand{
      display:flex;
      align-items:center;
    }
    .home-masthead-edition{
      color:var(--muted);
      font-size:10px;
      letter-spacing:.16em;
      text-transform:uppercase;
    }
    .home-masthead-body{
      display:grid;
      grid-template-columns:minmax(0,1.45fr) minmax(260px,.55fr);
      align-items:end;
      gap:64px;
      padding-top:48px;
    }
    .home-masthead-kicker{
      display:block;
      margin-bottom:12px;
      color:var(--blue);
      font-size:11px;
      font-weight:700;
      letter-spacing:.16em;
      text-transform:uppercase;
    }
    .home-masthead h1{
      max-width:820px;
      margin:0;
      font-size:clamp(40px,4.8vw,66px);
      line-height:1.08;
      letter-spacing:-.065em;
      text-wrap:balance;
    }
    .home-masthead-copy{
      margin:0 0 6px;
      color:var(--soft);
      font-size:15px;
      line-height:1.85;
      text-wrap:pretty;
    }
    .today-hero{
      display:grid;
      grid-template-columns:minmax(320px,.82fr) minmax(0,1.18fr);
      border:1px solid var(--line);
      background:#fff;
    }
    .today-intro{
      display:flex;
      flex-direction:column;
      align-items:flex-start;
      justify-content:center;
      min-height:300px;
      padding:30px;
      border-right:1px solid var(--line);
      background:#f7f9fc;
    }
    .today-intro h1{
      margin:12px 0 18px;
      font-size:clamp(32px,3.2vw,42px);
      line-height:1.08;
      letter-spacing:-.045em;
    }
    .today-intro .text-link{
      margin-top:14px;
      color:var(--muted);
      font-size:13px;
    }
    .today-preview{
      padding:10px 26px;
    }
    .today-project{
      display:grid;
      grid-template-columns:34px minmax(0,1fr);
      gap:12px;
      padding:18px 0;
      border-bottom:1px solid var(--line);
    }
    .today-project:last-child{
      border-bottom:0;
    }
    .today-rank{
      padding-top:3px;
      color:var(--amber);
      font-size:11px;
      font-weight:700;
    }
    .today-project h2{
      margin:0 0 7px;
      font-size:18px;
      line-height:1.35;
      overflow-wrap:anywhere;
    }
    .today-project p{
      margin:0;
      color:var(--soft);
      font-size:14px;
      line-height:1.72;
    }
    .report-library{
      margin:38px 0 18px;
    }
    .library-head{
      max-width:680px;
      margin-bottom:16px;
    }
    .library-head h2{
      margin:6px 0 0;
      font-size:28px;
      line-height:1.2;
      letter-spacing:-.04em;
    }
    .report-grid{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      border:1px solid var(--line);
      background:#fff;
    }
    .report-entry{
      min-height:190px;
      padding:22px;
      border-right:1px solid var(--line);
    }
    .report-entry:last-child{
      border-right:0;
    }
    .report-number{
      color:var(--amber);
      font-size:11px;
      font-weight:700;
    }
    .report-entry h3{
      margin:12px 0 8px;
      font-size:25px;
      line-height:1.1;
      letter-spacing:-.04em;
    }
    .report-meta{
      display:flex;
      justify-content:space-between;
      gap:12px;
      margin-top:18px;
      padding-top:12px;
      border-top:1px solid var(--line);
      color:var(--muted);
      font-size:11px;
    }
    .report-links{
      display:flex;
      gap:16px;
      margin-top:14px;
    }
    .report-links a{
      color:var(--text);
      font-size:13px;
      font-weight:700;
    }
    .report-links a:last-child{
      color:var(--blue);
    }
    .home-report-tabs{
      display:flex;
      gap:0;
      margin-bottom:14px;
      border-bottom:1px solid var(--line);
    }
    .home-report-tab{
      appearance:none;
      padding:12px 22px;
      color:var(--muted);
      border:0;
      border-bottom:2px solid transparent;
      background:transparent;
      font:inherit;
      font-size:14px;
      font-weight:700;
      cursor:pointer;
    }
    .home-report-tab:hover,
    .home-report-tab[aria-selected="true"]{
      color:var(--blue);
      border-bottom-color:var(--blue);
    }
    .home-report-panel[hidden]{
      display:none;
    }
    .home-report-head{
      display:flex;
      align-items:flex-end;
      justify-content:space-between;
      gap:24px;
      padding:20px 0 18px;
    }
    .home-report-head .mono{
      color:var(--blue);
      font-size:11px;
      font-weight:700;
      letter-spacing:.12em;
    }
    .home-report-head h1{
      margin:6px 0 4px;
      font-size:30px;
      line-height:1.2;
      letter-spacing:-.045em;
    }
    .home-report-head p{
      margin:0;
      color:var(--muted);
      font-size:13px;
    }
    .home-report-links{
      display:flex;
      gap:8px;
    }
    .home-report-links a{
      padding:8px 12px;
      color:var(--blue);
      border:1px solid var(--line-strong);
      background:#fff;
      font-size:12px;
      font-weight:700;
    }
    .home-project-list{
      border-top:1px solid var(--line);
      border-bottom:1px solid var(--line);
      background:#fff;
    }
    .home-project-row{
      display:grid;
      grid-template-columns:52px minmax(0,1fr) 110px;
      gap:18px;
      padding:20px 6px;
      border-bottom:1px solid var(--line);
    }
    .home-project-row:last-child{
      border-bottom:0;
    }
    .home-project-rank{
      padding-top:3px;
      color:var(--blue);
      font-size:11px;
      font-weight:700;
    }
    .home-project-main h2{
      margin:0 0 6px;
      font-size:19px;
      line-height:1.3;
      overflow-wrap:anywhere;
    }
    .home-project-main p{
      max-width:850px;
      margin:0;
      color:var(--soft);
      font-size:14px;
      line-height:1.7;
    }
    .home-project-signal{
      display:flex;
      flex-direction:column;
      align-items:flex-end;
      gap:8px;
      color:var(--muted);
      font-size:11px;
    }
    .home-project-signal strong{
      color:var(--blue);
      font-size:12px;
    }
    .home-project-signal a{
      color:var(--muted);
      font-size:12px;
      font-weight:700;
    }
    .archive-main{
      margin-top:26px;
    }
    .archive-policy{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      margin-bottom:24px;
      border:1px solid var(--line);
      background:#fff;
    }
    .archive-policy-item{
      padding:18px 20px;
      border-right:1px solid var(--line);
    }
    .archive-policy-item:last-child{
      border-right:0;
    }
    .archive-policy-item span{
      display:block;
      color:var(--muted);
      font-size:12px;
    }
    .archive-policy-item strong{
      display:block;
      margin:4px 0 2px;
      color:var(--text);
      font-size:24px;
      line-height:1.2;
    }
    .archive-report-list{
      border-top:1px solid var(--line);
      border-bottom:1px solid var(--line);
      background:#fff;
    }
    .archive-report-row{
      display:grid;
      grid-template-columns:76px minmax(0,1fr) 96px;
      gap:16px;
      align-items:center;
      padding:18px 8px;
      border-bottom:1px solid var(--line);
    }
    .archive-report-row:last-child{
      border-bottom:0;
    }
    .archive-report-category{
      width:max-content;
      padding:4px 8px;
      color:var(--blue);
      border:1px solid #c8d2e3;
      background:#f7f9fc;
      font-size:11px;
      font-weight:700;
    }
    .archive-report-title{
      font-size:16px;
      font-weight:700;
      line-height:1.45;
    }
    .archive-report-meta{
      color:var(--muted);
      font-size:11px;
      text-align:right;
    }
    .archive-empty{
      padding:28px 8px;
      color:var(--muted);
      font-size:14px;
    }
    .site-footer{
      color:#a7adbc;
      background:#080b13;
      border-top:1px solid #222735;
    }
    .footer-inner{
      display:grid;
      grid-template-columns:minmax(280px,2.2fr) repeat(3,minmax(130px,1fr));
      gap:56px;
      max-width:1180px;
      margin:0 auto;
      padding:64px 20px 72px;
    }
    .footer-brand a{
      color:#f5f6fa;
      font-size:24px;
      font-weight:700;
      letter-spacing:-.02em;
    }
    .footer-brand p{
      margin:4px 0 0;
      color:#a7adbc;
      font-size:15px;
      font-weight:600;
    }
    .footer-column{
      display:grid;
      align-content:start;
      gap:14px;
    }
    .footer-column h2{
      margin:0 0 4px;
      color:#777f91;
      font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;
      font-size:12px;
      font-weight:700;
      letter-spacing:.18em;
      text-transform:uppercase;
    }
    .footer-column a{
      width:max-content;
      max-width:100%;
      color:#a7adbc;
      font-size:14px;
      font-weight:600;
    }
    .footer-column a:hover{
      color:#fff;
    }
    @media (max-width:980px){
      .hero{grid-template-columns:1fr}
      .stat-grid,.card-grid,.card-grid.three{grid-template-columns:repeat(2,minmax(0,1fr))}
      .flow-intro{display:block}
      .flow-meta{display:block;margin-top:10px}
      .today-hero{grid-template-columns:1fr}
      .today-intro{
        min-height:0;
        border-right:0;
        border-bottom:1px solid var(--line);
      }
      .footer-inner{
        grid-template-columns:repeat(2,minmax(0,1fr));
        gap:44px 32px;
      }
    }
    @media (max-width:680px){
      .wrap{padding:22px 14px 72px}
      .topbar{align-items:flex-start;flex-direction:column}
      .nav{
        width:100%;
        flex-wrap:nowrap;
        justify-content:flex-start;
        overflow-x:auto;
        padding-bottom:4px;
        scrollbar-width:none;
      }
      .nav::-webkit-scrollbar{display:none}
      .nav a{flex:0 0 auto}
      .section{grid-template-columns:1fr}
      .section-rail{padding-top:0}
      .section-rail::after{display:none}
      .stat-grid,.card-grid,.card-grid.three{grid-template-columns:1fr}
      .status-grid{grid-template-columns:1fr}
      .row{grid-template-columns:1fr;gap:6px}
      .row .meta{text-align:left}
      .list.open .row{padding:14px 0}
      h1{font-size:clamp(38px,15vw,66px)}
      .today-intro{padding:30px 24px}
      .today-intro h1{font-size:34px}
      .today-preview{padding:10px 20px}
      .report-library{margin-top:48px}
      .report-grid{grid-template-columns:1fr}
      .home-report-tabs{
        overflow-x:auto;
      }
      .home-masthead{
        padding-top:2px;
        padding-bottom:26px;
      }
      .home-masthead-top{
        align-items:flex-start;
        flex-direction:column;
        gap:10px;
      }
      .home-masthead-body{
        grid-template-columns:1fr;
        gap:18px;
        padding-top:34px;
      }
      .home-masthead h1{
        font-size:clamp(36px,11vw,50px);
      }
      .home-masthead-copy{
        max-width:32em;
      }
      .home-report-tab{
        flex:1 0 auto;
        padding:11px 16px;
      }
      .home-report-head{
        align-items:flex-start;
        flex-direction:column;
        gap:14px;
      }
      .home-report-head h1{
        font-size:27px;
      }
      .home-project-row{
        grid-template-columns:32px minmax(0,1fr);
        gap:10px;
        padding:18px 0;
      }
      .home-project-signal{
        grid-column:2;
        flex-direction:row;
        align-items:center;
        justify-content:space-between;
      }
      .archive-policy{
        grid-template-columns:1fr;
      }
      .archive-policy-item{
        border-right:0;
        border-bottom:1px solid var(--line);
      }
      .archive-policy-item:last-child{
        border-bottom:0;
      }
      .archive-report-row{
        grid-template-columns:64px minmax(0,1fr);
        gap:10px;
        padding:16px 0;
      }
      .archive-report-meta{
        grid-column:2;
        text-align:left;
      }
      .report-entry{
        min-height:0;
        border-right:0;
        border-bottom:1px solid var(--line);
      }
      .report-entry:last-child{border-bottom:0}
      .report-entry > p{min-height:0}
      .footer-inner{
        padding:44px 20px 52px;
      }
    }
    """


def render_daily_index(period: str, stats: dict, reports: list[dict]) -> str:
    daily_reports = visible_reports(reports, "daily")
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["category"]}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in daily_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Radar · GitHub Signal · ReelOS</title>
  <style>{shell_css()}{reelos_brand_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      {render_reelos_brand("/", "GitHub 热榜情报", "brand")}
      <nav class="nav">{nav_links("daily")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Daily Signal Layer</div>
        <h1 class="headline"><span class="headline-line"><span class="ghost-word">Daily</span> <span class="texture-word">Radar</span></span></h1>
        <p class="lead">日报负责把当天爆发项目转译成适合中文读者快速阅读的信号页。它不是简单搬运榜单，而是先给出今天应该打开哪一篇、盯哪一类项目、把哪些仓库送进观察池。</p>
        <div class="hero-actions">
          <a class="btn primary" href="/daily/{period}/">打开 {period} 日报</a>
          <a class="btn" href="/top10-{period}.json">Top10 JSON</a>
          <a class="btn" href="/trending-data-{period}.json">Raw Data</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Latest Issue</div>
        <h2 class="signal-title"><a href="/daily/{period}/">GitHub 热榜情报日报 · {period}</a></h2>
        <p class="signal-copy">本期主信号是 <span class="mono">{stats["top_signal"]}</span>。六个切片共抓取 {stats["candidate_count"]} 个候选，移动端仍保持中文趋势卡片和快读密度。</p>
        <div class="mini-list">
          <div class="mini-item"><div><b>Top 10 完整处理</b><span>已做中文判断与加权排序</span></div><span class="mono">{stats["top_count"]}</span></div>
          <div class="mini-item"><div><b>README 覆盖</b><span>用于增强判断和依赖线索</span></div><span class="mono">{stats["readme_coverage"]}</span></div>
          <div class="mini-item"><div><b>API 异常</b><span>越低代表元数据越完整</span></div><span class="mono">{stats["api_failures"]}</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Metrics</div>
      <div>
        <div class="stat-grid">
          <div class="metric"><b class="mono">{stats["candidate_count"]}</b><span>候选项目</span></div>
          <div class="metric"><b class="mono">{stats["top_count"]}</b><span>情报项目</span></div>
          <div class="metric"><b class="mono">{stats["readme_coverage"]}</b><span>README 覆盖</span></div>
          <div class="metric"><b class="mono">{stats["api_failures"]}</b><span>API 失败</span></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">02 / Use</div>
      <div class="panel">
        <h2>日报负责什么，不负责什么</h2>
        <p>它负责筛出今天该先看的仓库和需要继续盯的方向，不负责做完整战略结论。真正的“是否值得投入”会交给周报完成。</p>
        <div class="card-grid three" style="margin-top:16px">
          <div class="card"><b>Top 10</b><p>把当天高热仓库转成可判断的优先级，而不是按星数机械排序。</p></div>
          <div class="card"><b>中文趋势卡片</b><p>保留高密度摘要和行动含义，适合手机端和团队转发。</p></div>
          <div class="card"><b>观察池入口</b><p>把可能进入周报深挖的项目优先送入 watchlist。</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">03 / Archive</div>
      <div>
        <div class="panel">
          <h2>最近 15 天日报</h2>
          <p>仅展示距今天不超过 15 天的日报，减少过期信息干扰；更早报告仍保留原链接。</p>
        </div>
        <div class="list">{rows}</div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def render_archive_panel(report_type: str, reports: list[dict], active: bool = False) -> str:
    category = REPORT_CATEGORIES[report_type]
    window_days = REPORT_WINDOWS_DAYS[report_type]
    visible = visible_reports(reports, report_type)
    rows = "".join(
        f"""<a class="archive-report-row" href="{escape(item["html"])}">
          <span class="archive-report-category">{escape(item["category"])}</span>
          <span class="archive-report-title">{escape(item["title"])}</span>
          <span class="archive-report-meta mono">Top {item["top_count"]}</span>
        </a>"""
        for item in visible
    )
    hidden = "" if active else " hidden"
    return f"""<section class="home-report-panel" id="archive-{report_type}" data-archive-panel="{report_type}"{hidden}>
      <header class="home-report-head">
        <div>
          <span class="mono">最近 {window_days} 天</span>
          <h1>{category}</h1>
          <p>{len(visible)} 份可见报告，超出时间窗口的历史报告不再占用列表。</p>
        </div>
      </header>
      <div class="archive-report-list">{rows or '<div class="archive-empty">当前时间窗口内暂无报告。</div>'}</div>
    </section>"""


def render_archive(reports: list[dict]) -> str:
    report_groups = {
        report_type: visible_reports(reports, report_type)
        for report_type in REPORT_WINDOWS_DAYS
    }
    panels = "".join(
        render_archive_panel(report_type, reports, active=report_type == "daily")
        for report_type in REPORT_WINDOWS_DAYS
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>报告归档 · GitHub 热榜情报 · ReelOS</title>
  <meta name="description" content="按日报、周报、月报分类查看 ReelOS GitHub 热榜情报报告。">
  <style>{shell_css()}{reelos_brand_css()}</style>
</head>
<body class="home-page">
  <div class="wrap">
    <header class="home-masthead">
      <div class="home-masthead-top">
        {render_reelos_brand("/", "GitHub 热榜情报", "home-masthead-brand")}
        <span class="home-masthead-edition mono">Daily · Weekly · Monthly</span>
      </div>
      <div class="home-masthead-body">
        <div>
          <span class="home-masthead-kicker mono">Report Archive</span>
          <h1>按周期查看，不让旧信息淹没新信号。</h1>
        </div>
        <p class="home-masthead-copy">日报保留 15 天，周报保留 30 天，月报保留 50 天。历史文件继续保存，列表只呈现当前有效窗口。</p>
      </div>
    </header>

    <main class="archive-main">
      <section class="archive-policy" aria-label="报告展示期限">
        <div class="archive-policy-item">
          <span>日报</span>
          <strong>≤ 15 天</strong>
          <span>{len(report_groups["daily"])} 份可见</span>
        </div>
        <div class="archive-policy-item">
          <span>周报</span>
          <strong>≤ 30 天</strong>
          <span>{len(report_groups["weekly"])} 份可见</span>
        </div>
        <div class="archive-policy-item">
          <span>月报</span>
          <strong>≤ 50 天</strong>
          <span>{len(report_groups["monthly"])} 份可见</span>
        </div>
      </section>

      <nav class="home-report-tabs" aria-label="报告类别">
        <button class="home-report-tab" type="button" data-archive-tab="daily" aria-controls="archive-daily" aria-selected="true">日报</button>
        <button class="home-report-tab" type="button" data-archive-tab="weekly" aria-controls="archive-weekly" aria-selected="false">周报</button>
        <button class="home-report-tab" type="button" data-archive-tab="monthly" aria-controls="archive-monthly" aria-selected="false">月报</button>
      </nav>
      {panels}
    </main>
  </div>
  {render_site_footer()}
  <script>
    (() => {{
      const tabs = [...document.querySelectorAll("[data-archive-tab]")];
      const panels = [...document.querySelectorAll("[data-archive-panel]")];
      const show = (type, updateHash = true) => {{
        if (!panels.some((panel) => panel.dataset.archivePanel === type)) return;
        tabs.forEach((tab) => tab.setAttribute("aria-selected", String(tab.dataset.archiveTab === type)));
        panels.forEach((panel) => {{ panel.hidden = panel.dataset.archivePanel !== type; }});
        if (updateHash) history.replaceState(null, "", `#${{type}}`);
      }};
      tabs.forEach((tab) => tab.addEventListener("click", () => show(tab.dataset.archiveTab)));
      window.addEventListener("hashchange", () => show(location.hash.slice(1), false));
      const initial = location.hash.slice(1);
      if (["daily", "weekly", "monthly"].includes(initial)) show(initial, false);
    }})();
  </script>
</body>
</html>
"""


def render_home(period: str, stats: dict, reports: list[dict]) -> str:
    latest_daily = latest_report(reports, "daily")
    latest_weekly = latest_report(reports, "weekly")
    latest_monthly = latest_report(reports, "monthly")
    daily_period = latest_daily["period"] if latest_daily else period
    weekly_period = latest_weekly["period"] if latest_weekly else "尚未发布"
    monthly_period = latest_monthly["period"] if latest_monthly else "尚未发布"
    briefs = read_json(ROOT / "project-briefs-zh.json") if (ROOT / "project-briefs-zh.json").exists() else {}
    daily_repositories = load_report_repositories(latest_daily, stats["top10"])
    weekly_repositories = load_report_repositories(latest_weekly)
    monthly_repositories = load_report_repositories(latest_monthly)
    panels = "".join(
        [
            render_home_report_panel(
                "daily",
                daily_period,
                latest_daily,
                daily_repositories,
                briefs,
                active=True,
            ),
            render_home_report_panel(
                "weekly",
                weekly_period,
                latest_weekly,
                weekly_repositories,
                briefs,
            ),
            render_home_report_panel(
                "monthly",
                monthly_period,
                latest_monthly,
                monthly_repositories,
                briefs,
            ),
        ]
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GitHub Signal Intelligence · ReelOS</title>
  <meta name="description" content="ReelOS GitHub 热榜情报中心：日报、周报、月报与往期归档。">
  <style>{shell_css()}{reelos_brand_css()}</style>
</head>
  <body class="home-page">
  <div class="wrap">
    <header class="home-masthead">
      <div class="home-masthead-top">
        {render_reelos_brand("/", "GitHub 热榜情报", "home-masthead-brand")}
        <span class="home-masthead-edition mono">Daily · Weekly · Monthly</span>
      </div>
      <div class="home-masthead-body">
        <div>
          <span class="home-masthead-kicker mono">Open Source Signals</span>
          <h1>不追热榜，识别开源世界的结构变化。</h1>
        </div>
        <p class="home-masthead-copy">把每天涌现的开源项目，压缩成一句话能看懂、值得继续追踪的信号。</p>
      </div>
    </header>

    <main class="home-main">
      <nav class="home-report-tabs" aria-label="报告类型">
        <button class="home-report-tab" type="button" data-report-tab="daily" aria-controls="home-daily" aria-selected="true">日报</button>
        <button class="home-report-tab" type="button" data-report-tab="weekly" aria-controls="home-weekly" aria-selected="false">周报</button>
        <button class="home-report-tab" type="button" data-report-tab="monthly" aria-controls="home-monthly" aria-selected="false">月报</button>
      </nav>
      {panels}
    </main>
  </div>
  {render_site_footer()}
  <script>
    (() => {{
      const tabs = [...document.querySelectorAll("[data-report-tab]")];
      const panels = [...document.querySelectorAll("[data-report-panel]")];
      const show = (type, updateHash = true) => {{
        if (!panels.some((panel) => panel.dataset.reportPanel === type)) return;
        tabs.forEach((tab) => tab.setAttribute("aria-selected", String(tab.dataset.reportTab === type)));
        panels.forEach((panel) => {{ panel.hidden = panel.dataset.reportPanel !== type; }});
        if (updateHash) history.replaceState(null, "", `#${{type}}`);
      }};
      tabs.forEach((tab) => tab.addEventListener("click", () => show(tab.dataset.reportTab)));
      window.addEventListener("hashchange", () => show(location.hash.slice(1), false));
      const initial = location.hash.slice(1);
      if (["daily", "weekly", "monthly"].includes(initial)) show(initial, false);
    }})();
  </script>
</body>
</html>
"""


def update_readme(period: str, reports: list[dict]) -> None:
    content = f"""# GitHub Signal Intelligence

ReelOS GitHub 热榜情报站，发布 GitHub Trending 日报、周报、月报与往期归档。

## Site

- Production: https://gh.reelos.ai
- Cloudflare Pages: https://github-hot-daily.pages.dev
- GitHub: https://github.com/reelos-ai/github-hot-daily

## Structure

- `/` - 情报中心首页
- `/daily/` - 日报入口
- `/weekly/` - 周报入口
- `/monthly/` - 月报入口
- `/archive/` - 往期归档
- `/reports.json` - 报告索引元数据

## Current Report

- HTML: `/daily/{period}/`
- Top 10 data: `/top10-{period}.json`
- Raw trending data: `/trending-data-{period}.json`
"""
    write_text(ROOT / "README.md", content)


def resolve_daily_period(default_period: str) -> str:
    if (ROOT / f"top10-{default_period}.json").exists() and (ROOT / f"trending-data-{default_period}.json").exists():
        return default_period
    reports_path = ROOT / "reports.json"
    if reports_path.exists():
        reports = read_json(reports_path).get("reports", [])
        latest_daily = latest_report(reports, "daily")
        if latest_daily:
            return latest_daily["period"]
    raise FileNotFoundError(f"Missing daily assets for {default_period} and no fallback daily report found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish daily GitHub trending report pages.")
    parser.add_argument("--period", default=None, help="Daily report period in YYYY-MM-DD.")
    args = parser.parse_args()
    period = resolve_daily_period(args.period or datetime.now().strftime("%Y-%m-%d"))
    stats = load_report_stats(period)
    sync_daily_report_dir(period)
    reports = upsert_report_entry(period, stats)
    write_text(ROOT / "daily" / "index.html", render_daily_index(period, stats, reports))
    write_text(ROOT / "archive" / "index.html", render_archive(reports))
    write_text(ROOT / "index.html", render_home(period, stats, reports))
    update_readme(period, reports)


if __name__ == "__main__":
    main()

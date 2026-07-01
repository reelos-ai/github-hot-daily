#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from restyle_report_pages import restyle_report_html


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://gh.reelos.ai"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def asset_paths(period: str) -> dict:
    compact = period.replace("-", "")
    return {
        "html": f"/monthly/{period}/",
        "top10": f"/monthly-top10-{period}.json",
        "raw_data": f"/monthly-trending-data-{period}.json",
        "report_html": f"/github-trending-monthly-{compact}.html",
    }


def copy_unique_assets(period: str) -> dict:
    compact = period.replace("-", "")
    html_src = ROOT / f"github-trending-monthly-{compact}.html"
    top_src = ROOT / f"top10-{period}-01.json"
    raw_src = ROOT / f"trending-data-{period}-01.json"

    html_dst = ROOT / "monthly" / period / "index.html"
    top_dst = ROOT / f"monthly-top10-{period}.json"
    raw_dst = ROOT / f"monthly-trending-data-{period}.json"

    html_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(html_src, html_dst)
    html_dst.write_text(restyle_report_html(html_dst.read_text(encoding="utf-8")), encoding="utf-8")
    shutil.copyfile(top_src, top_dst)
    shutil.copyfile(raw_src, raw_dst)

    return asset_paths(period)


def load_report_stats(period: str) -> dict:
    top10 = read_json(ROOT / f"monthly-top10-{period}.json")
    data = read_json(ROOT / f"monthly-trending-data-{period}.json")
    return {
        "top10": top10,
        "data": data,
        "top_count": len(top10),
        "candidate_count": len(data),
        "readme_coverage": sum(1 for item in data if item.get("readme_content")),
        "api_failures": sum(1 for item in data if item.get("metadata_error")),
        "top_signal": top10[0]["full_name"] if top10 else "N/A",
    }


def upsert_report_entry(period: str, stats: dict, assets: dict) -> list[dict]:
    reports_path = ROOT / "reports.json"
    if reports_path.exists():
        payload = read_json(reports_path)
        reports = payload.get("reports", [])
    else:
        reports = []

    entry = {
        "type": "monthly",
        "period": period,
        "title": f"GitHub 热榜情报月报 · {period}",
        "html": assets["html"],
        "top10": assets["top10"],
        "raw_data": assets["raw_data"],
        "report_html": assets["report_html"],
        "top_count": stats["top_count"],
        "candidate_count": stats["candidate_count"],
        "readme_coverage": stats["readme_coverage"],
        "api_failures": stats["api_failures"],
    }
    reports = [item for item in reports if not (item.get("type") == "monthly" and item.get("period") == period)]
    reports.insert(0, entry)
    reports.sort(key=lambda item: (item.get("period", ""), item.get("type", "")), reverse=True)

    payload = {
        "updated_at": datetime.now().astimezone().isoformat(timespec="minutes"),
        "site": SITE,
        "reports": reports,
    }
    write_text(reports_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return reports


def latest_report(reports: list[dict], report_type: str) -> dict | None:
    for item in reports:
        if item.get("type") == report_type:
            return item
    return None


def nav_links(active: str) -> str:
    items = [
        ("overview", "/", "Overview"),
        ("daily", "/daily/", "Daily"),
        ("weekly", "/weekly/", "Weekly"),
        ("monthly", "/monthly/", "Monthly"),
        ("archive", "/archive/", "Archive"),
    ]
    links = []
    for key, href, label in items:
        cls = "active" if key == active else ""
        links.append(f'<a class="{cls}" href="{href}">{label}</a>')
    return "".join(links)


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
      --rail:rgba(177,164,148,.34);
      --shadow:0 20px 70px rgba(17,17,17,.07);
      --radius:14px;
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
    .brand{display:flex;align-items:center;gap:12px;min-width:0}
    .brand-mark{
      width:10px;height:10px;border-radius:999px;
      background:linear-gradient(180deg,#ff9f54,#f97316);
      box-shadow:0 0 14px rgba(249,115,22,.22);
    }
    .brand-kicker{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.18em}
    .brand-title{font-size:14px;color:var(--text);white-space:nowrap}
    .nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}
    .nav a{
      padding:8px 12px;border:1px solid var(--line);border-radius:999px;
      background:rgba(255,255,255,.6);color:var(--muted);font-size:12px;
      text-transform:uppercase;letter-spacing:.12em;
      backdrop-filter:blur(12px);
    }
    .nav a.active,.nav a:hover{
      color:var(--text);border-color:var(--line-strong);background:rgba(255,244,232,.92);
    }
    .hero{
      display:grid;grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr);
      gap:18px;margin-top:22px;align-items:stretch;
    }
    .hero-main,.hero-side,.panel,.list,.quote{
      border:1px solid var(--line);
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,253,248,.72));
      box-shadow:var(--shadow);
      backdrop-filter:blur(20px);
    }
    .hero-main{border-radius:22px;padding:24px;position:relative;overflow:hidden}
    .hero-main::before{
      content:"";position:absolute;inset:auto -10% -35% 30%;height:260px;
      background:radial-gradient(circle, rgba(249,115,22,.14), transparent 60%);
      pointer-events:none;
    }
    .eyebrow{
      display:inline-flex;align-items:center;gap:8px;padding:6px 10px;
      border:1px solid var(--line);border-radius:999px;color:var(--soft);
      font-size:11px;text-transform:uppercase;letter-spacing:.16em;background:rgba(255,255,255,.46);
    }
    .eyebrow::before{
      content:"";width:6px;height:6px;border-radius:999px;background:var(--amber);
      box-shadow:0 0 10px rgba(249,115,22,.3);
    }
    h1{margin:16px 0 10px;font-size:clamp(42px,8vw,86px);line-height:.94;letter-spacing:-.045em;font-weight:650;font-family:Sora,"Space Grotesk","IBM Plex Sans",ui-sans-serif,system-ui,sans-serif}
    .headline{display:block;max-width:10ch}
    .headline-line{display:block}
    .ghost-word,.texture-word{display:inline-block;position:relative;font-weight:700;letter-spacing:-.06em}
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
    }
    .lead,.hero-side p,.panel p,.quote p{margin:0;color:var(--soft);font-size:15px}
    .hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
    .btn{
      display:inline-flex;align-items:center;gap:8px;padding:11px 16px;border-radius:999px;
      border:1px solid var(--line);background:rgba(255,255,255,.65);font-size:13px;color:var(--soft)
    }
    .btn.primary{background:#111111;color:#fffaf1;border-color:#111111}
    .hero-side{border-radius:22px;padding:24px;display:flex;flex-direction:column;justify-content:space-between;gap:16px}
    .side-label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.18em}
    .signal-title{font-size:28px;line-height:1.14;letter-spacing:-.03em;margin:0}
    .signal-copy{color:var(--soft);font-size:14px}
    .status-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
    .status-item{border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:6px}
    .status-item.wide{grid-column:1 / -1}
    .status-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.16em}
    .status-value{font-size:13px;color:var(--soft)}
    .section{display:grid;grid-template-columns:120px minmax(0,1fr);gap:18px;margin-top:22px}
    .section-rail{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.18em;padding-top:8px}
    .panel{border-radius:20px;padding:22px}
    .panel h2{margin:0 0 8px;font-size:28px;line-height:1.16;letter-spacing:-.04em}
    .list{border-radius:20px;overflow:hidden}
    .row{
      display:grid;grid-template-columns:120px minmax(0,1fr) 90px;
      gap:12px;padding:16px 18px;border-top:1px solid var(--line);background:rgba(255,255,255,.56)
    }
    .row:first-child{border-top:0}
    .row:hover{background:rgba(255,244,232,.8)}
    .type{font-size:11px;color:var(--muted);text-transform:uppercase}
    .title{font-size:15px;color:var(--text)}
    .meta{font-size:12px;color:var(--muted);text-align:right}
    .card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
    .card{
      border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.48);
      padding:16px;display:block
    }
    .card b{display:block;margin-bottom:8px;font-size:14px}
    .card p{margin:0;font-size:13px;color:var(--muted)}
    .quote{
      margin-top:22px;border-radius:20px;padding:18px 22px;border-left:3px solid var(--amber)
    }
    .mini-list{display:grid;gap:10px}
    .mini-item{display:flex;justify-content:space-between;gap:12px;padding-top:12px;border-top:1px solid var(--line)}
    .mini-item:first-child{padding-top:0;border-top:0}
    .mini-item b{display:block;margin-bottom:4px;font-size:13px}
    .mini-item span{color:var(--muted);font-size:12px}
    @media (max-width:980px){
      .hero,.section,.card-grid,.status-grid{grid-template-columns:1fr}
      .section-rail{padding-top:0}
      .status-item.wide{grid-column:auto}
    }
    @media (max-width:680px){
      .wrap{padding:22px 14px 72px}
      .topbar{align-items:flex-start;flex-direction:column}
      .nav{justify-content:flex-start}
      .row{grid-template-columns:1fr}
      .meta{text-align:left}
      h1{font-size:clamp(38px,15vw,66px)}
    }
    """


def render_monthly_index(reports: list[dict]) -> str:
    monthly_reports = [item for item in reports if item.get("type") == "monthly"]
    latest = monthly_reports[0] if monthly_reports else None
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">Monthly</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in monthly_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Monthly Trend Review · GitHub Signal · ReelOS</title>
  <style>{shell_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div class="brand-copy">
          <div class="brand-kicker mono">ReelOS Long Cycle Desk</div>
          <div class="brand-title">GitHub Signal / Monthly Trend Review</div>
        </div>
      </div>
      <nav class="nav">{nav_links("monthly")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Category Migration Layer</div>
        <h1 class="headline"><span class="headline-line"><span class="ghost-word">Monthly</span> <span class="texture-word">Trend Review</span></span></h1>
        <p class="lead">月报是更慢的判断层。它把一个月里反复出现的仓库和主题抬升到赛道视角，回答哪些方向开始成熟、哪些能力正在基础设施化、哪些只是情绪性泡沫。</p>
        <div class="hero-actions">
          <a class="btn primary" href="{latest["html"] if latest else "/monthly/"}">打开最新月报</a>
          <a class="btn" href="{latest["top10"] if latest else "/monthly/"}">Evidence JSON</a>
          <a class="btn" href="{latest["raw_data"] if latest else "/monthly/"}">Raw Data</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Current Monthly</div>
        <h2 class="signal-title"><a href="{latest["html"] if latest else "/monthly/"}">{latest["title"] if latest else "尚未发布月报"}</a></h2>
        <p class="signal-copy">月报不是把周报拉长，而是把 Top 项目还原成品类、项目簇和赛道迁移，用更低噪音的视角做判断。</p>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Review</div>
      <div>
        <div class="panel">
          <h2>月报目录</h2>
          <p>每期月报都以品类热度地图、项目簇、成熟度评分和下月动作四层结构输出，避免再次退回单项目列表化叙述。</p>
        </div>
        <div class="list">{rows or '<div class="row"><span class="type mono">Empty</span><span class="title">尚未发布月报</span><span class="meta mono">--</span></div>'}</div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def render_archive(reports: list[dict]) -> str:
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in reports[:12]
    )
    daily_count = sum(1 for item in reports if item.get("type") == "daily")
    weekly_count = sum(1 for item in reports if item.get("type") == "weekly")
    monthly_count = sum(1 for item in reports if item.get("type") == "monthly")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Archive · GitHub Signal · ReelOS</title>
  <style>{shell_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div class="brand-copy">
          <div class="brand-kicker mono">ReelOS Archive System</div>
          <div class="brand-title">GitHub Signal / History</div>
        </div>
      </div>
      <nav class="nav">{nav_links("archive")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Stored Reports</div>
        <h1>Signal <span class="texture-word">Archive</span></h1>
        <p class="lead">归档页要让日报、周报、月报回到同一条时间线上。日报负责快采样，周报负责稳定判断，月报负责赛道迁移。</p>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Coverage</div>
        <div class="mini-list">
          <div class="mini-item"><div><b>日报</b><span>快信号入口</span></div><span class="mono">{daily_count}</span></div>
          <div class="mini-item"><div><b>周报</b><span>战略判断层</span></div><span class="mono">{weekly_count}</span></div>
          <div class="mini-item"><div><b>月报</b><span>赛道迁移复盘</span></div><span class="mono">{monthly_count}</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Timeline</div>
      <div>
        <div class="panel">
          <h2>最近归档</h2>
          <p>最近 12 份报告保留在同一条时间轴里，便于横向比较不同周期的判断变化。</p>
        </div>
        <div class="list">{rows}</div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def render_home(reports: list[dict], watchlist: list[dict]) -> str:
    latest_monthly = latest_report(reports, "monthly")
    latest_weekly = latest_report(reports, "weekly")
    latest_daily = latest_report(reports, "daily")
    hero = latest_monthly or latest_weekly or latest_daily or reports[0]
    top_signal = next((item["name"] for item in watchlist if item.get("priority") == "A"), "N/A")
    recent_rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in reports[:6]
    )
    monthly_link = latest_monthly["html"] if latest_monthly else "/monthly/"
    monthly_title = latest_monthly["title"] if latest_monthly else "尚未发布月报"
    watch_names = ", ".join(item["name"] for item in watchlist[:5]) or "暂无"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GitHub Signal Intelligence · ReelOS</title>
  <meta name="description" content="ReelOS GitHub 热榜情报中心：日报、周报、月报与往期归档。">
  <style>{shell_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div class="brand-copy">
          <div class="brand-kicker mono">ReelOS Frontier Desk</div>
          <div class="brand-title">GitHub Signal Intelligence</div>
        </div>
      </div>
      <nav class="nav">{nav_links("overview")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Primary Intelligence Layer</div>
        <h1 class="headline"><span class="headline-line"><span class="ghost-word">Monthly</span> <span class="texture-word">Signal Review</span></span></h1>
        <p class="lead">首页主入口在月初切到月报：优先回答一个月里真正发生了什么赛道迁移。日报继续负责快信号，周报继续负责中周期判断，但首页先展示更慢、更稳的结构性结论。</p>
        <div class="hero-actions">
          <a class="btn primary" href="{hero["html"]}">打开当前主报告</a>
          <a class="btn" href="{latest_weekly["html"] if latest_weekly else '/weekly/'}">查看最新周报</a>
          <a class="btn" href="/archive/">浏览归档</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Current Brief</div>
        <h2 class="signal-title"><a href="{hero["html"]}">{hero["title"]}</a></h2>
        <p class="signal-copy">当前首页主判断层已经切到月报，优先跟踪的长期信号是 <span class="mono">{top_signal}</span>。</p>
        <div class="status-grid">
          <div class="status-item">
            <span class="status-label mono">Primary</span>
            <span class="status-value mono">{hero["type"].upper()}</span>
          </div>
          <div class="status-item">
            <span class="status-label mono">Monthly</span>
            <span class="status-value mono">{latest_monthly["period"] if latest_monthly else "暂无"}</span>
          </div>
          <div class="status-item wide">
            <span class="status-label mono">Latest Monthly</span>
            <span class="status-value"><a href="{monthly_link}">{monthly_title}</a></span>
          </div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Structure</div>
      <div class="panel">
        <h2>首页改成月度主判断台</h2>
        <p>月初这一次主入口不再继续指向周报，而是让月报承担“全站第一屏”的职责，把项目噪音折叠成品类迁移和赛道成熟度判断。</p>
        <div class="card-grid" style="margin-top:16px">
          <a class="card" href="/daily/"><b>Daily Radar</b><p>当天爆点、Top10 与观察池入口，服务速度和刷新率。</p></a>
          <a class="card" href="/weekly/"><b>Weekly Intelligence</b><p>中周期判断层，适合追踪一周内持续升温的主题。</p></a>
          <a class="card" href="/monthly/"><b>Monthly Trend Review</b><p>把 Agent、Memory、MCP、Workspace、Runtime 升到赛道层复盘。</p></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">02 / Feed</div>
      <div>
        <div class="panel">
          <h2>最新流</h2>
          <p>最近 6 份报告保留在开放时间轴中，方便快速回看不同周期的判断重心。</p>
        </div>
        <div class="list">{recent_rows}</div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">03 / Watch</div>
      <div class="panel">
        <h2>观察池优先级</h2>
        <p>观察池继续作为下次日报、周报和月报的输入层，保证首页不是只读展示，而是带有工作流指向的前台。</p>
        <div class="card-grid" style="margin-top:16px">
          <div class="card"><b>A 类信号</b><p>{watch_names}</p></div>
          <div class="card"><b>月报角色</b><p>把连续出现的仓库还原成项目簇、成熟度和泡沫风险判断。</p></div>
          <div class="card"><b>首页原则</b><p>月初优先展示长期判断，避免首屏继续被单日或单周波动占据。</p></div>
        </div>
      </div>
    </section>

    <div class="quote">
      <p>这次首页更新的重点不是换皮，而是把站点的“主判断层”切到月报，让读者先看到赛道迁移，而不是项目噪音。</p>
    </div>
  </div>
</body>
</html>
"""


def update_readme(latest_daily: dict | None, latest_weekly: dict | None, latest_monthly: dict | None) -> None:
    latest_daily_html = latest_daily["html"] if latest_daily else "/daily/"
    latest_weekly_html = latest_weekly["html"] if latest_weekly else "/weekly/"
    latest_monthly_html = latest_monthly["html"] if latest_monthly else "/monthly/"
    latest_monthly_top10 = latest_monthly["top10"] if latest_monthly else ""
    latest_monthly_raw = latest_monthly["raw_data"] if latest_monthly else ""
    content = f"""# GitHub Signal Intelligence

ReelOS GitHub 热榜情报站，发布 GitHub Trending 日报、周报、月报与往期归档。

## Site

- Production: https://gh.reelos.ai
- Cloudflare Pages: https://github-hot-daily.pages.dev
- GitHub: https://github.com/reelos-ai/github-hot-daily

## Structure

- `/` - 情报中心首页
- `/daily/` - 日报入口
- `{latest_daily_html}` - 当前日报
- `/weekly/` - 周报入口
- `{latest_weekly_html}` - 当前周报
- `/monthly/` - 月报入口
- `{latest_monthly_html}` - 当前月报
- `/archive/` - 往期归档
- `/reports.json` - 报告索引元数据

## Current Report

- HTML: `{latest_monthly_html}`
- Top 10 data: `{latest_monthly_top10}`
- Raw trending data: `{latest_monthly_raw}`
"""
    write_text(ROOT / "README.md", content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", default=None, help="Month period like 2026-07. Defaults to latest monthly report period.")
    parser.add_argument("--skip-copy", action="store_true", help="Reuse existing monthly assets and only refresh indexes.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports = read_json(ROOT / "reports.json").get("reports", []) if (ROOT / "reports.json").exists() else []
    period = args.period

    if period is None:
        monthly_htmls = sorted(ROOT.glob("github-trending-monthly-*.html"))
        if not monthly_htmls:
            raise SystemExit("No generated monthly HTML report found.")
        period = f"{monthly_htmls[-1].stem[-6:-2]}-{monthly_htmls[-1].stem[-2:]}"

    if not args.skip_copy:
        assets = copy_unique_assets(period)
        stats = load_report_stats(period)
        reports = upsert_report_entry(period, stats, assets)
    else:
        monthly_exists = any(item.get("type") == "monthly" and item.get("period") == period for item in reports)
        if not monthly_exists:
            assets = asset_paths(period)
            stats = load_report_stats(period)
            reports = upsert_report_entry(period, stats, assets)
        else:
            stats = load_report_stats(period)

    latest_daily = latest_report(reports, "daily")
    latest_weekly = latest_report(reports, "weekly")
    latest_monthly = latest_report(reports, "monthly")
    watchlist = read_json(ROOT / "watchlist.json")
    write_text(ROOT / "monthly" / "index.html", render_monthly_index(reports))
    write_text(ROOT / "archive" / "index.html", render_archive(reports))
    write_text(ROOT / "index.html", render_home(reports, watchlist))
    update_readme(latest_daily, latest_weekly, latest_monthly)


if __name__ == "__main__":
    main()

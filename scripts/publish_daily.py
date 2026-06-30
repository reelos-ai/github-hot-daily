#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://gh.reelos.ai"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
      color-scheme:dark;
      --bg:#05070a;
      --bg-2:#0a0f16;
      --surface:rgba(11,15,22,.72);
      --surface-2:rgba(255,255,255,.035);
      --surface-3:rgba(255,255,255,.06);
      --line:rgba(255,255,255,.1);
      --line-strong:rgba(121,162,255,.34);
      --text:#f5f7fb;
      --muted:rgba(245,247,251,.62);
      --soft:rgba(245,247,251,.78);
      --blue:#79a2ff;
      --cyan:#69e6ff;
      --amber:#ff8a3d;
      --amber-soft:rgba(255,138,61,.16);
      --rail:rgba(105,230,255,.22);
      --ok:#6ee7b7;
      --shadow:0 24px 80px rgba(0,0,0,.32);
      --radius:14px;
      --radius-sm:8px;
    }
    *{box-sizing:border-box}
    html{color-scheme:dark}
    body{
      margin:0;
      color:var(--text);
      font-family:Inter,"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;
      line-height:1.7;
      -webkit-font-smoothing:antialiased;
      text-rendering:optimizeLegibility;
      background:
        radial-gradient(circle at 18% 0%, rgba(121,162,255,.18), transparent 28%),
        radial-gradient(circle at 84% 14%, rgba(255,138,61,.14), transparent 24%),
        linear-gradient(rgba(121,162,255,.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(121,162,255,.05) 1px, transparent 1px),
        linear-gradient(180deg, var(--bg), var(--bg-2));
      background-size:auto,auto,72px 72px,72px 72px,auto;
      background-attachment:fixed;
    }
    a{color:inherit;text-decoration:none}
    a:hover{color:var(--blue)}
    .mono{
      font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;
      letter-spacing:.04em;
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
      border-radius:2px;
      background:linear-gradient(180deg,var(--cyan),var(--blue));
      box-shadow:0 0 18px rgba(105,230,255,.55);
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
      background:rgba(255,255,255,.02);
      color:var(--muted);
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.12em;
    }
    .nav a.active,.nav a:hover{
      color:var(--text);
      border-color:var(--line-strong);
      background:rgba(121,162,255,.12);
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
      background:linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      box-shadow:var(--shadow);
      backdrop-filter:blur(16px);
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
      background:radial-gradient(circle, rgba(255,138,61,.18), transparent 60%);
      pointer-events:none;
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
      background:rgba(255,255,255,.03);
    }
    .eyebrow::before{
      content:"";
      width:6px;
      height:6px;
      border-radius:999px;
      background:var(--amber);
      box-shadow:0 0 12px rgba(255,138,61,.45);
    }
    h1{
      margin:16px 0 10px;
      font-size:clamp(42px,8vw,86px);
      line-height:.98;
      letter-spacing:-.045em;
      font-weight:650;
    }
    h1 .accent{color:var(--amber)}
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
      background:rgba(255,255,255,.03);
      color:var(--text);
      font-size:12px;
      text-transform:uppercase;
      letter-spacing:.14em;
    }
    .btn.primary{
      border-color:rgba(255,138,61,.35);
      background:linear-gradient(180deg, rgba(255,138,61,.22), rgba(255,138,61,.1));
    }
    .hero-side{
      border-radius:22px;
      padding:18px;
      display:grid;
      gap:12px;
      align-content:start;
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
      color:var(--cyan);
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
      color:var(--blue);
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
      background:rgba(121,162,255,.08);
      transform:translateX(2px);
      border-color:rgba(121,162,255,.2);
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
    @media (max-width:980px){
      .hero{grid-template-columns:1fr}
      .stat-grid,.card-grid,.card-grid.three{grid-template-columns:repeat(2,minmax(0,1fr))}
    }
    @media (max-width:680px){
      .wrap{padding:22px 14px 72px}
      .topbar{align-items:flex-start;flex-direction:column}
      .nav{justify-content:flex-start}
      .section{grid-template-columns:1fr}
      .section-rail{padding-top:0}
      .section-rail::after{display:none}
      .stat-grid,.card-grid,.card-grid.three{grid-template-columns:1fr}
      .row{grid-template-columns:1fr;gap:6px}
      .row .meta{text-align:left}
      h1{font-size:clamp(38px,15vw,66px)}
    }
    """


def render_daily_index(period: str, stats: dict, reports: list[dict]) -> str:
    daily_reports = [item for item in reports if item.get("type") == "daily"][:6]
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">Daily</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in daily_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Radar · GitHub Signal · ReelOS</title>
  <style>{shell_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div class="brand-copy">
          <div class="brand-kicker mono">ReelOS Frontier Desk</div>
          <div class="brand-title">GitHub Signal / Daily Radar</div>
        </div>
      </div>
      <nav class="nav">{nav_links("daily")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Daily Signal Layer</div>
        <h1>Daily <span class="accent">Radar</span></h1>
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
          <h2>最近日报</h2>
          <p>按时间连续保留，方便回看哪些信号只是一天热度，哪些方向正在积累成趋势。</p>
        </div>
        <div class="list">{rows}</div>
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
        <h1>Signal <span class="accent">Archive</span></h1>
        <p class="lead">归档页不是简单的往期列表，而是这套 GitHub 情报站的时间轴。日报看噪音、周报看判断、月报看迁移，三种节奏都在这里沉淀成可回查资产。</p>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Coverage</div>
        <div class="mini-list">
          <div class="mini-item"><div><b>日报</b><span>快信号与观察池入口</span></div><span class="mono">{daily_count}</span></div>
          <div class="mini-item"><div><b>周报</b><span>主判断和深度分析</span></div><span class="mono">{weekly_count}</span></div>
          <div class="mini-item"><div><b>月报</b><span>品类级迁移复盘</span></div><span class="mono">{monthly_count}</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Timeline</div>
      <div>
        <div class="panel">
          <h2>最近归档</h2>
          <p>站点持续保留最新 12 份报告入口，便于快速切换到具体周期和上下文。</p>
        </div>
        <div class="list">{rows}</div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def render_home(period: str, stats: dict, reports: list[dict], watchlist: list[dict]) -> str:
    latest_daily = latest_report(reports, "daily")
    latest_weekly = latest_report(reports, "weekly")
    recent = reports[:6]
    recent_rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in recent
    )
    watch_names = ", ".join(item["name"] for item in watchlist[:5]) or "暂无"
    top_names = ", ".join(repo["full_name"] for repo in stats["top10"][:4])
    weekly_title = latest_weekly["title"] if latest_weekly else "尚未发布周报"
    weekly_link = latest_weekly["html"] if latest_weekly else "/weekly/"
    weekly_period = latest_weekly["period"] if latest_weekly else "N/A"
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
        <div class="eyebrow mono">Chinese Open-Source Intel</div>
        <h1>GitHub <span class="accent">Signal</span><br>Intelligence</h1>
        <p class="lead">这不是热榜镜像站，而是一套把 GitHub Trending 转成中文判断的前台。首页优先服务“今天先看什么”，并把日报、周报、月报拆成不同节奏的情报产品，而不是堆在同一个列表里。</p>
        <div class="hero-actions">
          <a class="btn primary" href="{latest_daily["html"] if latest_daily else f"/daily/{period}/"}">打开最新日报</a>
          <a class="btn" href="{weekly_link}">进入主周报</a>
          <a class="btn" href="/archive/">浏览归档</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Live Feed</div>
        <h2 class="signal-title"><a href="{latest_daily["html"] if latest_daily else f"/daily/{period}/"}">{latest_daily["title"] if latest_daily else f"GitHub 热榜情报日报 · {period}"}</a></h2>
        <p class="signal-copy">当前首页锚定 {period} 日报，主信号为 <span class="mono">{stats["top_signal"]}</span>。同时保留周报作为更慢但更重的判断层，避免首页变成单一列表页面。</p>
        <div class="mini-list">
          <div class="mini-item"><div><b>Daily</b><span>快信号 / 观察池 / Top10</span></div><span class="mono">{latest_daily["period"] if latest_daily else period}</span></div>
          <div class="mini-item"><div><b>Weekly</b><span>主报告 / 深度判断</span></div><span class="mono">{weekly_period}</span></div>
          <div class="mini-item"><div><b>Watch</b><span>优先跟踪的项目方向</span></div><span class="mono">{stats["top_count"]}</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Metrics</div>
      <div>
        <div class="stat-grid">
          <div class="metric"><b class="mono">{stats["candidate_count"]}</b><span>候选项目</span></div>
          <div class="metric"><b class="mono">{stats["top_count"]}</b><span>当日 Top</span></div>
          <div class="metric"><b class="mono">{stats["readme_coverage"]}</b><span>README 覆盖</span></div>
          <div class="metric"><b class="mono">{stats["api_failures"]}</b><span>API 失败</span></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">02 / System</div>
      <div class="panel">
        <h2>三层报告，不同判断密度</h2>
        <p>首页用一套更像情报台的布局，把产品节奏讲清楚：日报先抓爆点，周报负责判断是否成立，月报再看赛道迁移。这样视觉和结构都更像一套系统，而不是几个平行入口。</p>
        <div class="card-grid three" style="margin-top:16px">
          <a class="card" href="/daily/"><b>Daily Radar</b><p>移动端优先，适合快速扫当天信号和观察池变化。</p></a>
          <a class="card" href="{weekly_link}"><b>Weekly Intelligence</b><p>{weekly_title} 作为主判断入口，承担深度分析和行动建议。</p></a>
          <a class="card" href="/monthly/"><b>Monthly Trend Review</b><p>把高频仓库和持续出现的方向上升到品类级复盘。</p></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">03 / Flow</div>
      <div>
        <div class="panel">
          <h2>最新流</h2>
          <p>最近更新的报告保留在同一时间轴中，便于对比日报和周报之间的叙事切换。</p>
        </div>
        <div class="list">{recent_rows}</div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">04 / Watchlist</div>
      <div class="panel">
        <h2>当前观察池</h2>
        <p>A 类项目先看持续性与可复用性，B 类项目观察 7-14 天，C 类只保留事实记录。首页直接暴露观察池，是为了让站点更像一块工作台。</p>
        <div class="card-grid three" style="margin-top:16px">
          <div class="card"><b>A 类信号</b><p>{watch_names}</p></div>
          <div class="card"><b>今日高优</b><p>{top_names}</p></div>
          <div class="card"><b>策略焦点</b><p>优先看跨切片重复出现、README 完整且落在 Memory / Runtime / Skill / Workspace 的项目。</p></div>
        </div>
      </div>
    </section>

    <div class="quote">
      <p>首页现在更明确地表达为一套“GitHub 信号前台”：日报提供速度，周报提供判断，观察池提供持续跟踪，而不是把所有入口都压成同一种卡片。</p>
    </div>
  </div>
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


def main() -> None:
    period = datetime.now().strftime("%Y-%m-%d")
    stats = load_report_stats(period)
    sync_daily_report_dir(period)
    reports = upsert_report_entry(period, stats)
    watchlist = read_json(ROOT / "watchlist.json")
    write_text(ROOT / "daily" / "index.html", render_daily_index(period, stats, reports))
    write_text(ROOT / "archive" / "index.html", render_archive(reports))
    write_text(ROOT / "index.html", render_home(period, stats, reports, watchlist))
    update_readme(period, reports)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def asset_paths(period: str) -> dict:
    compact = period.replace("-", "")
    return {
        "html": f"/weekly/{period}/",
        "markdown": f"/github-trending-weekly-{compact}.md",
        "top10": f"/weekly-top10-{period}.json",
        "raw_data": f"/weekly-trending-data-{period}.json",
    }


def copy_unique_assets(period: str) -> dict:
    compact = period.replace("-", "")
    html_src = ROOT / f"github-trending-weekly-{compact}.html"
    top_src = ROOT / f"top10-{period}.json"
    raw_src = ROOT / f"trending-data-{period}.json"

    html_dst = ROOT / "weekly" / period / "index.html"
    top_dst = ROOT / f"weekly-top10-{period}.json"
    raw_dst = ROOT / f"weekly-trending-data-{period}.json"

    html_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(html_src, html_dst)
    shutil.copyfile(top_src, top_dst)
    shutil.copyfile(raw_src, raw_dst)

    return asset_paths(period)


def load_report_stats(period: str) -> dict:
    top10 = read_json(ROOT / f"weekly-top10-{period}.json")
    data = read_json(ROOT / f"weekly-trending-data-{period}.json")
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
        "type": "weekly",
        "period": period,
        "title": f"GitHub 热榜情报周报 · {period}",
        "html": assets["html"],
        "markdown": assets["markdown"],
        "top10": assets["top10"],
        "raw_data": assets["raw_data"],
        "top_count": stats["top_count"],
        "candidate_count": stats["candidate_count"],
        "readme_coverage": stats["readme_coverage"],
        "api_failures": stats["api_failures"],
    }
    reports = [item for item in reports if not (item.get("type") == "weekly" and item.get("period") == period)]
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
      --rail:rgba(105,230,255,.22);
      --shadow:0 24px 80px rgba(0,0,0,.32);
      --radius:14px;
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
    .brand{display:flex;align-items:center;gap:12px;min-width:0}
    .brand-mark{
      width:10px;height:10px;border-radius:2px;
      background:linear-gradient(180deg,var(--cyan),var(--blue));
      box-shadow:0 0 18px rgba(105,230,255,.55);
    }
    .brand-kicker{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.18em}
    .brand-title{font-size:14px;color:var(--text);white-space:nowrap}
    .nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end}
    .nav a{
      padding:8px 12px;border:1px solid var(--line);border-radius:999px;
      background:rgba(255,255,255,.02);color:var(--muted);font-size:12px;
      text-transform:uppercase;letter-spacing:.12em;
    }
    .nav a.active,.nav a:hover{
      color:var(--text);border-color:var(--line-strong);background:rgba(121,162,255,.12);
    }
    .hero{
      display:grid;grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr);
      gap:18px;margin-top:22px;align-items:stretch;
    }
    .hero-main,.hero-side,.panel,.list,.quote{
      border:1px solid var(--line);
      background:linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      box-shadow:var(--shadow);
      backdrop-filter:blur(16px);
    }
    .hero-main{border-radius:22px;padding:24px;position:relative;overflow:hidden}
    .hero-main::before{
      content:"";position:absolute;inset:auto -10% -35% 30%;height:260px;
      background:radial-gradient(circle, rgba(255,138,61,.18), transparent 60%);
      pointer-events:none;
    }
    .eyebrow{
      display:inline-flex;align-items:center;gap:8px;padding:6px 10px;
      border:1px solid var(--line);border-radius:999px;color:var(--soft);
      font-size:11px;text-transform:uppercase;letter-spacing:.16em;background:rgba(255,255,255,.03);
    }
    .eyebrow::before{
      content:"";width:6px;height:6px;border-radius:999px;background:var(--amber);
      box-shadow:0 0 12px rgba(255,138,61,.45);
    }
    h1{margin:16px 0 10px;font-size:clamp(42px,8vw,86px);line-height:.98;letter-spacing:-.045em;font-weight:650}
    h1 .accent{color:var(--amber)}
    .lead{max-width:62ch;margin:0;color:var(--soft);font-size:16px}
    .hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
    .btn{
      display:inline-flex;align-items:center;gap:9px;padding:11px 15px;border-radius:999px;
      border:1px solid var(--line);background:rgba(255,255,255,.03);color:var(--text);
      font-size:12px;text-transform:uppercase;letter-spacing:.14em;
    }
    .btn.primary{border-color:rgba(255,138,61,.35);background:linear-gradient(180deg, rgba(255,138,61,.22), rgba(255,138,61,.1))}
    .hero-side{border-radius:22px;padding:18px;display:grid;gap:12px;align-content:start}
    .side-label{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.16em}
    .signal-title{font-size:24px;line-height:1.15;margin:0}
    .signal-copy{margin:0;color:var(--soft);font-size:14px}
    .stat-grid,.card-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}
    .card-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
    .metric,.card{border:1px solid var(--line);border-radius:14px;background:var(--surface-2);padding:14px;min-width:0}
    .metric b{display:block;font-size:28px;line-height:1;color:var(--text);margin-bottom:6px}
    .metric span,.card p{color:var(--muted);font-size:13px}
    .card b{display:block;margin-bottom:8px;color:var(--cyan);font-size:11px;text-transform:uppercase;letter-spacing:.14em}
    .section{display:grid;grid-template-columns:96px minmax(0,1fr);gap:16px;margin-top:18px;align-items:start}
    .section-rail{
      padding-top:8px;color:var(--blue);font-size:12px;text-transform:uppercase;letter-spacing:.18em;position:relative;
    }
    .section-rail::after{
      content:"";position:absolute;left:8px;top:34px;bottom:-24px;width:1px;background:linear-gradient(180deg,var(--rail),transparent);
    }
    .panel{border-radius:20px;padding:18px}
    .panel h2{margin:0;font-size:26px;line-height:1.15;letter-spacing:-.03em}
    .panel > p{margin:8px 0 0;color:var(--muted);font-size:14px;max-width:68ch}
    .list{border-radius:20px;margin-top:14px;overflow:hidden}
    .row{
      display:grid;grid-template-columns:90px minmax(0,1fr) 104px;gap:12px;align-items:center;
      padding:15px 18px;border-bottom:1px solid var(--line);transition:background .2s ease, transform .2s ease, border-color .2s ease;
    }
    .row:last-child{border-bottom:0}
    .row:hover{background:rgba(121,162,255,.08);transform:translateX(2px);border-color:rgba(121,162,255,.2)}
    .row .type{color:var(--amber);font-size:11px;text-transform:uppercase;letter-spacing:.16em}
    .row .title{font-size:15px;color:var(--text)}
    .row .meta{text-align:right;color:var(--muted);font-size:11px}
    .quote{border-radius:20px;margin-top:22px;padding:18px 20px}
    .quote::before{content:"Conclusion";display:block;margin-bottom:8px;color:var(--amber);font-size:11px;text-transform:uppercase;letter-spacing:.18em}
    .quote p{margin:0;color:var(--text);font-size:18px;line-height:1.6}
    .mini-list{display:grid;gap:10px}
    .mini-item{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;padding:12px 0;border-top:1px solid var(--line)}
    .mini-item:first-child{border-top:0;padding-top:0}
    .mini-item b{display:block;margin-bottom:4px;font-size:13px}
    .mini-item span{color:var(--muted);font-size:12px}
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


def render_weekly_index(reports: list[dict]) -> str:
    weekly_reports = [item for item in reports if item.get("type") == "weekly"][:6]
    latest = weekly_reports[0] if weekly_reports else None
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">Weekly</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in weekly_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Weekly Intelligence · GitHub Signal · ReelOS</title>
  <style>{shell_css()}</style>
</head>
<body>
  <div class="wrap">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark"></span>
        <div class="brand-copy">
          <div class="brand-kicker mono">ReelOS Strategy Layer</div>
          <div class="brand-title">GitHub Signal / Weekly Intelligence</div>
        </div>
      </div>
      <nav class="nav">{nav_links("weekly")}</nav>
    </header>

    <section class="hero">
      <div class="hero-main">
        <div class="eyebrow mono">Strategic Report Layer</div>
        <h1>Weekly <span class="accent">Intelligence</span></h1>
        <p class="lead">周报是整站的主判断层。它不只说“什么火了”，而是把一周内累积的 README、metadata、连续上榜和生态关系整理成能指导决策的判断。</p>
        <div class="hero-actions">
          <a class="btn primary" href="{latest["html"] if latest else "/weekly/"}">打开最新周报</a>
          <a class="btn" href="{latest["top10"] if latest else "/weekly/"}">Top10 JSON</a>
          <a class="btn" href="{latest["raw_data"] if latest else "/weekly/"}">Raw Data</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Current Weekly</div>
        <h2 class="signal-title"><a href="{latest["html"] if latest else "/weekly/"}">{latest["title"] if latest else "尚未发布周报"}</a></h2>
        <p class="signal-copy">周报负责筛出真正值得深挖的开源项目、趋势与赛道信号，把日报的高频波动转成更稳的结论。</p>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Index</div>
      <div>
        <div class="panel">
          <h2>周报目录</h2>
          <p>每期周报保持完整 6 段结构，便于从 Top10 直接跳到深度分析、趋势和 A/B/C 跟进建议。</p>
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
        <p class="lead">归档页保留站点的完整节奏：日报负责快速采样，周报负责稳定判断，月报负责品类迁移。统一视觉后，归档也更像情报系统的一部分。</p>
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
          <p>最近 12 份报告都保留在同一个时间轴中，适合横向比较不同周期的判断变化。</p>
        </div>
        <div class="list">{rows}</div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def render_home(reports: list[dict], watchlist: list[dict]) -> str:
    latest_daily = latest_report(reports, "daily")
    latest_weekly = latest_report(reports, "weekly")
    hero = latest_weekly or latest_daily or reports[0]
    top_signal = next((item["name"] for item in watchlist if item.get("priority") == "A"), "N/A")
    recent_rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in reports[:6]
    )
    latest_daily_text = latest_daily["period"] if latest_daily else "暂无"
    latest_weekly_text = latest_weekly["period"] if latest_weekly else "暂无"
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
        <h1>GitHub <span class="accent">Signal</span><br>Intelligence</h1>
        <p class="lead">周报接管首页主入口后，整站更像一张情报工作台：日报负责速度，周报负责判断，月报负责赛道迁移。视觉上则统一为更锋利的 Frontier Intelligence 系统，而不是松散的工具站。</p>
        <div class="hero-actions">
          <a class="btn primary" href="{hero["html"]}">打开当前主报告</a>
          <a class="btn" href="{latest_daily["html"] if latest_daily else "/daily/"}">查看最新日报</a>
          <a class="btn" href="/archive/">浏览归档</a>
        </div>
      </div>
      <aside class="hero-side">
        <div class="side-label mono">Live Feed</div>
        <h2 class="signal-title"><a href="{hero["html"]}">{hero["title"]}</a></h2>
        <p class="signal-copy">首页当前主入口指向 {hero["type"]} 报告。周报周期为 <span class="mono">{latest_weekly_text}</span>，日报周期为 <span class="mono">{latest_daily_text}</span>，观察池首位信号为 <span class="mono">{top_signal}</span>。</p>
        <div class="mini-list">
          <div class="mini-item"><div><b>Primary</b><span>主入口报告类型</span></div><span class="mono">{hero["type"].upper()}</span></div>
          <div class="mini-item"><div><b>Weekly</b><span>主判断节奏</span></div><span class="mono">{latest_weekly_text}</span></div>
          <div class="mini-item"><div><b>Daily</b><span>快信号节奏</span></div><span class="mono">{latest_daily_text}</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-rail mono">01 / Structure</div>
      <div class="panel">
        <h2>整站结构更像一套情报前台</h2>
        <p>视觉与信息架构同步收紧：首页承接主判断，日报/周报/月报变成清晰的功能区，而不是只有导航切换的兄弟页面。</p>
        <div class="card-grid three" style="margin-top:16px">
          <a class="card" href="/daily/"><b>Daily Radar</b><p>当天爆点、Top10 与观察池入口，服务速度和刷新率。</p></a>
          <a class="card" href="/weekly/"><b>Weekly Intelligence</b><p>主力战略判断，完整 6 段结构，适合沉淀研究和决策。</p></a>
          <a class="card" href="/monthly/"><b>Monthly Trend Review</b><p>观察 Agent、Memory、MCP、Workspace、Runtime 的赛道迁移。</p></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">02 / Feed</div>
      <div>
        <div class="panel">
          <h2>最新流</h2>
          <p>所有最新报告统一进入时间轴，站点不会再因为首页壳层过弱而显得像一批静态文件集合。</p>
        </div>
        <div class="list">{recent_rows}</div>
      </div>
    </section>

    <section class="section">
      <div class="section-rail mono">03 / Watch</div>
      <div class="panel">
        <h2>观察池优先级</h2>
        <p>首页直接暴露观察池，保证这不是只读展示层，而是对下一次日报和周报有输入的工作台。</p>
        <div class="card-grid three" style="margin-top:16px">
          <div class="card"><b>A 类信号</b><p>{watch_names}</p></div>
          <div class="card"><b>周报角色</b><p>把日报的高频波动折叠成更稳的趋势判断和跟进行动。</p></div>
          <div class="card"><b>设计原则</b><p>统一为高密度情报视觉，减少圆角卡片泛滥与弱层级导航。</p></div>
        </div>
      </div>
    </section>

    <div class="quote">
      <p>新版首页的核心变化不是“更好看”，而是更像一套真正有主次、有节奏、有工作流的 GitHub 情报前台。</p>
    </div>
  </div>
</body>
</html>
"""


def update_readme(latest_daily: dict | None, latest_weekly: dict | None) -> None:
    latest_daily_html = latest_daily["html"] if latest_daily else "/daily/"
    latest_daily_top10 = latest_daily["top10"] if latest_daily else ""
    latest_daily_raw = latest_daily["raw_data"] if latest_daily else ""
    latest_weekly_html = latest_weekly["html"] if latest_weekly else "/weekly/"
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
- `{latest_weekly_html}` - 当前周报
- `/monthly/` - 月报入口
- `/archive/` - 往期归档
- `/reports.json` - 报告索引元数据

## Current Report

- HTML: `{latest_daily_html}`
- Top 10 data: `{latest_daily_top10}`
- Raw trending data: `{latest_daily_raw}`
"""
    write_text(ROOT / "README.md", content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-copy", action="store_true", help="Reuse existing weekly assets and only refresh indexes.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports = read_json(ROOT / "reports.json").get("reports", []) if (ROOT / "reports.json").exists() else []
    if not reports:
      raise SystemExit("reports.json is missing or empty.")

    latest_weekly = latest_report(reports, "weekly")
    if latest_weekly is None:
        raise SystemExit("No weekly report found in reports.json.")

    period = latest_weekly["period"]
    if not args.skip_copy:
        assets = copy_unique_assets(period)
        stats = load_report_stats(period)
        reports = upsert_report_entry(period, stats, assets)
    else:
        stats = load_report_stats(period)

    latest_daily = latest_report(reports, "daily")
    watchlist = read_json(ROOT / "watchlist.json")
    write_text(ROOT / "weekly" / "index.html", render_weekly_index(reports))
    write_text(ROOT / "archive" / "index.html", render_archive(reports))
    write_text(ROOT / "index.html", render_home(reports, watchlist))
    update_readme(latest_daily, latest_report(reports, "weekly"))


if __name__ == "__main__":
    main()

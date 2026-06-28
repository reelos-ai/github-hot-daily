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
    md_src = ROOT / f"github-trending-weekly-{compact}.md"
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


def render_weekly_index(reports: list[dict]) -> str:
    weekly_reports = [item for item in reports if item.get("type") == "weekly"][:6]
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type">Weekly</span><span>{item["title"]}</span><span class="meta">Top {item["top_count"]}</span></a>'
        for item in weekly_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Weekly Intelligence · GitHub Signal · ReelOS</title>
  <style>
    body{{margin:0;background:#05070a;color:#fffaf1;font-family:Inter,"PingFang SC",ui-sans-serif,system-ui,sans-serif;line-height:1.72}}
    a{{color:inherit;text-decoration:none}}a:hover{{color:#7d96ff}}.wrap{{max-width:820px;margin:0 auto;padding:44px 22px 80px}}
    .top{{display:flex;justify-content:space-between;gap:16px;align-items:center;border-bottom:1px solid rgba(255,250,241,.085);padding-bottom:18px}}
    .brand{{color:rgba(255,250,241,.58);font-size:13px;letter-spacing:.06em;text-transform:uppercase}}.nav{{display:flex;gap:8px;flex-wrap:wrap}}
    .nav a{{border:1px solid rgba(255,250,241,.12);border-radius:999px;padding:5px 11px;color:rgba(255,250,241,.7);font-size:12px}}.nav a.active{{background:rgba(125,150,255,.16);color:#fffaf1}}
    h1{{font-size:clamp(36px,6vw,58px);line-height:1.06;margin:28px 0 10px}}.ac{{color:#fb8b3c}}p{{color:rgba(255,250,241,.68)}}
    .list{{border:1px solid rgba(255,250,241,.085);border-radius:10px;overflow:hidden;background:rgba(255,250,241,.032);margin-top:22px}}.row{{display:grid;grid-template-columns:96px 1fr 90px;gap:12px;padding:14px;border-bottom:1px solid rgba(255,250,241,.085);align-items:center}}.row:last-child{{border-bottom:0}}.type{{color:#fb8b3c;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-transform:uppercase}}.meta{{color:rgba(255,250,241,.55);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-align:right}}
    @media(max-width:620px){{.top{{align-items:flex-start;flex-direction:column}}.row{{grid-template-columns:1fr}}.meta{{text-align:left}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div class="brand">ReelOS · GitHub Signal</div>
      <nav class="nav"><a href="/">Overview</a><a href="/daily/">Daily</a><a class="active" href="/weekly/">Weekly</a><a href="/monthly/">Monthly</a><a href="/archive/">Archive</a></nav>
    </div>
    <h1>Weekly <span class="ac">Intelligence</span></h1>
    <p>周报是主力战略产物：完整 6 段结构，覆盖 Top10、深度分析、趋势、六视角、跟进建议和结论。</p>
    <div class="list">{rows}</div>
  </div>
</body>
</html>
"""


def render_archive(reports: list[dict]) -> str:
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type">{item["type"].title()}</span><span>{item["title"]}</span><span class="meta">Top {item["top_count"]}</span></a>'
        for item in reports[:10]
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Archive · GitHub Signal · ReelOS</title>
  <style>
    body{{margin:0;background:#05070a;color:#fffaf1;font-family:Inter,"PingFang SC",ui-sans-serif,system-ui,sans-serif;line-height:1.72}}
    a{{color:inherit;text-decoration:none}}a:hover{{color:#7d96ff}}.wrap{{max-width:820px;margin:0 auto;padding:44px 22px 80px}}
    .top{{display:flex;justify-content:space-between;gap:16px;align-items:center;border-bottom:1px solid rgba(255,250,241,.085);padding-bottom:18px}}
    .brand{{color:rgba(255,250,241,.58);font-size:13px;letter-spacing:.06em;text-transform:uppercase}}.nav{{display:flex;gap:8px;flex-wrap:wrap}}
    .nav a{{border:1px solid rgba(255,250,241,.12);border-radius:999px;padding:5px 11px;color:rgba(255,250,241,.7);font-size:12px}}.nav a.active{{background:rgba(125,150,255,.16);color:#fffaf1}}
    h1{{font-size:clamp(36px,6vw,58px);line-height:1.06;margin:28px 0 10px}}.ac{{color:#fb8b3c}}
    p{{color:rgba(255,250,241,.68)}}.list{{border:1px solid rgba(255,250,241,.085);border-radius:10px;overflow:hidden;background:rgba(255,250,241,.032);margin-top:22px}}
    .row{{display:grid;grid-template-columns:92px 1fr 90px;gap:12px;padding:14px;border-bottom:1px solid rgba(255,250,241,.085);align-items:center}}
    .row:last-child{{border-bottom:0}}.type{{color:#fb8b3c;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-transform:uppercase}}.meta{{color:rgba(255,250,241,.55);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-align:right}}
    @media(max-width:620px){{.top{{align-items:flex-start;flex-direction:column}}.row{{grid-template-columns:1fr}}.meta{{text-align:left}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div class="brand">ReelOS · GitHub Signal</div>
      <nav class="nav"><a href="/">Overview</a><a href="/daily/">Daily</a><a href="/weekly/">Weekly</a><a href="/monthly/">Monthly</a><a class="active" href="/archive/">Archive</a></nav>
    </div>
    <h1>往期 <span class="ac">归档</span></h1>
    <p>按周期沉淀报告，日报负责捕捉快信号，周报负责做深判断，月报继续补足品类迁移观察。</p>
    <div class="list">{rows}</div>
  </div>
</body>
</html>
"""


def latest_report(reports: list[dict], report_type: str) -> dict | None:
    for item in reports:
        if item.get("type") == report_type:
            return item
    return None


def render_home(reports: list[dict], watchlist: list[dict]) -> str:
    latest_daily = latest_report(reports, "daily")
    latest_weekly = latest_report(reports, "weekly")
    hero = latest_weekly or latest_daily or reports[0]
    hero_type = hero["type"].upper()
    top_signal = next((item["name"] for item in watchlist if item.get("priority") == "A"), "N/A")
    recent_rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in reports[:4]
    )
    latest_daily_text = latest_daily["period"] if latest_daily else "暂无"
    latest_weekly_text = latest_weekly["period"] if latest_weekly else "暂无"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GitHub Signal Intelligence · ReelOS</title>
  <meta name="description" content="ReelOS GitHub 热榜情报中心：日报、周报、月报与往期归档。">
  <style>
    :root {{ color-scheme: dark; --bg:#05070a; --panel:rgba(255,250,241,.032); --panel2:rgba(255,250,241,.055); --line:rgba(255,250,241,.085); --line2:rgba(255,250,241,.16); --text:#fffaf1; --muted:rgba(255,250,241,.58); --soft:rgba(255,250,241,.74); --blue:#7d96ff; --blue-dim:rgba(125,150,255,.16); --orange:#fb8b3c; --orange-dim:rgba(251,139,60,.14); --rail:rgba(125,150,255,.28); --grid:rgba(91,124,255,.045); }}
    * {{ box-sizing:border-box; }} html {{ color-scheme:dark; }} body {{ margin:0; background:var(--bg); color:var(--text); font-family:Inter,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",ui-sans-serif,system-ui,sans-serif; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; line-height:1.72; background-image:radial-gradient(circle at 50% -12%, rgba(91,124,255,.10), transparent 58%),linear-gradient(var(--grid) 1px, transparent 1px),linear-gradient(90deg, var(--grid) 1px, transparent 1px); background-size:auto,72px 72px,72px 72px; background-attachment:fixed; }}
    a {{ color:inherit; text-decoration:none; }} a:hover {{ color:var(--blue); }} .mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }} .wrap {{ max-width:860px; margin:0 auto; padding:46px 24px 92px; }} .toprow {{ display:flex; align-items:center; justify-content:space-between; gap:18px; border-bottom:1px solid var(--line); padding-bottom:20px; }} .brand {{ display:flex; align-items:center; gap:11px; color:var(--muted); font-size:13px; letter-spacing:.06em; text-transform:uppercase; }} .dot {{ width:8px; height:8px; border-radius:50%; background:var(--orange); box-shadow:0 0 16px var(--orange); }} .nav {{ display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end; }} .nav a {{ padding:5px 11px; border:1px solid var(--line); border-radius:999px; color:var(--muted); font-size:12px; background:var(--panel); }} .nav a.active, .nav a:hover {{ color:var(--text); border-color:var(--blue); background:var(--blue-dim); }} h1 {{ margin:28px 0 8px; font-size:clamp(38px,7vw,64px); line-height:1.04; letter-spacing:-.01em; font-weight:790; }} h1 .ac {{ color:var(--orange); }} .lead {{ max-width:680px; margin:0; color:var(--soft); font-size:16px; line-height:1.8; }} .chips {{ display:flex; flex-wrap:wrap; gap:9px; margin-top:18px; }} .chip {{ border:1px solid var(--line2); border-radius:999px; padding:4px 12px; color:var(--text); font-size:11.5px; letter-spacing:.03em; background:var(--panel); }} .chip b {{ color:var(--orange); }} .timeline {{ position:relative; margin-top:30px; }} .timeline::before {{ content:""; position:absolute; left:20px; top:8px; bottom:22px; width:1px; background:linear-gradient(180deg,var(--rail),transparent); }} .section {{ position:relative; padding-left:66px; margin-top:24px; }} .section::before {{ content:attr(data-n); position:absolute; left:0; top:2px; width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:var(--blue); background:#070a0f; border:1px solid var(--line2); font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px; }} h2 {{ margin:0 0 6px; font-size:18px; line-height:1.35; }} .section > p {{ margin:0 0 12px; color:var(--muted); font-size:13px; }} .hero-report {{ border:1px solid var(--line2); border-radius:12px; background:linear-gradient(120deg,var(--orange-dim),var(--panel) 48%,transparent); padding:18px; }} .hero-report h3 {{ margin:0; font-size:24px; line-height:1.25; }} .hero-report p {{ margin:9px 0 0; color:var(--soft); font-size:14px; }} .actions {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }} .btn {{ display:inline-flex; align-items:center; gap:8px; border:1px solid var(--line2); border-radius:999px; padding:7px 13px; color:var(--text); background:var(--panel2); font-size:12px; }} .btn.primary {{ border-color:rgba(251,139,60,.45); background:var(--orange-dim); color:var(--text); }} .grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }} .card {{ border:1px solid var(--line); border-radius:10px; background:var(--panel); padding:14px; min-width:0; }} .card b {{ display:block; color:var(--blue); font-size:12px; margin-bottom:6px; }} .card p {{ margin:0; color:var(--soft); font-size:13px; line-height:1.65; }} .list {{ border:1px solid var(--line); border-radius:10px; overflow:hidden; background:var(--panel); }} .row {{ display:grid; grid-template-columns:92px 1fr 90px; gap:12px; padding:13px 14px; border-bottom:1px solid var(--line); align-items:center; }} .row:last-child {{ border-bottom:0; }} .row .type {{ color:var(--orange); font-size:11px; letter-spacing:.06em; text-transform:uppercase; }} .row .title {{ color:var(--text); font-size:14px; }} .row .meta {{ color:var(--muted); font-size:11px; text-align:right; }} blockquote {{ margin:28px 0 0 66px; padding:16px 20px; border:1px solid var(--line); border-left:3px solid var(--orange); border-radius:0 12px 12px 0; background:linear-gradient(100deg,var(--orange-dim),transparent 70%); font-size:18px; line-height:1.58; }}
    @media (max-width:680px) {{ .wrap {{ padding:32px 16px 70px; }} .toprow {{ align-items:flex-start; flex-direction:column; }} .nav {{ justify-content:flex-start; }} .grid {{ grid-template-columns:1fr; }} .section {{ padding-left:50px; }} .section::before {{ width:38px; height:38px; }} .timeline::before {{ left:18px; }} .row {{ grid-template-columns:1fr; gap:3px; }} .row .meta {{ text-align:left; }} blockquote {{ margin-left:50px; font-size:16px; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="toprow">
        <div class="brand"><span class="dot"></span> ReelOS · GitHub Signal</div>
        <nav class="nav" aria-label="报告导航">
          <a class="active" href="/">Overview</a>
          <a href="/daily/">Daily</a>
          <a href="/weekly/">Weekly</a>
          <a href="/monthly/">Monthly</a>
          <a href="/archive/">Archive</a>
        </nav>
      </div>
      <h1>GitHub <span class="ac">热榜</span> 情报中心</h1>
      <p class="lead">把 GitHub Trending 从热度列表加工成可决策的 AI Builder / Investor / Product / Architecture 情报系统；首页保留日报节奏，同时把最新周报前置为主判断入口。</p>
      <div class="chips">
        <span class="chip">LATEST / <b>{hero_type}</b></span>
        <span class="chip">WEEKLY / <b>{latest_weekly_text}</b></span>
        <span class="chip">DAILY / <b>{latest_daily_text}</b></span>
        <span class="chip">WATCH / <b>{top_signal}</b></span>
      </div>
    </header>

    <main class="timeline">
      <section class="section" data-n="01">
        <h2>最新主报告</h2>
        <p>周报负责战略判断，日报负责早信号捕捉；首页优先把当前最值得读的一篇放在最前。</p>
        <div class="hero-report">
          <h3><a href="{hero["html"]}">{hero["title"]}</a></h3>
          <p>当前主入口已切到 {hero["period"]} 的 {hero["type"]} 报告。周报提供完整 6 段结构，日报继续服务观察池更新。</p>
          <div class="actions">
            <a class="btn primary" href="{hero["html"]}">打开报告</a>
            <a class="btn" href="{hero["top10"]}">Top10 JSON</a>
            <a class="btn" href="{hero["raw_data"]}">Raw Data</a>
          </div>
        </div>
      </section>

      <section class="section" data-n="02">
        <h2>报告类型</h2>
        <p>同一套数据流水线，不同周期服务不同决策节奏。</p>
        <div class="grid">
          <a class="card" href="/daily/"><b>Daily Radar</b><p>当天热度爆发、早信号、新项目和噪音提示，适合每日监控与观察池更新。</p></a>
          <a class="card" href="/weekly/"><b>Weekly Intelligence</b><p>主力战略报告，保留完整 6 段结构，决定建什么、看什么、防什么。</p></a>
          <a class="card" href="/monthly/"><b>Monthly Trend Review</b><p>品类级趋势复盘，观察 Agent、Memory、MCP、Workspace、Runtime 成熟度。</p></a>
        </div>
      </section>

      <section class="section" data-n="03">
        <h2>最近报告</h2>
        <p>往期沉淀为可检索资产，而不是被最新单篇覆盖。</p>
        <div class="list">{recent_rows}</div>
      </section>

      <section class="section" data-n="04">
        <h2>观察池</h2>
        <p>A 类立即深挖，B 类观察 7-14 天，C 类仅保留基础记录。</p>
        <div class="grid">
          <div class="card"><b>A 类信号</b><p>{", ".join(item["name"] for item in watchlist[:5]) or "暂无"}</p></div>
          <div class="card"><b>周报职责</b><p>把日报沉淀为判断：趋势是否成立、项目是否值得集成、风险是否可控。</p></div>
          <div class="card"><b>跟踪重点</b><p>优先看跨切片重复出现、README 完整且关系标签落在 Memory / Runtime / Skill / Workspace 的项目。</p></div>
        </div>
      </section>

      <blockquote>当前站点已同时维护“日报抓早信号”和“周报做主判断”两条入口，最新周报已进入首页主入口。</blockquote>
    </main>
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
    period = datetime.now().strftime("%Y-%m-%d")
    assets = asset_paths(period) if args.skip_copy else copy_unique_assets(period)
    stats = load_report_stats(period)
    reports = upsert_report_entry(period, stats, assets)
    watchlist = read_json(ROOT / "watchlist.json")
    write_text(ROOT / "weekly" / "index.html", render_weekly_index(reports))
    write_text(ROOT / "archive" / "index.html", render_archive(reports))
    write_text(ROOT / "index.html", render_home(reports, watchlist))
    update_readme(latest_report(reports, "daily"), latest_report(reports, "weekly"))


if __name__ == "__main__":
    main()

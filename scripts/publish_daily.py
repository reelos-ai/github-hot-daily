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


def render_daily_index(period: str, stats: dict, reports: list[dict]) -> str:
    daily_reports = [item for item in reports if item.get("type") == "daily"][:6]
    rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type">Daily</span><span>{item["title"]}</span><span class="meta">Top {item["top_count"]}</span></a>'
        for item in daily_reports
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Radar · GitHub Signal · ReelOS</title>
  <style>
    body{{margin:0;background:#05070a;color:#fffaf1;font-family:Inter,"PingFang SC",ui-sans-serif,system-ui,sans-serif;line-height:1.72}}
    a{{color:inherit;text-decoration:none}}a:hover{{color:#7d96ff}}.wrap{{max-width:820px;margin:0 auto;padding:44px 22px 80px}}
    .top{{display:flex;justify-content:space-between;gap:16px;align-items:center;border-bottom:1px solid rgba(255,250,241,.085);padding-bottom:18px}}
    .brand{{color:rgba(255,250,241,.58);font-size:13px;letter-spacing:.06em;text-transform:uppercase}}.nav{{display:flex;gap:8px;flex-wrap:wrap}}
    .nav a{{border:1px solid rgba(255,250,241,.12);border-radius:999px;padding:5px 11px;color:rgba(255,250,241,.7);font-size:12px}}.nav a.active{{background:rgba(125,150,255,.16);color:#fffaf1}}
    h1{{font-size:clamp(36px,6vw,58px);line-height:1.06;margin:28px 0 10px}}.ac{{color:#fb8b3c}}p{{color:rgba(255,250,241,.68)}}
    .hero{{margin-top:22px;border:1px solid rgba(255,250,241,.085);border-left:3px solid #fb8b3c;border-radius:0 12px 12px 0;padding:16px 18px;background:rgba(251,139,60,.12)}}
    .hero h2{{margin:0;font-size:24px;line-height:1.25}} .hero p{{margin:8px 0 0;font-size:14px}}
    .actions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}} .btn{{border:1px solid rgba(255,250,241,.12);border-radius:999px;padding:7px 12px;font-size:12px;background:rgba(255,250,241,.03)}}
    .grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:22px}}.card{{border:1px solid rgba(255,250,241,.085);border-radius:10px;background:rgba(255,250,241,.032);padding:14px}}.card b{{display:block;color:#7d96ff;font-size:12px;margin-bottom:6px}}.card p{{margin:0;font-size:13px}}
    .list{{border:1px solid rgba(255,250,241,.085);border-radius:10px;overflow:hidden;background:rgba(255,250,241,.032);margin-top:22px}}.row{{display:grid;grid-template-columns:96px 1fr 90px;gap:12px;padding:14px;border-bottom:1px solid rgba(255,250,241,.085);align-items:center}}.row:last-child{{border-bottom:0}}.type{{color:#fb8b3c;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-transform:uppercase}}.meta{{color:rgba(255,250,241,.55);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;text-align:right}}
    @media(max-width:620px){{.top{{align-items:flex-start;flex-direction:column}}.grid{{grid-template-columns:1fr}}.row{{grid-template-columns:1fr}}.meta{{text-align:left}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div class="brand">ReelOS · GitHub Signal</div>
      <nav class="nav"><a href="/">Overview</a><a class="active" href="/daily/">Daily</a><a href="/weekly/">Weekly</a><a href="/monthly/">Monthly</a><a href="/archive/">Archive</a></nav>
    </div>
    <h1>Daily <span class="ac">Radar</span></h1>
    <p>日报用于捕捉当天爆发项目，信号更早，但噪音更高。它不追求完整战略判断，而是判断哪些项目值得进入观察池。</p>
    <div class="hero">
      <h2><a href="/daily/{period}/">GitHub 热榜情报日报 · {period}</a></h2>
      <p>本期 Top signal：{stats["top_signal"]}。六个切片共抓取 {stats["candidate_count"]} 个候选项目，Top 10 已完成中文情报化处理。</p>
      <div class="actions"><a class="btn" href="/daily/{period}/">打开日报</a><a class="btn" href="/top10-{period}.json">Top10 JSON</a><a class="btn" href="/trending-data-{period}.json">Raw Data</a></div>
    </div>
    <div class="grid">
      <div class="card"><b>Top 10</b><p>当天 GitHub Trending 候选项目与加权排序。</p></div>
      <div class="card"><b>中文趋势卡片</b><p>保持趋势观察为中文卡片式结论，方便移动端快速阅读。</p></div>
      <div class="card"><b>观察池</b><p>把值得周报深挖的项目标记为 A/B/C，并写回 watchlist。</p></div>
    </div>
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


def render_home(period: str, stats: dict, reports: list[dict], watchlist: list[dict]) -> str:
    recent = reports[:4]
    recent_rows = "".join(
        f'<a class="row" href="{item["html"]}"><span class="type mono">{item["type"].title()}</span><span class="title">{item["title"]}</span><span class="meta mono">Top {item["top_count"]}</span></a>'
        for item in recent
    )
    watch_text = ", ".join(item["name"] for item in watchlist[:5]) or "暂无"
    top_names = ", ".join(repo["full_name"] for repo in stats["top10"][:5])
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
    a {{ color:inherit; text-decoration:none; }} a:hover {{ color:var(--blue); }} .mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }} .wrap {{ max-width:860px; margin:0 auto; padding:46px 24px 92px; }} .toprow {{ display:flex; align-items:center; justify-content:space-between; gap:18px; border-bottom:1px solid var(--line); padding-bottom:20px; }} .brand {{ display:flex; align-items:center; gap:11px; color:var(--muted); font-size:13px; letter-spacing:.06em; text-transform:uppercase; }} .dot {{ width:8px; height:8px; border-radius:50%; background:var(--orange); box-shadow:0 0 16px var(--orange); }} .nav {{ display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end; }} .nav a {{ padding:5px 11px; border:1px solid var(--line); border-radius:999px; color:var(--muted); font-size:12px; background:var(--panel); }} .nav a.active, .nav a:hover {{ color:var(--text); border-color:var(--blue); background:var(--blue-dim); }} h1 {{ margin:28px 0 8px; font-size:clamp(38px,7vw,64px); line-height:1.04; letter-spacing:-.01em; font-weight:790; }} h1 .ac {{ color:var(--orange); }} .lead {{ max-width:680px; margin:0; color:var(--soft); font-size:16px; line-height:1.8; }} .chips {{ display:flex; flex-wrap:wrap; gap:9px; margin-top:18px; }} .chip {{ border:1px solid var(--line2); border-radius:999px; padding:4px 12px; color:var(--text); font-size:11.5px; letter-spacing:.03em; background:var(--panel); }} .chip b {{ color:var(--orange); }} .stats {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin-top:24px; }} .stat {{ border:1px solid var(--line); border-radius:8px; background:linear-gradient(160deg,var(--panel2),var(--panel)); padding:12px 14px; }} .stat b {{ display:block; color:var(--orange); font-size:24px; line-height:1.1; }} .stat span {{ color:var(--muted); font-size:12px; }} .timeline {{ position:relative; margin-top:30px; }} .timeline::before {{ content:""; position:absolute; left:20px; top:8px; bottom:22px; width:1px; background:linear-gradient(180deg,var(--rail),transparent); }} .section {{ position:relative; padding-left:66px; margin-top:24px; }} .section::before {{ content:attr(data-n); position:absolute; left:0; top:2px; width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:var(--blue); background:#070a0f; border:1px solid var(--line2); font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px; }} h2 {{ margin:0 0 6px; font-size:18px; line-height:1.35; }} .section > p {{ margin:0 0 12px; color:var(--muted); font-size:13px; }} .hero-report {{ border:1px solid var(--line2); border-radius:12px; background:linear-gradient(120deg,var(--orange-dim),var(--panel) 48%,transparent); padding:18px; }} .hero-report h3 {{ margin:0; font-size:24px; line-height:1.25; }} .hero-report p {{ margin:9px 0 0; color:var(--soft); font-size:14px; }} .actions {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }} .btn {{ display:inline-flex; align-items:center; gap:8px; border:1px solid var(--line2); border-radius:999px; padding:7px 13px; color:var(--text); background:var(--panel2); font-size:12px; }} .btn.primary {{ border-color:rgba(251,139,60,.45); background:var(--orange-dim); color:var(--text); }} .grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }} .card {{ border:1px solid var(--line); border-radius:10px; background:var(--panel); padding:14px; min-width:0; }} .card b {{ display:block; color:var(--blue); font-size:12px; margin-bottom:6px; }} .card p {{ margin:0; color:var(--soft); font-size:13px; line-height:1.65; }} .list {{ border:1px solid var(--line); border-radius:10px; overflow:hidden; background:var(--panel); }} .row {{ display:grid; grid-template-columns:92px 1fr 90px; gap:12px; padding:13px 14px; border-bottom:1px solid var(--line); align-items:center; }} .row:last-child {{ border-bottom:0; }} .row .type {{ color:var(--orange); font-size:11px; letter-spacing:.06em; text-transform:uppercase; }} .row .title {{ color:var(--text); font-size:14px; }} .row .meta {{ color:var(--muted); font-size:11px; text-align:right; }} blockquote {{ margin:28px 0 0 66px; padding:16px 20px; border:1px solid var(--line); border-left:3px solid var(--orange); border-radius:0 12px 12px 0; background:linear-gradient(100deg,var(--orange-dim),transparent 70%); font-size:18px; line-height:1.58; }}
    @media (max-width:680px) {{ .wrap {{ padding:32px 16px 70px; }} .toprow {{ align-items:flex-start; flex-direction:column; }} .nav {{ justify-content:flex-start; }} .stats,.grid {{ grid-template-columns:1fr; }} .section {{ padding-left:50px; }} .section::before {{ width:38px; height:38px; }} .timeline::before {{ left:18px; }} .row {{ grid-template-columns:1fr; gap:3px; }} .row .meta {{ text-align:left; }} blockquote {{ margin-left:50px; font-size:16px; }} }}
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
      <p class="lead">把 GitHub Trending 从热度列表加工成可决策的 AI Builder / Investor / Product / Architecture 情报系统；首页始终突出最新日报，周报继续承担更长周期的战略判断。</p>
      <div class="chips">
        <span class="chip">LATEST / <b>DAILY</b></span>
        <span class="chip">DATE / <b>{period}</b></span>
        <span class="chip">TOP SIGNAL / <b>{stats["top_signal"]}</b></span>
        <span class="chip">STATUS / <b>LIVE</b></span>
      </div>
      <section class="stats">
        <div class="stat"><b class="mono">{stats["candidate_count"]}</b><span>候选项目</span></div>
        <div class="stat"><b class="mono">{stats["top_count"]}</b><span>Top 项目</span></div>
        <div class="stat"><b class="mono">{stats["readme_coverage"]}</b><span>README 覆盖</span></div>
        <div class="stat"><b class="mono">{stats["api_failures"]}</b><span>API 失败</span></div>
      </section>
    </header>

    <main class="timeline">
      <section class="section" data-n="01">
        <h2>最新日报</h2>
        <p>日报负责捕捉当天爆发项目与早信号，优先回答“今天值得先看什么”。</p>
        <div class="hero-report">
          <h3><a href="/daily/{period}/">GitHub 热榜情报日报 · {period}</a></h3>
          <p>本期 Top signal：{stats["top_signal"]}。今天的信号集中在 memory infra、runtime 工具、MCP 服务和高密度开发者工作台能力。</p>
          <div class="actions">
            <a class="btn primary" href="/daily/{period}/">打开日报</a>
            <a class="btn" href="/top10-{period}.json">Top10 JSON</a>
            <a class="btn" href="/trending-data-{period}.json">Raw Data</a>
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
          <div class="card"><b>A 类</b><p>{watch_text}</p></div>
          <div class="card"><b>新增日报 Top</b><p>{top_names}</p></div>
          <div class="card"><b>跟踪重点</b><p>优先看跨切片重复出现、README 完整且关系标签落在 Memory / Runtime / Skill / Workspace 的项目。</p></div>
        </div>
      </section>

      <blockquote>日报抓早信号，周报做战略判断，月报看品类迁移；当前首页已切换到 {period} 的新日报。</blockquote>
    </main>
  </div>
</body>
</html>
"""


def update_readme(period: str) -> None:
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
- `/weekly/2026-06-25/` - 当前周报
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
    update_readme(period)


if __name__ == "__main__":
    main()

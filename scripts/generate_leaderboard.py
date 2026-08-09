#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_RE = re.compile(r"snapshot-(\d{8})\.json$")
TOP10_RE = re.compile(r"top10-(\d{4}-\d{2}-\d{2})\.json$")
CHINESE_RE = re.compile(r"[\u3400-\u9fff]")
GENERIC_SUMMARY_MARKERS = (
    "更适合被看作",
    "方向的候选样本",
    "方向的持续观察样本",
)
PROJECT_SUMMARY_RE = re.compile(
    r'<article class="project-row">.*?<h3>(.*?)</h3>.*?<p>(.*?)</p>',
    re.DOTALL,
)

KEYWORD_LABELS = {
    "agent": "Agent 工具",
    "agent loop": "Agent 循环",
    "agentic-coding": "Agent 编码",
    "agentic-ai": "Agent AI 工作流",
    "agent-ide": "Agent 开发环境",
    "agent-memory": "Agent 记忆",
    "agent-orchestration": "Agent 编排",
    "agent-skill": "Agent 技能包",
    "agent-skills": "Agent 技能包",
    "acp": "Agent 协议",
    "ade": "Agent 开发环境",
    "ai-tools": "AI 工具链",
    "agents": "多 Agent",
    "ai": "AI 应用",
    "ai-agent": "AI Agent 工具",
    "ai-agents": "多 Agent",
    "ai-tutor": "AI 导师",
    "advanced-driver-assistance-systems": "高级辅助驾驶",
    "anthropic": "Anthropic 生态",
    "automation": "自动化",
    "astrbot": "AstrBot 生态",
    "authentication": "身份认证",
    "bash": "终端脚本",
    "bun": "Bun 运行时",
    "browser": "浏览器 Agent",
    "claude-code": "Claude Code 生态",
    "cli": "CLI",
    "coding": "编码 Agent",
    "code-editor": "代码编辑器",
    "codegen": "代码生成",
    "container": "容器运行时",
    "context": "上下文工程",
    "database": "数据基础设施",
    "deployments": "部署流程",
    "devtool": "开发者工具",
    "devtools": "开发者工具",
    "durable objects": "持久化对象运行时",
    "eval": "评测",
    "infra": "AI Infra",
    "inference": "模型推理",
    "llm": "大模型应用",
    "mcp": "MCP 集成",
    "memory": "长期记忆",
    "multimodal": "多模态",
    "nextjs": "Next.js 应用",
    "open-source": "开源项目",
    "open-source-social-media-scheduling-tool": "开源社媒排程",
    "protocol": "开放协议",
    "rag": "RAG 检索",
    "runtime": "运行时",
    "sandbox": "沙箱",
    "search": "搜索",
    "self-hosted": "自托管",
    "skill": "技能扩展",
    "skills": "技能扩展",
    "unified llm api": "统一模型接口",
    "vector": "向量检索",
    "workflow": "工作流",
    "workspace": "工作区",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def strip_tags(value: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", value)).strip()


def load_report_summaries(root: Path) -> dict[str, str]:
    summaries: dict[str, str] = {}
    report_paths = sorted((root / "daily").glob("*/index.html"))
    for report_path in report_paths:
        source = report_path.read_text(encoding="utf-8")
        for name, summary in PROJECT_SUMMARY_RE.findall(source):
            clean_name = strip_tags(name)
            clean_summary = strip_tags(summary)
            if clean_name and clean_summary:
                current = summaries.get(clean_name, "")
                if CHINESE_RE.search(clean_summary) or not current:
                    summaries[clean_name] = clean_summary
    return summaries


def load_top10_records(root: Path) -> dict[str, dict[str, dict]]:
    records: dict[str, dict[str, dict]] = {}
    for path in root.glob("top10-*.json"):
        match = TOP10_RE.fullmatch(path.name)
        if not match:
            continue
        period = match.group(1)
        records[period] = {
            item.get("full_name", ""): item
            for item in read_json(path)
            if item.get("full_name")
        }
    return records


def split_capabilities(value: str) -> list[str]:
    return [
        item.strip()
        for item in re.split(r"[、,，/|]+", value or "")
        if item.strip()
    ]


def translate_capability(value: str) -> str:
    key = value.strip().lower().replace("_", "-").replace(" ", "-")
    return KEYWORD_LABELS.get(key) or KEYWORD_LABELS.get(key.replace("-", " ")) or value.strip()


def project_capabilities(repo: dict, brief: dict) -> list[str]:
    labels = [translate_capability(item) for item in split_capabilities(brief.get("capabilities", ""))]
    labels.extend(translate_capability(item) for item in split_capabilities("、".join(repo.get("capability_tags", []))))
    relationship = repo.get("relationship_label")
    if relationship:
        labels.append(relationship)
    for keyword in repo.get("strategic_keywords", []):
        label = KEYWORD_LABELS.get(str(keyword).lower())
        if label:
            labels.append(label)

    unique = []
    for label in labels:
        if label not in unique:
            unique.append(label)
    return unique[:4] or ["开源信号"]


def choose_summary(brief: dict, report_summary: str, description: str) -> tuple[str, str]:
    candidates = (
        ("project_brief", brief.get("summary", "")),
        ("daily_report", report_summary),
        ("repo_description", description),
    )
    for source, value in candidates:
        if (
            value
            and CHINESE_RE.search(value)
            and not any(marker in value for marker in GENERIC_SUMMARY_MARKERS)
        ):
            return value, source
    if description:
        return "暂无可靠中文说明；以下保留仓库原始 description 供核对。", "original_description"
    return "暂无可靠项目说明，具体能力边界仍需核实。", "missing"


def normalized_log(value: int | float, maximum: int | float) -> float:
    if value <= 0 or maximum <= 0:
        return 0.0
    return math.log1p(value) / math.log1p(maximum)


def build_items(root: Path) -> tuple[list[dict], dict]:
    briefs_path = root / "project-briefs-zh.json"
    briefs = read_json(briefs_path) if briefs_path.exists() else {}
    report_summaries = load_report_summaries(root)
    top10_records = load_top10_records(root)
    observations: dict[str, list[dict]] = defaultdict(list)

    snapshot_paths = []
    for path in (root / "trending-history").glob("snapshot-*.json"):
        match = SNAPSHOT_RE.fullmatch(path.name)
        if match:
            snapshot_paths.append((datetime.strptime(match.group(1), "%Y%m%d").date(), path))
    snapshot_paths.sort()

    for snapshot_date, path in snapshot_paths:
        period = snapshot_date.isoformat()
        enriched = top10_records.get(period, {})
        for snapshot in read_json(path):
            name = snapshot.get("name")
            if not name:
                continue
            observations[name].append(
                {
                    "date": snapshot_date,
                    "snapshot": snapshot,
                    "repo": enriched.get(name, {}),
                }
            )

    if not observations:
        raise ValueError("No valid trending history snapshots were found.")

    provisional = []
    for name, repo_observations in observations.items():
        repo_observations.sort(key=lambda item: item["date"])
        first = repo_observations[0]
        latest = repo_observations[-1]
        latest_repo = latest["repo"]
        latest_snapshot = latest["snapshot"]
        brief = briefs.get(name, {})

        ranks = [
            int(item["snapshot"].get("rank"))
            for item in repo_observations
            if item["snapshot"].get("rank") is not None
        ]
        star_totals = [
            int(item["snapshot"].get("stars_total"))
            for item in repo_observations
            if item["snapshot"].get("stars_total") is not None
        ]
        period_growth = [
            int(item["snapshot"].get("stars_today_or_period") or 0)
            for item in repo_observations
        ]
        strategic_scores = [
            float(item["repo"].get("strategic_score"))
            for item in repo_observations
            if item["repo"].get("strategic_score") is not None
        ]

        latest_stars = star_totals[-1] if star_totals else int(latest_repo.get("total_stars") or 0)
        first_stars = star_totals[0] if star_totals else latest_stars
        observed_star_change = max(0, latest_stars - first_stars)
        peak_period_growth = max(period_growth, default=0)
        growth_signal = max(observed_star_change, peak_period_growth)
        original_description = latest_repo.get("description") or ""
        summary, summary_source = choose_summary(
            brief,
            report_summaries.get(name, ""),
            original_description,
        )
        capabilities = project_capabilities(latest_repo, brief)
        relationship = latest_repo.get("relationship_label") or ""

        provisional.append(
            {
                "full_name": name,
                "url": latest_repo.get("url") or f"https://github.com/{name}",
                "summary": summary,
                "summary_source": summary_source,
                "original_description": original_description,
                "language": latest_snapshot.get("language") or latest_repo.get("language") or "Unknown",
                "latest_stars": latest_stars,
                "observed_star_change": observed_star_change,
                "peak_period_growth": peak_period_growth,
                "growth_signal": growth_signal,
                "appearances": len(repo_observations),
                "best_rank": min(ranks, default=10),
                "first_seen": first["date"].isoformat(),
                "last_seen": latest["date"].isoformat(),
                "strategic_score": round(sum(strategic_scores) / len(strategic_scores), 1)
                if strategic_scores
                else 0,
                "relationship_label": relationship,
                "capabilities": capabilities,
                "data_confidence": latest_repo.get("data_confidence") or "medium",
            }
        )

    latest_snapshot_date = snapshot_paths[-1][0]
    max_appearances = max(item["appearances"] for item in provisional)
    max_growth_signal = max(item["growth_signal"] for item in provisional)
    max_period_growth = max(item["peak_period_growth"] for item in provisional)

    for item in provisional:
        days_since_seen = (latest_snapshot_date - date.fromisoformat(item["last_seen"])).days
        components = {
            "continuity": item["appearances"] / max_appearances * 30,
            "growth": normalized_log(item["growth_signal"], max_growth_signal) * 20,
            "strategic": item["strategic_score"] / 100 * 20,
            "heat": normalized_log(item["peak_period_growth"], max_period_growth) * 15,
            "best_rank": (11 - min(item["best_rank"], 10)) / 10 * 10,
            "recency": max(0, 1 - days_since_seen / 30) * 5,
        }
        item["score_breakdown"] = {
            key: round(value, 1) for key, value in components.items()
        }
        item["rank_score"] = round(sum(components.values()), 1)

    provisional.sort(
        key=lambda item: (
            -item["rank_score"],
            -item["appearances"],
            -item["growth_signal"],
            item["best_rank"],
            item["full_name"].lower(),
        )
    )
    for rank, item in enumerate(provisional, start=1):
        item["rank"] = rank

    metadata = {
        "first_snapshot": snapshot_paths[0][0].isoformat(),
        "last_snapshot": latest_snapshot_date.isoformat(),
        "snapshot_count": len(snapshot_paths),
        "repository_count": len(provisional),
        "languages": sorted({item["language"] for item in provisional}),
        "summary_sources": dict(Counter(item["summary_source"] for item in provisional)),
    }
    return provisional, metadata


def render_page() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#fcfaf6">
  <title>开源信号总榜 · GitHub Signal · ReelOS</title>
  <meta name="description" content="基于 ReelOS GitHub 热榜历史快照生成的可检索、可排序、可分页开源项目总榜。">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%23111722'/%3E%3Ccircle cx='32' cy='32' r='11' fill='none' stroke='%23f97316' stroke-width='5'/%3E%3C/svg%3E">
  <style>
    :root{
      color-scheme:light;
      --bg:#edf1f6;
      --paper:#f7f9fc;
      --surface:rgba(255,255,255,.82);
      --line:#d7dce5;
      --line-strong:#bcc5d2;
      --text:#0d1424;
      --muted:#6c788d;
      --blue:#315fc8;
      --blue-soft:#eef3ff;
      --orange:#315fc8;
      --orange-soft:#eef3ff;
      --brand-orange:#f97316;
      --green:#27734b;
      --green-soft:#eaf6ef;
      --shadow:0 18px 60px rgba(17,23,34,.07);
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{
      margin:0;
      overflow-x:hidden;
      color:var(--text);
      font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif;
      line-height:1.65;
      touch-action:manipulation;
      -webkit-tap-highlight-color:rgba(83,111,203,.16);
      background:
        radial-gradient(circle at 12% 0%,rgba(49,95,200,.12),transparent 28%),
        linear-gradient(rgba(196,203,230,.16) 1px,transparent 1px),
        linear-gradient(90deg,rgba(196,203,230,.16) 1px,transparent 1px),
        linear-gradient(180deg,var(--bg),var(--paper));
      background-size:auto,72px 72px,72px 72px,auto;
      min-height:100vh;
    }
    a{color:inherit;text-decoration:none}
    a:hover{color:var(--blue)}
    button,input,select{font:inherit}
    button{color:inherit}
    :where(a,button,input,select):focus-visible{
      outline:2px solid var(--blue);
      outline-offset:3px;
    }
    .mono,.metric,.hero-meta{font-variant-numeric:tabular-nums}
    .mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace}
    .skip-link{
      position:fixed;
      z-index:100;
      left:16px;
      top:12px;
      padding:9px 12px;
      color:#fff;
      background:var(--text);
      transform:translateY(-160%);
      transition:transform .18s ease;
    }
    .skip-link:focus{transform:translateY(0)}
    .shell{
      max-width:1180px;
      margin:0 auto;
      padding:28px max(20px,env(safe-area-inset-right)) 80px max(20px,env(safe-area-inset-left));
    }
    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:20px;
      padding:10px 0 18px;
      border-bottom:1px solid var(--line);
    }
    .brand{display:inline-flex;align-items:center;gap:10px}
    .brand-mark{
      position:relative;
      display:grid;
      width:30px;
      height:30px;
      place-items:center;
      border-radius:50%;
      background:var(--text);
    }
    .brand-mark::before,.brand-mark::after,.brand-mark span{
      content:"";
      position:absolute;
      border:1.5px solid #fff7ed;
      border-radius:50%;
    }
    .brand-mark::before{width:18px;height:18px}
    .brand-mark::after{width:8px;height:8px;border-color:var(--brand-orange)}
    .brand-mark span{width:24px;height:24px;border-top-color:transparent;transform:rotate(-25deg)}
    .brand-copy{display:grid;gap:1px}
    .wordmark{font-size:16px;font-weight:700;line-height:1.2}
    .wordmark b{color:var(--brand-orange)}
    .brand-copy small{color:var(--muted);font-size:10px;letter-spacing:.14em;text-transform:uppercase}
    .nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px}
    .nav a{
      padding:7px 10px;
      border:1px solid transparent;
      color:var(--muted);
      font-size:12px;
      font-weight:700;
    }
    .nav a:hover,.nav a.active,.nav a:focus-visible{color:var(--blue);border-color:var(--line);background:rgba(255,255,255,.72)}
    .hero{
      display:grid;
      grid-template-columns:minmax(0,1fr) minmax(260px,.42fr);
      gap:32px;
      padding:60px 0 38px;
      border-bottom:1px solid var(--line);
    }
    .kicker{display:block;color:var(--blue);font-size:11px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
    h1{margin:12px 0 14px;font-size:clamp(42px,7vw,78px);line-height:1.04;letter-spacing:0;text-wrap:balance}
    h1 span{color:var(--orange)}
    .hero p{max-width:650px;margin:0;color:var(--muted);font-size:16px}
    .hero-meta{
      align-self:end;
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      border-top:1px solid var(--line);
      border-left:1px solid var(--line);
    }
    .hero-meta div{padding:14px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);background:rgba(255,255,255,.58)}
    .hero-meta b{display:block;font-size:24px;line-height:1.1;white-space:nowrap}
    .hero-meta #first-snapshot,.hero-meta #last-snapshot{font-size:18px;letter-spacing:-.025em}
    .hero-meta span{color:var(--muted);font-size:11px}
    .method{margin-top:18px;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
    .method summary{padding:14px 0;color:var(--blue);font-size:12px;font-weight:800;cursor:pointer;list-style:none}
    .method summary::-webkit-details-marker{display:none}
    .method summary::after{content:"展开";float:right;color:var(--muted);font-size:10px;font-weight:600}
    .method[open] summary::after{content:"收起"}
    .method p{max-width:850px;margin:0;padding:0 0 18px;color:var(--muted);font-size:13px}
    .controls{
      position:sticky;
      top:0;
      z-index:10;
      display:grid;
      grid-template-columns:minmax(220px,1fr) 170px 190px 120px;
      gap:10px;
      padding:16px 0;
      background:linear-gradient(180deg,rgba(252,250,246,.98),rgba(252,250,246,.9));
      backdrop-filter:blur(18px);
      border-bottom:1px solid var(--line);
    }
    .field{position:relative}
    .field label{position:absolute;left:12px;top:6px;color:var(--muted);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;pointer-events:none}
    .field input,.field select{
      width:100%;
      height:52px;
      padding:20px 12px 5px;
      border:1px solid var(--line);
      border-radius:2px;
      outline:none;
      color:var(--text);
      background:rgba(255,255,255,.86);
    }
    .field input:focus-visible,.field select:focus-visible{border-color:var(--blue);box-shadow:0 0 0 3px rgba(83,111,203,.1)}
    .result-head{display:flex;align-items:end;justify-content:space-between;gap:20px;padding:26px 0 12px}
    .result-head h2{margin:0;font-size:26px;letter-spacing:-.035em;scroll-margin-top:92px}
    .result-head p{margin:4px 0 0;color:var(--muted);font-size:12px}
    .updated{color:var(--muted);font-size:11px;text-align:right}
    .ranking{border-top:1px solid var(--line)}
    .rank-row{
      display:grid;
      grid-template-columns:54px minmax(0,1fr) 94px 92px 108px 76px;
      gap:14px;
      align-items:start;
      padding:22px 6px;
      border-bottom:1px solid var(--line);
      animation:reveal .35s ease both;
    }
    .rank-number{padding-top:2px;color:var(--blue)}
    .rank-number span{display:block;color:var(--muted);font-size:8px;font-weight:700;letter-spacing:.08em}
    .rank-number b{display:block;margin-top:2px;font-size:13px}
    .repo-main{min-width:0}
    .repo-title{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:6px}
    .repo-title a{font-size:18px;font-weight:800;line-height:1.35;overflow-wrap:anywhere}
    .language{padding:2px 6px;border:1px solid var(--line);color:var(--muted);font-size:10px;font-weight:700}
    .confidence{padding:2px 6px;font-size:10px;font-weight:700}
    .confidence-high{color:var(--green);background:var(--green-soft)}
    .confidence-medium{color:#59667d;background:#edf1f6}
    .confidence-low{color:#9a3f33;background:#fff0ed}
    .summary{max-width:760px;margin:0;color:#444b55;font-size:14px}
    .original-description{
      max-width:760px;
      margin:7px 0 0;
      padding-left:10px;
      color:var(--muted);
      border-left:2px solid var(--line-strong);
      font-size:12px;
      overflow-wrap:anywhere;
    }
    .original-description span{display:block;margin-bottom:2px;color:var(--orange);font-size:9px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
    .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
    .tag{padding:3px 7px;background:var(--blue-soft);color:var(--blue);font-size:10px;font-weight:700}
    .source{display:inline-block;margin-top:10px;color:var(--muted);font-size:11px;font-weight:700}
    .metric{padding-top:2px}
    .metric b{display:block;font-size:15px;line-height:1.2}
    .metric span{display:block;margin-top:5px;color:var(--muted);font-size:10px}
    .stars b{font-size:14px}
    .score b{color:var(--orange);font-size:22px}
    .empty,.error{padding:70px 20px;text-align:center;color:var(--muted)}
    .pagination{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:6px;padding:26px 0}
    .pagination button{
      min-width:38px;
      height:38px;
      padding:0 10px;
      border:1px solid var(--line);
      background:rgba(255,255,255,.72);
      cursor:pointer;
    }
    .pagination button:hover:not(:disabled),.pagination button.active{border-color:var(--blue);color:var(--blue);background:var(--blue-soft)}
    .pagination button:focus-visible{border-color:var(--blue);background:var(--blue-soft)}
    .pagination button:disabled{opacity:.35;cursor:not-allowed}
    .footer{display:flex;justify-content:space-between;gap:20px;margin-top:44px;padding-top:24px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}
    .footer strong{color:var(--text)}
    @keyframes reveal{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
    @media (max-width:840px){
      .hero{grid-template-columns:1fr}
      .controls{grid-template-columns:1fr 1fr}
      .rank-row{grid-template-columns:42px minmax(0,1fr) 90px}
      .rank-number{grid-column:1;grid-row:1}
      .repo-main{grid-column:2;grid-row:1}
      .metric.stars{grid-column:2;grid-row:2}
      .metric.appearances{grid-column:3;grid-row:2}
      .metric.last-seen{grid-column:2 / 4;grid-row:3}
      .score{grid-column:3;grid-row:1}
    }
    @media (max-width:620px){
      .shell{padding:16px max(16px,env(safe-area-inset-right)) 60px max(16px,env(safe-area-inset-left))}
      .topbar{align-items:flex-start}
      .nav{max-width:190px}
      .nav a{padding:5px 7px;font-size:11px}
      .hero{gap:20px;padding:28px 0 20px}
      .hero h1{font-size:44px}
      .hero p{font-size:14px;line-height:1.65}
      .hero-meta{grid-template-columns:repeat(2,1fr)}
      .hero-meta div{padding:10px 12px}
      .hero-meta b{font-size:20px}
      .controls{position:static;grid-template-columns:1fr 1fr;padding:12px 0}
      .controls .field:first-child{grid-column:1 / -1}
      .field input,.field select{height:48px}
      .rank-row{grid-template-columns:38px minmax(0,1fr);gap:12px;padding:20px 0}
      .rank-number{grid-column:1;grid-row:1;padding-top:4px}
      .repo-main{grid-column:2;grid-row:1}
      .score{grid-column:1;grid-row:2;text-align:left}
      .metric.stars{grid-column:2;grid-row:2}
      .metric.appearances{grid-column:1;grid-row:3}
      .metric.last-seen{grid-column:2;grid-row:3}
      .result-head{align-items:start}
      .updated{max-width:140px}
      .footer{display:block}
      .footer div + div{margin-top:12px}
    }
    @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.rank-row{animation:none}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">跳至榜单</a>
  <div class="shell">
    <header class="topbar">
      <a class="brand" href="/" aria-label="ReelOS.ai">
        <span class="brand-mark" aria-hidden="true"><span></span></span>
        <span class="brand-copy">
          <span class="wordmark" translate="no">Reel<b>OS</b>.ai</span>
          <small>GitHub 热榜情报</small>
        </span>
      </a>
      <nav class="nav" aria-label="主导航">
        <a href="/">首页</a>
        <a href="/daily/">日报</a>
        <a href="/weekly/">周报</a>
        <a href="/monthly/">月报</a>
        <a class="active" href="/leaderboard/" aria-current="page">总榜</a>
        <a href="/archive/">归档</a>
      </nav>
    </header>

    <main id="main">
      <section class="hero">
        <div>
          <span class="kicker mono">Open Source Signal Index</span>
          <h1>开源信号<span>总榜</span></h1>
          <p>把分散在每份日报里的项目放回同一个坐标系：谁持续出现、谁增长更快、谁的能力更值得长期追踪。支持搜索、筛选、排序和分页，数据随发布流水线自动重算。</p>
        </div>
        <div class="hero-meta" aria-label="数据概览">
          <div><b id="repo-count">--</b><span>收录项目</span></div>
          <div><b id="snapshot-count">--</b><span>历史快照</span></div>
          <div><b id="first-snapshot">--</b><span>起始日期</span></div>
          <div><b id="last-snapshot">--</b><span id="last-snapshot-label">最新快照</span></div>
        </div>
      </section>

      <form class="controls" id="controls" role="search">
        <div class="field">
          <label for="query">搜索项目或能力</label>
          <input id="query" name="q" type="search" autocomplete="off" placeholder="例如 Agent、MCP、memory…">
        </div>
        <div class="field">
          <label for="language">语言</label>
          <select id="language" name="language"><option value="">全部语言</option></select>
        </div>
        <div class="field">
          <label for="sort">排序</label>
          <select id="sort" name="sort">
            <option value="score">综合得分</option>
            <option value="appearances">入榜次数</option>
            <option value="growth">增长信号</option>
            <option value="stars">Star 基数</option>
            <option value="recent">最近出现</option>
          </select>
        </div>
        <div class="field">
          <label for="page-size">每页</label>
          <select id="page-size" name="pageSize">
            <option value="10" selected>10 条</option>
            <option value="20">20 条</option>
            <option value="50">50 条</option>
          </select>
        </div>
      </form>

      <section id="results" aria-live="polite" aria-busy="true">
        <header class="result-head">
          <div><h2 id="ranking-heading">项目排名</h2><p id="result-status">正在读取榜单数据…</p></div>
          <div class="updated mono" id="updated-at"></div>
        </header>
        <div class="ranking" id="ranking"></div>
        <nav class="pagination" id="pagination" aria-label="榜单分页"></nav>
      </section>
      <details class="method">
        <summary>查看计分方法</summary>
        <p>总分 100：持续入榜 30%、增长信号 20%、战略评分 20%、近期热度 15%、最佳名次 10%、最近出现 5%。增长信号取“快照期间 Star 变化”和“单期最高增长”的较高值。它是当前样本内的相对分，每次更新会重新标定；Star 只代表关注度，不等于采用度、生产可用性或商业价值。中文摘要优先来自人工 brief 与日报，缺失时保留仓库原始 description，不做猜测式翻译。</p>
      </details>
    </main>

    <footer class="footer">
      <div><strong>ReelOS.ai</strong><br>不追热榜，识别开源世界的结构变化。</div>
      <div>数据来源：GitHub Trending 历史快照与公开仓库元数据</div>
    </footer>
  </div>

  <script>
    (() => {
      const state = { items: [], meta: {}, q: "", language: "", sort: "score", page: 1, pageSize: 10 };
      const ranking = document.querySelector("#ranking");
      const pagination = document.querySelector("#pagination");
      const status = document.querySelector("#result-status");
      const results = document.querySelector("#results");
      const controls = document.querySelector("#controls");
      const queryInput = document.querySelector("#query");
      const languageSelect = document.querySelector("#language");
      const sortSelect = document.querySelector("#sort");
      const pageSizeSelect = document.querySelector("#page-size");
      const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
      })[char]);
      const formatNumber = (value) => new Intl.NumberFormat("zh-CN").format(value || 0);
      const dateFormatter = new Intl.DateTimeFormat("zh-CN", {
        year: "numeric", month: "2-digit", day: "2-digit", timeZone: "UTC"
      });
      const dateTimeFormatter = new Intl.DateTimeFormat("zh-CN", {
        year: "numeric", month: "2-digit", day: "2-digit",
        hour: "2-digit", minute: "2-digit"
      });
      const confidenceLabels = { high: "高可信", medium: "中可信", low: "低可信" };
      const sortLabels = {
        score: "综合得分", appearances: "入榜次数", growth: "增长信号",
        stars: "Star 基数", recent: "最近出现"
      };
      const validPageSizes = new Set([10, 20, 50]);
      const validSorts = new Set(["score", "appearances", "growth", "stars", "recent"]);
      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      function parseDate(value) {
        const [year, month, day] = String(value || "").split("-").map(Number);
        return year && month && day ? new Date(Date.UTC(year, month - 1, day)) : null;
      }

      function formatDate(value) {
        const parsed = parseDate(value);
        return parsed ? dateFormatter.format(parsed) : "--";
      }

      function readUrl() {
        const params = new URLSearchParams(location.search);
        state.q = params.get("q") || "";
        state.language = params.get("language") || "";
        state.sort = validSorts.has(params.get("sort")) ? params.get("sort") : "score";
        state.page = Math.max(1, Number.parseInt(params.get("page") || "1", 10) || 1);
        const requestedSize = Number.parseInt(params.get("pageSize") || "10", 10);
        state.pageSize = validPageSizes.has(requestedSize) ? requestedSize : 10;
      }

      function syncControls() {
        queryInput.value = state.q;
        languageSelect.value = state.language;
        sortSelect.value = state.sort;
        pageSizeSelect.value = String(state.pageSize);
      }

      function writeUrl() {
        const params = new URLSearchParams();
        if (state.q) params.set("q", state.q);
        if (state.language) params.set("language", state.language);
        if (state.sort !== "score") params.set("sort", state.sort);
        if (state.page > 1) params.set("page", String(state.page));
        if (state.pageSize !== 10) params.set("pageSize", String(state.pageSize));
        const query = params.toString();
        history.replaceState(null, "", query ? `?${query}` : location.pathname);
      }

      function filteredItems() {
        const needle = state.q.trim().toLocaleLowerCase("zh-CN");
        const items = state.items.filter((item) => {
          if (state.language && item.language !== state.language) return false;
          if (!needle) return true;
          const haystack = [
            item.full_name,
            item.summary,
            item.original_description,
            item.language,
            item.relationship_label,
            ...(item.capabilities || [])
          ].join(" ").toLocaleLowerCase("zh-CN");
          return haystack.includes(needle);
        });
        const sorters = {
          score: (a, b) => b.rank_score - a.rank_score || a.rank - b.rank,
          appearances: (a, b) => b.appearances - a.appearances || b.rank_score - a.rank_score,
          growth: (a, b) => b.growth_signal - a.growth_signal || b.rank_score - a.rank_score,
          stars: (a, b) => b.latest_stars - a.latest_stars || b.rank_score - a.rank_score,
          recent: (a, b) => b.last_seen.localeCompare(a.last_seen) || b.rank_score - a.rank_score
        };
        return items.sort(sorters[state.sort]);
      }

      function rowHtml(item, index) {
        const tags = (item.capabilities || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
        const confidence = ["high", "medium", "low"].includes(item.data_confidence) ? item.data_confidence : "medium";
        const originalDescription = item.summary_source === "original_description" && item.original_description
          ? `<p class="original-description" lang="en"><span>Repo description</span>${escapeHtml(item.original_description)}</p>`
          : "";
        return `<article class="rank-row" style="animation-delay:${Math.min(index * 22, 220)}ms">
          <span class="rank-number mono"><span>综合榜</span><b>#${String(item.rank).padStart(3, "0")}</b></span>
          <div class="repo-main">
            <div class="repo-title">
              <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer" translate="no">${escapeHtml(item.full_name)}</a>
              <span class="language">${escapeHtml(item.language)}</span>
              <span class="confidence confidence-${confidence}">${confidenceLabels[confidence]}</span>
            </div>
            <p class="summary">${escapeHtml(item.summary)}</p>
            ${originalDescription}
            <div class="tags">${tags}</div>
            <a class="source" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">原文 ↗</a>
          </div>
          <div class="metric stars"><b>${formatNumber(item.latest_stars)}</b><span>Star 基数</span></div>
          <div class="metric appearances"><b>${item.appearances} 次</b><span>历史入榜 · 最佳 #${item.best_rank}</span></div>
          <div class="metric last-seen"><b>+${formatNumber(item.growth_signal)}</b><span>增长信号 · ${formatDate(item.last_seen)}</span></div>
          <div class="metric score" aria-label="综合得分 ${item.rank_score}"><b>${item.rank_score}</b><span>综合得分</span></div>
        </article>`;
      }

      function pageNumbers(current, total) {
        const pages = new Set([1, total, current - 2, current - 1, current, current + 1, current + 2]);
        return [...pages].filter((page) => page >= 1 && page <= total).sort((a, b) => a - b);
      }

      function renderPagination(totalPages) {
        if (totalPages <= 1) {
          pagination.innerHTML = "";
          return;
        }
        const buttons = [];
        buttons.push(`<button type="button" data-page="${state.page - 1}" ${state.page === 1 ? "disabled" : ""}>上一页</button>`);
        let previous = 0;
        for (const page of pageNumbers(state.page, totalPages)) {
          if (previous && page - previous > 1) buttons.push('<span aria-hidden="true">…</span>');
          buttons.push(`<button type="button" data-page="${page}" class="${page === state.page ? "active" : ""}" ${page === state.page ? 'aria-current="page"' : ""}>${page}</button>`);
          previous = page;
        }
        buttons.push(`<button type="button" data-page="${state.page + 1}" ${state.page === totalPages ? "disabled" : ""}>下一页</button>`);
        pagination.innerHTML = buttons.join("");
      }

      function render() {
        const items = filteredItems();
        const totalPages = Math.max(1, Math.ceil(items.length / state.pageSize));
        state.page = Math.min(state.page, totalPages);
        const start = (state.page - 1) * state.pageSize;
        const pageItems = items.slice(start, start + state.pageSize);
        ranking.innerHTML = pageItems.length
          ? pageItems.map(rowHtml).join("")
          : '<div class="empty">没有找到匹配项目，换一个关键词或筛选条件试试。</div>';
        const sortNote = state.sort === "score"
          ? "按综合得分排序"
          : `按${sortLabels[state.sort]}排序 · 编号仍为综合榜位`;
        status.textContent = `共 ${items.length} 个项目 · ${sortNote} · 第 ${state.page} / ${totalPages} 页`;
        renderPagination(totalPages);
        writeUrl();
      }

      function applyControls() {
        state.q = queryInput.value.trim();
        state.language = languageSelect.value;
        state.sort = sortSelect.value;
        state.pageSize = Number(pageSizeSelect.value);
        state.page = 1;
        render();
      }

      controls.addEventListener("submit", (event) => event.preventDefault());
      queryInput.addEventListener("input", applyControls);
      languageSelect.addEventListener("change", applyControls);
      sortSelect.addEventListener("change", applyControls);
      pageSizeSelect.addEventListener("change", applyControls);
      pagination.addEventListener("click", (event) => {
        const button = event.target.closest("[data-page]");
        if (!button || button.disabled) return;
        state.page = Number(button.dataset.page);
        render();
        document.querySelector(".result-head").scrollIntoView({
          behavior: reduceMotion ? "auto" : "smooth",
          block: "start"
        });
      });
      window.addEventListener("popstate", () => {
        readUrl();
        syncControls();
        render();
      });

      readUrl();
      fetch("./data.json", { cache: "no-store" })
        .then((response) => {
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          return response.json();
        })
        .then((data) => {
          state.items = data.items || [];
          state.meta = data.source || {};
          if (state.language && !(state.meta.languages || []).includes(state.language)) {
            state.language = "";
          }
          languageSelect.insertAdjacentHTML(
            "beforeend",
            (state.meta.languages || []).map((language) => `<option value="${escapeHtml(language)}">${escapeHtml(language)}</option>`).join("")
          );
          syncControls();
          document.querySelector("#repo-count").textContent = formatNumber(state.meta.repository_count);
          document.querySelector("#snapshot-count").textContent = formatNumber(state.meta.snapshot_count);
          document.querySelector("#first-snapshot").textContent = formatDate(state.meta.first_snapshot);
          document.querySelector("#last-snapshot").textContent = formatDate(state.meta.last_snapshot);
          const latestSnapshot = parseDate(state.meta.last_snapshot);
          const now = new Date();
          const today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
          const staleDays = latestSnapshot
            ? Math.max(0, Math.floor((today - latestSnapshot.getTime()) / 86400000))
            : null;
          document.querySelector("#last-snapshot-label").textContent = staleDays === null
            ? "最新快照"
            : staleDays === 0 ? "最新快照 · 今天" : `最新快照 · ${staleDays} 天前`;
          const generatedAt = data.generated_at ? new Date(data.generated_at) : null;
          document.querySelector("#updated-at").textContent = generatedAt && !Number.isNaN(generatedAt.getTime())
            ? `页面生成于 ${dateTimeFormatter.format(generatedAt)}`
            : "页面生成时间未知";
          results.setAttribute("aria-busy", "false");
          render();
        })
        .catch((error) => {
          ranking.innerHTML = `<div class="error">榜单数据暂时无法读取：${escapeHtml(error.message)}。请刷新页面或稍后重试。</div>`;
          status.textContent = "数据加载失败";
          results.setAttribute("aria-busy", "false");
        });
    })();
  </script>
</body>
</html>
"""


def build_leaderboard(root: Path = ROOT) -> dict:
    items, metadata = build_items(root)
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="minutes"),
        "methodology": {
            "name": "ReelOS Open Source Signal Index",
            "version": 2,
            "model_version": "leaderboard-v2",
            "normalization": "relative_to_current_dataset",
            "weights": {
                "continuity": 30,
                "growth": 20,
                "strategic": 20,
                "heat": 15,
                "best_rank": 10,
                "recency": 5,
            },
            "note": "Scores are rebased when the dataset changes. Stars represent attention, not adoption or production readiness.",
        },
        "source": metadata,
        "items": items,
    }
    write_text(root / "leaderboard" / "data.json", json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    write_text(root / "leaderboard" / "index.html", render_page())
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the paginated GitHub signal leaderboard.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    args = parser.parse_args()
    payload = build_leaderboard(args.root.resolve())
    print(
        json.dumps(
            {
                "output": str(args.root.resolve() / "leaderboard" / "index.html"),
                "data": str(args.root.resolve() / "leaderboard" / "data.json"),
                "repository_count": payload["source"]["repository_count"],
                "snapshot_count": payload["source"]["snapshot_count"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()

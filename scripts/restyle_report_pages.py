#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REPORT_STYLE = """
  <style>
    :root {
      color-scheme: light;
      --bg:#f6f0e8;
      --bg-2:#fbf7f1;
      --paper:rgba(255,252,247,0.92);
      --panel:rgba(255,255,255,0.70);
      --panel-strong:rgba(255,255,255,0.86);
      --line:rgba(119,99,76,0.18);
      --line-strong:rgba(249,115,22,0.34);
      --text:#181512;
      --muted:rgba(24,21,18,0.62);
      --soft:rgba(24,21,18,0.78);
      --blue:#8e9fc9;
      --blue-strong:#6177ad;
      --orange:#f97316;
      --orange-soft:rgba(249,115,22,0.12);
      --rail:rgba(142,159,201,0.24);
      --grid:rgba(142,159,201,0.10);
      --node:#fffaf4;
      --shadow:0 18px 48px rgba(40,26,14,0.08);
      --shadow-soft:0 10px 28px rgba(40,26,14,0.05);
      --red:#b5543d;
      --font-cn:"PingFang SC","Hiragino Sans GB","Noto Sans CJK SC","Source Han Sans SC","Microsoft YaHei",sans-serif;
      --font-body:var(--font-cn);
      --font-display:"Iowan Old Style","Palatino Linotype","Book Antiqua","Noto Serif SC","Source Han Serif SC",serif;
      --font-mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;
    }
    * { box-sizing:border-box; }
    html { color-scheme:light; scroll-behavior:smooth; }
    body {
      margin:0;
      color:var(--text);
      font-family:var(--font-body);
      font-weight:400;
      font-synthesis-weight:none;
      -webkit-font-smoothing:antialiased;
      text-rendering:optimizeLegibility;
      line-height:1.84;
      background:
        radial-gradient(circle at 14% 0%, rgba(142,159,201,.18), transparent 24%),
        radial-gradient(circle at 86% 10%, rgba(249,115,22,.13), transparent 20%),
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px),
        linear-gradient(180deg, var(--bg), var(--bg-2));
      background-size:auto,auto,72px 72px,72px 72px,auto;
      background-attachment:fixed;
    }
    a { color:inherit; text-decoration:none; }
    a:hover { color:var(--orange); }
    .mono {
      font-family:var(--font-mono);
      letter-spacing:.08em;
      text-transform:uppercase;
    }
    .pixel-word {
      display:inline-block;
      font-family:var(--font-mono);
      font-size:.78em;
      font-weight:640;
      letter-spacing:.16em;
      text-transform:uppercase;
      color:var(--blue-strong);
      padding:.18em .42em;
      border:1px solid rgba(97,119,173,.22);
      border-radius:999px;
      background:rgba(142,159,201,.08);
      box-shadow:inset 0 1px 0 rgba(255,255,255,.7);
      vertical-align:middle;
      transform:translateY(-.08em);
    }
    .wrap { max-width:1120px; margin:0 auto; padding:34px 22px 96px; }
    header {
      position:relative;
      margin-bottom:12px;
      padding:0 0 32px;
      border-bottom:1px solid var(--line);
    }
    header::before {
      content:"";
      position:absolute;
      inset:-14px -18px auto -18px;
      height:228px;
      pointer-events:none;
      background:
        radial-gradient(circle at 14% 18%, rgba(249,115,22,.13), transparent 28%),
        radial-gradient(circle at 72% 14%, rgba(142,159,201,.18), transparent 34%);
      opacity:.92;
    }
    header > * { position:relative; }
    .toprow {
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:18px;
      padding-top:4px;
    }
    .brand {
      display:flex;
      align-items:center;
      gap:12px;
      color:var(--muted);
      font-size:11px;
      letter-spacing:.16em;
      text-transform:uppercase;
    }
    .dot {
      width:10px;
      height:10px;
      border-radius:999px;
      background:linear-gradient(180deg,#ffb36d,var(--orange));
      box-shadow:0 0 16px rgba(249,115,22,.18);
    }
    h1 {
      display:flex;
      flex-wrap:wrap;
      align-items:flex-end;
      gap:12px;
      margin:20px 0 8px;
      font-family:var(--font-display);
      font-size:clamp(44px,8vw,82px);
      font-weight:650;
      letter-spacing:-.045em;
      line-height:.92;
    }
    h1 .ac {
      color:var(--text);
      position:relative;
      display:inline-block;
      padding-right:.08em;
    }
    h1 .ac::after {
      content:"";
      position:absolute;
      left:.08em;
      right:.02em;
      bottom:.12em;
      height:.18em;
      background:linear-gradient(90deg, rgba(249,115,22,.26), rgba(249,115,22,.04));
      z-index:-1;
      border-radius:999px;
    }
    h2 {
      margin:0;
      color:var(--text);
      font-size:24px;
      line-height:1.2;
      font-weight:620;
      letter-spacing:-.03em;
    }
    h3 {
      margin:0 0 8px;
      color:var(--text);
      font-size:26px;
      font-weight:620;
      line-height:1.28;
      letter-spacing:-.03em;
    }
    h4 {
      margin:22px 0 10px;
      color:var(--blue-strong);
      font-size:11px;
      font-family:var(--font-mono);
      font-weight:600;
      letter-spacing:.16em;
      text-transform:uppercase;
    }
    .sub {
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      align-items:center;
      margin-top:18px;
      color:var(--muted);
      font-size:13px;
    }
    .chip {
      border:1px solid var(--line);
      border-radius:999px;
      padding:6px 11px;
      color:var(--soft);
      font-size:11px;
      letter-spacing:.12em;
      text-transform:uppercase;
      background:rgba(255,255,255,.58);
      backdrop-filter:blur(14px);
    }
    .chip b { color:var(--orange); font-weight:700; }
    .hero-lede {
      max-width:58ch;
      margin:16px 0 0;
      color:var(--soft);
      font-size:16px;
      line-height:1.9;
    }
    .briefing-strip {
      display:grid;
      grid-template-columns:1.24fr 1fr 1fr;
      gap:12px;
      margin-top:20px;
    }
    .briefing-item {
      border:1px solid var(--line);
      border-radius:18px;
      background:linear-gradient(180deg, var(--panel-strong), var(--panel));
      box-shadow:var(--shadow-soft);
      padding:15px 16px;
      min-width:0;
      backdrop-filter:blur(18px);
    }
    .briefing-item b {
      display:block;
      color:var(--blue-strong);
      font-family:var(--font-mono);
      font-size:10px;
      font-weight:620;
      letter-spacing:.16em;
      text-transform:uppercase;
      margin-bottom:7px;
    }
    .briefing-item span {
      display:block;
      color:var(--soft);
      font-size:13px;
      line-height:1.68;
      text-wrap:pretty;
    }
    .section-nav {
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      margin-top:18px;
    }
    .section-link {
      display:flex;
      align-items:center;
      gap:8px;
      padding:7px 11px;
      border:1px solid var(--line);
      border-radius:999px;
      background:rgba(255,255,255,.56);
      color:var(--muted);
      font-size:11px;
      transition:border-color .2s,color .2s,background .2s,transform .2s;
      backdrop-filter:blur(12px);
    }
    .section-link:hover {
      border-color:var(--line-strong);
      color:var(--text);
      background:rgba(255,247,238,.92);
      transform:translateY(-1px);
    }
    .section-link .nr { color:var(--orange); }
    .timeline {
      position:relative;
      margin-top:22px;
    }
    .timeline::before {
      content:"";
      position:absolute;
      left:28px;
      top:4px;
      bottom:28px;
      width:1px;
      background:linear-gradient(180deg, var(--rail), transparent);
    }
    .signal-section { position:relative; }
    .signal-section + .signal-section { margin-top:18px; }
    .section-head {
      display:flex;
      gap:18px;
      align-items:flex-start;
      padding:8px 0 10px 84px;
      color:var(--muted);
    }
    .section-head .range {
      min-width:54px;
      color:var(--orange);
      font-size:11px;
      padding-top:10px;
    }
    .section-head > div {
      display:inline-block;
      max-width:620px;
      padding:12px 14px 10px;
      border:1px solid var(--line);
      border-radius:16px;
      background:linear-gradient(180deg, rgba(255,255,255,.76), rgba(255,251,244,.68));
      box-shadow:var(--shadow-soft);
      backdrop-filter:blur(16px);
    }
    .section-head p {
      margin:7px 0 0;
      font-size:13px;
      line-height:1.62;
      color:var(--muted);
    }
    .section-tools {
      margin:0 0 12px 84px;
      display:flex;
      flex-wrap:wrap;
      align-items:center;
      gap:8px;
    }
    .tool-btn {
      appearance:none;
      border:1px solid var(--line);
      border-radius:999px;
      background:rgba(255,255,255,.62);
      color:var(--muted);
      font-family:var(--font-mono);
      font-size:10px;
      padding:8px 11px;
      cursor:pointer;
      transition:background .18s,border-color .18s,color .18s,transform .18s;
    }
    .tool-btn:hover {
      color:var(--text);
      border-color:var(--line-strong);
      background:rgba(255,247,238,.9);
      transform:translateY(-1px);
    }
    .stats {
      display:grid;
      grid-template-columns:repeat(4,minmax(0,1fr));
      gap:10px;
      margin-top:18px;
    }
    .stat {
      border:1px solid var(--line);
      border-radius:18px;
      background:linear-gradient(180deg, var(--panel-strong), var(--panel));
      box-shadow:var(--shadow-soft);
      padding:14px 15px 13px;
      backdrop-filter:blur(18px);
    }
    .stat b {
      display:block;
      color:var(--text);
      font-family:var(--font-display);
      font-size:29px;
      font-weight:650;
      line-height:1;
      margin-bottom:6px;
      letter-spacing:-.04em;
    }
    .stat span,
    .meta {
      color:var(--muted);
      font-family:var(--font-mono);
      font-size:11px;
    }
    .table-wrap {
      margin-left:84px;
      overflow-x:auto;
      border:1px solid var(--line);
      border-radius:22px;
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,252,247,.72));
      box-shadow:var(--shadow);
      backdrop-filter:blur(18px);
    }
    table {
      width:100%;
      border-collapse:collapse;
      min-width:1040px;
    }
    th, td {
      padding:12px 14px;
      border-bottom:1px solid rgba(119,99,76,.12);
      text-align:left;
      vertical-align:top;
      font-size:13px;
      line-height:1.6;
    }
    th {
      color:var(--blue-strong);
      font-family:var(--font-mono);
      font-size:10px;
      font-weight:620;
      text-transform:uppercase;
      letter-spacing:.12em;
      background:rgba(142,159,201,.05);
    }
    td { color:var(--soft); }
    td:first-child,
    td:nth-child(4),
    td:nth-child(5),
    td:nth-child(8) {
      color:var(--text);
      font-family:var(--font-mono);
    }
    .cards {
      display:grid;
      grid-template-columns:1fr;
      gap:14px;
    }
    .card {
      display:block;
      position:relative;
      margin-left:84px;
      padding:22px 22px 24px;
      border:1px solid var(--line);
      border-radius:22px;
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,252,247,.72));
      box-shadow:var(--shadow);
      backdrop-filter:blur(18px);
    }
    .card[data-rank]::before {
      content:attr(data-rank);
      position:absolute;
      left:-64px;
      top:18px;
      width:42px;
      height:42px;
      border-radius:999px;
      display:flex;
      align-items:center;
      justify-content:center;
      color:var(--orange);
      font-family:var(--font-mono);
      font-size:12px;
      background:var(--node);
      border:1px solid rgba(249,115,22,.18);
      box-shadow:0 12px 22px rgba(249,115,22,.08);
    }
    .card[data-rank]:hover::before {
      border-color:rgba(249,115,22,.34);
      transform:translateY(-1px);
    }
    .card h3 a { color:var(--text); }
    .card h3 a:hover { color:var(--orange); }
    .card > p {
      margin:11px 0 0;
      color:var(--soft);
      font-size:15px;
      line-height:1.94;
      max-width:72ch;
    }
    .tag {
      display:inline-block;
      margin:2px 6px 2px 0;
      padding:3px 8px;
      border:1px solid var(--line);
      border-radius:999px;
      color:var(--muted);
      font-family:var(--font-mono);
      font-size:10px;
      white-space:nowrap;
      background:rgba(255,255,255,.58);
    }
    .tag:nth-child(1), .tag.primary {
      border-color:rgba(97,119,173,.18);
      color:var(--blue-strong);
      background:rgba(142,159,201,.08);
    }
    .tag:nth-child(2), .tag.value {
      border-color:rgba(249,115,22,.22);
      color:rgba(184,90,26,.96);
      background:rgba(249,115,22,.06);
    }
    .read-first {
      margin:18px 0 0;
      padding:16px 17px;
      border:1px solid rgba(249,115,22,.18);
      border-left:3px solid var(--orange);
      border-radius:0 16px 16px 0;
      background:linear-gradient(90deg, rgba(249,115,22,.09), rgba(249,115,22,.015) 76%);
    }
    .read-label {
      color:var(--orange);
      font-family:var(--font-mono);
      font-size:10px;
      letter-spacing:.16em;
      text-transform:uppercase;
    }
    .read-first ol { margin-top:9px; }
    .detail-stack {
      display:grid;
      gap:10px;
      margin:15px 0 0;
    }
    .detail-fold {
      border:1px solid var(--line);
      border-radius:16px;
      background:rgba(255,255,255,.58);
      overflow:hidden;
      transition:border-color .18s,background .18s,transform .18s;
      backdrop-filter:blur(14px);
    }
    .detail-fold:hover {
      border-color:rgba(142,159,201,.28);
      background:rgba(255,255,255,.76);
      transform:translateY(-1px);
    }
    .detail-fold summary {
      cursor:pointer;
      list-style:none;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:12px 14px;
      color:var(--blue-strong);
      font-family:var(--font-mono);
      font-size:10px;
      letter-spacing:.14em;
      text-transform:uppercase;
      user-select:none;
    }
    .detail-fold summary::-webkit-details-marker { display:none; }
    .detail-fold summary::after {
      content:"+";
      color:var(--muted);
      font-size:14px;
      line-height:1;
    }
    .detail-fold[open] summary {
      border-bottom:1px solid var(--line);
      background:rgba(142,159,201,.05);
    }
    .detail-fold[open] summary::after {
      content:"−";
      color:var(--orange);
    }
    .detail-fold > ol,
    .detail-fold > .lenses {
      margin:10px 14px 14px;
    }
    .detail-fold.risk-fold summary { color:var(--red); }
    .mini-grid {
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:8px;
      padding:12px;
    }
    .mini-grid div {
      border:1px solid var(--line);
      background:rgba(255,255,255,.6);
      border-radius:14px;
      padding:8px 10px;
      min-width:0;
    }
    .mini-grid b {
      display:block;
      color:var(--blue-strong);
      font-family:var(--font-mono);
      font-size:10px;
      letter-spacing:.12em;
      text-transform:uppercase;
    }
    .mini-grid span {
      color:var(--text);
      font-size:12.5px;
      overflow-wrap:anywhere;
    }
    ol {
      margin:7px 0 0;
      padding-left:22px;
    }
    li {
      margin:8px 0;
      color:var(--soft);
      font-size:14px;
      line-height:1.82;
    }
    li b {
      color:var(--text);
      font-weight:620;
    }
    .lenses {
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:10px;
    }
    .lens {
      border:1px solid var(--line);
      background:rgba(255,255,255,.64);
      border-radius:16px;
      padding:13px 14px;
    }
    .lens b {
      color:var(--blue-strong);
      font-family:var(--font-mono);
      font-size:10px;
      font-weight:620;
      letter-spacing:.14em;
      text-transform:uppercase;
    }
    .lens p {
      margin:7px 0 0;
      color:var(--soft);
      font-size:13px;
      line-height:1.72;
    }
    .trend-cards {
      margin:14px 0 0 84px;
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:14px;
    }
    .trend-card {
      border:1px solid var(--line);
      border-radius:20px;
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,251,244,.72));
      box-shadow:var(--shadow);
      padding:18px 18px 17px;
    }
    .trend-card h3 {
      margin:0 0 8px;
      font-size:20px;
      line-height:1.34;
    }
    .trend-card p {
      margin:0;
      color:var(--soft);
      font-size:14px;
      line-height:1.82;
    }
    .trend-evidence {
      display:flex;
      flex-wrap:wrap;
      gap:7px;
      margin:12px 0 0;
    }
    .trend-evidence span {
      border:1px solid rgba(97,119,173,.16);
      background:rgba(142,159,201,.08);
      color:var(--blue-strong);
      border-radius:999px;
      padding:4px 9px;
      font-family:var(--font-mono);
      font-size:10px;
    }
    .trend-action {
      margin-top:10px;
      color:rgba(184,90,26,.98);
      font-size:13px;
      line-height:1.7;
    }
    blockquote {
      margin:24px 0 0 84px;
      padding:22px 22px 24px;
      border:1px solid rgba(249,115,22,.18);
      border-left:4px solid var(--orange);
      border-radius:0 22px 22px 0;
      background:linear-gradient(180deg, rgba(255,248,240,.96), rgba(255,252,247,.82));
      color:var(--text);
      font-size:22px;
      font-weight:540;
      line-height:1.66;
      box-shadow:var(--shadow);
    }
    blockquote::before {
      content:"Conclusion";
      display:block;
      margin-bottom:10px;
      color:var(--orange);
      font-family:var(--font-mono);
      font-size:10px;
      letter-spacing:.18em;
      text-transform:uppercase;
    }
    .caveat {
      margin:14px 0 0;
      color:var(--muted);
      font-size:12px;
    }
    @media (max-width:860px) {
      .trend-cards { grid-template-columns:1fr; }
      .briefing-strip { grid-template-columns:1fr; }
      .stats { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .lenses,.mini-grid { grid-template-columns:1fr; }
    }
    @media (max-width:680px) {
      .wrap { padding:28px 14px 64px; }
      .toprow { flex-direction:column; }
      h1 { font-size:clamp(36px,14vw,60px); gap:10px; }
      .hero-lede { font-size:15px; line-height:1.82; }
      .timeline::before { left:18px; }
      .section-head {
        padding-left:54px;
        gap:10px;
      }
      .section-head .range { min-width:42px; }
      .table-wrap,
      .card,
      .trend-cards,
      blockquote,
      .section-tools { margin-left:54px; }
      .table-wrap {
        overflow:visible;
        border:0;
        background:transparent;
        border-radius:0;
        box-shadow:none;
        backdrop-filter:none;
      }
      table, thead, tbody, tr, td {
        display:block;
        width:100%;
        min-width:0;
      }
      table { min-width:0; }
      thead { display:none; }
      tbody { display:grid; gap:10px; }
      tbody tr {
        border:1px solid var(--line);
        border-radius:16px;
        background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,252,247,.72));
        padding:12px 12px 10px;
        box-shadow:var(--shadow-soft);
      }
      td {
        border:0;
        display:grid;
        grid-template-columns:84px minmax(0,1fr);
        gap:8px;
        align-items:start;
        padding:4px 0;
        font-size:12.5px;
      }
      td::before {
        color:var(--muted);
        font-family:var(--font-mono);
        font-size:10px;
        letter-spacing:.08em;
        text-transform:uppercase;
      }
      td:nth-child(1)::before { content:"Rank"; }
      td:nth-child(2)::before { content:"Repo"; }
      td:nth-child(3)::before { content:"Lang"; }
      td:nth-child(4)::before { content:"Period"; }
      td:nth-child(5)::before { content:"Stars"; }
      td:nth-child(6)::before { content:"Forks"; }
      td:nth-child(7)::before { content:"Issues"; }
      td:nth-child(8)::before { content:"Score"; }
      td:nth-child(9)::before { content:"Confidence"; }
      td:nth-child(10)::before { content:"Relation"; }
      td:nth-child(11)::before { content:"Signals"; }
      .card[data-rank]::before {
        left:-54px;
        width:36px;
        height:36px;
      }
      .detail-fold summary { min-height:46px; }
      .card > p { font-size:14.5px; line-height:1.88; }
      blockquote { font-size:19px; }
    }
  </style>
"""

STYLE_RE = re.compile(r"<style>.*?</style>", re.S)
PERIOD_LABEL_RE = re.compile(r"(PERIOD / <b>)(DAILY|WEEKLY)(</b>)")

TEXT_REPLACEMENTS = (
    ('<html lang="zh-CN" data-theme="dark">', '<html lang="zh-CN" data-theme="warm-signal">'),
    ("collect · judge · build", "scan · judge · decide"),
    (
        "面向中文 AI builder / founder / investor 的开源信号读物：先看趋势和判断，再按需展开技术证据。",
        "给中文 AI builder / operator / investor 的开源判断简报：先扫信号，再读结论，最后按需下钻证据。",
    ),
    ("<div class=\"briefing-item\"><b>Reading Order</b><span>先扫 Top10 与趋势卡片，再进入 Top 项目的“先读判断”。</span></div>",
     "<div class=\"briefing-item\"><b>Signal First</b><span>先扫 Top 10 与趋势卡片，快速建立今天最值得看的判断顺序。</span></div>"),
    ("<div class=\"briefing-item\"><b>Evidence</b><span>技术、数据、风险默认折叠，保留给需要核查的人。</span></div>",
     "<div class=\"briefing-item\"><b>Evidence on Demand</b><span>技术、数据与风险维持折叠，默认把注意力留给真正重要的结论。</span></div>"),
    ("<div class=\"briefing-item\"><b>Mobile</b><span>手机端 Top10 自动卡片化，减少横向拖拽。</span></div>",
     "<div class=\"briefing-item\"><b>Mobile Read</b><span>手机端自动转卡片布局，适合快速扫读、收藏和分享重点项目。</span></div>"),
    ("<span>跟进</span></a>", "<span>行动</span></a>"),
    ("<h2>A/B/C 跟进建议</h2><p>把热度变成下一步动作，而不是收藏夹。</p>",
     "<h2>A/B/C 行动建议</h2><p>把热度转成行动队列，而不是把好项目丢进收藏夹后失联。</p>"),
)


def restyle_report_html(html: str) -> str:
    if "<title>GitHub 热榜情报" not in html:
      return html

    if not STYLE_RE.search(html):
        raise ValueError("report page style block not found")

    html = STYLE_RE.sub(REPORT_STYLE, html, count=1)
    html = PERIOD_LABEL_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}", html)

    for old, new in TEXT_REPLACEMENTS:
        html = html.replace(old, new)

    return html


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = restyle_report_html(original)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def default_targets() -> list[Path]:
    globs = [
        "github-trending-daily-*.html",
        "github-trending-weekly-*.html",
        "daily/*/index.html",
        "weekly/*/index.html",
    ]
    paths: list[Path] = []
    for pattern in globs:
        paths.extend(sorted(ROOT.glob(pattern)))
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Restyle generated report HTML pages.")
    parser.add_argument("paths", nargs="*", help="Specific HTML files to restyle.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = [Path(path).resolve() for path in args.paths] if args.paths else default_targets()
    changed = 0
    for path in targets:
        if process_file(path):
            changed += 1
    print(f"restyled {changed} report page(s)")


if __name__ == "__main__":
    main()

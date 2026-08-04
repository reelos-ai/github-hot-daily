#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent.parent

_LEGACY_REPORT_STYLE = """
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

REPORT_STYLE_PATH = ROOT / "scripts" / "report_editorial.css"
PROJECT_BRIEFS_PATH = ROOT / "project-briefs-zh.json"
REPORT_STYLE = f"""<style>
{REPORT_STYLE_PATH.read_text(encoding="utf-8")}
</style>"""

STYLE_RE = re.compile(r"<style>.*?</style>", re.S)
PERIOD_LABEL_RE = re.compile(r"(PERIOD / <b>)(DAILY|WEEKLY)(</b>)")
BRIEFING_RE = re.compile(r"\s*<section class=\"briefing-strip\".*?</section>", re.S)
NAV_RE = re.compile(r"<nav class=\"section-nav\".*?</nav>", re.S)
STATS_RE = re.compile(r"<section class=\"stats\"[^>]*>.*?</section>", re.S)
STAT_RE = re.compile(r"<div class=\"stat\"><b>(.*?)</b><span>(.*?)</span></div>", re.S)
FIRST_ROW_RE = re.compile(r"<tbody><tr>(.*?)</tr>", re.S)
TD_RE = re.compile(r"<td>(.*?)</td>", re.S)
HERO_LEDE_RE = re.compile(r"(<p class=\"hero-lede\">.*?</p>)", re.S)
BLOCKQUOTE_RE = re.compile(r"\s*<blockquote>(.*?)</blockquote>", re.S)
CAVEAT_RE = re.compile(r"\s*<p class=\"caveat\">(.*?)</p>", re.S)
SECTION_MARKER = '<section class="signal-section" id="{section_id}">'
SECTION_ORDER = ("sec-top10", "sec-trends", "sec-deep", "sec-lens", "sec-actions")
SECTION_NUMBERS = {
    "sec-top10": "01",
    "sec-trends": "02",
    "sec-deep": "03",
    "sec-lens": "04",
    "sec-actions": "05",
}

EDITORIAL_NAV = """<nav class="section-nav" aria-label="报告分组导航">
      <a class="section-link" href="#sec-top10"><span class="nr mono">01</span><span>项目速览</span></a>
      <a class="section-link" href="#sec-deep"><span class="nr mono">02</span><span>重点项目</span></a>
      <a class="section-link" href="#sec-trends"><span class="nr mono">03</span><span>今日趋势</span></a>
    </nav>"""

TEXT_REPLACEMENTS = (
    ('<html lang="zh-CN" data-theme="dark">', '<html lang="zh-CN" data-theme="warm-signal">'),
    ('<html lang="zh-CN" data-theme="warm-signal">', '<html lang="zh-CN" data-theme="editorial">'),
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
    ("<h2>Top 3-5 深度分析</h2>", "<h2>重点项目深度分析</h2>"),
)


def strip_tags(value: str) -> str:
    return re.sub(r"<.*?>", "", value).strip()


def build_editorial_stats(html: str) -> str:
    stats_match = STATS_RE.search(html)
    if not stats_match:
        return html

    stats = STAT_RE.findall(stats_match.group(0))
    candidate_count = strip_tags(stats[0][0]) if stats else "—"
    top_count = strip_tags(stats[1][0]) if len(stats) > 1 else "10"
    highest_score = "—"
    row_match = FIRST_ROW_RE.search(html)
    if row_match:
        cells = TD_RE.findall(row_match.group(1))
        if len(cells) > 7:
            highest_score = strip_tags(cells[7])

    replacement = f"""<section class="stats" aria-label="本期核心数据">
      <div class="stat"><b>{candidate_count}</b><span>候选项目</span></div>
      <div class="stat"><b>{top_count}</b><span>核心信号</span></div>
      <div class="stat"><b>{highest_score}</b><span>最高评分</span></div>
    </section>"""
    return STATS_RE.sub(replacement, html, count=1)


def reorder_report_sections(html: str) -> str:
    main_start = html.find('<main class="timeline"')
    if main_start < 0:
        return html
    main_content_start = html.find(">", main_start) + 1
    main_end = html.find("</main>", main_content_start)
    if main_end < 0:
        return html

    body = html[main_content_start:main_end]
    positions = {
        section_id: body.find(SECTION_MARKER.format(section_id=section_id))
        for section_id in SECTION_ORDER
    }
    if any(position < 0 for position in positions.values()):
        return html

    ordered_by_position = sorted(positions, key=positions.get)
    chunks: dict[str, str] = {}
    for index, section_id in enumerate(ordered_by_position):
        start = positions[section_id]
        end = positions[ordered_by_position[index + 1]] if index + 1 < len(ordered_by_position) else len(body)
        chunk = body[start:end].strip()
        chunk = re.sub(
            r'(<span class="range mono">)\d{2}(</span>)',
            rf"\g<1>{SECTION_NUMBERS[section_id]}\2",
            chunk,
            count=1,
        )
        chunks[section_id] = chunk

    replacement = "\n  ".join(chunks[section_id] for section_id in SECTION_ORDER)
    return html[:main_content_start] + "\n  " + replacement + "\n" + html[main_end:]


def add_deep_project_toggle(html: str) -> str:
    if "data-deep-toggle" in html:
        return html

    deep_start = html.find(SECTION_MARKER.format(section_id="sec-deep"))
    deep_end = html.find(SECTION_MARKER.format(section_id="sec-lens"))
    if deep_start < 0 or deep_end < 0:
        return html

    chunk = html[deep_start:deep_end]
    tools_match = re.search(r'(<div class="section-tools".*?)(</div>)', chunk, re.S)
    button = '<button class="tool-btn" type="button" data-deep-toggle aria-expanded="false">查看全部 5 个项目</button>'
    if tools_match:
        chunk = chunk[:tools_match.end(1)] + button + chunk[tools_match.end(1):]
    else:
        cards_marker = "<div class='cards'>"
        chunk = chunk.replace(
            cards_marker,
            f'<div class="section-tools">{button}</div>{cards_marker}',
            1,
        )

    return html[:deep_start] + chunk + html[deep_end:]


def add_editorial_interaction(html: str) -> str:
    if "editorial-deep-toggle" in html:
        return html

    interaction = """
  // editorial-deep-toggle
  const deepSection = document.querySelector('#sec-deep');
  const deepToggle = document.querySelector('[data-deep-toggle]');
  if (deepSection && deepToggle) {
    deepToggle.addEventListener('click', () => {
      const expanded = deepSection.classList.toggle('show-all');
      deepToggle.setAttribute('aria-expanded', String(expanded));
      deepToggle.textContent = expanded ? '仅显示 Top 3' : '查看全部 5 个项目';
    });
  }
"""
    return html.replace("</script>", interaction + "</script>", 1)


def add_editorial_content(html: str) -> str:
    if '<a class="skip-link"' not in html:
        html = html.replace(
            "<body>",
            '<body>\n<a class="skip-link" href="#main-content">跳到主要内容</a>',
            1,
        )

    html = html.replace('<main class="timeline">', '<main class="timeline" id="main-content">', 1)
    html = BRIEFING_RE.sub("", html, count=1)
    html = NAV_RE.sub(EDITORIAL_NAV, html, count=1)

    if 'class="hero-verdict"' not in html:
        quote_match = BLOCKQUOTE_RE.search(html)
        if quote_match:
            verdict = strip_tags(quote_match.group(1))
            verdict = re.sub(r"^一句话结论[：:]\s*", "", verdict)
            verdict_html = (
                '<div class="hero-verdict">'
                '<span class="label">今日结论</span>'
                f"<p>{verdict}</p>"
                "</div>"
            )
            html = HERO_LEDE_RE.sub(rf"\1\n    {verdict_html}", html, count=1)
            html = BLOCKQUOTE_RE.sub("", html, count=1)

    caveat_match = CAVEAT_RE.search(html)
    if caveat_match and 'class="data-note"' not in html:
        caveat = caveat_match.group(1).strip()
        html = CAVEAT_RE.sub("", html, count=1)
        data_note = (
            '<section class="data-note" aria-labelledby="data-note-title">'
            '<h2 id="data-note-title">数据说明</h2>'
            f"<p>{caveat}</p>"
            "</section>"
        )
        html = html.replace("</main>", f"  {data_note}\n</main>", 1)

    return html


def detect_report_context(html: str) -> tuple[str, str] | None:
    period_match = re.search(r"\d{4}-\d{2}(?:-\d{2})?", html)
    if not period_match:
        return None
    period = period_match.group(0)
    if "GitHub 热榜情报日报" in html:
        return "daily", period
    if "GitHub 热榜情报周报" in html:
        return "weekly", period
    if "GitHub 热榜情报月报" in html:
        return "monthly", period[:7]
    return None


def extract_page_projects(html: str) -> dict[str, dict]:
    soup = BeautifulSoup(html, "html.parser")
    projects: dict[str, dict] = {}

    for row in soup.select("#sec-top10 tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        source = cells[1].find("a")
        name = cells[1].get_text(" ", strip=True)
        projects[name] = {
            "full_name": name,
            "url": source.get("href", "#") if source else "#",
            "language": cells[2].get_text(" ", strip=True),
            "stars_this_period": int(re.sub(r"\D", "", cells[3].get_text()) or 0),
            "strategic_keywords": [
                tag.get_text(" ", strip=True)
                for tag in cells[-1].select(".tag")
            ],
        }

    for card in soup.select("#sec-deep .card, .project-row"):
        heading = card.find("h3")
        paragraph = card.find("p")
        if not heading or not paragraph:
            continue
        name = heading.get_text(" ", strip=True)
        if name not in projects:
            source = card.select_one(".source-link") or heading.find("a")
            signal = card.select_one(".project-signal")
            language = signal.find("span").get_text(" ", strip=True) if signal and signal.find("span") else ""
            heat = signal.find("strong").get_text(" ", strip=True) if signal and signal.find("strong") else ""
            projects[name] = {
                "full_name": name,
                "url": source.get("href", "#") if source else "#",
                "language": language,
                "stars_this_period": int(re.sub(r"\D", "", heat) or 0),
                "strategic_keywords": [
                    tag.get_text(" ", strip=True)
                    for tag in card.select(".project-tag")
                ],
            }
        text = paragraph.get_text(" ", strip=True)
        if text:
            projects[name]["page_summary"] = text
    return projects


def load_report_projects(html: str) -> tuple[str, str, list[dict]] | None:
    context = detect_report_context(html)
    if not context:
        return None
    report_type, period = context
    page_projects = extract_page_projects(html)
    data_candidates = {
        "daily": [ROOT / f"top10-{period}.json"],
        "weekly": [
            ROOT / f"weekly-top10-{period}.json",
            ROOT / f"top10-{period}.json",
        ],
        "monthly": [
            ROOT / f"monthly-top10-{period}.json",
            ROOT / f"top10-{period}-01.json",
        ],
    }
    data_path = next((path for path in data_candidates[report_type] if path.exists()), None)
    if data_path:
        projects = json.loads(data_path.read_text(encoding="utf-8"))
    else:
        projects = list(page_projects.values())
    if not projects:
        return None

    briefs = {}
    if PROJECT_BRIEFS_PATH.exists():
        briefs = json.loads(PROJECT_BRIEFS_PATH.read_text(encoding="utf-8"))

    for project in projects:
        name = project.get("full_name", "")
        brief = dict(briefs.get(name, {}))
        page_project = page_projects.get(name, {})
        if not brief.get("summary") and page_project.get("page_summary"):
            page_summary = page_project["page_summary"]
            if "更适合被看作" not in page_summary or len(page_summary) <= 220:
                brief["summary"] = page_summary
        project["brief_zh"] = brief
        if not project.get("strategic_keywords"):
            project["strategic_keywords"] = page_project.get("strategic_keywords", [])
    return report_type, period, projects


TAG_TRANSLATIONS = {
    "agent": "Agent 工具",
    "agents": "多 Agent",
    "agent-framework": "Agent 框架",
    "agent-frameworks": "Agent 框架",
    "agent-skill": "Agent 技能",
    "agent-skills": "Agent 技能",
    "agentic-ai": "Agent 系统",
    "ai": "AI 应用",
    "automation": "自动化",
    "browser": "浏览器 Agent",
    "chatbot": "聊天机器人",
    "claude": "Claude 生态",
    "cli": "命令行",
    "code-review": "代码审查",
    "context": "上下文工程",
    "database": "数据基础设施",
    "dashboard": "可视化看板",
    "developer-tools": "开发工具",
    "devtools": "开发者工具",
    "eval": "评测",
    "infra": "AI Infra",
    "llm": "大模型应用",
    "mcp": "MCP 集成",
    "memory": "长期记忆",
    "rag": "RAG",
    "runtime": "运行时",
    "search": "搜索",
    "security": "安全能力",
    "skill": "技能扩展",
    "skills": "技能扩展",
    "voice": "语音能力",
    "workflow": "工作流",
    "workspace": "工作区",
}


def project_capability_tags(project: dict, brief: dict) -> list[str]:
    capabilities = brief.get("capabilities") or ""
    tags = [item.strip() for item in capabilities.split("、") if item.strip()]
    if not tags:
        metadata_topics = (project.get("metadata") or {}).get("topics") or []
        candidates = [*(project.get("strategic_keywords") or []), *metadata_topics]
        tags = [TAG_TRANSLATIONS.get(str(item).lower(), str(item)) for item in candidates]
    tags = list(dict.fromkeys(tags))
    if len(tags) < 3 and project.get("language"):
        tags.append(f'{project["language"]} 项目')
    return tags[:4]


def render_project_overview(projects: list[dict], report_type: str) -> str:
    heat_labels = {
        "daily": "今日",
        "weekly": "本周",
        "monthly": "本月",
    }
    heat_label = heat_labels[report_type]
    rows = []
    for rank, project in enumerate(projects, start=1):
        brief = project.get("brief_zh", {})
        summary = brief.get("summary") or project.get("description") or "项目说明暂缺。"
        tags = project_capability_tags(project, brief)
        if not tags:
            tags = [project.get("language") or "开源项目"]
        tags_html = "".join(
            f'<span class="project-tag">{escape(tag)}</span>'
            for tag in tags
        )
        rows.append(
            f"""<article class="project-row">
          <span class="project-rank mono">{rank:02d}</span>
          <div class="project-main">
            <h3>{escape(project.get('full_name', ''))}</h3>
            <p>{escape(summary)}</p>
            <div class="project-actions">
              <div class="project-tags" aria-label="项目标签">{tags_html}</div>
              <a class="source-link" href="{escape(project.get('url', '#'))}" target="_blank" rel="noopener noreferrer">原文 ↗</a>
            </div>
          </div>
          <div class="project-signal">
            <span>{escape(project.get('language') or 'Unknown')}</span>
            <strong>{heat_label} +{project.get('stars_this_period', 0)}</strong>
          </div>
        </article>"""
        )

    return f"""<section class="signal-section project-overview" id="sec-top10">
    <div class="section-head"><div><h2>10 个项目，一句话看懂</h2><p>标签用于快速识别能力，点击“原文”打开 GitHub 仓库。</p></div></div>
    <div class="project-list">{''.join(rows)}</div>
  </section>"""


def render_report_navigation(report_type: str, period: str) -> str:
    labels = {
        "daily": "日报",
        "weekly": "周报",
        "monthly": "月报",
    }
    periods = sorted(
        path.parent.name
        for path in (ROOT / report_type).glob("*/index.html")
        if re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", path.parent.name)
    )
    previous = max((item for item in periods if item < period), default=None)
    following = min((item for item in periods if item > period), default=None)
    links = []
    if previous:
        links.append(f'<a href="/{report_type}/{previous}/">← {previous[5:]}</a>')
    links.append(f'<a href="/{report_type}/">全部{labels[report_type]}</a>')
    if following:
        links.append(f'<a href="/{report_type}/{following}/">{following[5:]} →</a>')
    return f'<nav class="issue-nav" aria-label="{labels[report_type]}日期导航">{"".join(links)}</nav>'


def render_reelos_brand() -> str:
    return """<a class="reelos-lockup" href="/" aria-label="ReelOS.ai">
      <span class="reelos-mark" aria-hidden="true"><span></span></span>
      <span class="reelos-lockup-copy">
        <span class="reelos-wordmark">Reel<span class="reelos-logo-os">OS</span>.ai</span>
        <span class="reelos-lockup-subtitle">GitHub 热榜情报</span>
      </span>
    </a>"""


def simplify_report(html: str, context: tuple[str, str, list[dict]] | None) -> str:
    if not context:
        return html
    report_type, period, projects = context
    title_labels = {
        "daily": "今日项目",
        "weekly": "本周项目",
        "monthly": "本月项目",
    }

    html = STATS_RE.sub("", html, count=1)
    main_start = html.find('<main class="timeline"')
    main_content_start = html.find(">", main_start) + 1
    main_end = html.find("</main>", main_content_start)
    if min(main_start, main_content_start, main_end) < 0:
        return html

    main_content = render_project_overview(projects, report_type)
    html = html[:main_content_start] + "\n  " + main_content + "\n" + html[main_end:]
    html = html.replace("<header>", '<header class="project-header">', 1)
    html = re.sub(
        r'<div class="mono" style="color:var\(--muted\);font-size:12px;">.*?</div>',
        "",
        html,
        count=1,
    )
    html = re.sub(
        r"<h1>.*?</h1>",
        f'<h1><span class="pixel-word">GitHub</span> {title_labels[report_type]}</h1>',
        html,
        count=1,
        flags=re.S,
    )
    if 'class="issue-nav"' not in html:
        html = re.sub(
            r'(<div class="toprow">\s*<div class="brand">.*?</div>)',
            rf"\1{render_report_navigation(report_type, period)}",
            html,
            count=1,
            flags=re.S,
        )
    html = re.sub(
        r'<div class="brand">.*?</div>',
        f'<div class="brand">{render_reelos_brand()}</div>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<div class="sub">.*?</div>',
        f'<div class="sub"><span class="mono">{period}</span></div>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<p class="hero-lede">.*?</p>',
        '<p class="hero-lede">只回答一个问题：这些项目是做什么的。</p>',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r'\s*<div class="hero-verdict">.*?</div>', "", html, count=1, flags=re.S)
    html = NAV_RE.sub("", html, count=1)
    return html


def restyle_report_html(html: str) -> str:
    if "<title>GitHub 热榜情报" not in html:
      return html

    if not STYLE_RE.search(html):
        raise ValueError("report page style block not found")

    html = STYLE_RE.sub(REPORT_STYLE, html, count=1)
    html = PERIOD_LABEL_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}", html)

    for old, new in TEXT_REPLACEMENTS:
        html = html.replace(old, new)

    html = build_editorial_stats(html)
    html = reorder_report_sections(html)
    html = add_deep_project_toggle(html)
    html = add_editorial_content(html)
    html = simplify_report(html, load_report_projects(html))
    html = add_editorial_interaction(html)

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
        "github-trending-monthly-*.html",
        "daily/*/index.html",
        "weekly/*/index.html",
        "monthly/*/index.html",
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

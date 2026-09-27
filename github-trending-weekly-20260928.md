# GitHub 热榜情报周报｜2026-09-28

完整的中文交互报告见 [周报页面](/weekly/2026-09-28/)；本 Markdown 文件用于归档与快速检索。

本周的主线是 Agent 能力从“模型调用”转向可持续的记忆、可执行的办公运行时与可治理的代码审查。热度只反映关注度，不等同于真实采用或生产成熟度。

## Top 10

| # | 项目 | 语言 | 周期新增 stars | 总 stars | 关系标签 | 评分 |
|---:|---|---|---:|---:|---|---:|
| 1 | vectorize-io/hindsight | Python | 7,282 | 37,160 | Memory 组件 | 97 |
| 2 | affaan-m/ECC | JavaScript | 5,522 | 268,373 | Memory 组件 | 97 |
| 3 | dream-num/univer | TypeScript | 4,660 | 20,120 | Runtime 参考 | 97 |
| 4 | hydra-db/hydradb | Rust | 4,415 | 10,881 | Memory 组件 | 97 |
| 5 | alibaba/open-code-review | Go | 4,310 | 41,911 | Memory 组件 | 97 |
| 6 | Tencent/WeKnora | Go | 3,015 | 30,589 | Memory 组件 | 97 |
| 7 | strands-agents/harness-sdk | Python | 1,097 | 8,485 | Memory 组件 | 97 |
| 8 | TencentCloud/Octop | Python | 951 | 5,255 | Memory 组件 | 97 |
| 9 | superdesigndev/treg | Python | 1,773 | 3,584 | Skill 来源 | 96 |
| 10 | rohitg00/ai-engineering-from-scratch | Python | 3,207 | 59,208 | Memory 组件 | 95 |

## 跟进建议

- A：拆解 Hindsight 的 retain / recall / reflect 与 MCP 接口；复核 Open Code Review 的确定性规则与 LLM Agent 边界；评估 Univer 作为办公任务运行时的隔离与权限模型。
- B：追踪 HydraDB 的对象存储图数据库路径、WeKnora 的数据生命周期，以及 Strands harness 的评测与恢复机制。
- C：对 Octop、treg 与教程型仓库保持榜单记录，先验证持续性、维护投入与真实使用案例。

## 数据质量

覆盖 GitHub Trending 全站、Python、TypeScript、JavaScript、Go、Rust 六个切片；60 个去重候选均拿到 README 与元数据，46 个拿到依赖清单，API 失败 0。战略评分为可审计的启发式排序，不代表项目质量或市场确定性。

> 一句话结论：本周值得研究的不是某个单一 Agent，而是围绕记忆、工作空间运行时和可治理开发流程的能力层正在一起升温。

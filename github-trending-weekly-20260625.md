# GitHub 热榜情报分析 - 2026-06-25

- 周期: weekly
- 候选项目: 60
- Top 项目: 10
- README 覆盖: 59

## Top 10

| # | Repository | Language | Period Stars | Total Stars | Forks | Issues | Score | Confidence | Label | Keywords |
|---|------------|----------|--------------|-------------|-------|--------|-------|------------|-------|----------|
| 1 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | Python | 12948 | 21587 | 2414 | 123 | 98 | high | Skill 来源 | agent, skill, workflow |
| 2 | [google-research/timesfm](https://github.com/google-research/timesfm) | Python | 3915 | 25531 | 2427 | 228 | 97 | high | Memory 组件 | agent, agents, skill, workspace, inference |
| 3 | [topoteretes/cognee](https://github.com/topoteretes/cognee) | Python | 3631 | 22191 | 2139 | 224 | 97 | high | Memory 组件 | agent, agents, memory, rag, skill |
| 4 | [jamiepine/voicebox](https://github.com/jamiepine/voicebox) | TypeScript | 3583 | 34112 | 4102 | 485 | 97 | high | Workspace 组件 | agent, agents, mcp, workspace, llm |
| 5 | [googleworkspace/cli](https://github.com/googleworkspace/cli) | Rust | 1411 | 28588 | 1587 | 121 | 97 | high | Runtime 参考 | agent, agents, runtime, skill, workspace |
| 6 | [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | Go | 748 | 17306 | 2261 | 286 | 96 | high | Skill 来源 | agent, agents, mcp, rag, skill |
| 7 | [modem-dev/hunk](https://github.com/modem-dev/hunk) | TypeScript | 718 | 5648 | 145 | 63 | 96 | high | Memory 组件 | agent, agents, skill, workspace, workflow |
| 8 | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | Go | 545 | 83628 | 9699 | 2849 | 96 | high | Memory 组件 | agent, agents, rag, llm, eval |
| 9 | [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | C | 9589 | 14605 | 1074 | 150 | 95 | high | Memory 组件 | agent, agents, memory, mcp, rag |
| 10 | [OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) | TypeScript | 3550 | 59699 | 6484 | 329 | 95 | high | Skill 来源 | agent, agents, mcp, automation |

## Top 3-5 深度分析

### [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)

- 关系标签: Skill 来源
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, requirements.txt
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 9, "risk_signal": 10, "total": 98}
- 描述: World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.

#### 基础数据
- 周期 stars: 12948
- 总 stars: 21587
- forks: 2414
- open issues: 123
- 主语言: Python
- license: AGPL-3.0
- 创建时间: 2026-03-29
- 最后 push: 2026-06-24
- topics: agent, agentic-ai, ai, claude, copilot, cursor, elevenlabs, ffmpeg

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 依赖线索：检测到 `requirements.txt`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.
- Topics：agent, agentic-ai, ai, claude, copilot, cursor, elevenlabs, ffmpeg
- 许可证：AGPL-3.0
- 热度：本周期新增 12948 stars，当前总星标 21587。
- README 数字信号：Starting from a reference video is often faster than starting from a blank prompt

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 出现 workflow/automation/pipeline 信号，可能具备可复用流程编排模式。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: 从当前描述看，主要痛点是：World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.
- 为什么现在 trending: 本周期新增 12948 stars；跨多个 Trending 切片重复出现；命中 agent, skill, workflow；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 存在协议、运行时、记忆或 agentic workflow 信号，可能具备架构层创新。

#### 六视角解读
- AI Builder: 评估 calesthio/OpenMontage 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Skill 来源` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=AGPL-3.0；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=123，last push=2026-06-24；需进一步查看 contributors、release cadence 和 bus factor。

### [google-research/timesfm](https://github.com/google-research/timesfm)

- 关系标签: Memory 组件
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, pyproject.toml
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.

#### 基础数据
- 周期 stars: 3915
- 总 stars: 25531
- forks: 2427
- open issues: 228
- 主语言: Python
- license: Apache-2.0
- 创建时间: 2024-04-29
- 最后 push: 2026-06-23
- topics: -

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 依赖线索：检测到 `pyproject.toml`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.
- 许可证：Apache-2.0
- 热度：本周期新增 3915 stars，当前总星标 25531。
- README 数字信号：✅ Flax version of the model for faster inference
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 出现 memory/context/state 信号，适合跟踪上下文持久化或状态管理方式。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 未从 README 摘要中确认。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: 从当前描述看，主要痛点是：TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.
- 为什么现在 trending: 本周期新增 3915 stars；跨多个 Trending 切片重复出现；命中 agent, agents, skill, workspace；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 存在协议、运行时、记忆或 agentic workflow 信号，可能具备架构层创新。

#### 六视角解读
- AI Builder: 评估 google-research/timesfm 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Memory 组件` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=Apache-2.0；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=228，last push=2026-06-23；需进一步查看 contributors、release cadence 和 bus factor。

### [topoteretes/cognee](https://github.com/topoteretes/cognee)

- 关系标签: Memory 组件
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, pyproject.toml
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.

#### 基础数据
- 周期 stars: 3631
- 总 stars: 22191
- forks: 2139
- open issues: 224
- 主语言: Python
- license: Apache-2.0
- 创建时间: 2023-08-16
- 最后 push: 2026-06-25
- topics: agent-memory, agent-skills, ai, ai-agents, ai-memory, cognitive-architecture, cognitive-memory, context-engineering

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 检索增强：出现 RAG/retrieval/embedding 信号，可跟踪知识接入与上下文管理模式。
- 依赖线索：检测到 `pyproject.toml`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.
- Topics：agent-memory, agent-skills, ai, ai-agents, ai-memory, cognitive-architecture, cognitive-memory, context-engineering
- 许可证：Apache-2.0
- 热度：本周期新增 3631 stars，当前总星标 22191。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 出现 memory/context/state 信号，适合跟踪上下文持久化或状态管理方式。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 未从 README 摘要中确认。
- Storage: 出现 database/vector/storage/cache 信号，可继续核实数据层设计。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: 从当前描述看，主要痛点是：Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.
- 为什么现在 trending: 本周期新增 3631 stars；命中 agent, agents, memory, rag；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 存在协议、运行时、记忆或 agentic workflow 信号，可能具备架构层创新。

#### 六视角解读
- AI Builder: 评估 topoteretes/cognee 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Memory 组件` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=Apache-2.0；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=224，last push=2026-06-25；需进一步查看 contributors、release cadence 和 bus factor。

### [jamiepine/voicebox](https://github.com/jamiepine/voicebox)

- 关系标签: Workspace 组件
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, package.json
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: The open-source AI voice studio. Clone, dictate, create.

#### 基础数据
- 周期 stars: 3583
- 总 stars: 34112
- forks: 4102
- open issues: 485
- 主语言: TypeScript
- license: MIT
- 创建时间: 2026-01-25
- 最后 push: 2026-04-26
- topics: ai, cuda, mlx, qwen3-tts, qwen3-tts-ui, voice-ai, voice-clone, whisper

#### 技术原理与实现
- 协议/接口层：README 或 topics 出现 MCP/protocol 信号，适合作为跨工具互操作参考。
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 依赖线索：检测到 `package.json`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：The open-source AI voice studio. Clone, dictate, create.
- Topics：ai, cuda, mlx, qwen3-tts, qwen3-tts-ui, voice-ai, voice-clone, whisper
- 许可证：MIT
- 热度：本周期新增 3583 stars，当前总星标 34112。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 未从 README 摘要中确认。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: 从当前描述看，主要痛点是：The open-source AI voice studio. Clone, dictate, create.
- 为什么现在 trending: 本周期新增 3583 stars；跨多个 Trending 切片重复出现；命中 agent, agents, mcp, workspace；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 存在协议、运行时、记忆或 agentic workflow 信号，可能具备架构层创新。

#### 六视角解读
- AI Builder: 评估 jamiepine/voicebox 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Workspace 组件` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=MIT；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=485，last push=2026-04-26；需进一步查看 contributors、release cadence 和 bus factor。

### [googleworkspace/cli](https://github.com/googleworkspace/cli)

- 关系标签: Runtime 参考
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, Cargo.toml
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.

#### 基础数据
- 周期 stars: 1411
- 总 stars: 28588
- forks: 1587
- open issues: 121
- 主语言: Rust
- license: Apache-2.0
- 创建时间: 2026-03-02
- 最后 push: 2026-06-24
- topics: agent-skills, ai-agent, automation, cli, discovery-api, gemini-cli-extension, google-admin, google-api

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 运行时隔离：出现 runtime/sandbox/wasm 信号，可作为执行环境或安全边界参考。
- 依赖线索：检测到 `Cargo.toml`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.
- Topics：agent-skills, ai-agent, automation, cli, discovery-api, gemini-cli-extension, google-admin, google-api
- 许可证：Apache-2.0
- 热度：本周期新增 1411 stars，当前总星标 28588。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 出现 workflow/automation/pipeline 信号，可能具备可复用流程编排模式。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: 从当前描述看，主要痛点是：Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.
- 为什么现在 trending: 本周期新增 1411 stars；命中 agent, agents, runtime, skill；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 出现 wrapper/template/boilerplate 信号，需警惕只是重新包装。

#### 六视角解读
- AI Builder: 评估 googleworkspace/cli 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Runtime 参考` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=Apache-2.0；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=121，last push=2026-06-24；需进一步查看 contributors、release cadence 和 bus factor。

## 趋势观察

1. `agent` 成为交叉信号，代表项目包括 calesthio/OpenMontage 和 google-research/timesfm，说明该能力正在从单点工具扩散为生态能力。
2. `agents` 成为交叉信号，代表项目包括 google-research/timesfm 和 topoteretes/cognee，说明该能力正在从单点工具扩散为生态能力。
3. `skill` 成为交叉信号，代表项目包括 calesthio/OpenMontage 和 google-research/timesfm，说明该能力正在从单点工具扩散为生态能力。
4. `llm` 成为交叉信号，代表项目包括 topoteretes/cognee 和 jamiepine/voicebox，说明该能力正在从单点工具扩散为生态能力。
5. `workflow` 成为交叉信号，代表项目包括 calesthio/OpenMontage 和 googleworkspace/cli，说明该能力正在从单点工具扩散为生态能力。
6. `workspace` 成为交叉信号，代表项目包括 google-research/timesfm 和 jamiepine/voicebox，说明该能力正在从单点工具扩散为生态能力。
7. Skill 来源 类项目同时出现 calesthio/OpenMontage 和 Tencent/WeKnora，值得作为同类架构/市场定位样本持续跟踪。
8. Memory 组件 类项目同时出现 google-research/timesfm 和 topoteretes/cognee，值得作为同类架构/市场定位样本持续跟踪。

## 一句话结论

本期优先关注 calesthio/OpenMontage 代表的高相关方向。
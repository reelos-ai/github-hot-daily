# GitHub 热榜情报分析 - 2026-06-29

- 周期: weekly
- 候选项目: 60
- Top 项目: 10
- README 覆盖: 60

## Top 10

| # | Repository | Language | Period Stars | Total Stars | Forks | Issues | Score | Confidence | Label | Keywords |
|---|------------|----------|--------------|-------------|-------|--------|-------|------------|-------|----------|
| 1 | [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | Python | 18000 | 26831 | 2973 | 120 | 99 | high | Skill 来源 | agent, rag, skill, workflow |
| 2 | [topoteretes/cognee](https://github.com/topoteretes/cognee) | Python | 5519 | 24869 | 2302 | 373 | 97 | high | Memory 组件 | agent, agents, memory, rag, skill |
| 3 | [jamiepine/voicebox](https://github.com/jamiepine/voicebox) | TypeScript | 3965 | 35393 | 4252 | 491 | 97 | high | Workspace 组件 | agent, agents, mcp, workspace, llm |
| 4 | [googleworkspace/cli](https://github.com/googleworkspace/cli) | Rust | 1848 | 29072 | 1648 | 124 | 97 | high | Runtime 参考 | agent, agents, runtime, skill, workspace |
| 5 | [Tencent/WeKnora](https://github.com/Tencent/WeKnora) | Go | 934 | 17450 | 2294 | 284 | 97 | high | Skill 来源 | agent, agents, mcp, rag, skill |
| 6 | [stanford-oval/storm](https://github.com/stanford-oval/storm) | Python | 631 | 29561 | 2750 | 107 | 96 | high | Workspace 组件 | agent, rag, llm, eval, vector |
| 7 | [modem-dev/hunk](https://github.com/modem-dev/hunk) | TypeScript | 556 | 5761 | 151 | 70 | 96 | high | Memory 组件 | agent, agents, skill, workspace, workflow |
| 8 | [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | C | 7674 | 19508 | 1416 | 167 | 95 | high | Memory 组件 | agent, agents, memory, mcp, rag |
| 9 | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | Python | 3258 | 75223 | 10153 | 966 | 95 | high | Memory 组件 | agent, agents, memory, mcp, rag |
| 10 | [alibaba/page-agent](https://github.com/alibaba/page-agent) | TypeScript | 1649 | 20465 | 1763 | 47 | 95 | high | Skill 来源 | agent, agents, mcp, workspace, llm |

## Top 3-5 深度分析

### [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage)

- 关系标签: Skill 来源
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, requirements.txt
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 10, "total": 99}
- 描述: World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.

#### 基础数据
- 周期 stars: 18000
- 总 stars: 26831
- forks: 2973
- open issues: 120
- 主语言: Python
- license: AGPL-3.0
- 创建时间: 2026-03-29
- 最后 push: 2026-06-28
- topics: agent, agentic-ai, ai, claude, copilot, cursor, elevenlabs, ffmpeg

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 检索增强：出现 RAG/retrieval/embedding 信号，可跟踪知识接入与上下文管理模式。
- 依赖线索：检测到 `requirements.txt`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.
- Topics：agent, agentic-ai, ai, claude, copilot, cursor, elevenlabs, ffmpeg
- 许可证：AGPL-3.0
- 热度：本周期新增 18000 stars，当前总星标 26831。
- README 数字信号：Starting from a reference video is often faster than starting from a blank prompt

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 出现 workflow/automation/pipeline 信号，可能具备可复用流程编排模式。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: calesthio/OpenMontage 更适合被看作「Skill 来源」方向的候选样本，而不是单纯的热门仓库。公开描述显示它聚焦于「World's first open-source, agentic video production system. 12 pipelines, 52 tools, 500+ agent skills. Turn your AI coding assistant into a full video production studio.」。本周期新增 18000 stars、累计 26831 stars，主要信号集中在 agent、rag、skill、workflow。对中文读者而言，关键不是它有多少 star，而是它是否能被复用为产品能力、架构参考或观察池对象。
- 为什么现在 trending: 本周期新增 18000 stars；跨多个 Trending 切片重复出现；命中 agent, rag, skill, workflow；已有较高 star 基数，可能是老项目翻红。
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
- 社区维护风险: open issues=120，last push=2026-06-28；需进一步查看 contributors、release cadence 和 bus factor。

### [topoteretes/cognee](https://github.com/topoteretes/cognee)

- 关系标签: Memory 组件
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, pyproject.toml
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.

#### 基础数据
- 周期 stars: 5519
- 总 stars: 24869
- forks: 2302
- open issues: 373
- 主语言: Python
- license: Apache-2.0
- 创建时间: 2023-08-16
- 最后 push: 2026-06-27
- topics: agent-memory, agent-skills, ai, ai-agents, ai-memory, cognitive-architecture, cognitive-memory, context-engineering

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 检索增强：出现 RAG/retrieval/embedding 信号，可跟踪知识接入与上下文管理模式。
- 依赖线索：检测到 `pyproject.toml`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.
- Topics：agent-memory, agent-skills, ai, ai-agents, ai-memory, cognitive-architecture, cognitive-memory, context-engineering
- 许可证：Apache-2.0
- 热度：本周期新增 5519 stars，当前总星标 24869。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 出现 memory/context/state 信号，适合跟踪上下文持久化或状态管理方式。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 未从 README 摘要中确认。
- Storage: 出现 database/vector/storage/cache 信号，可继续核实数据层设计。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: topoteretes/cognee 更适合被看作「Memory 组件」方向的候选样本，而不是单纯的热门仓库。公开描述显示它聚焦于「Cognee is the open-source AI memory platform for agents. Give your AI agents persistent long-term memory across sessions with a self-hosted knowledge graph engine.」。本周期新增 5519 stars、累计 24869 stars，主要信号集中在 agent、agents、memory、rag。对中文读者而言，关键不是它有多少 star，而是它是否能被复用为产品能力、架构参考或观察池对象。
- 为什么现在 trending: 本周期新增 5519 stars；跨多个 Trending 切片重复出现；命中 agent, agents, memory, rag；已有较高 star 基数，可能是老项目翻红。
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
- 社区维护风险: open issues=373，last push=2026-06-27；需进一步查看 contributors、release cadence 和 bus factor。

### [jamiepine/voicebox](https://github.com/jamiepine/voicebox)

- 关系标签: Workspace 组件
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, package.json
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: The open-source AI voice studio. Clone, dictate, create.

#### 基础数据
- 周期 stars: 3965
- 总 stars: 35393
- forks: 4252
- open issues: 491
- 主语言: TypeScript
- license: MIT
- 创建时间: 2026-01-25
- 最后 push: 2026-06-28
- topics: ai, cuda, mlx, qwen3-tts, qwen3-tts-ui, voice-ai, voice-clone, whisper

#### 技术原理与实现
- 协议/接口层：README 或 topics 出现 MCP/protocol 信号，适合作为跨工具互操作参考。
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 依赖线索：检测到 `package.json`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：The open-source AI voice studio. Clone, dictate, create.
- Topics：ai, cuda, mlx, qwen3-tts, qwen3-tts-ui, voice-ai, voice-clone, whisper
- 许可证：MIT
- 热度：本周期新增 3965 stars，当前总星标 35393。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 未从 README 摘要中确认。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: jamiepine/voicebox 更适合被看作「Workspace 组件」方向的候选样本，而不是单纯的热门仓库。公开描述显示它聚焦于「The open-source AI voice studio. Clone, dictate, create.」。本周期新增 3965 stars、累计 35393 stars，主要信号集中在 agent、agents、mcp、workspace。对中文读者而言，关键不是它有多少 star，而是它是否能被复用为产品能力、架构参考或观察池对象。
- 为什么现在 trending: 本周期新增 3965 stars；跨多个 Trending 切片重复出现；命中 agent, agents, mcp, workspace；已有较高 star 基数，可能是老项目翻红。
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
- 社区维护风险: open issues=491，last push=2026-06-28；需进一步查看 contributors、release cadence 和 bus factor。

### [googleworkspace/cli](https://github.com/googleworkspace/cli)

- 关系标签: Runtime 参考
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, Cargo.toml
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.

#### 基础数据
- 周期 stars: 1848
- 总 stars: 29072
- forks: 1648
- open issues: 124
- 主语言: Rust
- license: Apache-2.0
- 创建时间: 2026-03-02
- 最后 push: 2026-06-28
- topics: agent-skills, ai-agent, automation, cli, discovery-api, gemini-cli-extension, google-admin, google-api

#### 技术原理与实现
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 运行时隔离：出现 runtime/sandbox/wasm 信号，可作为执行环境或安全边界参考。
- 依赖线索：检测到 `Cargo.toml`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.
- Topics：agent-skills, ai-agent, automation, cli, discovery-api, gemini-cli-extension, google-admin, google-api
- 许可证：Apache-2.0
- 热度：本周期新增 1848 stars，当前总星标 29072。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 出现 workflow/automation/pipeline 信号，可能具备可复用流程编排模式。
- Storage: 未从 README 摘要中确认。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: googleworkspace/cli 更适合被看作「Runtime 参考」方向的候选样本，而不是单纯的热门仓库。公开描述显示它聚焦于「Google Workspace CLI — one command-line tool for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, and more. Dynamically built from Google Discovery Service. Includes AI agent skills.」。本周期新增 1848 stars、累计 29072 stars，主要信号集中在 agent、agents、runtime、skill。对中文读者而言，关键不是它有多少 star，而是它是否能被复用为产品能力、架构参考或观察池对象。
- 为什么现在 trending: 本周期新增 1848 stars；命中 agent, agents, runtime, skill；已有较高 star 基数，可能是老项目翻红。
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
- 社区维护风险: open issues=124，last push=2026-06-28；需进一步查看 contributors、release cadence 和 bus factor。

### [Tencent/WeKnora](https://github.com/Tencent/WeKnora)

- 关系标签: Skill 来源
- 数据可信度: high
- 证据来源: github_trending, github_repo_api, readme, go.mod
- 评分分解: {"heat": 20, "relevance": 20, "novelty": 15, "productize": 14, "adoption": 10, "relation": 10, "risk_signal": 8, "total": 97}
- 描述: Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki.

#### 基础数据
- 周期 stars: 934
- 总 stars: 17450
- forks: 2294
- open issues: 284
- 主语言: Go
- license: NOASSERTION
- 创建时间: 2025-07-22
- 最后 push: 2026-06-27
- topics: agent, agentic, ai, chatbot, embeddings, evaluation, generative-ai, golang

#### 技术原理与实现
- 协议/接口层：README 或 topics 出现 MCP/protocol 信号，适合作为跨工具互操作参考。
- Agent 工作流：项目围绕 agent/workflow 自动化组织能力，适合评估任务编排方式。
- 检索增强：出现 RAG/retrieval/embedding 信号，可跟踪知识接入与上下文管理模式。
- 依赖线索：检测到 `go.mod`，可继续核实核心框架和运行依赖。

#### 核心特性
- 定位：Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki.
- Topics：agent, agentic, ai, chatbot, embeddings, evaluation, generative-ai, golang
- 许可证：NOASSERTION
- 热度：本周期新增 934 stars，当前总星标 17450。
- README 覆盖不足时，后续应人工补抓并核实具体功能边界。

#### 系统设计拆解
- Agent 编排: 出现 agent/workflow/orchestration 信号，可继续拆解任务规划与执行循环。
- Memory: 未从 README 摘要中确认。
- Tool Use: 出现 tool/plugin/connector/API 信号，可继续核实工具调用边界。
- Workflow: 出现 workflow/automation/pipeline 信号，可能具备可复用流程编排模式。
- Storage: 出现 database/vector/storage/cache 信号，可继续核实数据层设计。
- UI: 出现 UI/web/dashboard/editor 信号，可继续核实交互形态。

#### 三问判断
- 解决什么真问题: Tencent/WeKnora 更适合被看作「Skill 来源」方向的候选样本，而不是单纯的热门仓库。公开描述显示它聚焦于「Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki.」。本周期新增 934 stars、累计 17450 stars，主要信号集中在 agent、agents、mcp、rag。对中文读者而言，关键不是它有多少 star，而是它是否能被复用为产品能力、架构参考或观察池对象。
- 为什么现在 trending: 本周期新增 934 stars；命中 agent, agents, mcp, rag；已有较高 star 基数，可能是老项目翻红。
- 是真创新还是重新包装: 存在协议、运行时、记忆或 agentic workflow 信号，可能具备架构层创新。

#### 六视角解读
- AI Builder: 评估 Tencent/WeKnora 是否能复用为 agent、tool use、workflow、memory 或 workspace 组件。
- Investor: 结合 star 增速、总 star、license 与维护活跃度，判断它是品类机会、短期噪音还是开源分发信号。
- Product: 把 README 功能映射到用户痛点，确认它改变的是交互范式、开发效率还是部署/运维成本。
- Architecture: 重点拆解运行时边界、依赖栈、状态管理、扩展接口和安全边界。
- Founder: 根据关系标签 `Skill 来源` 判断是应跟进、集成、防守、学习架构，还是纳入观察池。
- 生态（OPC）: 判断它对开放协议、agentic computing、工具互操作和社区标准化的信号强度。

#### 风险评估
- 技术风险: 需继续核查核心依赖、执行边界、扩展点和性能瓶颈。
- 市场风险: Trending 只能证明短期注意力，需验证真实付费需求、替代方案和目标用户频次。
- 安全合规风险: license=NOASSERTION；如涉及代码执行、浏览器、数据抓取或 agent tool use，需额外核查安全边界。
- 社区维护风险: open issues=284，last push=2026-06-27；需进一步查看 contributors、release cadence 和 bus factor。

## 趋势观察

1. Agent 正在从聊天走向生产工作流：本周的强信号不是又多了几个聊天机器人，而是 agent 开始进入视频生产、企业工具和流程编排。它更像一套可执行工作流，而不是一个对话窗口。佐证项目：calesthio/OpenMontage, topoteretes/cognee, jamiepine/voicebox。行动含义：优先看它们如何组织 tool、pipeline、权限和失败恢复。
2. Memory / RAG 正在变成基础设施：记忆不再只是 prompt 技巧，而是开始以知识图谱、RAG、代码库记忆的形式进入 agent 底座。佐证项目：calesthio/OpenMontage, topoteretes/cognee, Tencent/WeKnora。行动含义：重点评估数据层、更新机制、权限边界和长期维护成本。
3. Workspace 工具正在被包装成 agent 可调用能力：CLI、编辑器、语音和企业软件项目同时升温，说明下一阶段竞争点是把现有工作工具变成 agent 能稳定调用的接口。佐证项目：calesthio/OpenMontage, jamiepine/voicebox, googleworkspace/cli。行动含义：适合跟进 CLI、MCP、插件化、权限模型和 SaaS API 封装方式。
4. 多模态生产工具开始进入开源工作台：视频、语音、文档和企业工具开始汇合，说明 AI workspace 不只服务开发者，也会服务内容生产和运营场景。佐证项目：calesthio/OpenMontage, jamiepine/voicebox, googleworkspace/cli。行动含义：短期看工具链复用，长期看是否形成稳定创作者工作流。

## 一句话结论

本期优先关注 calesthio/OpenMontage 代表的高相关方向。
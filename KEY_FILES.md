# 关键文件说明

## 原项目后端接口

| 文件 | 作用 | 面试讲解重点 |
|---|---|---|
| `../app/main.py` | FastAPI 入口，注册路由和静态文件，生命周期里连接 Milvus | 服务入口、路由分层、资源生命周期 |
| `../app/api/chat.py` | 普通对话与流式对话接口 | RAG Agent 如何通过 SSE 输出 |
| `../app/api/aiops.py` | AIOps 诊断接口 | 面试重点接口，返回诊断过程事件流 |
| `../app/api/file.py` | 文档上传与目录索引接口 | 上传文档后自动写入向量库 |
| `../app/api/health.py` | 健康检查接口 | 检查服务和 Milvus 状态 |

## 原项目 Agent 与工具

| 文件 | 作用 | 面试讲解重点 |
|---|---|---|
| `../app/services/rag_agent_service.py` | RAG Agent 服务 | ChatQwen、工具绑定、会话 MemorySaver |
| `../app/services/aiops_service.py` | Plan-Execute-Replan 工作流 | LangGraph 状态图，核心 Agent 流程 |
| `../app/agent/aiops/planner.py` | 规划节点 | 先查知识库，再制定诊断计划 |
| `../app/agent/aiops/executor.py` | 执行节点 | 每次执行一个步骤，调用本地工具或 MCP 工具 |
| `../app/agent/aiops/replanner.py` | 重规划节点 | 判断继续、改计划或生成最终报告 |
| `../app/agent/mcp_client.py` | MCP 客户端 | 多服务工具注册和重试拦截器 |
| `../app/tools/knowledge_tool.py` | 知识库检索工具 | Agent 与 Milvus RAG 的边界 |

## 原项目 RAG 与向量库

| 文件 | 作用 | 面试讲解重点 |
|---|---|---|
| `../app/services/document_splitter_service.py` | Markdown 和文本分块 | 两阶段分割，减少碎片化 |
| `../app/services/vector_embedding_service.py` | DashScope Embedding | OpenAI 兼容模式，1024 维向量 |
| `../app/services/vector_store_manager.py` | LangChain Milvus VectorStore | 写入和检索知识库 |
| `../app/core/milvus_client.py` | Milvus schema、连接和索引 | `biz` collection，向量字段和 JSON metadata |

## 原项目 MCP 服务

| 文件 | 作用 | 面试讲解重点 |
|---|---|---|
| `../mcp_servers/cls_server.py` | 日志查询 MCP 服务 | 模拟 CLS 主题搜索和日志检索 |
| `../mcp_servers/monitor_server.py` | 监控 MCP 服务 | 模拟 CPU 和内存指标 |

## 本次补充的文件

| 文件 | 作用 | 验证方式 |
|---|---|---|
| `ai_enhancement/aiops_summary_enhancer.py` | AI 增强点：结构化摘要、风险解释、下一步动作 | `python scripts/run_offline_demo.py` |
| `scripts/run_offline_demo.py` | 离线 demo 入口 | 不依赖外部服务 |
| `tests/test_aiops_summary_enhancer.py` | 两条测试样例 | `python -m unittest discover -s tests` |
| `sample_events/cpu_alert_events.json` | CPU 告警事件样例 | 验证 P1 风险和下一步动作 |
| `sample_events/tool_failure_events.json` | 工具失败事件样例 | 验证异常解释 |
| `DEBUG_RECORD.md` | 真实排错记录 | 展示测试失败、根因、修复、验证 |

## 面试中可明确表达的负责范围

本次面试包里可以重点讲：

- 我负责梳理原项目的后端接口、Agent 状态流和工具边界。
- 我补充了一个可离线验证的 AI 增强模块，把 Agent 过程事件转成结构化摘要。
- 我提供了两条可复现测试样例，覆盖正常告警和工具失败。
- 我整理了启动方式、关键文件说明、截图材料和真实排错记录。

# SuperBizAgent 面试 10 分钟验证包

本目录把原项目升级成“面试官 10 分钟内可验证”的交付形态。它围绕一个真实场景展开：值班人员收到 `data-sync-service` 告警后，需要 Agent 自动查询知识库、监控和日志，给出根因、风险解释和下一步动作。

## 1. 先看什么

建议面试官按这个顺序验证：

1. 阅读 `INTERVIEWER_QUICK_START.md`，直接复制验证命令。
2. 阅读 `RUNBOOK_10MIN.md`，按 10 分钟路线跑离线 demo 和测试。
3. 打开 `ARCHITECTURE.md`，确认 Agent 状态流和工具调用边界。
4. 打开 `KEY_FILES.md`，查看后端接口、关键模块和本次补充的 AI 增强点。
5. 打开 `TEST_SAMPLES.md`，复制两条样例命令或接口请求。
6. 打开 `DEBUG_RECORD.md`，查看一次真实排错记录。

## 2. 快速离线验证

不依赖 DashScope、Milvus、Docker 或 MCP 服务：

```powershell
cd <项目根目录>\agent_package
python scripts\run_full_verification.py
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
python -m unittest discover -s tests -p "test_*.py"
```

面试官测试时只需要把 `<项目根目录>` 替换为解压后的项目根目录。示例：如果代码包解压到 `D:\interview\SuperBizAgent`，则进入：

```powershell
cd D:\interview\SuperBizAgent\agent_package
```

预期结果：

- demo 输出 `AIOps 结构化诊断摘要`
- CPU 样例被识别为 `P1 - 高风险，需要立即处理`
- 单元测试显示 `Ran 2 tests` 和 `OK`
- `verification_logs/latest_verification.txt` 记录完整验证过程

## 3. 原项目完整启动方式

原项目根目录：

```text
<项目根目录>
```

Windows 推荐方式：

```powershell
cd <项目根目录>
.\start-windows.bat
```

启动后访问：

- Web 页面: http://localhost:9900
- API 文档: http://localhost:9900/docs
- AIOps 接口: `POST /api/aiops`
- 对话接口: `POST /api/chat`、`POST /api/chat_stream`
- 文件上传接口: `POST /api/upload`

完整启动依赖 `.env` 中的 DashScope API Key、Docker Desktop、Milvus 和两个 MCP 服务。为了面试快速验证，本包提供了不需要外部依赖的离线 demo。

## 4. 本次 AI 增强点

新增 `ai_enhancement/aiops_summary_enhancer.py`。它的定位是 AIOps Agent 的报告后处理层：把 Agent 过程事件和工具观测结果转换成结构化摘要，让面试官不用启动完整外部依赖，也能验证 AI 增强逻辑。

输入：

- `sample_events/cpu_alert_events.json`：模拟 CPU 告警、监控指标和日志证据。
- `sample_events/tool_failure_events.json`：模拟 MCP 工具失败和证据链中断。

输出：

- 影响服务
- 风险等级
- 根因判断
- 关键指标
- 证据列表
- 风险/异常解释
- 自动生成下一步动作
- 工具调用边界

这个增强点对应面试题中的“结构化摘要、风险/异常解释、自动生成下一步动作”。

验证命令：

```powershell
cd <项目根目录>\agent_package
python scripts\run_full_verification.py
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
python -m unittest discover -s tests -p "test_*.py"
```

## 5. 交付物清单

```text
agent_package/
├── README.md
├── INTERVIEWER_QUICK_START.md
├── RUNBOOK_10MIN.md
├── ARCHITECTURE.md
├── KEY_FILES.md
├── AI_COLLABORATION.md
├── TEST_SAMPLES.md
├── DEBUG_RECORD.md
├── RECORDING_OR_SCREENSHOTS.md
├── ai_enhancement/
├── sample_events/
├── sample_requests/
├── scripts/
├── tests/
├── screenshots/
└── verification_logs/
```

## 6. 面试陈述口径

这个项目不是单纯聊天机器人，而是一个面向企业 OnCall 的 Agent 系统。普通问答走 RAG，AIOps 诊断走 LangGraph 的 Plan-Execute-Replan 状态流；工具调用通过 MCP 边界隔离，Agent 只查询知识库、日志和监控，不直接做生产变更。本次补充的 AI 增强模块把诊断过程转成结构化风险摘要，方便面试官在 10 分钟内看到可运行、可测试、可解释的结果。

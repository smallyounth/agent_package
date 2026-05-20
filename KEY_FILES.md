# 关键文件说明

## 可运行代码

| 文件 | 作用 | 验证方式 |
|---|---|---|
| `ai_enhancement/aiops_summary_enhancer.py` | AI 增强点：结构化摘要、风险解释、下一步动作 | `python scripts/run_offline_demo.py` |
| `scripts/run_offline_demo.py` | 单样例离线 demo 入口 | 读取 `sample_events/*.json` 并输出摘要 |
| `scripts/run_full_verification.py` | 一键验证脚本 | 运行两个 demo 和单元测试，写入完整日志 |
| `tests/test_aiops_summary_enhancer.py` | 两条测试样例 | `python -m unittest discover -s tests` |

## 样例数据

| 文件 | 作用 |
|---|---|
| `sample_events/cpu_alert_events.json` | 模拟 CPU 告警、监控指标和日志证据 |
| `sample_events/tool_failure_events.json` | 模拟工具失败和证据链中断 |

## 面试材料

| 文件 | 作用 |
|---|---|
| `INTERVIEWER_QUICK_START.md` | 面试官快速测试命令 |
| `RUNBOOK_10MIN.md` | 10 分钟验证路线 |
| `ARCHITECTURE.md` | 最小可验证架构和 Agent 状态流 |
| `AI_COLLABORATION.md` | AI 协作说明 |
| `TEST_SAMPLES.md` | 样例命令和断言 |
| `DEBUG_RECORD.md` | 真实排错记录 |
| `RECORDING_OR_SCREENSHOTS.md` | 关键截图说明 |
| `SUBMISSION_CHECKLIST.md` | 面试题提交项对照 |

## 本人负责范围

- 设计最小可验证 Agent 项目结构。
- 实现 `AIOpsSummaryEnhancer`，将 Agent 事件转成结构化摘要。
- 编写 CPU 告警和工具失败两类样例。
- 编写一键验证脚本和单元测试。
- 生成运行日志、截图说明、排错记录和面试说明文档。

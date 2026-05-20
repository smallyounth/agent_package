# 面试题提交项对照表

| 题目要求 | 本包对应文件 |
|---|---|
| GitHub/Gitee/代码包或核心目录截图 | `README.md`、`screenshots/01-core-directory.svg` |
| README 和启动方式 | `README.md`、`RUNBOOK_10MIN.md` |
| 面试官快速测试路径和命令 | `INTERVIEWER_QUICK_START.md` |
| 3-5 分钟录屏或关键运行截图 | `RECORDING_OR_SCREENSHOTS.md`、`screenshots/*.svg` |
| AI 协作说明 | `AI_COLLABORATION.md` |
| 关键文件说明 | `KEY_FILES.md` |
| 至少 2 条测试样例或接口调用截图 | `TEST_SAMPLES.md`、`tests/test_aiops_summary_enhancer.py`、`verification_logs/*.txt` |
| 1 条真实排错记录 | `DEBUG_RECORD.md` |
| 项目解决的真实场景 | `README.md`、`ARCHITECTURE.md` |
| Agent 状态流/工具调用边界 | `ARCHITECTURE.md`、`screenshots/04-agent-state-flow.svg` |
| 后端接口或关键模块 | `KEY_FILES.md` |
| 本人负责的文件/接口/配置 | `KEY_FILES.md` |
| AI 相关增强点 | `ai_enhancement/aiops_summary_enhancer.py`、`TEST_SAMPLES.md` |

## 最短验收命令

```powershell
cd <项目根目录>\agent_package
python scripts\run_full_verification.py
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
python -m unittest discover -s tests -p "test_*.py"
```

可选补充验证：

```powershell
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
```

AI 增强点说明：`ai_enhancement/aiops_summary_enhancer.py` 将 AIOps Agent 的过程事件和工具结果转成结构化摘要，自动输出影响服务、风险等级、根因、证据、风险解释和下一步动作。

## 已生成运行证据

```text
verification_logs/offline_demo_cpu.txt
verification_logs/offline_demo_tool_failure.txt
verification_logs/latest_verification.txt
verification_logs/latest_verification_summary.json
verification_logs/unittest.txt
```

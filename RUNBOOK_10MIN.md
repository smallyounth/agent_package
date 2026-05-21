# 10 分钟验证路线

## 0-1 分钟：确认代码包

面试官先 clone 仓库并进入根目录：

```powershell
git clone https://github.com/smallyounth/agent_package.git
cd agent_package
```

这个仓库本身就是独立最小可验证项目，主要提供可运行 AI 增强模块、样例、测试、日志和截图说明。

## 1-3 分钟：跑 AI 增强离线 demo

```powershell
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
```

面试官应看到：

- `affected_services` 包含 `data-sync-service`
- `severity` 为 `P1 - 高风险，需要立即处理`
- `cpu_max_percent` 为 `96.0`
- `next_actions` 自动给出 3 条下一步动作

## 3-5 分钟：跑两条测试样例

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

验证内容：

1. CPU 高使用率样例能生成高风险摘要和下一步动作。
2. 工具失败样例能解释“证据不足/诊断链路异常”。

## 5-7 分钟：看关键代码和工具边界

重点看这些文件：

- `ai_enhancement/aiops_summary_enhancer.py`
- `scripts/run_offline_demo.py`
- `scripts/run_full_verification.py`
- `sample_events/cpu_alert_events.json`
- `sample_events/tool_failure_events.json`

一句话解释：样例事件模拟 Agent 状态流，增强模块负责结构化摘要，验证脚本负责可复现测试。

## 7-9 分钟：看架构和截图材料

打开：

- `ARCHITECTURE.md`
- `KEY_FILES.md`
- `RECORDING_OR_SCREENSHOTS.md`
- `screenshots_and_recording/04-agent-state-flow.svg`

## 9-10 分钟：看排错记录

打开 `DEBUG_RECORD.md`。里面记录了本包开发时真实出现的一次测试失败：CPU 文本被识别，但嵌套指标 `statistics.max=96.0` 没被提取，导致风险等级错误。随后通过修正指标提取的上下文传播逻辑解决，并用两条测试验证。

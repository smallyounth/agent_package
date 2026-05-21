# AIOps Agent Package

这是一个独立的最小可验证 Agent 项目。面试官只需要 Python 环境，不需要准备任何外部服务、历史工程或账号密钥，就可以在 10 分钟内验证核心逻辑。

项目模拟一个真实 OnCall 场景：值班人员收到 `data-sync-service` 告警后，Agent 根据过程事件和工具观测结果，输出结构化摘要、风险解释和下一步动作。

## 快速验证

```powershell
git clone https://github.com/smallyounth/agent_package.git
cd agent_package
python scripts\run_full_verification.py
```

预期输出：

```text
overall_result: PASS
```

完整日志会写入：

```text
verification_logs/latest_verification.txt
verification_logs/latest_verification_summary.json
```

## 单项验证命令

CPU 告警摘要：

```powershell
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
```

工具失败异常解释：

```powershell
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
```

单元测试：

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## AI 增强点

核心模块：

```text
ai_enhancement/aiops_summary_enhancer.py
```

它把 AIOps Agent 的过程事件和工具观测结果转换成结构化摘要，包含：

- 影响服务
- 风险等级
- 根因判断
- 关键指标
- 证据列表
- 风险/异常解释
- 自动生成下一步动作
- 工具调用边界

对应面试题要求中的“结构化摘要、风险/异常解释、自动生成下一步动作”。

## 项目结构

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
├── scripts/
├── tests/
├── screenshots/
└── verification_logs/
```

## 面试陈述口径

这个仓库是从真实 AIOps Agent 落地思路中抽出的最小可验证版本。它保留了 Agent 最关键的状态流、工具边界和 AI 增强点，但把外部系统都替换成可复现的样例事件，方便面试官直接运行、审阅和测试。

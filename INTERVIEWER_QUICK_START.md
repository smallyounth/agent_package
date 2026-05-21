# 面试官快速测试说明

## 测试路径

请进入 GitHub 仓库根目录：

```powershell
git clone https://github.com/smallyounth/agent_package.git
cd agent_package
```

仓库本身就是最小可验证项目，不需要再准备其他工程目录。

## 10 分钟内验证命令

### 一键验证并生成完整日志

```powershell
python scripts\run_full_verification.py
```

预期看到：

```text
overall_result: PASS
log_file: ...\verification_logs\latest_verification.txt
summary_file: ...\verification_logs\latest_verification_summary.json
```

完整日志会记录每条命令、退出码、stdout/stderr 和总结果。

### 1. 验证 AI 增强点：CPU 告警摘要

```powershell
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
```

预期看到：

```text
"severity": "P1 - 高风险，需要立即处理"
"cpu_max_percent": 96.0
"affected_services": ["data-sync-service"]
```

### 2. 验证 AI 增强点：工具失败解释

```powershell
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
```

预期看到：

```text
"root_cause": "诊断证据不足..."
"severity": "P2 - 诊断链路异常，需要先恢复可观测性"
```

### 3. 运行测试

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

预期看到：

```text
Ran 2 tests
OK
```

## AI 增强点说明

新增模块：

```text
ai_enhancement/aiops_summary_enhancer.py
```

它把 AIOps Agent 的过程事件和工具观测结果转成结构化摘要。这个增强点不依赖外部 API，面试官可直接离线运行验证。

输入：

- Agent 状态事件：计划、步骤执行、报告、错误。
- 工具观测结果：CPU/内存指标、日志、工具失败信息。

输出：

- 影响服务
- 风险等级
- 根因判断
- 关键指标
- 证据列表
- 风险/异常解释
- 自动生成下一步动作
- 工具调用边界

对应面试题要求：

```text
结构化摘要 + 风险/异常解释 + 自动生成下一步动作
```

## 依赖说明

只需要 Python 3.10+。本项目不依赖外部服务、模型账号、数据库、后端接口或浏览器页面。

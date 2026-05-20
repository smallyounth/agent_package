# 面试官快速测试说明

## 测试路径

请进入解压后的面试交付包目录：

```powershell
cd <项目根目录>\agent_package
```

示例：

```powershell
cd D:\interview\SuperBizAgent\agent_package
```

其中 `<项目根目录>` 是包含 `agent_package/` 的目录。

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

## 完整项目启动命令

如果面试机器已配置 DashScope API Key、Docker、Milvus 和 MCP 服务，可在项目根目录启动完整服务：

```powershell
cd <项目根目录>
.\start-windows.bat
```

启动后访问：

```text
http://localhost:9900
http://localhost:9900/docs
```

如果没有外部依赖配置，优先使用上面的离线验证命令。

# 测试样例

## 一键验证

```powershell
python scripts\run_full_verification.py
```

预期输出：

```text
overall_result: PASS
```

## 样例 1：CPU 告警摘要

```powershell
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
```

核心断言：

- `affected_services` 包含 `data-sync-service`
- `severity` 是 `P1 - 高风险，需要立即处理`
- `cpu_max_percent` 是 `96.0`
- `next_actions` 包含限流/扩容、日志核对、重试逻辑排查

截图文件：

```text
screenshots/02-ai-enhancement-output.svg
```

## 样例 2：工具失败异常解释

```powershell
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
```

核心断言：

- `root_cause` 包含 `诊断证据不足`
- `severity` 包含 `诊断链路异常`
- `next_actions` 第一条要求检查工具服务和数据源连通性

## 样例 3：单元测试

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

预期输出：

```text
Ran 2 tests
OK
```

截图文件：

```text
screenshots/03-test-output.svg
```

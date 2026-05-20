# 真实排错记录

## 问题

在第一次运行测试时，CPU 告警样例没有被判定为 P1：

```text
FAIL: test_cpu_alert_generates_high_risk_summary_and_actions
AssertionError: False is not true
```

同时离线 demo 输出显示：

```text
"severity": "P4 - 低风险"
"cpu_max_percent": null
```

## 期望

样例中 `query_cpu_metrics` 工具返回：

```json
{
  "metric_name": "cpu_usage_percent",
  "statistics": {
    "max": 96.0,
    "p95": 94.8
  }
}
```

因此摘要应输出：

```text
severity = P1 - 高风险，需要立即处理
cpu_max_percent = 96.0
```

## 根因

`AIOpsSummaryEnhancer._collect_metric_values()` 只在当前字典直接包含 `cpu` 字段时提取 `max`、`p95`、`value`。

真实样例结构是嵌套的：

```text
result.metric_name = cpu_usage_percent
result.statistics.max = 96.0
```

递归进入 `statistics` 后，上下文里已经没有 `cpu` 字符串，所以 `max=96.0` 被忽略。

## 修复

修复方式：递归提取指标时传递 `metric_context`。只要父级字典里出现过 `cpu`，子级的 `max`、`p95`、`value` 就可以作为 CPU 指标候选值。

关键修改位置：

```text
ai_enhancement/aiops_summary_enhancer.py
```

## 验证

重新运行：

```powershell
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
python -m unittest discover -s tests -p "test_*.py"
```

结果：

```text
"severity": "P1 - 高风险，需要立即处理"
"cpu_max_percent": 96.0

Ran 2 tests
OK
```

## 面试可讲点

这条排错能说明三件事：

1. 我不是只做静态文档，而是写了可运行验证。
2. Agent 输出常见问题在于“结构化证据的路径和语义上下文丢失”。
3. 修复时没有硬编码字段路径，而是把指标上下文沿递归传播，能兼容更多工具返回结构。

# 测试样例与接口调用

## 样例 1：离线 CPU 告警摘要

推荐先运行完整验证脚本，它会自动生成完整日志：

```powershell
cd <项目根目录>\agent_package
python scripts\run_full_verification.py
```

命令：

```powershell
cd <项目根目录>\agent_package
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

## 样例 2：离线工具失败异常解释

命令：

```powershell
cd <项目根目录>\agent_package
python scripts\run_offline_demo.py --sample sample_events\tool_failure_events.json
```

核心断言：

- `root_cause` 包含 `诊断证据不足`
- `severity` 包含 `诊断链路异常`
- `next_actions` 第一条要求检查 MCP 服务和数据源连通性

## 样例 3：单元测试

命令：

```powershell
cd <项目根目录>\agent_package
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

## 原项目接口调用样例

完整启动原项目后可调用：

### AIOps 诊断

```powershell
cd <项目根目录>\agent_package
curl -X POST "http://localhost:9900/api/aiops" ^
  -H "Content-Type: application/json" ^
  -d "@sample_requests/aiops_request.json" ^
  --no-buffer
```

### RAG 对话

```powershell
cd <项目根目录>\agent_package
curl -X POST "http://localhost:9900/api/chat" ^
  -H "Content-Type: application/json" ^
  -d "@sample_requests/chat_request.json"
```

### 健康检查

```powershell
curl "http://localhost:9900/health"
```

注意：原项目完整接口依赖 DashScope、Milvus 和 MCP 服务。离线样例用于 10 分钟快速验证，完整接口用于展示真实系统边界。

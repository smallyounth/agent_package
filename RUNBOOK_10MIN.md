# 10 分钟验证路线

## 0-1 分钟：确认代码包

面试官测试路径统一写法：

```text
<项目根目录>\agent_package
```

其中 `<项目根目录>` 是解压后的项目根目录。例如代码包解压到 `D:\interview\SuperBizAgent`，则测试目录是：

```powershell
cd D:\interview\SuperBizAgent\agent_package
```

它是原项目 `SuperBizAgent` 的面试交付包，不修改原核心代码，主要提供可验证说明、AI 增强模块、样例、测试和截图。

## 1-3 分钟：跑 AI 增强离线 demo

```powershell
cd <项目根目录>\agent_package
python scripts\run_offline_demo.py --sample sample_events\cpu_alert_events.json
```

面试官应看到：

- `affected_services` 包含 `data-sync-service`
- `severity` 为 `P1 - 高风险，需要立即处理`
- `cpu_max_percent` 为 `96.0`
- `next_actions` 自动给出 3 条下一步动作

## 3-5 分钟：跑两条测试样例

```powershell
cd <项目根目录>\agent_package
python -m unittest discover -s tests -p "test_*.py"
```

验证内容：

1. CPU 高使用率样例能生成高风险摘要和下一步动作。
2. MCP 工具失败样例能解释“证据不足/诊断链路异常”。

## 5-7 分钟：看原项目接口边界

重点看这些文件：

- `../app/api/aiops.py`
- `../app/services/aiops_service.py`
- `../app/agent/aiops/planner.py`
- `../app/agent/aiops/executor.py`
- `../app/agent/aiops/replanner.py`
- `../app/agent/mcp_client.py`

一句话解释：FastAPI 只暴露接口，LangGraph 管状态流，MCP 管工具边界。

## 7-9 分钟：看完整项目启动方式

如果现场允许配置外部依赖：

```powershell
cd <项目根目录>
.\start-windows.bat
```

然后访问：

- http://localhost:9900
- http://localhost:9900/docs

如果没有 API Key 或 Docker，不影响前 5 分钟的离线验证。

## 9-10 分钟：看排错记录

打开 `DEBUG_RECORD.md`。里面记录了本包开发时真实出现的一次测试失败：CPU 文本被识别，但嵌套指标 `statistics.max=96.0` 没被提取，导致风险等级错误。随后通过修正指标提取的上下文传播逻辑解决，并用两条测试验证。

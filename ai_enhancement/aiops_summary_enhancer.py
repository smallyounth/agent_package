"""AIOps structured summary enhancement.

This module is intentionally self-contained so an interviewer can verify the
AI product idea without configuring model keys, databases, containers, or
external observability services.
It mirrors the production Agent boundary: it only consumes Agent events and
tool observations, then turns them into a structured risk summary and next
actions.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any


SERVICE_PATTERN = re.compile(r"\b[a-z][a-z0-9]+(?:-[a-z0-9]+)+\b")


@dataclass(frozen=True)
class SummaryConfig:
    """Configurable thresholds for the offline verifier."""

    cpu_critical_threshold: float = 90.0
    cpu_warning_threshold: float = 80.0
    memory_warning_threshold: float = 70.0
    max_evidence_items: int = 5


class AIOpsSummaryEnhancer:
    """Generate a structured summary from AIOps Agent execution evidence."""

    def __init__(self, config: SummaryConfig | None = None) -> None:
        self.config = config or SummaryConfig()

    def summarize(self, events: list[dict[str, Any]], original_task: str = "") -> dict[str, Any]:
        """Return a structured summary with risk explanation and next actions."""

        all_text = self._flatten_text(events)
        services = self._extract_services(events, all_text)
        cpu_max = self._extract_metric(events, "cpu", default=0.0)
        memory_max = self._extract_metric(events, "memory", default=0.0)
        tool_errors = self._extract_tool_errors(events, all_text)
        root_cause = self._infer_root_cause(all_text, cpu_max, memory_max, tool_errors)
        severity = self._infer_severity(root_cause, cpu_max, memory_max, tool_errors)
        evidence = self._extract_evidence(events, all_text)

        return {
            "title": "AIOps 结构化诊断摘要",
            "scenario": original_task or "当前系统告警诊断",
            "affected_services": services or ["未从证据中识别到明确服务"],
            "severity": severity,
            "root_cause": root_cause,
            "key_metrics": {
                "cpu_max_percent": cpu_max if cpu_max else None,
                "memory_max_percent": memory_max if memory_max else None,
            },
            "evidence": evidence,
            "risk_explanation": self._explain_risk(root_cause, severity, tool_errors),
            "next_actions": self._next_actions(root_cause, tool_errors),
            "tool_call_boundary": self.tool_boundary(),
            "verification_hint": "Run scripts/run_offline_demo.py and tests/test_aiops_summary_enhancer.py.",
        }

    @staticmethod
    def tool_boundary() -> list[str]:
        """Describe what the Agent is allowed to do."""

        return [
            "只通过工具读取知识库、日志和监控数据，不直接登录机器。",
            "查询工具只负责读取证据；重启、扩容、回滚等变更动作必须人工确认。",
            "报告必须引用工具证据；证据不足时输出不确定性和补查动作。",
        ]

    def format_markdown(self, summary: dict[str, Any]) -> str:
        """Render a summary as concise Markdown."""

        evidence = "\n".join(f"- {item}" for item in summary.get("evidence", []))
        actions = "\n".join(f"{idx}. {item}" for idx, item in enumerate(summary["next_actions"], 1))
        boundaries = "\n".join(f"- {item}" for item in summary["tool_call_boundary"])
        metrics = summary.get("key_metrics", {})

        return (
            f"# {summary['title']}\n\n"
            f"## 场景\n{summary['scenario']}\n\n"
            f"## 影响范围\n{', '.join(summary['affected_services'])}\n\n"
            f"## 风险等级\n{summary['severity']}\n\n"
            f"## 根因判断\n{summary['root_cause']}\n\n"
            f"## 关键指标\n"
            f"- CPU 峰值: {metrics.get('cpu_max_percent') or '未获取'}\n"
            f"- 内存峰值: {metrics.get('memory_max_percent') or '未获取'}\n\n"
            f"## 证据\n{evidence or '- 暂无'}\n\n"
            f"## 风险解释\n{summary['risk_explanation']}\n\n"
            f"## 下一步动作\n{actions}\n\n"
            f"## 工具调用边界\n{boundaries}\n"
        )

    def _infer_root_cause(
        self,
        text: str,
        cpu_max: float,
        memory_max: float,
        tool_errors: list[str],
    ) -> str:
        lowered = text.lower()
        if tool_errors and not cpu_max and not memory_max:
            return "诊断证据不足：关键工具调用失败，需要先恢复日志或监控查询链路。"
        if cpu_max >= self.config.cpu_warning_threshold or "cpu" in lowered:
            if "timeout" in lowered or "超时" in text:
                return "CPU 使用率过高导致任务处理超时，疑似数据同步工作线程被计算或重试逻辑拖慢。"
            return "CPU 使用率持续高位，服务存在计算资源瓶颈或异常循环风险。"
        if memory_max >= self.config.memory_warning_threshold or "memory" in lowered or "内存" in text:
            return "内存使用率过高，可能存在缓存膨胀、对象堆积或内存泄漏。"
        if "error" in lowered or "exception" in lowered or "异常" in text:
            return "日志中存在异常，需要结合调用链和监控指标继续定位。"
        return "未发现单一明确根因，当前信息更像健康巡检或低风险告警。"

    def _infer_severity(
        self,
        root_cause: str,
        cpu_max: float,
        memory_max: float,
        tool_errors: list[str],
    ) -> str:
        if cpu_max >= self.config.cpu_critical_threshold:
            return "P1 - 高风险，需要立即处理"
        if cpu_max >= self.config.cpu_warning_threshold or memory_max >= self.config.memory_warning_threshold:
            return "P2 - 中高风险，需要本班次处理"
        if tool_errors:
            return "P2 - 诊断链路异常，需要先恢复可观测性"
        if "异常" in root_cause:
            return "P3 - 需要继续观察和补证据"
        return "P4 - 低风险"

    def _explain_risk(self, root_cause: str, severity: str, tool_errors: list[str]) -> str:
        if tool_errors:
            return (
                f"{severity}。当前最大风险不是业务结论本身，而是证据链不完整："
                f"{'; '.join(tool_errors[:2])}。需要先恢复工具查询再下结论。"
            )
        if "CPU" in root_cause:
            return f"{severity}。CPU 高位会放大请求排队、任务超时和重试风暴，可能进一步拖慢下游依赖。"
        if "内存" in root_cause:
            return f"{severity}。内存压力会增加 GC、OOM 和容器重启风险，影响服务稳定性。"
        return f"{severity}。当前证据不足以支持高危判断，建议继续补充日志和监控证据。"

    def _next_actions(self, root_cause: str, tool_errors: list[str]) -> list[str]:
        if tool_errors:
            return [
                "先检查观测工具和监控/日志数据源连通性。",
                "重试失败工具，并记录失败参数和错误信息。",
                "如果工具恢复后仍无数据，再升级给可观测性平台负责人。",
            ]
        if "CPU" in root_cause:
            return [
                "确认高 CPU 进程和最近 15 分钟错误日志是否集中在同一服务。",
                "临时限流或扩容 data-sync-service，避免重试继续放大负载。",
                "排查同步任务是否存在重试间隔过短、死循环或大批量数据扫描。",
            ]
        if "内存" in root_cause:
            return [
                "导出堆或进程内存摘要，确认对象增长来源。",
                "检查缓存大小、批处理窗口和大文件加载逻辑。",
                "必要时先滚动重启受影响实例，并保留现场证据。",
            ]
        return [
            "补查最近 30 分钟错误日志和服务指标。",
            "对比历史工单，确认是否为重复故障模式。",
            "如果没有新的异常证据，将告警降级为观察项。",
        ]

    def _extract_services(self, events: list[dict[str, Any]], text: str) -> list[str]:
        services: set[str] = set()
        for event in events:
            service_name = self._find_key(event, "service_name")
            if isinstance(service_name, str):
                services.add(service_name)
        services.update(SERVICE_PATTERN.findall(text))
        return sorted(services)

    def _extract_metric(self, events: list[dict[str, Any]], metric: str, default: float) -> float:
        candidates: list[float] = []
        for event in events:
            self._collect_metric_values(event, metric, candidates)
        return max(candidates) if candidates else default

    def _collect_metric_values(
        self,
        value: Any,
        metric: str,
        candidates: list[float],
        metric_context: bool = False,
    ) -> None:
        if isinstance(value, dict):
            current_context = metric_context or self._dict_context_mentions(value, metric)
            for key, nested in value.items():
                key_lower = str(key).lower()
                if metric in key_lower and isinstance(nested, (int, float)):
                    candidates.append(float(nested))
                elif key_lower in {"max", "p95", "value"} and current_context:
                    if isinstance(nested, (int, float)):
                        candidates.append(float(nested))
                self._collect_metric_values(nested, metric, candidates, current_context)
        elif isinstance(value, list):
            for item in value:
                self._collect_metric_values(item, metric, candidates, metric_context)

    @staticmethod
    def _dict_context_mentions(value: dict[str, Any], metric: str) -> bool:
        try:
            return metric in json.dumps(value, ensure_ascii=False).lower()
        except TypeError:
            return False

    def _extract_tool_errors(self, events: list[dict[str, Any]], text: str) -> list[str]:
        errors: list[str] = []
        for event in events:
            if event.get("type") == "error" or event.get("isError") is True:
                errors.append(str(event.get("message") or event.get("data") or event))
        lowered = text.lower()
        if "tool" in lowered and ("failed" in lowered or "失败" in text):
            errors.append("工具调用失败或返回错误")
        return errors

    def _extract_evidence(self, events: list[dict[str, Any]], text: str) -> list[str]:
        evidence: list[str] = []
        for event in events:
            event_type = event.get("type", "event")
            if event_type in {"plan", "status"}:
                continue
            line = self._event_to_evidence(event)
            if line:
                evidence.append(line)
            if len(evidence) >= self.config.max_evidence_items:
                return evidence
        if not evidence and text.strip():
            evidence.append(text[:180])
        return evidence[: self.config.max_evidence_items]

    def _event_to_evidence(self, event: dict[str, Any]) -> str:
        for key in ("current_step", "message", "report", "result", "data"):
            value = event.get(key)
            if not value:
                continue
            if isinstance(value, str):
                return value[:220]
            return json.dumps(value, ensure_ascii=False)[:220]
        return ""

    def _flatten_text(self, value: Any) -> str:
        parts: list[str] = []
        self._collect_text(value, parts)
        return "\n".join(parts)

    def _collect_text(self, value: Any, parts: list[str]) -> None:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            for nested in value.values():
                self._collect_text(nested, parts)
        elif isinstance(value, list):
            for item in value:
                self._collect_text(item, parts)

    def _find_key(self, value: Any, target: str) -> Any:
        if isinstance(value, dict):
            if target in value:
                return value[target]
            for nested in value.values():
                found = self._find_key(nested, target)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for item in value:
                found = self._find_key(item, target)
                if found is not None:
                    return found
        return None

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from ai_enhancement import AIOpsSummaryEnhancer  # noqa: E402


class AIOpsSummaryEnhancerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.enhancer = AIOpsSummaryEnhancer()

    def load_sample(self, name: str) -> list[dict]:
        path = PACKAGE_ROOT / "sample_events" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_cpu_alert_generates_high_risk_summary_and_actions(self) -> None:
        summary = self.enhancer.summarize(self.load_sample("cpu_alert_events.json"))

        self.assertIn("data-sync-service", summary["affected_services"])
        self.assertTrue(summary["severity"].startswith("P1"))
        self.assertIn("CPU", summary["root_cause"])
        self.assertGreaterEqual(summary["key_metrics"]["cpu_max_percent"], 90)
        self.assertGreaterEqual(len(summary["next_actions"]), 3)

    def test_tool_failure_explains_observability_gap(self) -> None:
        summary = self.enhancer.summarize(self.load_sample("tool_failure_events.json"))

        self.assertIn("证据不足", summary["root_cause"])
        self.assertIn("诊断链路异常", summary["severity"])
        self.assertIn("MCP", summary["next_actions"][0])
        self.assertIn("工具", summary["risk_explanation"])


if __name__ == "__main__":
    unittest.main()

"""Run the interview-ready AIOps summary demo.

Usage:
    python scripts/run_offline_demo.py --sample sample_events/cpu_alert_events.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from ai_enhancement import AIOpsSummaryEnhancer  # noqa: E402


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Offline AIOps structured summary demo")
    parser.add_argument(
        "--sample",
        default="sample_events/cpu_alert_events.json",
        help="Path to sample event JSON, relative to the package root unless absolute.",
    )
    parser.add_argument("--json-only", action="store_true", help="Only print JSON output.")
    args = parser.parse_args()

    sample_path = Path(args.sample)
    if not sample_path.is_absolute():
        sample_path = PACKAGE_ROOT / sample_path

    events = json.loads(sample_path.read_text(encoding="utf-8"))
    enhancer = AIOpsSummaryEnhancer()
    summary = enhancer.summarize(
        events,
        original_task="诊断 data-sync-service 当前是否存在告警，并给出根因、风险和下一步动作。",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not args.json_only:
        print("\n--- Markdown Preview ---\n")
        print(enhancer.format_markdown(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

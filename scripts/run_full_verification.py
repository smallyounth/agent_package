"""Run all interviewer verification checks and write an explicit log.

Usage:
    python scripts/run_full_verification.py
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import time


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PACKAGE_ROOT / "verification_logs"
LATEST_LOG = LOG_DIR / "latest_verification.txt"
SUMMARY_JSON = LOG_DIR / "latest_verification_summary.json"


def run_command(name: str, args: list[str]) -> dict[str, object]:
    """Run one command and return structured execution evidence."""

    start = time.perf_counter()
    completed = subprocess.run(
        args,
        cwd=PACKAGE_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    duration = round(time.perf_counter() - start, 3)

    display_command = " ".join("python" if arg == sys.executable else arg for arg in args)

    return {
        "name": name,
        "command": display_command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_log(results: list[dict[str, object]]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    passed = all(result["exit_code"] == 0 for result in results)

    lines: list[str] = [
        "SuperBizAgent Interview Verification Log",
        f"generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"package_root: <项目根目录>\\agent_package",
        "python: python on PATH",
        f"overall_result: {'PASS' if passed else 'FAIL'}",
        "",
    ]

    for index, result in enumerate(results, 1):
        lines.extend(
            [
                f"## Check {index}: {result['name']}",
                f"command: {result['command']}",
                f"exit_code: {result['exit_code']}",
                f"duration_seconds: {result['duration_seconds']}",
                "",
                "[stdout]",
                str(result["stdout"]).rstrip() or "<empty>",
                "",
                "[stderr]",
                str(result["stderr"]).rstrip() or "<empty>",
                "",
            ]
        )

    LATEST_LOG.write_text("\n".join(lines), encoding="utf-8")
    SUMMARY_JSON.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "overall_result": "PASS" if passed else "FAIL",
                "checks": [
                    {
                        "name": result["name"],
                        "command": result["command"],
                        "exit_code": result["exit_code"],
                        "duration_seconds": result["duration_seconds"],
                    }
                    for result in results
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    commands = [
        (
            "AI enhancement CPU alert demo",
            [
                sys.executable,
                "scripts/run_offline_demo.py",
                "--sample",
                "sample_events/cpu_alert_events.json",
                "--json-only",
            ],
        ),
        (
            "AI enhancement tool failure demo",
            [
                sys.executable,
                "scripts/run_offline_demo.py",
                "--sample",
                "sample_events/tool_failure_events.json",
                "--json-only",
            ],
        ),
        (
            "Unit tests",
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        ),
    ]

    results = [run_command(name, args) for name, args in commands]
    write_log(results)

    passed = all(result["exit_code"] == 0 for result in results)
    print(f"overall_result: {'PASS' if passed else 'FAIL'}")
    print(f"log_file: {LATEST_LOG}")
    print(f"summary_file: {SUMMARY_JSON}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

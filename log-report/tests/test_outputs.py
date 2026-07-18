import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    """Independently recompute expected values from access.log (not the
    agent's own logic), used as ground truth by the criterion tests below."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_criterion_1_report_exists_and_is_valid_json():
    """instruction.md criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_criterion_2_total_requests_matches():
    """instruction.md criterion 2: total_requests matches the number of
    non-empty lines in the log."""
    expected = _expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("total_requests") == expected["total_requests"], (
        f"total_requests mismatch: got {data.get('total_requests')!r}, "
        f"expected {expected['total_requests']}"
    )


def test_criterion_3_unique_ips_matches():
    """instruction.md criterion 3: unique_ips matches the number of distinct
    client IPs in the log."""
    expected = _expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips mismatch: got {data.get('unique_ips')!r}, "
        f"expected {expected['unique_ips']}"
    )


def test_criterion_4_top_path_matches():
    """instruction.md criterion 4: top_path matches the single most-requested
    path in the log."""
    expected = _expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("top_path") == expected["top_path"], (
        f"top_path mismatch: got {data.get('top_path')!r}, "
        f"expected {expected['top_path']!r}"
    )
import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
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


def test_report_exists():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"


def test_report_matches_expected():
    expected = _expected()
    data = json.loads(REPORT_PATH.read_text())
    assert data.get("total_requests") == expected["total_requests"], (
        f"total_requests mismatch: got {data.get('total_requests')!r}, "
        f"expected {expected['total_requests']}"
    )
    assert data.get("unique_ips") == expected["unique_ips"], (
        f"unique_ips mismatch: got {data.get('unique_ips')!r}, "
        f"expected {expected['unique_ips']}"
    )
    assert data.get("top_path") == expected["top_path"], (
        f"top_path mismatch: got {data.get('top_path')!r}, "
        f"expected {expected['top_path']!r}"
    )
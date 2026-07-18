There is an access log at `/app/access.log`.

Analyze it and write a JSON summary report to `/app/report.json` with
these exact fields:

- `total_requests` (integer) — total number of request lines in the log.
- `unique_ips` (integer) — number of distinct client IP addresses.
- `top_path` (string) — the most frequently requested path.

**Success criteria**

1. `/app/report.json` exists and contains valid JSON.
2. `total_requests` matches the number of non-empty lines in the log.
3. `unique_ips` matches the number of distinct client IPs in the log.
4. `top_path` matches the single most-requested path in the log.

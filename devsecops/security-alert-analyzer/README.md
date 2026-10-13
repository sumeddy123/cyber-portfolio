# Security Alert Analyzer

An offline Python CLI for investigating repeated failed logins and a successful login following repeated failures. It reads normalized JSON Lines rather than relying on a particular vendor's log format. Only the Python standard library is required.

## Run from the repository root

```bash
python devsecops/security-alert-analyzer/analyzer.py devsecops/security-alert-analyzer/sample_events.jsonl --output reports/alerts.json
python -m unittest discover -s devsecops/security-alert-analyzer -v
```

Expected: **12 events, 3 alerts**. See [example_report.json](example_report.json) for reproducible output. `--threshold 5 --window-seconds 300` are defaults.

## Input schema

One object per line; blank lines are ignored:

```json
{"timestamp":"2026-01-01T12:00:00Z","source_ip":"192.0.2.10","username":"demo","outcome":"failure"}
```

`timestamp` must include a timezone; timestamps are normalized to UTC. IPv4 and IPv6 are supported. `outcome` must be `failure` or `success`. Usernames must be nonblank strings with at most 128 characters. Invalid input fails with a line number and exit code 2. The CLI writes no partial report for invalid input. Exit code 0 means processing succeeded, including when alerts exist.

## Rules

- **repeated_failed_logins:** At least N failures from one IP within an inclusive sliding window of W seconds. Accounts are combined to detect a burst across usernames. Rate-limited to one such alert per IP per W seconds; counts are snapshots at alert time.
- **success_after_repeated_failures:** A success from the same IP and account after at least N failures for that account within W seconds. A success consumes that account's failure history to prevent duplicate alerts.

Events are sorted chronologically. Equal timestamps preserve input order. Failures exactly W seconds old count; older failures expire. The JSON report contains rule, severity, source IP, account names, timestamps, and failure counts.

## Investigation and limitations

Shared IPs, NAT, user mistakes, and automated tests can cause false positives. A success is not proof of compromise. Compare with device, identity, MFA, and endpoint evidence. Slow attacks, distributed attacks, and successes from another IP may be missed. No accounts are blocked and no network requests are made.

This batch tool sorts and stores the input in memory. It is for small lab datasets, not unbounded production ingestion. It does not deduplicate identical records or normalize case in usernames. Only use sanitized logs; reports retain account and IP information. Sample IPs are documentation addresses and the events are fictional.

## Design and tests

A deque holds recent failures per source IP. Sorting costs O(n log n); window eviction is amortized linear, while per-success account filtering can cost O(k) for the current window. Tests cover threshold boundaries, timestamps outside the window, unsorted input, source/account isolation, cooldown, repeated successes, malformed records, and CLI output.

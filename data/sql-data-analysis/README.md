# SQL security analytics

An in-memory SQLite investigation demo built around synthetic authentication events. No credentials, external services, or database server required.

```bash
python data/sql-data-analysis/analyze.py
python data/sql-data-analysis/analyze.py --threshold 4
python -m unittest discover -s data/sql-data-analysis -v
```

Run from the repository root. `schema.sql` defines users and login events with foreign keys, an outcome constraint, and an index. `sample.sql` inserts three fictional users and six events. `queries.sql` contains the actual queries executed by the Python runner.

## Findings from the included fixture

- alex: 4 events, 3 failures; sam: 2 events, 1 failure; riley: no events.
- At threshold 3, `192.0.2.10` is the only flagged source, with 3 failures.
- At threshold 4, no sources are flagged.

## Design choices

The account summary uses LEFT JOIN to retain users without events. COUNT(event.id) avoids counting an unmatched user as an event. Conditional aggregation counts only failures. The threshold is passed as a bound parameter, rather than interpolated into SQL.

This query counts failures across the complete fixture, not a rolling time window. Shared IP addresses and ordinary typing mistakes can cause false positives. See the authentication alert analyzer for time-window correlation. The database is recreated for each run, so demonstrations are repeatable and never overwrite a persistent database.

Next exercise: add a date-range filter with bound parameters and test events at both boundaries.

# Failed Login Detector

A small Python **practice utility** for parsing Linux-style SSH authentication logs and flagging IP addresses with repeated failed login attempts.

## Concepts Practiced

- Log parsing
- Regular expressions
- Python file handling
- Counters and dictionaries
- Threshold-based alert logic
- Basic brute-force detection concepts

## Run

```bash
python detector.py sample_auth.log
```

Use a custom threshold:

```bash
python detector.py sample_auth.log 5
```

## Next Improvements

- Add timestamp-based rate detection
- Export alerts to JSON or CSV
- Correlate failed and successful logins
- Test against logs generated from my own VM

> This is a practice project that I am using to strengthen Python and security-monitoring fundamentals.

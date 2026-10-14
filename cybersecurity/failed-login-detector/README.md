# SSH failure counter

An offline parser for Linux-style `Failed password ... from <IP>` lines. Counts valid source addresses, normalizes IPv6, flags a configurable threshold, and exports JSON. The bundled log is synthetic.

```bash
python cybersecurity/failed-login-detector/detector.py
python cybersecurity/failed-login-detector/detector.py cybersecurity/failed-login-detector/sample_auth.log 5 --output reports/ssh.json
python -m unittest discover -s cybersecurity/failed-login-detector -v
```

The JSON contains counts, suspicious addresses, total valid failures, and an invalid-address counter. The threshold must be positive. Invalid addresses are skipped and counted; unrelated log lines are ignored. Missing files and invalid CLI arguments produce nonzero exits.

This is a whole-file counter, not a time-based brute-force detector. It does not resolve hostnames or block traffic, and supports this SSH message pattern only. See [the alert analyzer](../../devsecops/security-alert-analyzer/) for sliding windows and successful-login correlation.

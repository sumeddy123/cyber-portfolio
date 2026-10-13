# DevSecOps portfolio labs

Three connected, runnable learning projects: validate authentication events in a small API, package it in a restricted container, and run automated checks before accepting code changes. An offline analyzer turns synthetic authentication events into investigation leads.

| Project | Implementation | Start here |
| --- | --- | --- |
| Automated Security Pipeline | GitHub Actions, Bandit, pip-audit, Trivy, downloadable reports | [Pipeline guide](automated-security-pipeline/README.md) |
| Container Security Lab | Flask API, Gunicorn, non-root Docker image, read-only runtime | [Container guide](container-security-lab/README.md) |
| Security Alert Analyzer | Python CLI, sliding time windows, IPv4/IPv6, JSON reports | [Analyzer guide](security-alert-analyzer/README.md) |

These are educational portfolio implementations created with AI assistance. Sample events are synthetic. They do not represent a production deployment, a real incident investigation, or employer work. Run, inspect, and modify the code before presenting it as personal hands-on experience.

## Quick start

Requires Python 3.12. Run from the repository root. On Windows, use `py -3.12` in place of `python` if needed.

```bash
python devsecops/security-alert-analyzer/analyzer.py devsecops/security-alert-analyzer/sample_events.jsonl
python -m unittest discover -s devsecops/security-alert-analyzer -v
```

The sample processes 12 events and returns 3 alerts. No dependencies are required for the analyzer.

For the API:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r devsecops/container-security-lab/requirements.txt
python -m unittest discover -s devsecops/container-security-lab -v
python -m flask --app devsecops/container-security-lab/app.py run --host 127.0.0.1 --port 8080
```

The Flask command is a local development server. Docker uses Gunicorn instead. Open `http://127.0.0.1:8080/health`.

## What to understand before an interview

- **CI:** The workflow automatically tests and scans changed code. This lab does not deploy an application to production.
- **SAST:** Bandit inspects Python code for risky patterns; it cannot prove the application is secure.
- **Dependency scanning:** pip-audit compares installed package versions with published vulnerability advisories.
- **Secret scanning:** Trivy checks files for recognizable secret patterns. This workflow scans the current `devsecops` directory, not Git history.
- **Container hardening:** A non-root user, read-only filesystem, removed capabilities, and resource limits restrict runtime behavior.
- **Detection logic:** A time-window threshold is an investigation signal, not proof of an attack.

## Validation

The initial implementation passed 17 local unit tests and a Bandit source scan. The analyzer's example output is generated from the included fixture. Runtime dependency audit results and Docker/Trivy results are available in GitHub Actions; advisory databases and base images change over time. Consult the actual run status rather than treating any scan as a permanent clean bill of health.

## Next hands-on exercises

1. Change the analyzer threshold and explain which sample alerts disappear.
2. Add a new API validation test, then implement the change.
3. Run the container and attempt to write to `/app` and `/tmp`; explain the difference.
4. Inspect the Actions reports and describe how you would investigate and fix a finding.

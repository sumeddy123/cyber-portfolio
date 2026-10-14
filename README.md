# Sumedh Machhi · Cybersecurity & DevSecOps Portfolio

Cyber Security Engineering student focused on Python automation, security monitoring, and reliable software delivery.

[![DevSecOps labs](https://github.com/sumeddy123/cyber-portfolio/actions/workflows/devsecops.yml/badge.svg)](https://github.com/sumeddy123/cyber-portfolio/actions/workflows/devsecops.yml)

## Start with the code

| Project | What it demonstrates | Evidence |
| --- | --- | --- |
| [Security pipeline](devsecops/automated-security-pipeline/) | GitHub Actions, SAST, dependency and secret scans, container checks | [Workflow and reports](https://github.com/sumeddy123/cyber-portfolio/actions/workflows/devsecops.yml) |
| [Container API](devsecops/container-security-lab/) | Flask validation, non-root Docker, restricted runtime | API tests, Dockerfile, Compose configuration |
| [Authentication alert analyzer](devsecops/security-alert-analyzer/) | Sliding-window detection and failure/success correlation | Synthetic events, example JSON, boundary tests |
| [Vulnerability report analyzer](cybersecurity/vulnerability-report-analyzer/) | CSV validation, severity prioritization, host summaries | Runnable fixture and malformed-input tests |
| [SQL security analytics](data/sql-data-analysis/) | Relational schema, LEFT JOIN, aggregation, parameter binding | SQLite demo and constraint tests |
| [Binary search tree](programming/data-structures/) | Iterative insertion, search, ordered traversal | Duplicate, empty, invalid-input and skewed-tree tests |
| [SSH failure counter](cybersecurity/failed-login-detector/) | Log parsing, IPv4/IPv6 normalization, JSON output | Synthetic log and parser tests |

## Run in two minutes

Requires Python 3.12+. From the repository root, no packages are needed for these commands:

```bash
python scripts/verify.py
python data/sql-data-analysis/analyze.py
python programming/data-structures/bst.py
python cybersecurity/vulnerability-report-analyzer/analyze_vulns.py
python cybersecurity/failed-login-detector/detector.py
python devsecops/security-alert-analyzer/analyzer.py devsecops/security-alert-analyzer/sample_events.jsonl
```

For the API, create a virtual environment, install its dependencies, then include its tests:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r devsecops/container-security-lab/requirements.txt
python scripts/verify.py --with-api
```

See the [DevSecOps guide](devsecops/) for Docker and API commands, and the [project walkthrough](docs/project-walkthrough.md) for design decisions and hands-on exercises.

## Background and ongoing learning

[Azure & Defender lab notes](cybersecurity/azure-defender-lab/) · [Engineering coursework](engineering/study-assistant-robot/) · [Security+ preparation](security-plus/)

These sections contain learning notes; the table above points to executable implementations. Samples are synthetic. These educational projects were developed with AI assistance and do not represent employer work or production deployments. CI badges reflect the current run status, not a guarantee that software is vulnerability-free.

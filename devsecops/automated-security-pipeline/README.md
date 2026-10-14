# Automated Security Pipeline

The executable pipeline is [`.github/workflows/devsecops.yml`](../../../.github/workflows/devsecops.yml). It tests all executable portfolio projects on pushes to main, pull requests, and manual Actions runs.

## Stages and gates

| Job / check | Purpose | Failure behavior |
| --- | --- | --- |
| Portfolio unit tests | Verify detection and validation behavior | Fail on test failure |
| Bandit | Scan application Python for risky patterns | Fail on detected findings |
| pip-audit | Check pinned runtime packages against advisories | Fail on known vulnerabilities |
| Trivy filesystem scan | Detect recognizable secrets in current repository files | Fail on a secret finding |
| Docker build and smoke test | Check health, non-root UID, and restricted writes | Fail on build/runtime assertion failure |
| Trivy image scan | Scan OS and language packages | Fail on HIGH/CRITICAL findings, including unfixed |
| Report upload | Retain reports for investigation | Runs even after failures; artifacts retained 14 days |

Security checks use read-only repository permissions, SHA-pinned actions, bounded job timeouts, and no deployment credentials. Checkout does not persist credentials. No images are published and nothing is deployed. Workflow failures do not themselves enforce branch protection; required status checks must be configured separately.

## Use on GitHub

Open the repository's **Actions → DevSecOps labs** page. Inspect the `code-security` and `container-security` jobs. Download the `code-security-reports` and `container-security-reports` artifacts from a completed run. GitHub may require enabling Actions in repository settings if execution is disabled.

## Reproduce Python scans locally

From the repository root inside a Python 3.12 virtual environment:

```bash
python -m pip install -r devsecops/container-security-lab/requirements.txt
python -m pip install -r devsecops/automated-security-pipeline/requirements-tools.txt
bandit -r devsecops cybersecurity data programming -x test_app.py,test_analyzer.py,test_detector.py,test_vulns.py,test_sql.py,test_bst.py
pip-audit -r devsecops/container-security-lab/requirements.txt --no-deps --disable-pip
```

Runtime requirements include the resolved transitive packages. Audit scans exactly that set; update the full set together when dependencies change. Tool top-level versions are pinned, but their transitive dependencies are not fully locked. The image base tag is also mutable. Full hash locks and a maintained base digest are useful next steps.

Trivy needs network access for its databases. Dependency auditing sends package names and versions to the advisory service. Secret scanning covers the current repository working tree, excluding `.git` and `.venv`; it does not scan repository history or remote systems.

## Interpreting a failure

1. Open the failing step and its JSON report.
2. Identify the affected file or installed package and the cited rule/advisory.
3. Determine whether the finding is relevant; remediate with a safe code or dependency change.
4. Rerun the tests and scan. Document any narrowly scoped exception with a reason and expiry rather than suppressing whole checks.

Scanners have false positives and blind spots. Passing checks demonstrate only what these tools tested at run time.

## References

- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [Bandit](https://bandit.readthedocs.io/)
- [pip-audit](https://github.com/pypa/pip-audit)
- [Trivy Action](https://github.com/aquasecurity/trivy-action)
- [Flask package](https://pypi.org/project/Flask/3.1.3/)
- [Gunicorn package](https://pypi.org/project/gunicorn/26.2.0/)

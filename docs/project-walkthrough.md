# Project walkthrough and practice guide

Use these exercises to develop an explanation backed by something you ran and changed.

| Project | Trace through the code | Try a change | Explain the tradeoff |
| --- | --- | --- | --- |
| Authentication analyzer | load_events → analyze → JSON report | Change the threshold from 5 to 6 | Sensitivity versus noisy alerts; same-account success correlation |
| Container API | create_app → validate_event → security_headers | Add a regression test for a bad field | Validation does not provide authentication or authorization |
| Security pipeline | tests → scans → uploaded reports | Inspect a failed gate and its report | A passing scan is limited by rules and advisory data |
| Vulnerability utility | CSV schema validation → severity sorting | Add one synthetic Critical finding | Severity is only one prioritization factor |
| SQL analytics | schema → sample inserts → named queries | Change threshold from 3 to 4 | Whole-dataset counts versus time-window detection |
| Binary tree | insert → contains → inorder | Insert sorted versus mixed values | Unbalanced trees can become linear |

## Review routine

1. Run `python scripts/verify.py` and read a test that checks an edge case.
2. Run a demo and predict the output before looking at the result.
3. Make a small behavior change, add a relevant test, and explain why it matters.
4. Inspect `git diff` before committing. Record what you changed and verified.

## DevSecOps talking points

CI automatically runs checks on changes. This repository's pipeline is CI with security checks; it does not deploy to production. Bandit checks Python patterns, pip-audit checks dependency advisories, and Trivy scans for secrets and image vulnerabilities. These tools cover different failure modes.

The Docker configuration limits privileges and writable locations. A non-root user reduces privileges inside the container; read-only filesystems and dropped capabilities add separate restrictions. These controls do not replace application security.

## Scope and attribution

These projects use synthetic data and AI-assisted implementation. Describe your own work precisely: what you ran, modified, debugged, or investigated. Do not turn sample counts into real incident metrics or describe the labs as employer deployments. The code and tests are available for review; practical understanding comes from working through them.

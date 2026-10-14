"""Run isolated test suites from any working directory; exit nonzero on failure."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    'cybersecurity/failed-login-detector',
    'cybersecurity/vulnerability-report-analyzer',
    'devsecops/security-alert-analyzer',
    'data/sql-data-analysis',
    'programming/data-structures',
]
if '--with-api' in sys.argv:
    SUITES.append('devsecops/container-security-lab')
failed = []
for suite in SUITES:
    print(f'\nTesting {suite}', flush=True)
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', suite, '-v'],
                            cwd=ROOT, check=False)
    if result.returncode:
        failed.append(suite)
print('\nFailed suites: ' + ', '.join(failed) if failed else '\nAll selected suites passed.')
sys.exit(bool(failed))

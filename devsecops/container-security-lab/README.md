# Container Security Lab

A stateless Flask API served by Gunicorn in a non-root Docker container. The API validates the same event schema used by the log analyzer, but does not store logs or perform detection itself.

## Docker quick start

Install Docker with Compose, then run from this directory:

```bash
docker compose up --build -d
curl http://127.0.0.1:8080/health
docker compose exec api id
docker compose exec api touch /app/blocked
# Expected: read-only filesystem or permission denied.
docker compose down
```

`GET /health` returns `{"status":"ok"}`. The container runs as UID/GID 10001. Port 8080 is published only to localhost.

```bash
curl -X POST http://127.0.0.1:8080/validate-event \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2026-01-01T12:00:00Z","source_ip":"192.0.2.10","username":"demo","outcome":"failure"}'
```

Expected response: `{"valid":true}`. Invalid fields or malformed JSON return 400, wrong content type returns 415, and bodies over 16 KiB return 413. The API sends restrictive browser headers and does not echo event data.

## Controls

| Control | Where | Purpose |
| --- | --- | --- |
| UID/GID 10001 | Dockerfile | Run application without root |
| Read-only root filesystem | Compose / CI | Prevent writes to application and system files |
| Writable, bounded `/tmp` | Compose / CI | Allow Gunicorn worker temporary files |
| Drop all Linux capabilities | Compose / CI | Remove unnecessary process privileges |
| No new privileges | Compose / CI | Block gaining privileges through exec |
| CPU, memory and PID limits | Compose / CI | Bound resource consumption |
| Localhost port publishing | Compose / CI | Keep the lab off the public interface |
| Minimal build context | .dockerignore | Exclude local files and credentials |
| Pinned Python dependencies | requirements.txt | Record resolved package versions |
| Health check | Dockerfile | Check the process can serve requests |

Runtime controls are supplied by Compose or `docker run`; the image alone does not enforce all of them. Source files remain root-owned and readable by the app user. The Python base tag intentionally tracks updates; it is not digest-pinned, so rebuilds may change. For a reproducible deployment, pin an inspected digest and maintain a deliberate update process.

## Scan

With Trivy installed:

```bash
docker build --pull -t portfolio-api:local .
trivy image --scanners vuln --severity HIGH,CRITICAL --exit-code 1 portfolio-api:local
```

CI runs the same class of scan and uploads a JSON report. It includes unfixed findings. A failing scan is a result to investigate, not a reason to silently disable the gate.

## Local tests without Docker

From the repository root, install `requirements.txt` in a virtual environment and run:

```bash
python -m unittest discover -s devsecops/container-security-lab -v
```

See the parent guide for Windows-compatible Flask development commands. Gunicorn is intended for Unix-like systems; use Docker on Windows for the container workflow.

## Scope

This is a lab API, not a production service. It has no authentication, rate limiter, TLS termination, persistent store, or external integrations. Keep it on localhost. Before deployment those requirements need a separate design and testing effort. The test suite covers validation, body limits, error responses, methods, IPv6, and response headers.

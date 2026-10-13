# Docker + GitHub Actions Pipeline

A small Flask service with a CI/CD pipeline that lints, tests, builds a container, smoke-tests it,
and publishes it to GitHub Container Registry.

```
push / PR ──► lint (ruff) ──► test (pytest) ──► docker build ──► smoke test (/health)
                                                                        │
                                                      main only ────────┘
                                                                        ▼
                                                           push to ghcr.io (:sha, :latest)
```

## Pipeline (`.github/workflows/ci.yml`)

| Job | Runs on | What it does |
|---|---|---|
| `test` | every push and PR | `ruff check`, then `pytest` |
| `docker` | after `test` passes | Builds the image, starts it, and curls `/health`; on `main` only, logs in to GHCR and pushes |

Design choices:
- **Smoke test the real image**, not just the code: a broken Dockerfile fails the build before anything is published.
- **Publish only from `main`.** Pull requests build and test but never push.
- **Least privilege:** workflow-level permissions are read-only; only the `docker` job gets `packages: write`.
- **Layer caching** through the GitHub Actions cache, so the publish step reuses the smoke-test build.
- **Immutable tags:** each image is tagged with the commit SHA (and `latest`), and the SHA is baked in as `APP_VERSION`.
- **Container hygiene:** slim base image, non-root user, `HEALTHCHECK`, gunicorn instead of the Flask dev server.

## Run locally

```bash
pip install -r requirements-dev.txt
ruff check . && pytest -q

docker build -t pipeline-demo .
docker run --rm -p 8000:8000 pipeline-demo
curl localhost:8000/health        # {"status":"ok"}
curl localhost:8000/greet/Ada     # {"greeting":"Hello, Ada!"}
```

## Endpoints

| Path | Response |
|---|---|
| `/` | Greeting and the running version |
| `/health` | `{"status": "ok"}` |
| `/greet/<name>` | `{"greeting": "Hello, <name>!"}` |

## Next steps

- Add a deploy job (Kubernetes, ECS, or Cloud Run) gated on a protected `production` environment.
- Add image vulnerability scanning (e.g. Trivy) before the push step.
- Pin action versions by SHA and add Dependabot for actions and pip.

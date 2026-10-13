# basana: portable verification records

<!-- current-documentation-provenance -->
Documentation reviewed: 2026-10-13 · Git source base: `7eb2c1c3a67bd569d1bff695609c87e3f30bca32` · [Current architecture and feature guide](../ayu-develop.md).
Historical execution commands/results below retain their original dates and scope; this metadata update is not a new application test run.
<!-- /current-documentation-provenance -->


Full raw logs are retained in the workspace maintenance evidence, not distributed here. Hashes identify those original logs. A successful build or selected test subset does not imply a full test-suite pass. Commands containing <workspace> describe the original execution environment.

[Machine-readable records](verification.json) · [Repository validation summary](../validation.md)

## Executed commands

| Check | Exit | Duration | Command | Outcomes |
| --- | ---: | ---: | --- | --- |
| build | 0 | 0.13s | `uv build --python 3.14` | Successfully built dist/basana-1.11.tar.gz<br>Successfully built dist/basana-1.11-py3-none-any.whl |
| build-final | 0 | 0.13s | `uv build --python 3.14` | Successfully built dist/basana-1.11.tar.gz<br>Successfully built dist/basana-1.11-py3-none-any.whl |
| build-vendor-source-archive | 0 | 0.21s | `uv build --python 3.14` | Successfully built dist/basana-1.11.tar.gz<br>Successfully built dist/basana-1.11-py3-none-any.whl |
| compile | 0 | 0.13s | `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | See exit status; no test-count assertion. |
| compile-final | 0 | 0.08s | `uv run --no-sync python -m compileall -q src` | See exit status; no test-count assertion. |
| lint-owned-sources | 0 | 0.68s | `uv run --no-sync invoke lint` | See exit status; no test-count assertion. |
| lint-upstream-required | 1 | 11.58s | `uv run --no-sync invoke lint` | See exit status; no test-count assertion. |
| lock-3.14 | 0 | 0.34s | `uv lock --upgrade --python 3.14` | See exit status; no test-count assertion. |
| lock-3.15 | 0 | 0.58s | `uv lock --upgrade --python 3.15` | See exit status; no test-count assertion. |
| python315-host-deployment-probe | 1 | 4.27s | `env MACOSX_DEPLOYMENT_TARGET=27.0 uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | See exit status; no test-count assertion. |
| python315-source-probe | 1 | 4.5s | `uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | See exit status; no test-count assertion. |
| sync-3.14 | 0 | 1.26s | `uv sync --all-extras --all-groups --python 3.14` | See exit status; no test-count assertion. |
| sync-aiohttp-mock-compatibility | 0 | 0.09s | `uv sync --all-extras --all-groups --python 3.14` | See exit status; no test-count assertion. |
| sync-mock-rebuild | 0 | 0.58s | `uv sync --all-extras --all-groups --python 3.14 --reinstall-package aioresponses` | See exit status; no test-count assertion. |
| tests | 1 | 82.29s | `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml` | 87 failed, 358 passed in 67.74s (0:01:07) |
| tests-aiohttp-mock-compatibility | 1 | 97.67s | `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 86 failed, 359 passed in 93.93s (0:01:33) |
| tests-current-api-mock | 1 | 32.4s | `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 2 failed, 443 passed in 29.99s |
| tests-deprecated-api-assertion | 0 | 29.81s | `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 445 passed in 28.02s |
| versions-final | 0 | 0.18s | `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | See exit status; no test-count assertion. |
| wheel-probe-3.14 | 2 | 0.04s | `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | See exit status; no test-count assertion. |
| wheel-probe-3.15 | 2 | 3.4s | `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | See exit status; no test-count assertion. |

# Validation evidence: basana

Run date: 2026-10-12. Branch: `feature/ayu_develop`. Interpreter: `3.14.8 (main, Oct  9 2026, 15:11:09) [Clang 22.1.3 ]`.

| Check | Result |
|---|---|
| lock | passed |
| sync | passed |
| compile | passed |
| build | passed |
| tests | passed |
| lint | passed |

## Current result and compatibility decisions

- The full existing suite passes 445 cases and covers every one of 5535 source statements (100.00%). Deprecated API assertions use deprecated_call and retain their original value assertions.
- The simulator logs use the current fill.price field; log timestamps are included in pytest log formatting so the existing logging assertion remains meaningful. CSV/JSON input files close deterministically.
- Latest CCXT requires aiohttp 3.14; current aioresponses 0.7.9 needs the documented stream_writer mock patch. See vendor/aioresponses/PROVENANCE.md and original retained license.
- The source-build Python 3.15 attempt fails compiling pycares 5.1.0, required by aiohttp speedups. Native build evidence is retained.
- Invoke lint validates 95 owned Python files. Verified third-party vendor source retains its upstream lint conventions and is excluded from the project Ruff scan.

Current unresolved checks:

All supplied checks recorded below passed.

## Latest full-suite output

```text
$ uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100
........................................................................ [ 16%]
........................................................................ [ 32%]
........................................................................ [ 48%]
........................................................................ [ 64%]
........................................................................ [ 80%]
........................................................................ [ 97%]
.............                                                            [100%]
================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.8-final-0 _______________

Name    Stmts   Miss  Cover   Missing
-------------------------------------
TOTAL    5535      0   100%

95 files skipped due to complete coverage.
Required test coverage of 100% reached. Total coverage: 100.00%
445 passed in 28.02s

```

## Exact commands and exit codes

Unsuccessful rows are retained as historical compatibility attempts; they are not claims that a current passing check remains blocked. Source-build probes use isolated temporary copies to preserve the selected repository environment.

| Command | Exit | Seconds | Evidence |
|---|---:|---:|---|
| `uv lock --upgrade --python 3.15` | 0 | 0.58 | [log](../../docs/maintenance-2026-10-12/basana-lock-3.15.log) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 3.4 | [log](../../docs/maintenance-2026-10-12/basana-wheel-probe-3.15.log) |
| `uv lock --upgrade --python 3.14` | 0 | 0.34 | [log](../../docs/maintenance-2026-10-12/basana-lock-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 2 | 0.04 | [log](../../docs/maintenance-2026-10-12/basana-wheel-probe-3.14.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 1.26 | [log](../../docs/maintenance-2026-10-12/basana-sync-3.14.log) |
| `uv build --python 3.14` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/basana-build.log) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/basana-compile.log) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml` | 1 | 82.29 | [log](../../docs/maintenance-2026-10-12/basana-tests.log) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 0.09 | [log](../../docs/maintenance-2026-10-12/basana-sync-aiohttp-mock-compatibility.log) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 1 | 97.67 | [log](../../docs/maintenance-2026-10-12/basana-tests-aiohttp-mock-compatibility.log) |
| `uv sync --all-extras --all-groups --python 3.14 --reinstall-package aioresponses` | 0 | 0.58 | [log](../../docs/maintenance-2026-10-12/basana-sync-mock-rebuild.log) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 1 | 32.4 | [log](../../docs/maintenance-2026-10-12/basana-tests-current-api-mock.log) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 0 | 29.81 | [log](../../docs/maintenance-2026-10-12/basana-tests-deprecated-api-assertion.log) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.08 | [log](../../docs/maintenance-2026-10-12/basana-compile-final.log) |
| `uv build --python 3.14` | 0 | 0.13 | [log](../../docs/maintenance-2026-10-12/basana-build-final.log) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.18 | [log](../../docs/maintenance-2026-10-12/basana-versions-final.log) |
| `uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | 1 | 4.5 | [log](../../docs/maintenance-2026-10-12/basana-python315-source-probe.log) |
| `uv run --no-sync invoke lint` | 1 | 11.58 | [log](../../docs/maintenance-2026-10-12/basana-lint-upstream-required.log) |
| `uv run --no-sync invoke lint` | 0 | 0.68 | [log](../../docs/maintenance-2026-10-12/basana-lint-owned-sources.log) |
| `env MACOSX_DEPLOYMENT_TARGET=27.0 uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | 1 | 4.27 | [log](../../docs/maintenance-2026-10-12/basana-python315-host-deployment-probe.log) |
| `uv build --python 3.14` | 0 | 0.21 | [log](../../docs/maintenance-2026-10-12/basana-build-vendor-source-archive.log) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [result](../../docs/maintenance-2026-10-12/basana-result.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.

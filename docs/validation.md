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
| `uv lock --upgrade --python 3.15` | 0 | 0.58 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 3.4 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.14` | 0 | 0.34 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 2 | 0.04 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 1.26 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 0.13 | [check record](maintenance/index.html) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.13 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml` | 1 | 82.29 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 0.09 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 1 | 97.67 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14 --reinstall-package aioresponses` | 0 | 0.58 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 1 | 32.4 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest --cov=src/basana --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=100` | 0 | 29.81 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.08 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 0.13 | [check record](maintenance/index.html) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.18 | [check record](maintenance/index.html) |
| `uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | 1 | 4.5 | [check record](maintenance/index.html) |
| `uv run --no-sync invoke lint` | 1 | 11.58 | [check record](maintenance/index.html) |
| `uv run --no-sync invoke lint` | 0 | 0.68 | [check record](maintenance/index.html) |
| `env MACOSX_DEPLOYMENT_TARGET=27.0 uv sync --directory /tmp/trading-python315-probes/basana --all-extras --all-groups --python 3.15` | 1 | 4.27 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 0.21 | [check record](maintenance/index.html) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [verification record](maintenance/verification.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.

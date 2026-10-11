"""Compatibility namespace for the educational examples directory."""
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent.parent / "examples")]

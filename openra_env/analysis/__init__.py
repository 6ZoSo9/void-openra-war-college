"""Analysis tools for VOID War College evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["analyze_trajectory"]


def analyze_trajectory(
    trajectory_path: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    """Lazily invoke the spar training-utility analyzer."""
    from .spar_training_utility import analyze_trajectory as implementation

    return implementation(trajectory_path, **kwargs)

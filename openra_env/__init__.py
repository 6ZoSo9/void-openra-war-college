"""OpenRA-RL: Reinforcement Learning Environment for the OpenRA RTS Engine."""

from __future__ import annotations

from typing import Any

__all__ = ["OpenRAEnv", "OpenRAAction", "OpenRAObservation", "OpenRAState"]


def __getattr__(name: str) -> Any:
    """Load runtime-heavy public objects only when they are requested."""
    if name == "OpenRAEnv":
        from openra_env.client import OpenRAEnv

        return OpenRAEnv
    if name in {"OpenRAAction", "OpenRAObservation", "OpenRAState"}:
        from openra_env.models import OpenRAAction, OpenRAObservation, OpenRAState

        return {
            "OpenRAAction": OpenRAAction,
            "OpenRAObservation": OpenRAObservation,
            "OpenRAState": OpenRAState,
        }[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
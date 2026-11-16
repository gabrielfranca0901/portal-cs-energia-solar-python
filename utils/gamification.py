"""Simple in‑memory gamification utilities.

This module stores a per‑session XP balance and the subscription status
for the *Solar Care+* maintenance plan. In a real production system the
state would be persisted in a database or external service, but for the
purpose of this demo a module‑level dictionary is sufficient.
"""

import threading

_lock = threading.Lock()
_state = {
    "xp": 0,
    "subscribed": False,
    "multiplier": 1.0,
}

def get_state():
    """Return a copy of the current gamification state."""
    with _lock:
        return _state.copy()

def add_xp(amount: int) -> int:
    """Add XP applying the active multiplier.

    Parameters
    ----------
    amount: int
        Base amount of XP to credit.
    """
    with _lock:
        bonus = int(amount * _state["multiplier"])
        _state["xp"] += bonus
        return _state["xp"]

def subscribe_care(plan: str) -> int:
    """Register the user for the Solar Care+ plan.

    The *plan* argument can be ``"monthly"`` or ``"quarterly"`` – it is
    currently only stored for informational purposes.
    """
    with _lock:
        _state["subscribed"] = True
        _state["multiplier"] = 1.5
        # Immediate bonus of 500 XP (already multiplied)
        _state["xp"] += int(500 * _state["multiplier"])
        return _state["xp"]

def complete_quarterly_visit() -> int:
    """Credit the XP for completing a quarterly visit.

    Returns the new total XP.
    """
    with _lock:
        _state["xp"] += int(250 * _state["multiplier"])
        return _state["xp"]

__all__ = ["get_state", "add_xp", "subscribe_care", "complete_quarterly_visit"]

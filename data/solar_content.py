"""Data definitions for the Solar Energy Portal.

This module defines the core business concepts used throughout the application:
- Tiers: Different service packages.
- Missions: Typical customer journeys.
- MessageRuler: Mapping of user interaction tiers to message templates.
- Guardrails: Constraints and validation rules.
- ROI: Simple financial return calculations.
"""

from dataclasses import dataclass
from typing import List, Dict

# ---------------------------------------------------------------------------
# Service Tiers
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Tier:
    """A service tier offered to a customer.

    Attributes
    ----------
    name: str
        Human‑readable name of the tier.
    max_kw: float
        Maximum installed capacity (kW) covered by the tier.
    price_per_kw: float
        Price (USD) per kilowatt of installed capacity.
    """
    name: str
    max_kw: float
    price_per_kw: float

TIERS: List[Tier] = [
    Tier(name="Basic", max_kw=5, price_per_kw=1200),
    Tier(name="Standard", max_kw=10, price_per_kw=1100),
    Tier(name="Premium", max_kw=20, price_per_kw=1000),
]

# ---------------------------------------------------------------------------
# Customer Missions
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Mission:
    """Typical customer goal.

    Attributes
    ----------
    identifier: str
        Short code used internally.
    description: str
        Human description of the mission.
    target_savings_pct: float
        Desired reduction in electricity bill (percentage).
    """
    identifier: str
    description: str
    target_savings_pct: float

MISSIONS: List[Mission] = [
    Mission("RES", "Reduzir Energia Solar", 30),
    Mission("IND", "Indústria Sustentável", 45),
    Mission("AGR", "Agricultura Inteligente", 40),
]

# ---------------------------------------------------------------------------
# Message templates (Ruler)
# ---------------------------------------------------------------------------
MESSAGE_TEMPLATES: Dict[str, str] = {
    "welcome": "Bem‑vindo ao Portal CS Energia Solar! Escolha seu plano e comece a economizar.",
    "summary": "Seu sistema de {kw:.1f} kW gera aproximadamente {kwh_year:.0f} kWh/ano, com ROI estimado em {roi:.1f}%.",
}

# ---------------------------------------------------------------------------
# Guardrails – simple validation helpers
# ---------------------------------------------------------------------------
def validate_kw(kw: float) -> bool:
    """Return ``True`` if the requested kw is within any defined tier range."""
    return any(0 < kw <= tier.max_kw for tier in TIERS)

# ---------------------------------------------------------------------------
# ROI calculation (very simplified)
# ---------------------------------------------------------------------------
def simple_roi(initial_investment: float, annual_savings: float, years: int = 25) -> float:
    """Calculate a basic return‑on‑investment percentage.

    Parameters
    ----------
    initial_investment: float
        Total upfront cost in USD.
    annual_savings: float
        Expected yearly savings in USD.
    years: int, default 25
        Analysis horizon.

    Returns
    -------
    float
        ROI as a percentage of the invested amount.
    """
    total_return = annual_savings * years
    return (total_return - initial_investment) / initial_investment * 100

__all__ = [
    "Tier",
    "TIERS",
    "Mission",
    "MISSIONS",
    "MESSAGE_TEMPLATES",
    "validate_kw",
    "simple_roi",
]

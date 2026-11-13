"""Utility functions for photovoltaic sizing and financial simulation.

The functions are deliberately lightweight and have no external dependencies
apart from the data definitions in :pymod:`data.solar_content`.
"""

from typing import Tuple

from data.solar_content import TIERS, validate_kw, simple_roi

# ---------------------------------------------------------------------------
# Solar production estimation
# ---------------------------------------------------------------------------
def estimate_yearly_kwh(installed_kw: float, production_factor: float = 1500.0) -> float:
    """Estimate yearly energy production (kWh).

    The baseline factor (1500 kWh/kW/yr) is typical for sunny regions.
    Additional calculations (panel count, area, inverter oversizing) are
    provided by helper functions below and can be incorporated by the caller.
    """
    return installed_kw * production_factor
    """Estimate the yearly energy production (kWh) of a PV system.

    Parameters
    ----------
    installed_kw: float
        The rated capacity of the installation in kilowatts.
    production_factor: float, default 1500.0
        Approximate kWh generated per kW per year for a typical location.

    Returns
    -------
    float
        Estimated annual generation in kWh.
    """
    return installed_kw * production_factor

# ---------------------------------------------------------------------------
# Financial helpers
# ---------------------------------------------------------------------------
def compute_investment(installed_kw: float) -> float:
    """Return the upfront investment based on the tier pricing.

    The function selects the cheapest tier that can accommodate the requested
    ``installed_kw`` and multiplies the tier's ``price_per_kw`` by the capacity.
    """
    suitable = [t for t in TIERS if installed_kw <= t.max_kw]
    if not suitable:
        raise ValueError("Requested capacity exceeds all defined tiers.")
    tier = min(suitable, key=lambda t: t.max_kw)
    return installed_kw * tier.price_per_kw

def compute_annual_savings(yearly_kwh: float, electricity_rate: float = 0.30) -> float:
    """Convert energy production to monetary savings.

    Parameters
    ----------
    yearly_kwh: float
        Energy generated per year.
    electricity_rate: float, default 0.30
        Cost per kWh in USD (average residential rate).
    """
    return yearly_kwh * electricity_rate

def run_simulation(installed_kw: float) -> Tuple[float, float, float]:
    """Run the full sizing and financial simulation.

    Returns a tuple ``(yearly_kwh, investment, roi_percent)``.
    """
    if not validate_kw(installed_kw):
        raise ValueError("Installed capacity not covered by any tier.")
    yearly_kwh = estimate_yearly_kwh(installed_kw)
    investment = compute_investment(installed_kw)
    annual_savings = compute_annual_savings(yearly_kwh)
    roi = simple_roi(investment, annual_savings)
    return yearly_kwh, investment, roi

__all__ = [
    "estimate_yearly_kwh",
    "compute_investment",
    "compute_annual_savings",
    "run_simulation",
]

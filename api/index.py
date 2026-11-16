import os
import sys
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Ensure project root is in sys.path for imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import modules
from utils import calculator, gamification
from data import solar_content

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ---------------------------------------------------------------------------
# Main page – provides initial gamification state
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    state = gamification.get_state()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "welcome": solar_content.MESSAGE_TEMPLATES["welcome"],
            "xp": state["xp"],
            "subscribed": state["subscribed"],
            "multiplier": state["multiplier"],
        },
    )

# ---------------------------------------------------------------------------
# Solar calculation endpoint (existing functionality)
# ---------------------------------------------------------------------------
@app.post("/api/calcular-solar")
async def calcular_solar(installed_kw: float = Form(...)):
    try:
        yearly_kwh, investment, roi = calculator.run_simulation(installed_kw)
        annual_savings = calculator.compute_annual_savings(yearly_kwh)
        return JSONResponse(
            {
                "yearly_kwh": yearly_kwh,
                "investment": investment,
                "annual_savings": annual_savings,
                "roi": roi,
            }
        )
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# ---------------------------------------------------------------------------
# Gamification API – state & actions
# ---------------------------------------------------------------------------
@app.get("/api/gamification/state")
async def get_gamification_state():
    return JSONResponse(gamification.get_state())

@app.post("/api/gamification/subscribe")
async def subscribe_plan(plan: str = Form(...)):
    gamification.subscribe_care(plan)
    return JSONResponse(gamification.get_state())

@app.post("/api/gamification/complete-visit")
async def complete_visit():
    gamification.complete_quarterly_visit()
    return JSONResponse(gamification.get_state())

@app.post("/api/gamification/add-xp")
async def add_xp(amount: int = Form(...)):
    gamification.add_xp(amount)
    return JSONResponse(gamification.get_state())

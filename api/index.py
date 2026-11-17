import os
import sys
import traceback
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client

# Ensure project root is in sys.path for imports
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://eiyzudvtgkvhswhrhbgq.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpeXp1ZHZ0Z2t2aHN3aHJoYmdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ5MzA3MDgsImV4cCI6MjExMDUwNjcwOH0.jnUFXqTGbEjaCS7KGVMss2oyvy060gz0M_x2oXKR1zI")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Templates directory – same folder as this file
templates = Jinja2Templates(directory=os.path.dirname(os.path.abspath(__file__)))

TABLE_NAME = "solar_gamification"
DEFAULT_ID = "cliente_padrao"

def _initialize_default_state():
    default_state = {
        "id": DEFAULT_ID,
        "xp": 350,
        "subscribed": False,
        "plan_type": None,
        "multiplier": 1.0,
        "plantHealth": 88,
        "badges": ["Pioneiro Solar ☀️"],
        "completedGuides": [],
        "nextVisitDate": None,
    }
    supabase.from_(TABLE_NAME).insert(default_state).execute()
    return default_state

def get_state():
    res = supabase.from_(TABLE_NAME).select("*").eq("id", DEFAULT_ID).execute()
    if res.data:
        return res.data[0]
    return _initialize_default_state()

def update_state(updates: dict):
    supabase.from_(TABLE_NAME).update(updates).eq("id", DEFAULT_ID).execute()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        state = get_state()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "welcome": "Bem‑vindo ao portal!",
                "xp": state.get("xp"),
                "subscribed": state.get("subscribed"),
                "multiplier": state.get("multiplier"),
            },
        )
    except Exception:
        return HTMLResponse(content=f"<pre>{traceback.format_exc()}</pre>", status_code=500)

# Solar calculation endpoint (unchanged)
@app.post("/api/calcular-solar")
async def calcular_solar(installed_kw: float = Form(...)):
    try:
        from utils import calculator
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

@app.get("/api/gamification/state")
async def get_gamification_state():
    return JSONResponse(get_state())

@app.post("/api/gamification/subscribe")
async def subscribe_plan(plan: str = Form(...)):
    state = get_state()
    state["subscribed"] = True
    state["plan_type"] = plan
    state["multiplier"] = 1.5
    added_xp = int(500 * state["multiplier"])
    state["xp"] = state.get("xp", 0) + added_xp
    badges = state.get("badges", [])
    if "Usina Blindada 🛡️" not in badges:
        badges.append("Usina Blindada 🛡️")
    state["badges"] = badges
    update_state({
        "subscribed": state["subscribed"],
        "plan_type": state["plan_type"],
        "multiplier": state["multiplier"],
        "xp": state["xp"],
        "badges": state["badges"],
    })
    return JSONResponse(state)

@app.post("/api/gamification/complete-visit")
async def complete_visit():
    state = get_state()
    added_xp = int(250 * state.get("multiplier", 1.0))
    state["xp"] = state.get("xp", 0) + added_xp
    state["plantHealth"] = 100
    update_state({"xp": state["xp"], "plantHealth": state["plantHealth"]})
    return JSONResponse(state)

@app.post("/api/gamification/add-xp")
async def add_xp(amount: int = Form(...)):
    state = get_state()
    added = int(amount * state.get("multiplier", 1.0))
    state["xp"] = state.get("xp", 0) + added
    update_state({"xp": state["xp"]})
    return JSONResponse(state)

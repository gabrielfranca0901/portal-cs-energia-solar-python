import os
import sys
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

# Ensure project root is in sys.path for imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils import calculator
from data import solar_content

app = FastAPI()





templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "welcome": solar_content.MESSAGE_TEMPLATES["welcome"]})

@app.post("/api/calcular-solar")
async def calcular_solar(installed_kw: float = Form(...)):
    try:
        yearly_kwh, investment, roi = calculator.run_simulation(installed_kw)
        annual_savings = calculator.compute_annual_savings(yearly_kwh)
        return JSONResponse({
            "yearly_kwh": yearly_kwh,
            "investment": investment,
            "annual_savings": annual_savings,
            "roi": roi,
        })
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

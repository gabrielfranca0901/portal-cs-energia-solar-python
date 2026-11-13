import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import calculator
from data import solar_content

app = FastAPI()

# Mount static folder (if needed for assets)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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

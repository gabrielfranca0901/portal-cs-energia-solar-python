# CS Energia Solar Portal

A lightweight Streamlit application that demonstrates photovoltaic sizing and financial simulation for solar energy projects.

## Project Structure
```
portal-cs-energia-solar-python/
├─ .streamlit/
│   └─ config.toml            # Dark theme configuration
├─ data/
│   └─ solar_content.py       # Business data definitions
├─ utils/
│   └─ calculator.py          # Sizing and financial calculations
├─ app.py                      # Main Streamlit app
├─ requirements.txt            # Python dependencies
├─ .gitignore                  # Ignored files
└─ README.md                   # Project documentation (this file)
```

## Setup
1. **Install Python 3.11+** and ensure `python` is available in your `PATH`.
   - On Windows you can install via the Microsoft Store or download from
     https://www.python.org/downloads/windows/.
2. Open a PowerShell terminal and navigate to the project directory:
   ```powershell
   cd C:\Users\gabri\.gemini\antigravity\scratch\portal-cs-energia-solar-python
   ```
3. (Optional) Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install the required packages:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the app:
   ```powershell
   streamlit run app.py
   ```

The app will launch in your default browser at `http://localhost:8501`.

## Features
- **Home** – Welcome screen with a brief description.
- **Dimensionamento** – Input desired kW and get estimated yearly production, investment cost, and ROI.
- **Financeiro** – Shows investment amount, annual savings, and ROI metrics.
- **Sobre** – Documentation with formulas and project overview.

## Core Formulas
- **Annual production**: `kW * 1500` (kWh/yr) – a typical production factor for sunny regions.
- **Annual savings**: `production_kWh * electricity_rate` (USD).
- **ROI**: `((annual_savings * years) - investment) / investment * 100`.

## License
This is a prototype project intended for educational purposes.

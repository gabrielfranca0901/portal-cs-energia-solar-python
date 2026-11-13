"""Main Streamlit application for CS Energia Solar portal.

The app provides a sidebar with navigation between four simple modules:
1️⃣ **Home** – Welcome message.
2️⃣ **Sizing** – Input desired kW and run the photovoltaic sizing simulation.
3️⃣ **Financial** – Show investment, annual savings and ROI.
4️⃣ **About** – Project documentation.

All core logic lives in :pymod:`utils.calculator` and the data definitions in
:pymod:`data.solar_content`.
"""

import streamlit as st
from utils import calculator
from data import solar_content

st.set_page_config(page_title="CS Energia Solar", layout="centered")

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("Navegação")
page = st.sidebar.radio(
    "Selecione um módulo",
    ("Home", "Dimensionamento", "Financeiro", "Sobre"),
)

# ---------------------------------------------------------------------------
# Page implementations
# ---------------------------------------------------------------------------
if page == "Home":
    st.title("Portal CS Energia Solar")
    st.markdown(solar_content.MESSAGE_TEMPLATES["welcome"])

elif page == "Dimensionamento":
    st.title("Dimensionamento Fotovoltaico")
    kw = st.number_input("Capacidade desejada (kW)", min_value=0.5, max_value=20.0, step=0.5)
    if st.button("Calcular"):
        try:
            yearly_kwh, investment, roi = calculator.run_simulation(kw)
            st.success("Cálculo realizado com sucesso!")
            st.write(f"Produção anual estimada: {yearly_kwh:,.0f} kWh")
            st.write(f"Investimento aproximado: US${investment:,.0f}")
            st.write(f"ROI (25 anos): {roi:.1f}%")
        except ValueError as e:
            st.error(str(e))

elif page == "Financeiro":
    st.title("Simulação Financeira")
    kw = st.number_input("Capacidade (kW)", min_value=0.5, max_value=20.0, step=0.5, key="fin_kw")
    if st.button("Simular"):
        try:
            yearly_kwh, investment, roi = calculator.run_simulation(kw)
            annual_savings = calculator.compute_annual_savings(yearly_kwh)
            st.metric(label="Investimento", value=f"US${investment:,.0f}")
            st.metric(label="Economia anual", value=f"US${annual_savings:,.0f}")
            st.metric(label="ROI (25 anos)", value=f"{roi:.1f}%")
        except ValueError as e:
            st.error(str(e))

elif page == "Sobre":
    st.title("Sobre o Projeto")
    st.markdown(
        """
        **CS Energia Solar** é um protótipo de portal que demonstra:
        - Estrutura de dados de *tiers*, missões e guardrails.
        - Cálculo simplificado de dimensionamento fotovoltaico.
        - Simulação financeira básica (investimento, economia anual e ROI).

        ## Fórmulas chave
        - **Produção anual**: `kW * 1500` (kWh/ano) – fator típico para regiões solares.
        - **Economia anual**: `produzido_kWh * tarifa_kWh` (US$).
        - **ROI**: `((economia_anual * anos) - investimento) / investimento * 100`.
        """
    )
    st.info("Para mais detalhes, veja o README.md no repositório.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.caption("© 2026 CS Energia Solar – Todos os direitos reservados.")

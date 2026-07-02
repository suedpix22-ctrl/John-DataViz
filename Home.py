import streamlit as st

st.set_page_config(
    page_title="JohnDataViz | Telco Churn",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import render_sidebar, GLOBAL_CSS

name_val = render_sidebar("Home")

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.hero-card {
    background: linear-gradient(135deg, #1A3C5E 0%, #4A90D9 100%);
    border-radius: 16px; padding: 40px 48px; color: white; margin-bottom: 32px;
}
.hero-card h1 { font-size: 2.4rem; font-weight: 700; margin: 0 0 8px 0; }
.hero-card p  { font-size: 1.1rem; opacity: 0.88; margin: 0; }
.kpi-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
.kpi-box {
    flex: 1; min-width: 140px; background: white; border-radius: 12px;
    padding: 20px 24px; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07); border-top: 3px solid #1A3C5E;
}
.kpi-box .val { font-size: 2rem; font-weight: 700; color: #1A3C5E; }
.kpi-box .lbl { font-size: 0.78rem; color: #7F8C8D; margin-top: 4px;
                text-transform: uppercase; letter-spacing: 0.5px; }
.about-card {
    background: white; border-radius: 12px; padding: 28px 32px;
    border-left: 4px solid #E8534A;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
  <h1>📡 JohnDataViz</h1>
  <p>Plataforma de análise de <strong>Churn de Clientes</strong> — Setor de Telecomunicações</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="kpi-row">'
    '<div class="kpi-box"><div class="val">7.043</div><div class="lbl">Clientes Analisados</div></div>'
    '<div class="kpi-box"><div class="val" style="color:#E8534A">1.869</div><div class="lbl">Cancelamentos</div></div>'
    '<div class="kpi-box"><div class="val" style="color:#E8534A">26,5%</div><div class="lbl">Taxa de Churn</div></div>'
    '<div class="kpi-box"><div class="val" style="color:#27AE60">5.174</div><div class="lbl">Clientes Ativos</div></div>'
    '<div class="kpi-box"><div class="val">50</div><div class="lbl">Variáveis no Dataset</div></div>'
    '</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
<div class="about-card">
<h3 style="color:#1A3C5E; margin-top:0">🏢 Sobre a JohnDataViz</h3>
<p style="color:#444; line-height:1.7">
Somos uma consultoria especializada em <strong>análise de dados e inteligência de negócios</strong>.
Transformamos dados brutos em decisões estratégicas, entregando dashboards, relatórios e modelos
preditivos que impulsionam resultados reais.
</p>
<p style="color:#444; line-height:1.7">
Neste projeto, analisamos <strong>7.043 registros</strong> de clientes de uma empresa de
telecomunicações com o objetivo de identificar os principais <strong>drivers de cancelamento (churn)</strong>
e propor ações corretivas baseadas em dados.
</p>
<hr style="border-color:#eee; margin:16px 0">
<p style="color:#7F8C8D; font-size:0.85rem; margin:0">
📍 São Paulo, Brasil &nbsp;|&nbsp; 📧 contato@johndataviz.com.br &nbsp;|&nbsp; 🌐 johndataviz.com.br
</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="about-card" style="border-left-color:#1A3C5E">
<h3 style="color:#1A3C5E; margin-top:0">🧭 Como Navegar</h3>
<ul style="color:#444; line-height:2.2; padding-left:18px">
  <li><strong>📋 Tabela</strong> — Dataset completo</li>
  <li><strong>📊 Churn</strong> — Análise de cancelamentos</li>
  <li><strong>👥 Clientes</strong> — Perfil e comportamento</li>
  <li><strong>📧 E-mail</strong> — Envio de gráficos e relatório</li>
  <li><strong>⬇️ Download</strong> — Relatório em .txt</li>
</ul>
</div>
""", unsafe_allow_html=True)

if not name_val:
    st.info("💡 Digite seu nome na sidebar para personalizar sua experiência nas páginas!")

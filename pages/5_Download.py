import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import render_sidebar, GLOBAL_CSS, greeting, INSIGHTS_REPORT

st.set_page_config(page_title="Download | JohnDataViz", page_icon="⬇️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.download-card {
    background: white; border-radius: 14px; padding: 36px 40px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 0 auto;
    border-top: 4px solid #1A3C5E; max-width: 700px; text-align: center;
}
.preview-box {
    background: #F4F6F9; border-radius: 10px; padding: 20px;
    font-family: monospace; font-size: 0.82rem; color: #2C3E50;
    text-align: left; max-height: 400px; overflow-y: auto;
    border: 1px solid #D5D8DC; margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

name_val = render_sidebar("Download")

st.markdown(f"""
<div class="page-header">
  <h2 style="margin:0 0 4px 0">⬇️ Download do Relatório</h2>
  <p style="margin:0; opacity:.85">{greeting(name_val, 'Download do Relatório')}</p>
</div>
""", unsafe_allow_html=True)

_, col_mid, _ = st.columns([1, 3, 1])
with col_mid:
    st.markdown("""
<div class="download-card">
  <div style="font-size:4rem; margin-bottom:12px">📄</div>
  <h2 style="color:#1A3C5E; margin:0 0 8px 0">Relatório de Análise de Churn</h2>
  <p style="color:#7F8C8D; font-size:0.95rem; margin:0 0 24px 0">
    Relatório completo com insights, análise e recomendações estratégicas<br>
    elaborado pela <strong>JohnDataViz</strong>.
  </p>
  <div style="display:flex; justify-content:center; gap:24px; margin-bottom:24px; flex-wrap:wrap">
    <div style="background:#EBF5FB; border-radius:8px; padding:12px 20px; text-align:center">
      <div style="font-size:1.4rem; font-weight:700; color:#1A3C5E">7.043</div>
      <div style="font-size:0.75rem; color:#7F8C8D">Clientes analisados</div>
    </div>
    <div style="background:#FDEDEC; border-radius:8px; padding:12px 20px; text-align:center">
      <div style="font-size:1.4rem; font-weight:700; color:#E8534A">26,5%</div>
      <div style="font-size:0.75rem; color:#7F8C8D">Taxa de churn</div>
    </div>
    <div style="background:#EAFAF1; border-radius:8px; padding:12px 20px; text-align:center">
      <div style="font-size:1.4rem; font-weight:700; color:#27AE60">6</div>
      <div style="font-size:0.75rem; color:#7F8C8D">Recomendações</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("⬇️  Baixar Relatório (.txt)", data=INSIGHTS_REPORT.encode("utf-8"),
                       file_name="relatorio_churn_telco_dataviz.txt", mime="text/plain",
                       use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("👁️ Pré-visualizar conteúdo"):
        st.markdown(f'<div class="preview-box"><pre>{INSIGHTS_REPORT}</pre></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.82rem; color:#7F8C8D; margin-top:16px'>📡 JohnDataViz | contato@johndataviz.com.br</p>",
                unsafe_allow_html=True)

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, render_sidebar, GLOBAL_CSS, greeting

st.set_page_config(page_title="Tabela | JohnDataViz", page_icon="📋", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
name_val = render_sidebar("Tabela")

st.markdown(f"""
<div class="page-header">
  <h2 style="margin:0 0 4px 0">📋 Tabela de Dados</h2>
  <p style="margin:0; opacity:.85">{greeting(name_val, 'Tabela de Dados')}</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

with st.expander("🔍 Filtros", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        churn_filter = st.multiselect("Status de Churn", options=df["Churn Label"].unique().tolist(),
                                      default=df["Churn Label"].unique().tolist())
    with c2:
        contract_filter = st.multiselect("Tipo de Contrato", options=df["Contract"].unique().tolist(),
                                         default=df["Contract"].unique().tolist())
    with c3:
        internet_filter = st.multiselect("Serviço de Internet", options=df["Internet Service"].unique().tolist(),
                                         default=df["Internet Service"].unique().tolist())
    with c4:
        age_range = st.slider("Faixa de Idade", int(df["Age"].min()), int(df["Age"].max()),
                              (int(df["Age"].min()), int(df["Age"].max())))
    search_term = st.text_input("🔎 Buscar por Customer ID ou Cidade", "")

mask = (df["Churn Label"].isin(churn_filter) & df["Contract"].isin(contract_filter) &
        df["Internet Service"].isin(internet_filter) & df["Age"].between(age_range[0], age_range[1]))
if search_term:
    mask &= (df["Customer ID"].str.contains(search_term, case=False, na=False) |
             df["City"].str.contains(search_term, case=False, na=False))
df_filtered = df[mask].reset_index(drop=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total de Registros", f"{len(df_filtered):,}")
m2.metric("Cancelamentos", f"{(df_filtered['Churn Label']=='Yes').sum():,}")
m3.metric("Taxa de Churn", f"{(df_filtered['Churn Label']=='Yes').mean()*100:.1f}%")
m4.metric("Colunas", str(df_filtered.shape[1]))

st.markdown("---")

with st.expander("⚙️ Selecionar colunas", expanded=False):
    default_cols = ["Customer ID", "Gender", "Age", "Contract", "Internet Service",
                    "Monthly Charge", "Tenure in Months", "Churn Label",
                    "Churn Category", "Churn Reason", "Satisfaction Score"]
    selected_cols = st.multiselect("Colunas visíveis", df.columns.tolist(), default=default_cols)

if not selected_cols:
    selected_cols = df.columns.tolist()

st.markdown(f"**{len(df_filtered):,} registros encontrados**")
st.dataframe(df_filtered[selected_cols], use_container_width=True, hide_index=True, height=520)

csv_bytes = df_filtered[selected_cols].to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar tabela filtrada (.csv)", data=csv_bytes,
                   file_name="telco_filtrado.csv", mime="text/csv")

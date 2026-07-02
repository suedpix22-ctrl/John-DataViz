import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, render_sidebar, GLOBAL_CSS, greeting, BRAND_PRIMARY, BRAND_ACCENT, COLOR_SEQ, PLOTLY_TEMPLATE

st.set_page_config(page_title="Churn | JohnDataViz", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
name_val = render_sidebar("Graficos_Churn")

st.markdown(f"""
<div class="page-header">
  <h2 style="margin:0 0 4px 0">📊 Análise de Churn</h2>
  <p style="margin:0; opacity:.85">{greeting(name_val, 'Gráficos de Churn')}</p>
</div>
""", unsafe_allow_html=True)

df = load_data()
churned = df[df["Churn Label"] == "Yes"]

# KPIs
total = len(df); n_churn = len(churned)
m1,m2,m3,m4 = st.columns(4)
m1.metric("Total de Clientes", f"{total:,}")
m2.metric("Cancelamentos", f"{n_churn:,}")
m3.metric("Taxa de Churn", f"{n_churn/total*100:.1f}%")
m4.metric("Tenure médio (churn)", f"{churned['Tenure in Months'].mean():.0f} meses")
st.markdown("---")

# Linha 1
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🔵 Distribuição Geral de Churn")
    vc = df["Churn Label"].value_counts().reset_index()
    vc.columns = ["Status","Qtd"]
    vc["Status"] = vc["Status"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig = px.pie(vc, values="Qtd", names="Status",
                 color="Status", color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                 template=PLOTLY_TEMPLATE, hole=0.45)
    fig.update_traces(textinfo="percent+label", textfont_size=14)
    fig.update_layout(height=370, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### 🔴 Categorias de Motivo do Cancelamento")
    cat = churned["Churn Category"].value_counts().reset_index()
    cat.columns = ["Categoria","Qtd"]
    fig2 = px.bar(cat, x="Qtd", y="Categoria", orientation="h",
                  color="Qtd", color_continuous_scale=["#4A90D9","#E8534A"],
                  template=PLOTLY_TEMPLATE, text="Qtd")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(height=370, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig2, use_container_width=True)

# Top 15 motivos
st.markdown("#### 📋 Top 15 Motivos Específicos de Cancelamento")
reasons = churned["Churn Reason"].value_counts().head(15).reset_index()
reasons.columns = ["Motivo","Qtd"]
fig3 = px.bar(reasons, x="Qtd", y="Motivo", orientation="h",
              color="Qtd", color_continuous_scale=["#4A90D9","#E8534A"],
              template=PLOTLY_TEMPLATE, text="Qtd")
fig3.update_traces(textposition="outside")
fig3.update_layout(height=440, yaxis=dict(categoryorder="total ascending"),
                   coloraxis_showscale=False, margin=dict(t=10,b=10,l=10,r=10))
st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")

# Linha 3
c3, c4 = st.columns(2)
with c3:
    st.markdown("#### 📄 Taxa de Churn por Tipo de Contrato")
    grp = df.groupby("Contract")["Churn Label"].apply(
        lambda x: (x=="Yes").sum()/len(x)*100).reset_index()
    grp.columns = ["Contrato","Taxa de Churn (%)"]
    fig4 = px.bar(grp, x="Contrato", y="Taxa de Churn (%)",
                  color="Taxa de Churn (%)", color_continuous_scale=["#27AE60","#F39C12","#E8534A"],
                  template=PLOTLY_TEMPLATE, text=grp["Taxa de Churn (%)"].map("{:.1f}%".format))
    fig4.update_traces(textposition="outside")
    fig4.update_layout(height=370, coloraxis_showscale=False, margin=dict(t=30,b=10,l=10,r=10))
    st.plotly_chart(fig4, use_container_width=True)

with c4:
    st.markdown("#### 🌐 Taxa de Churn por Tipo de Internet")
    df_int = df[df["Internet Type"].notna()]
    grp2 = df_int.groupby("Internet Type")["Churn Label"].apply(
        lambda x: (x=="Yes").sum()/len(x)*100).reset_index()
    grp2.columns = ["Tipo","Taxa de Churn (%)"]
    fig5 = px.bar(grp2, x="Tipo", y="Taxa de Churn (%)",
                  color="Tipo", color_discrete_sequence=COLOR_SEQ,
                  template=PLOTLY_TEMPLATE, text=grp2["Taxa de Churn (%)"].map("{:.1f}%".format))
    fig5.update_traces(textposition="outside")
    fig5.update_layout(height=370, showlegend=False, margin=dict(t=30,b=10,l=10,r=10))
    st.plotly_chart(fig5, use_container_width=True)

# Linha 4
c5, c6 = st.columns(2)
with c5:
    st.markdown("#### ⭐ Churn por Score de Satisfação")
    sat = df.groupby(["Satisfaction Score","Churn Label"]).size().reset_index(name="Qtd")
    sat["Status"] = sat["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig6 = px.bar(sat, x="Satisfaction Score", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE)
    fig6.update_layout(height=370, margin=dict(t=30,b=10,l=10,r=10))
    st.plotly_chart(fig6, use_container_width=True)

with c6:
    st.markdown("#### 📈 Distribuição do Churn Score")
    fig7 = px.histogram(df, x="Churn Score", color="Churn Label",
                        color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                        nbins=20, barmode="overlay", opacity=0.8,
                        template=PLOTLY_TEMPLATE, labels={"Churn Label":"Churn"})
    fig7.update_layout(height=370, margin=dict(t=30,b=10,l=10,r=10))
    st.plotly_chart(fig7, use_container_width=True)

# Tenure box
st.markdown("#### ⏱️ Tempo na Empresa (Tenure) vs Churn")
fig8 = px.box(df, x="Churn Label", y="Tenure in Months", color="Churn Label",
              color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
              template=PLOTLY_TEMPLATE,
              labels={"Churn Label":"Churn","Tenure in Months":"Meses na Empresa"}, points="outliers")
fig8.update_layout(height=380, showlegend=False, margin=dict(t=20,b=10,l=10,r=10))
st.plotly_chart(fig8, use_container_width=True)

# Pagamento
st.markdown("#### 💳 Taxa de Churn por Método de Pagamento")
grp3 = df.groupby("Payment Method")["Churn Label"].apply(
    lambda x: (x=="Yes").sum()/len(x)*100).reset_index()
grp3.columns = ["Método de Pagamento","Taxa de Churn (%)"]
fig9 = px.bar(grp3, x="Método de Pagamento", y="Taxa de Churn (%)",
              color="Método de Pagamento", color_discrete_sequence=COLOR_SEQ,
              template=PLOTLY_TEMPLATE, text=grp3["Taxa de Churn (%)"].map("{:.1f}%".format))
fig9.update_traces(textposition="outside")
fig9.update_layout(height=370, showlegend=False, margin=dict(t=30,b=10,l=10,r=10))
st.plotly_chart(fig9, use_container_width=True)

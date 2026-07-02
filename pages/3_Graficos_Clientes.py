import streamlit as st
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, render_sidebar, GLOBAL_CSS, greeting, BRAND_PRIMARY, BRAND_ACCENT, COLOR_SEQ, PLOTLY_TEMPLATE

st.set_page_config(page_title="Clientes | JohnDataViz", page_icon="👥", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
name_val = render_sidebar("Graficos_Clientes")

st.markdown(f"""
<div class="page-header">
  <h2 style="margin:0 0 4px 0">👥 Perfil e Comportamento dos Clientes</h2>
  <p style="margin:0; opacity:.85">{greeting(name_val, 'Gráficos de Clientes')}</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 📅 Distribuição de Idade dos Clientes")
    fig = px.histogram(df, x="Age", color="Churn Label",
                       color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                       nbins=30, barmode="overlay", opacity=0.8,
                       template=PLOTLY_TEMPLATE, labels={"Churn Label":"Churn","Age":"Idade"})
    fig.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### 🚻 Churn por Gênero")
    grp = df.groupby(["Gender","Churn Label"]).size().reset_index(name="Qtd")
    grp["Status"] = grp["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig2 = px.bar(grp, x="Gender", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE,
                  labels={"Gender":"Gênero","Qtd":"Clientes"})
    fig2.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("#### 💍 Churn por Estado Civil")
    grp3 = df.groupby(["Married","Churn Label"]).size().reset_index(name="Qtd")
    grp3["Casado"] = grp3["Married"].map({"Yes":"Casado(a)","No":"Solteiro(a)"})
    grp3["Status"] = grp3["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig3 = px.bar(grp3, x="Casado", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE,
                  labels={"Casado":"Estado Civil","Qtd":"Clientes"})
    fig3.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown("#### 👶 Churn por Dependentes")
    grp4 = df.groupby(["Dependents","Churn Label"]).size().reset_index(name="Qtd")
    grp4["Dep"] = grp4["Dependents"].map({"Yes":"Com Dependentes","No":"Sem Dependentes"})
    grp4["Status"] = grp4["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig4 = px.bar(grp4, x="Dep", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE, labels={"Dep":"","Qtd":"Clientes"})
    fig4.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig4, use_container_width=True)

c5, c6 = st.columns(2)
with c5:
    st.markdown("#### 💰 Cobrança Mensal por Status de Churn")
    fig5 = px.violin(df, y="Monthly Charge", x="Churn Label", color="Churn Label",
                     color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                     box=True, points=False, template=PLOTLY_TEMPLATE,
                     labels={"Monthly Charge":"Cobrança Mensal (R$)","Churn Label":"Churn"})
    fig5.update_layout(height=370, showlegend=False, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    st.markdown("#### 💎 CLTV por Status de Churn")
    fig6 = px.box(df, x="Churn Label", y="CLTV", color="Churn Label",
                  color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                  template=PLOTLY_TEMPLATE, points="outliers",
                  labels={"CLTV":"Customer Lifetime Value","Churn Label":"Churn"})
    fig6.update_layout(height=370, showlegend=False, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig6, use_container_width=True)

c7, c8 = st.columns(2)
with c7:
    st.markdown("#### 🤝 Indicações de Amigos e Churn")
    grp7 = df.groupby(["Referred a Friend","Churn Label"]).size().reset_index(name="Qtd")
    grp7["Indicou"] = grp7["Referred a Friend"].map({"Yes":"Indicou","No":"Não Indicou"})
    grp7["Status"]  = grp7["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig7 = px.bar(grp7, x="Indicou", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE, labels={"Indicou":"","Qtd":"Clientes"})
    fig7.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig7, use_container_width=True)

with c8:
    st.markdown("#### 🛡️ Churn por Segurança Online")
    grp8 = df.groupby(["Online Security","Churn Label"]).size().reset_index(name="Qtd")
    grp8["Seg"] = grp8["Online Security"].map({"Yes":"Com Segurança","No":"Sem Segurança"})
    grp8["Status"] = grp8["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
    fig8 = px.bar(grp8, x="Seg", y="Qtd", color="Status",
                  color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                  barmode="group", template=PLOTLY_TEMPLATE, labels={"Seg":"","Qtd":"Clientes"})
    fig8.update_layout(height=370, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("#### 🔍 Relação entre Tempo na Empresa e Cobrança Mensal")
fig9 = px.scatter(df, x="Tenure in Months", y="Monthly Charge", color="Churn Label",
                  color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                  opacity=0.5, template=PLOTLY_TEMPLATE,
                  labels={"Tenure in Months":"Meses na Empresa","Monthly Charge":"Cobrança Mensal (R$)","Churn Label":"Churn"},
                  hover_data=["Contract","Internet Service"])
fig9.update_layout(height=420, margin=dict(t=20,b=10,l=10,r=10))
st.plotly_chart(fig9, use_container_width=True)

st.markdown("#### 🏙️ Top 15 Cidades com Mais Cancelamentos")
city_churn = (df[df["Churn Label"]=="Yes"].groupby("City").size()
              .reset_index(name="Cancelamentos").sort_values("Cancelamentos",ascending=False).head(15))
fig10 = px.bar(city_churn, x="Cancelamentos", y="City", orientation="h",
               color="Cancelamentos", color_continuous_scale=["#4A90D9","#E8534A"],
               template=PLOTLY_TEMPLATE, text="Cancelamentos")
fig10.update_traces(textposition="outside")
fig10.update_layout(height=440, yaxis=dict(categoryorder="total ascending"),
                    coloraxis_showscale=False, margin=dict(t=10,b=10,l=10,r=10))
st.plotly_chart(fig10, use_container_width=True)

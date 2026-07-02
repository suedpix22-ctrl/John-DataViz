import streamlit as st
import plotly.express as px
import plotly.io as pio
import smtplib
import sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, render_sidebar, GLOBAL_CSS, greeting, BRAND_PRIMARY, BRAND_ACCENT, COLOR_SEQ, PLOTLY_TEMPLATE, INSIGHTS_REPORT

st.set_page_config(page_title="E-mail | JohnDataViz", page_icon="📧", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.warn-box { background:#FEF9E7; border-radius:10px; padding:16px 20px;
            border-left:4px solid #F39C12; color:#B7770D; margin:12px 0; }
.success-box { background:#EAFAF1; border-radius:10px; padding:16px 20px;
               border-left:4px solid #27AE60; color:#1E8449; margin:12px 0; }
</style>
""", unsafe_allow_html=True)

name_val = render_sidebar("Email")

st.markdown(f"""
<div class="page-header">
  <h2 style="margin:0 0 4px 0">📧 Enviar por E-mail</h2>
  <p style="margin:0; opacity:.85">{greeting(name_val, 'Envio por E-mail')}</p>
</div>
""", unsafe_allow_html=True)

df = load_data()

st.markdown("### 📨 O que deseja enviar?")
send_type = st.radio("", ["📊 Gráfico estático (imagem PNG)", "📝 Relatório escrito com insights e análises"],
                     horizontal=True)
st.markdown("---")

GRAFICOS = {
    "Distribuição de Churn (Pizza)": "pizza",
    "Categorias de Motivo do Cancelamento": "categorias",
    "Taxa de Churn por Tipo de Contrato": "contrato",
    "Taxa de Churn por Tipo de Internet": "internet",
    "Churn por Score de Satisfação": "satisfacao",
    "Cobrança Mensal por Status de Churn": "cobranca",
}

selected_chart_name = None
fig_to_send = None

if "Gráfico" in send_type:
    st.markdown("### 🖼️ Selecione o gráfico")
    selected_chart_name = st.selectbox("Gráfico:", list(GRAFICOS.keys()))
    key = GRAFICOS[selected_chart_name]
    churned = df[df["Churn Label"] == "Yes"]

    if key == "pizza":
        vc = df["Churn Label"].value_counts().reset_index()
        vc.columns = ["Status","Qtd"]
        vc["Status"] = vc["Status"].map({"Yes":"Cancelou","No":"Permaneceu"})
        fig_to_send = px.pie(vc, values="Qtd", names="Status",
                             color="Status", color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                             template=PLOTLY_TEMPLATE, hole=0.45, title="Distribuição de Churn")
    elif key == "categorias":
        cat = churned["Churn Category"].value_counts().reset_index()
        cat.columns = ["Categoria","Qtd"]
        fig_to_send = px.bar(cat, x="Qtd", y="Categoria", orientation="h",
                             color="Qtd", color_continuous_scale=["#4A90D9","#E8534A"],
                             template=PLOTLY_TEMPLATE, text="Qtd", title="Categorias de Motivo do Cancelamento")
    elif key == "contrato":
        grp = df.groupby("Contract")["Churn Label"].apply(lambda x: (x=="Yes").sum()/len(x)*100).reset_index()
        grp.columns = ["Contrato","Taxa de Churn (%)"]
        fig_to_send = px.bar(grp, x="Contrato", y="Taxa de Churn (%)",
                             color="Taxa de Churn (%)", color_continuous_scale=["#27AE60","#F39C12","#E8534A"],
                             template=PLOTLY_TEMPLATE, text=grp["Taxa de Churn (%)"].map("{:.1f}%".format),
                             title="Taxa de Churn por Tipo de Contrato")
    elif key == "internet":
        df_int = df[df["Internet Type"].notna()]
        grp2 = df_int.groupby("Internet Type")["Churn Label"].apply(lambda x: (x=="Yes").sum()/len(x)*100).reset_index()
        grp2.columns = ["Tipo","Taxa de Churn (%)"]
        fig_to_send = px.bar(grp2, x="Tipo", y="Taxa de Churn (%)",
                             color="Tipo", color_discrete_sequence=COLOR_SEQ,
                             template=PLOTLY_TEMPLATE, text=grp2["Taxa de Churn (%)"].map("{:.1f}%".format),
                             title="Taxa de Churn por Tipo de Internet")
    elif key == "satisfacao":
        sat = df.groupby(["Satisfaction Score","Churn Label"]).size().reset_index(name="Qtd")
        sat["Status"] = sat["Churn Label"].map({"Yes":"Cancelou","No":"Permaneceu"})
        fig_to_send = px.bar(sat, x="Satisfaction Score", y="Qtd", color="Status",
                             color_discrete_map={"Cancelou":BRAND_ACCENT,"Permaneceu":BRAND_PRIMARY},
                             barmode="group", template=PLOTLY_TEMPLATE, title="Churn por Score de Satisfação")
    elif key == "cobranca":
        fig_to_send = px.violin(df, y="Monthly Charge", x="Churn Label", color="Churn Label",
                                color_discrete_map={"Yes":BRAND_ACCENT,"No":BRAND_PRIMARY},
                                box=True, points=False, template=PLOTLY_TEMPLATE,
                                title="Cobrança Mensal por Status de Churn")

    if fig_to_send:
        st.markdown("**Pré-visualização:**")
        st.plotly_chart(fig_to_send, use_container_width=True)
else:
    st.markdown("### 📄 Pré-visualização do Relatório")
    with st.expander("Ver relatório completo", expanded=False):
        st.text(INSIGHTS_REPORT)

st.markdown("---")
st.markdown("### ✉️ Configurações de Envio")
st.markdown('<div class="warn-box">⚠️ <strong>Use Gmail com senha de app</strong> — não a senha normal. Acesse: Google → Minha Conta → Segurança → Senhas de app.</div>', unsafe_allow_html=True)

with st.form("email_form"):
    col1, col2 = st.columns(2)
    with col1:
        smtp_server  = st.text_input("Servidor SMTP", value="smtp.gmail.com")
        smtp_port    = st.number_input("Porta SMTP", value=587, step=1)
        sender_email = st.text_input("Seu e-mail (remetente)")
        sender_pass  = st.text_input("Senha de app", type="password")
    with col2:
        recipient    = st.text_input("E-mail do destinatário")
        sender_name_ = st.text_input("Seu nome (assinatura)", value=name_val or "")
    submitted = st.form_submit_button("📤 Enviar E-mail", use_container_width=True)

if submitted:
    if not sender_email or not sender_pass or not recipient:
        st.error("⛔ Preencha remetente, senha e destinatário.")
    else:
        try:
            msg = MIMEMultipart()
            msg["From"] = f"JohnDataViz <{sender_email}>"
            msg["To"]   = recipient
            assinatura  = f"\n\nAtenciosamente,\n{sender_name_ or 'Equipe JohnDataViz'}\nJohnDataViz\ncontato@johndataviz.com.br"

            if "Gráfico" in send_type:
                msg["Subject"] = f"[JohnDataViz] Análise de Churn — {selected_chart_name}"
                corpo = f"Prezado(a),\n\nSegue em anexo o gráfico: {selected_chart_name}.\n\nEste material faz parte da análise de Churn — Dataset Telco Customer Churn (Q3).\n{assinatura}"
                msg.attach(MIMEText(corpo, "plain", "utf-8"))
                img_bytes = pio.to_image(fig_to_send, format="png", width=900, height=500, scale=2)
                part = MIMEBase("image", "png")
                part.set_payload(img_bytes)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment",
                                filename=f"grafico_{selected_chart_name.replace(' ','_')}.png")
                msg.attach(part)
            else:
                msg["Subject"] = "[JohnDataViz] Relatório de Análise de Churn — Telco Dataset"
                corpo = f"Prezado(a),\n\nSegue o relatório analítico de Churn elaborado pela JohnDataViz.\n\n{INSIGHTS_REPORT}{assinatura}"
                msg.attach(MIMEText(corpo, "plain", "utf-8"))

            with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                server.starttls()
                server.login(sender_email, sender_pass)
                server.sendmail(sender_email, recipient, msg.as_string())

            st.markdown('<div class="success-box">✅ <strong>E-mail enviado com sucesso!</strong></div>', unsafe_allow_html=True)
        except smtplib.SMTPAuthenticationError:
            st.error("❌ Falha na autenticação. Verifique o e-mail e a senha de app.")
        except Exception as e:
            st.error(f"❌ Erro: {e}")

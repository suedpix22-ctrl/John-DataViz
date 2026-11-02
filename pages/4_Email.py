import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import smtplib
import io
import sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, render_sidebar, GLOBAL_CSS, greeting, BRAND_PRIMARY, BRAND_ACCENT, INSIGHTS_REPORT

st.set_page_config(page_title="E-mail | JohnDataViz", page_icon="📧", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
.info-box { background:#EBF5FB; border-radius:10px; padding:16px 20px;
            border-left:4px solid #4A90D9; color:#1A3C5E; margin:12px 0; }
.success-box { background:#EAFAF1; border-radius:10px; padding:16px 20px;
               border-left:4px solid #27AE60; color:#1E8449; margin:12px 0; }
.err-box { background:#FDEDEC; border-radius:10px; padding:16px 20px;
           border-left:4px solid #E8534A; color:#943126; margin:12px 0; }
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

# ── Escolha do conteúdo ───────────────────────────────────
st.markdown("### 📨 O que deseja enviar?")
send_type = st.radio("", ["📊 Gráfico estático (imagem PNG)",
                          "📝 Relatório escrito com insights e análises"],
                     horizontal=True)
st.markdown("---")

GRAFICOS = [
    "Distribuição de Churn (Pizza)",
    "Categorias de Motivo do Cancelamento",
    "Taxa de Churn por Tipo de Contrato",
    "Taxa de Churn por Tipo de Internet",
    "Churn por Score de Satisfação",
    "Cobrança Mensal por Status de Churn",
]

selected_chart_name = None


def gerar_grafico_png(nome):
    """Gera o gráfico escolhido com matplotlib e devolve os bytes PNG."""
    churned = df[df["Churn Label"] == "Yes"]
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)

    if nome == "Distribuição de Churn (Pizza)":
        vc = df["Churn Label"].value_counts()
        labels = ["Permaneceu" if i == "No" else "Cancelou" for i in vc.index]
        cores = [BRAND_ACCENT if l == "Cancelou" else BRAND_PRIMARY for l in labels]
        ax.pie(vc.values, labels=labels, colors=cores, autopct="%1.1f%%",
               startangle=90, textprops={"fontsize": 12})
        ax.set_title("Distribuição de Churn", fontsize=14, fontweight="bold")

    elif nome == "Categorias de Motivo do Cancelamento":
        cat = churned["Churn Category"].value_counts().sort_values()
        ax.barh(cat.index, cat.values, color=BRAND_ACCENT)
        ax.set_title("Categorias de Motivo do Cancelamento", fontsize=14, fontweight="bold")
        ax.set_xlabel("Quantidade")

    elif nome == "Taxa de Churn por Tipo de Contrato":
        grp = df.groupby("Contract")["Churn Label"].apply(lambda x: (x=="Yes").mean()*100).sort_values()
        ax.bar(grp.index, grp.values, color=BRAND_PRIMARY)
        for i, v in enumerate(grp.values):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=11)
        ax.set_title("Taxa de Churn por Tipo de Contrato", fontsize=14, fontweight="bold")
        ax.set_ylabel("Taxa de Churn (%)")

    elif nome == "Taxa de Churn por Tipo de Internet":
        df_int = df[df["Internet Type"].notna()]
        grp = df_int.groupby("Internet Type")["Churn Label"].apply(lambda x: (x=="Yes").mean()*100).sort_values()
        ax.bar(grp.index, grp.values, color=BRAND_PRIMARY)
        for i, v in enumerate(grp.values):
            ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=11)
        ax.set_title("Taxa de Churn por Tipo de Internet", fontsize=14, fontweight="bold")
        ax.set_ylabel("Taxa de Churn (%)")

    elif nome == "Churn por Score de Satisfação":
        piv = df.groupby(["Satisfaction Score", "Churn Label"]).size().unstack(fill_value=0)
        x = piv.index
        if "No" in piv.columns:
            ax.bar(x - 0.2, piv["No"], width=0.4, label="Permaneceu", color=BRAND_PRIMARY)
        if "Yes" in piv.columns:
            ax.bar(x + 0.2, piv["Yes"], width=0.4, label="Cancelou", color=BRAND_ACCENT)
        ax.set_title("Churn por Score de Satisfação", fontsize=14, fontweight="bold")
        ax.set_xlabel("Score de Satisfação"); ax.set_ylabel("Clientes"); ax.legend()

    elif nome == "Cobrança Mensal por Status de Churn":
        dados = [df[df["Churn Label"]=="No"]["Monthly Charge"],
                 df[df["Churn Label"]=="Yes"]["Monthly Charge"]]
        bp = ax.boxplot(dados, labels=["Permaneceu", "Cancelou"], patch_artist=True)
        for patch, cor in zip(bp["boxes"], [BRAND_PRIMARY, BRAND_ACCENT]):
            patch.set_facecolor(cor)
        ax.set_title("Cobrança Mensal por Status de Churn", fontsize=14, fontweight="bold")
        ax.set_ylabel("Cobrança Mensal (R$)")

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


if "Gráfico" in send_type:
    st.markdown("### 🖼️ Selecione o gráfico")
    selected_chart_name = st.selectbox("Gráfico:", GRAFICOS)
    st.markdown("**Pré-visualização:**")
    st.image(gerar_grafico_png(selected_chart_name))
else:
    st.markdown("### 📄 Pré-visualização do Relatório")
    with st.expander("Ver relatório completo", expanded=False):
        st.text(INSIGHTS_REPORT)

st.markdown("---")

# ── Envio: só pede o destinatário ─────────────────────────
st.markdown("### ✉️ Enviar")

# Verifica se as credenciais estão configuradas nos Secrets.
# Envolvido em try/except porque acessar st.secrets sem nenhum
# arquivo secrets.toml lança StreamlitSecretNotFoundError.
try:
    cfg_ok = "email" in st.secrets and all(
        k in st.secrets["email"] for k in ("sender", "password")
    )
except Exception:
    cfg_ok = False

if not cfg_ok:
    st.markdown("""
<div class="err-box">
⚙️ <strong>Envio não configurado.</strong> O administrador precisa cadastrar as credenciais
de e-mail nos <em>Secrets</em> do app (veja instruções abaixo).
</div>
""", unsafe_allow_html=True)
    with st.expander("📖 Como configurar (para o administrador)"):
        st.markdown("""
No **Streamlit Cloud** → seu app → **⋮ (Manage app)** → **Settings** → **Secrets**,
cole o seguinte (usando um Gmail com **senha de app**):

```toml
[email]
sender = "seuemail@gmail.com"
password = "xxxx xxxx xxxx xxxx"
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_name = "JohnDataViz"
```

Para rodar **localmente**, crie o arquivo `.streamlit/secrets.toml` com o mesmo conteúdo.
""")

with st.form("email_form"):
    recipient = st.text_input("📬 E-mail do destinatário", placeholder="destino@email.com")
    submitted = st.form_submit_button("📤 Enviar E-mail", use_container_width=True)

if submitted:
    if not recipient:
        st.markdown('<div class="err-box">⛔ Informe o e-mail do destinatário.</div>', unsafe_allow_html=True)
    elif not cfg_ok:
        st.markdown('<div class="err-box">⛔ Envio não configurado pelo administrador.</div>', unsafe_allow_html=True)
    else:
        try:
            sender      = st.secrets["email"]["sender"]
            password    = st.secrets["email"]["password"]
            smtp_server = st.secrets["email"].get("smtp_server", "smtp.gmail.com")
            smtp_port   = int(st.secrets["email"].get("smtp_port", 587))
            sender_name = st.secrets["email"].get("sender_name", "JohnDataViz")

            msg = MIMEMultipart()
            msg["From"] = f"{sender_name} <{sender}>"
            msg["To"]   = recipient
            assinatura  = f"\n\nAtenciosamente,\n{sender_name}\nJohnDataViz\ncontato@johndataviz.com.br"

            if "Gráfico" in send_type:
                msg["Subject"] = f"[JohnDataViz] Análise de Churn — {selected_chart_name}"
                corpo = (f"Prezado(a),\n\nSegue em anexo o gráfico: {selected_chart_name}.\n\n"
                         f"Este material faz parte da análise de Churn — Dataset Telco Customer Churn (Q3)."
                         f"{assinatura}")
                msg.attach(MIMEText(corpo, "plain", "utf-8"))
                img_bytes = gerar_grafico_png(selected_chart_name)
                part = MIMEBase("image", "png")
                part.set_payload(img_bytes)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment",
                                filename=f"grafico_{selected_chart_name.replace(' ','_')}.png")
                msg.attach(part)
            else:
                msg["Subject"] = "[JohnDataViz] Relatório de Análise de Churn — Telco Dataset"
                corpo = (f"Prezado(a),\n\nSegue o relatório analítico de Churn elaborado pela JohnDataViz."
                         f"\n\n{INSIGHTS_REPORT}{assinatura}")
                msg.attach(MIMEText(corpo, "plain", "utf-8"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, recipient, msg.as_string())

            st.markdown(f'<div class="success-box">✅ <strong>E-mail enviado com sucesso para {recipient}!</strong></div>',
                        unsafe_allow_html=True)
        except smtplib.SMTPAuthenticationError:
            st.markdown('<div class="err-box">❌ Falha na autenticação. Verifique as credenciais nos Secrets.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="err-box">❌ Erro: {e}</div>', unsafe_allow_html=True)

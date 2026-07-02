import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("telco.csv")
    return df

BRAND_PRIMARY   = "#1A3C5E"
BRAND_ACCENT    = "#E8534A"
BRAND_LIGHT     = "#4A90D9"
BRAND_SUCCESS   = "#27AE60"
BRAND_WARN      = "#F39C12"
BRAND_BG        = "#F4F6F9"

PLOTLY_TEMPLATE = "plotly_white"

COLORS_CHURN = {
    "Sim (Churn)": BRAND_ACCENT,
    "Não (Ativo)": BRAND_PRIMARY,
    "Yes": BRAND_ACCENT,
    "No": BRAND_PRIMARY,
}

COLOR_SEQ = [BRAND_PRIMARY, BRAND_ACCENT, BRAND_LIGHT,
             BRAND_SUCCESS, BRAND_WARN, "#8E44AD", "#16A085"]

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A3C5E 0%, #0f2540 100%) !important;
    min-width: 220px !important;
}
section[data-testid="stSidebar"] * { color: #ECF0F1 !important; }
section[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #fff !important;
    border-radius: 8px !important;
}

/* Menu links */
.nav-link {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 14px; border-radius: 8px;
    color: rgba(255,255,255,0.82) !important;
    text-decoration: none; font-size: 0.9rem;
    transition: background 0.15s;
    margin-bottom: 2px;
}
.nav-link:hover { background: rgba(255,255,255,0.12); color: #fff !important; }
.nav-link.active { background: rgba(255,255,255,0.18); color: #fff !important; font-weight: 600; }

.page-header {
    background: linear-gradient(135deg, #1A3C5E, #4A90D9);
    border-radius: 12px; padding: 24px 32px; color: white; margin-bottom: 24px;
}
footer { display: none; }
</style>
"""

PAGES = [
    ("🏠", "Home",                  "Home",                  "/"),
    ("📋", "Tabela de Dados",       "Tabela",                "/Tabela"),
    ("📊", "Gráficos — Churn",      "Graficos_Churn",        "/Graficos_Churn"),
    ("👥", "Gráficos — Clientes",   "Graficos_Clientes",     "/Graficos_Clientes"),
    ("📧", "Enviar por E-mail",     "Email",                 "/Email"),
    ("⬇️", "Download do Relatório", "Download",              "/Download"),
]

def render_sidebar(current_page: str = "Home"):
    """Renderiza sidebar única igual em todas as páginas."""
    with st.sidebar:
        st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

        # Logo / título
        st.markdown("""
<div style="padding: 16px 4px 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.15); margin-bottom: 12px;">
  <div style="font-size:1.1rem; font-weight:700; color:#fff; letter-spacing:0.3px;">📡 JohnDataViz</div>
  <div style="font-size:0.72rem; color:rgba(255,255,255,0.5); margin-top:2px;">Análise de Churn — Telco</div>
</div>
""", unsafe_allow_html=True)

        # Campo de nome
        name = st.text_input("👤 Seu nome", placeholder="Digite seu nome...",
                             key="user_name", label_visibility="collapsed")
        if name:
            st.markdown(f"<div style='font-size:0.82rem; color:rgba(255,255,255,0.7); padding:0 4px 8px 4px'>Olá, <b>{name}</b> ✨</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-size:0.82rem; color:rgba(255,255,255,0.45); padding:0 4px 8px 4px'>👤 Seu nome</div>",
                        unsafe_allow_html=True)

        # Separador + label
        st.markdown("<div style='font-size:0.7rem; color:rgba(255,255,255,0.4); text-transform:uppercase; letter-spacing:1px; padding: 4px 4px 6px 4px; border-top:1px solid rgba(255,255,255,0.1); margin-top:4px'>Menu</div>",
                    unsafe_allow_html=True)

        # Links de navegação
        for icon, label, page_key, _ in PAGES:
            active_class = "active" if page_key == current_page else ""
            st.markdown(
                f'<a class="nav-link {active_class}" href="/{page_key if page_key != "Home" else ""}" target="_self">'
                f'{icon} {label}</a>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1px; background:rgba(255,255,255,0.1); margin:12px 0'></div>",
                    unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.7rem; color:rgba(255,255,255,0.3); padding: 0 4px'>© 2026 JohnDataViz</div>",
                    unsafe_allow_html=True)

    return st.session_state.get("user_name", "")


def greeting(name: str, page: str) -> str:
    if name and name.strip():
        return f"Olá, <b>{name.strip()}</b>! Bem-vindo(a) à página de <b>{page}</b>."
    return f"Bem-vindo(a) à página de <b>{page}</b>."


INSIGHTS_REPORT = """
=============================================================
  DATAVIZ INSIGHTS ANALYTICS — RELATÓRIO DE CHURN TELCO
=============================================================

Preparado por: JohnDataViz
Referência: Dataset Telco Customer Churn (Q3)
Clientes analisados: 7.043

-------------------------------------------------------------
1. VISÃO GERAL DO CHURN
-------------------------------------------------------------
Do total de 7.043 clientes, 1.869 cancelaram os serviços
neste trimestre, representando uma taxa de churn de 26,5%.
Este índice é preocupante e indica a necessidade urgente de
ações de retenção.

-------------------------------------------------------------
2. PRINCIPAIS CAUSAS DO CANCELAMENTO
-------------------------------------------------------------
A análise das respostas pós-cancelamento revelou que:

• Concorrência (45%): O principal motivo. Concorrentes
  ofereceram melhores dispositivos (313 clientes), melhores
  ofertas comerciais (311) e mais dados (117). Isso indica
  que a empresa está perdendo a guerra de proposta de valor.

• Atitude/Relacionamento (17%): 314 clientes saíram devido
  à postura inadequada de suporte e atendimento. Um problema
  grave de experiência do cliente.

• Insatisfação com produto/serviço (16%): Qualidade de rede,
  velocidade de download, serviços limitados e falta de
  suporte técnico qualificado foram mencionados.

• Preço (11%): Tarifas consideradas elevadas, especialmente
  cobranças de longa distância e dados extras.

-------------------------------------------------------------
3. PERFIL DO CLIENTE QUE CANCELA
-------------------------------------------------------------
• Tipo de contrato: Clientes "Mês a Mês" têm taxa de churn
  de 45,8% — contra apenas 2,5% em contratos de 2 anos.
  É o fator isolado de maior impacto.

• Tempo na empresa: Clientes que cancelam têm, em média,
  apenas 18 meses de tenure (vs. 38 meses dos que ficam).
  Os primeiros 12 meses são críticos para retenção.

• Tipo de internet: Fibra Óptica concentra 66% dos churns
  entre assinantes de internet — paradoxalmente o produto
  premium é o que mais perde clientes, sinalizando problema
  de expectativa vs. entrega (preço alto, falhas de rede).

• Cobranças mensais: Clientes que cancelam pagam, em média,
  R$74/mês vs. R$61 dos que permanecem. Custo percebido alto
  combinado com insatisfação é explosivo.

• Satisfação: Clientes com score 1 e 2 representam a grande
  maioria dos cancelamentos — confirmando que a insatisfação
  é um preditor direto de churn.

• Serviços adicionais: Clientes sem segurança online, backup
  ou suporte premium cancelam em taxas significativamente
  maiores — indicando que o engajamento com o ecossistema
  de serviços é fator de retenção.

-------------------------------------------------------------
4. RECOMENDAÇÕES BASEADAS EM DADOS
-------------------------------------------------------------

▶ AÇÃO 1 — Programa de migração contratual
  Oferecer incentivos agressivos para clientes Mês a Mês
  migrarem para contratos anuais ou bianuais nos primeiros
  6 meses. Desconto, bônus de dados ou upgrade de plano.

▶ AÇÃO 2 — Jornada de onboarding nos primeiros 90 dias
  Implementar touchpoints proativos nos primeiros 3 meses
  (o período crítico), com NPS, ofertas personalizadas e
  suporte dedicado para novos assinantes.

▶ AÇÃO 3 — Revisão da estratégia de Fibra Óptica
  Alinhar expectativa e entrega: revisar SLAs de velocidade,
  reduzir falhas de rede e criar pacotes competitivos para
  combater os concorrentes neste segmento.

▶ AÇÃO 4 — Capacitação e cultura de atendimento
  Com 17% dos churns por "atitude", investir em treinamento
  de suporte ao cliente é ROI direto em retenção.

▶ AÇÃO 5 — Bundling de serviços adicionais
  Clientes com mais serviços têm menor churn. Criar pacotes
  acessíveis que incluam segurança online + backup + suporte
  premium aumenta o "stickiness" do cliente.

▶ AÇÃO 6 — Monitoramento de Churn Score e CLTV
  Clientes com Churn Score > 70 e CLTV alto devem receber
  contato proativo da equipe de retenção antes do cancelamento.

-------------------------------------------------------------
5. CONCLUSÃO
-------------------------------------------------------------
A empresa enfrenta um churn multidimensional: perdendo para
concorrentes em proposta de valor, falhando no atendimento e
cobrando mais de clientes menos comprometidos. A solução não
é pontual — exige uma estratégia integrada de produto,
precificação, experiência do cliente e retenção proativa.

=============================================================
JohnDataViz | contato@johndataviz.com.br
=============================================================
"""

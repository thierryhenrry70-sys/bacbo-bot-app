import streamlit as st
import pandas as pd
from datetime import datetime

# ========================
# 🔐 USUÁRIOS (VOCÊ EDITA AQUI)
# ========================
usuarios = {
    "cliente1": {"senha": "1234", "expira": "2026-12-31"},
    "cliente2": {"senha": "5678", "expira": "2026-10-01"},
}

# ========================
# 🔐 LOGIN
# ========================
st.set_page_config(page_title="BacBo Pro", layout="wide")

st.markdown("## 🔐 Acesso ao sistema")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if usuario not in usuarios or senha != usuarios[usuario]["senha"]:
    st.warning("🔒 Acesso inválido")
    st.stop()

# ⏳ Verificação de expiração
data_expira = datetime.strptime(usuarios[usuario]["expira"], "%Y-%m-%d")
if datetime.now() > data_expira:
    st.error("⛔ Acesso expirado")
    st.stop()

# ========================
# ⚙️ ESTADO
# ========================
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000
    st.session_state.historico = []
    st.session_state.perdas = 0
    st.session_state.aposta_pct = 0.02
    st.session_state.stop_loss = 800
    st.session_state.stop_win = 1200

# ========================
# 🎨 HEADER
# ========================
st.title("🔥 BacBo Pro Analyzer")
st.markdown(f"👤 Usuário: **{usuario}**")
st.markdown("### 💡 Sistema inteligente de controle e análise de apostas")
st.divider()

# ========================
# 📂 ABAS
# ========================
aba1, aba2, aba3 = st.tabs(["📊 Dashboard", "⚙️ Configurações", "📜 Histórico"])

# ========================
# 📊 DASHBOARD
# ========================
with aba1:

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Saldo", f"R$ {st.session_state.saldo:.2f}")
    col2.metric("📊 Jogadas", len(st.session_state.historico))

    lucro = st.session_state.saldo - 1000
    col3.metric("📈 Lucro", f"R$ {lucro:.2f}")

    st.divider()

    modo = st.toggle("🔥 Modo PRO")

    if modo:
        st.success("Modo PRO ativado")

    resultado = st.selectbox("Resultado da rodada", ["win", "loss"])

    if st.button("Registrar rodada"):
        aposta = st.session_state.saldo * st.session_state.aposta_pct

        if resultado == "win":
            st.session_state.saldo += aposta
            st.session_state.perdas = 0
        else:
            st.session_state.saldo -= aposta
            st.session_state.perdas += 1

        st.session_state.historico.append(st.session_state.saldo)

    # 🚫 Controle de perdas
    if st.session_state.perdas >= 3:
        st.error("🚫 Muitas perdas seguidas — parar!")
        st.stop()

    # 📈 Gráfico
    if len(st.session_state.historico) > 0:
        df = pd.DataFrame(st.session_state.historico, columns=["saldo"])
        st.subheader("📈 Evolução do saldo")
        st.line_chart(df, use_container_width=True)

# ========================
# ⚙️ CONFIGURAÇÕES
# ========================
with aba2:

    st.subheader("⚙️ Ajustes")

    st.session_state.aposta_pct = st.slider("Aposta (%)", 1, 10, int(st.session_state.aposta_pct*100)) / 100
    st.session_state.stop_loss = st.number_input("Stop Loss", value=st.session_state.stop_loss)
    st.session_state.stop_win = st.number_input("Stop Win", value=st.session_state.stop_win)

    st.info("Defina seus limites de segurança")

# ========================
# 📜 HISTÓRICO
# ========================
with aba3:

    st.subheader("📜 Histórico")

    if len(st.session_state.historico) > 0:
        df = pd.DataFrame(st.session_state.historico, columns=["saldo"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Sem dados ainda")

# ========================
# 🚨 REGRAS GLOBAIS
# ========================
if st.session_state.saldo <= st.session_state.stop_loss:
    st.error("🛑 Stop Loss atingido!")

if st.session_state.saldo >= st.session_state.stop_win:
    st.success("🎯 Stop Win atingido!")

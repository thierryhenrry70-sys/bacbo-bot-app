import streamlit as st

senha_correta = "1234"

senha = st.text_input("🔐 Digite a senha", type="password")

if senha != senha_correta:
    st.warning("Acesso restrito")
    st.stop()
    
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BacBo Pro", layout="wide")

# Estado inicial
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000
    st.session_state.historico = []

# Sidebar
st.sidebar.title("⚙️ Configurações")
aposta_pct = st.sidebar.slider("Aposta (%)", 1, 10, 2) / 100
stop_loss = st.sidebar.number_input("Stop Loss", value=800)
stop_win = st.sidebar.number_input("Stop Win", value=1200)

# Título
st.title("🔥 BacBo Pro Analyzer")

# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("💰 Saldo", f"R$ {st.session_state.saldo:.2f}")
col2.metric("📊 Jogadas", len(st.session_state.historico))

lucro = st.session_state.saldo - 1000
col3.metric("📈 Lucro", f"R$ {lucro:.2f}")

st.divider()

# Entrada
resultado = st.selectbox("Resultado", ["win", "loss"])

if st.button("Registrar"):
    aposta = st.session_state.saldo * aposta_pct

    if resultado == "win":
        st.session_state.saldo += aposta
    else:
        st.session_state.saldo -= aposta

    st.session_state.historico.append(st.session_state.saldo)

# Stops
if st.session_state.saldo <= stop_loss:
    st.error("🛑 Stop Loss atingido")

if st.session_state.saldo >= stop_win:
    st.success("🎯 Stop Win atingido")

# Gráfico
st.subheader("📈 Evolução do saldo")

df = pd.DataFrame(st.session_state.historico, columns=["saldo"])
st.line_chart(df)

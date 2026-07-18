import sys
import os
import sqlite3
from datetime import datetime
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
from agente import responder
from config import HISTORICO_DB

st.set_page_config(page_title="Alessandra — Assistente Financeira", page_icon="💰")


def criar_tabela_historico():
    conn = sqlite3.connect(HISTORICO_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao TEXT,
            papel TEXT,
            conteudo TEXT,
            criado_em TEXT
        )
    """)
    conn.commit()
    conn.close()


def salvar_mensagem(sessao, papel, conteudo):
    conn = sqlite3.connect(HISTORICO_DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO historico (sessao, papel, conteudo, criado_em) VALUES (?, ?, ?, ?)",
        (sessao, papel, conteudo, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


criar_tabela_historico()

if "sessao_id" not in st.session_state:
    st.session_state.sessao_id = datetime.now().strftime("%Y%m%d%H%M%S")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

st.title("💰 Alessandra")
st.caption("Assistente financeira educacional — mercado brasileiro (B3)")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["papel"]):
        st.markdown(msg["conteudo"])

pergunta = st.chat_input("Pergunte sobre investimentos, cotações ou notícias do mercado...")

if pergunta:
    st.session_state.mensagens.append({"papel": "user", "conteudo": pergunta})
    salvar_mensagem(st.session_state.sessao_id, "user", pergunta)

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Alessandra está pensando..."):
            resultado = responder(pergunta)
            resposta = resultado["resposta"]
        st.markdown(resposta)

    st.session_state.mensagens.append({"papel": "assistant", "conteudo": resposta})
    salvar_mensagem(st.session_state.sessao_id, "assistant", resposta)
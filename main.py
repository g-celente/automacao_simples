import streamlit as st
import pandas as pd
from src.utils.boletos import filtrar_boletos, calcular_indicadores

def main():
    st.set_page_config(page_title="Dashboard de Inadimplência", layout="wide")

    st.title("📊 Dashboard de Inadimplência")
    st.write("Análise de boletos atrasados e indicadores financeiros.")

    indicadores, df_boletos = calcular_indicadores()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📌 Inadimplência Geral (%)", value=f"{indicadores['Inadimplência Geral (%)']}%")

    with col2:
        st.metric(label="💰 Valor Total em Atraso (R$)", value=f"R$ {indicadores['Valor Total em Atraso (R$)']:,.2f}")

    with col3:
        st.metric(label="📅 Média de Atraso (dias)", value=f"{indicadores['Média de Atraso (dias)']:.1f}")

    st.divider()

    st.subheader("📄 Boletos Atrasados")
    if not df_boletos.empty:
        st.dataframe(
            df_boletos[['Nome do Paciente', 'CPF', 'Valor Total (R$)', 'Data de Vencimento', 'Status']],
            use_container_width=True
        )
    else:
        st.info("Nenhum boleto atrasado encontrado.")

    if not df_boletos.empty:
        st.subheader("📊 Distribuição dos Dias de Atraso")
        df_boletos['Dias de Atraso'] = (pd.to_datetime('today') - df_boletos['Data de Vencimento']).dt.days
        st.bar_chart(df_boletos['Dias de Atraso'])

if __name__ == "__main__":
    main()

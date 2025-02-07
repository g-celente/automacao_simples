import streamlit as st
import pandas as pd
from src.utils.boletos import filtrar_boletos, calcular_indicadores

def main():
    st.set_page_config(page_title="Dashboard de Inadimplência", layout="wide")

    st.title("📊 Dashboard de Inadimplência")
    st.write("Análise de boletos atrasados e indicadores financeiros.")

    indicadores, df_boletos, data_boletos = calcular_indicadores()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📌 Inadimplência Geral (%)", value=f"{indicadores['Inadimplência Geral (%)']}%")

    with col2:
        st.metric(label="💰 Valor Total em Atraso (R$)", value=f"R$ {indicadores['Valor Total em Atraso (R$)']:,.2f}")

    with col3:
        st.metric(label="📅 Média de Atraso (dias)", value=f"{indicadores['Média de Atraso (dias)']:.1f}")

    st.divider()

    st.write('Quantidades de Boletos Atrasados por dia:')

    col4, col5, col6, col7 = st.columns(4)

    with col4:
        st.metric(label='Até 15 dias', value=data_boletos['Até 15 dias'])

    with col5:
        st.metric(label='Até 30 dias', value=data_boletos['Até 30 dias'])

    with col6:
        st.metric(label='Até 60 dias', value=data_boletos['Até 60 dias']) 

    with col7:
        st.metric(label='Mais que 60 dias', value=data_boletos['Mais que 60 dias']) 

    

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

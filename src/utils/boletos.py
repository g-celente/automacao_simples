import pandas as pd
from datetime import datetime

def filtrar_boletos(file_path):
    df = pd.read_excel(file_path)

    df['Data de Vencimento'] = pd.to_datetime(df['Data de Vencimento'], errors='cors')

    hoje = datetime.today()
    boletos_vencidos = df[(df['Data de Vencimento'] < hoje) & (df['Status'] == 'Pendente')]

    return boletos_vencidos, df

def calcular_indicadores():

    file_path = 'src/database/database.xlsx'

    df_boletos, df_total = filtrar_boletos(file_path)

    total_boletos_atrasados = len(df_boletos)
    total_boletos_emitidos = len(df_total)
    valor_total_atraso = df_boletos['Valor Total (R$)'].sum()

    df_boletos['Dias de Atraso'] = (datetime.today() - df_boletos['Data de Vencimento']).dt.days
    media_atraso = df_boletos['Dias de Atraso'].mean()

    inadimplencia_geral = (total_boletos_atrasados / total_boletos_emitidos) * 100 if total_boletos_emitidos > 0 else 0

    indicadores = {
        "Inadimplência Geral (%)": round(inadimplencia_geral, 2),
        "Valor Total em Atraso (R$)": round(valor_total_atraso, 2),
        "Média de Atraso (dias)": round(media_atraso, 2)
    }

    return indicadores, df_boletos
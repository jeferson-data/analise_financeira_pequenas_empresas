import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Análise Financeira para Pequenas Empresas")

# Upload do arquivo
arquivo = st.file_uploader("Envie seu arquivo financeiro (CSV ou Excel)", type=["csv", "xlsx"])

if arquivo:
    # Leitura do arquivo
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    # Padronizar nomes de colunas (caso venham em minúsculas ou com espaços)
    df.columns = [col.strip().capitalize() for col in df.columns] 
    
    # Verificação de campos essenciais
    campos_necessarios = ["Data", "Tipo", "Categoria", "Valor"]
    if not all(campo in df.columns for campo in campos_necessarios):
        st.error("❌ O arquivo está incompleto ou com nomes de colunas incorretos. Verifique se contém: Data, Tipo, Categoria e Valor.")
        st.stop()

    # Exibição dos dados
    st.subheader("📁 Dados Carregados")
    st.dataframe(df)

    # Cálculos principais
    receita = df[df["Tipo"] == "Receita"]["Valor"].sum()
    despesa = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    lucro = receita - despesa

    # Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {receita:,.2f}")
    col2.metric("Despesa Total", f"R$ {despesa:,.2f}")
    col3.metric("Lucro Líquido", f"R$ {lucro:,.2f}")

    # Gráfico de pizza por categoria
    st.subheader("📌 Distribuição por Categoria")
    fig = px.pie(df, names="Categoria", values="Valor", title="Categorias Financeiras")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de linha por data
    st.subheader("📈 Evolução Financeira ao Longo do Tempo")
    df["Data"] = pd.to_datetime(df["Data"])
    df_agrupado = df.groupby(["Data", "Tipo"])["Valor"].sum().reset_index()
    fig2 = px.line(df_agrupado, x="Data", y="Valor", color="Tipo", markers=True)
    st.plotly_chart(fig2, use_container_width=True)


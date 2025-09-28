import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import tempfile
import os

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

    # Criar pasta de imagens se não existir
    os.makedirs("imagens", exist_ok=True)

    # Salvar os gráficos como imagem
    fig.write_image("imagens/grafico_pizza.png")
    fig2.write_image("imagens/grafico_linha.png")

    # Função para gerar o PDF com os gráficos
    def gerar_pdf(receita, despesa, lucro):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório Financeiro", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Receita Total: R$ {receita:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Despesa Total: R$ {despesa:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Lucro Líquido: R$ {lucro:,.2f}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt="Gráfico de Distribuição por Categoria:", ln=True)
        pdf.image("imagens/grafico_pizza.png", w=180)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Evolução Financeira ao Longo do Tempo:", ln=True)
        pdf.image("imagens/grafico_linha.png", w=180)

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp.name)
        return temp.name

    # Botão para exportar o PDF
    st.subheader("📄 Exportar Relatório")
    if st.button("Gerar PDF com Gráficos"):
        caminho_pdf = gerar_pdf(receita, despesa, lucro)
        with open(caminho_pdf, "rb") as f:
            st.download_button("📥 Clique para baixar o PDF", f, file_name="relatorio_financeiro.pdf")
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("noticias_completas.csv")
        return df
    except FileNotFoundError:
        st.error("Arquivo 'noticias_completas.csv' não encontrado. Execute a coleta de dados primeiro.")
        return pd.DataFrame()

df = carregar_dados()

st.sidebar.header('🔍 Configurações', divider='blue')

data_expander = st.sidebar.expander("# **Exibir Dados**", icon=":material/table:")
with data_expander:
    with st.form("dados_form"):
        mostrar_tabela = st.checkbox("Exibir tabela de dados")
        mostrar_resumo = st.checkbox("Resumo estatístico dos dados")
        dados_form_submit = st.form_submit_button("Mostrar")

graph_expander = st.sidebar.expander("# **Gráficos**", icon=":material/monitoring:")
with graph_expander:
    with st.form("graficos_form"):
        mostrar_grafico_categorias = st.checkbox("Distribuição de Categorias")
        mostrar_grafico_fontes = st.checkbox("Distribuição por Fonte")
        graficos_form_submit = st.form_submit_button("Gerar Gráficos")

st.title("📰 Dashboard de Notícias Mais Lidas")

if df.empty:
    st.warning("Nenhuma notícia disponível. Execute a coleta de dados.")
else:
    st.sidebar.subheader("🎯 Filtrar Dados")
    categorias = df["Categoria"].unique()
    fontes = df["Fonte"].unique()

    categoria_selecionada = st.sidebar.multiselect("Filtrar por Categoria:", categorias, default=categorias)
    fonte_selecionada = st.sidebar.multiselect("Filtrar por Fonte:", fontes, default=fontes)

    df_filtrado = df[df["Categoria"].isin(categoria_selecionada) & df["Fonte"].isin(fonte_selecionada)]

    if dados_form_submit:
        if mostrar_tabela:
            st.subheader("📋 Dados das Notícias")
            st.write(df_filtrado)
        
        if mostrar_resumo:
            st.subheader("📊 Resumo Estatístico")
            st.write(df_filtrado.describe(include="all"))

    if graficos_form_submit:
        if mostrar_grafico_categorias:
            st.subheader("📊 Distribuição das Categorias")
            categoria_counts = df_filtrado["Categoria"].value_counts().reset_index()
            categoria_counts.columns = ["Categoria", "Quantidade"]
            
            fig = px.bar(categoria_counts, x="Categoria", y="Quantidade", 
                         title="Quantidade de Notícias por Categoria",
                         text_auto=True, color="Categoria")
            st.plotly_chart(fig, use_container_width=True)

        if mostrar_grafico_fontes:
            st.subheader("📊 Distribuição das Notícias por Fonte")
            fonte_counts = df_filtrado["Fonte"].value_counts().reset_index()
            fonte_counts.columns = ["Fonte", "Quantidade"]
            
            fig = px.pie(fonte_counts, names="Fonte", values="Quantidade",
                         title="Proporção de Notícias por Fonte", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Music Analytics", layout="wide")

st.title("🎵 Dashboard de Análise Musical")
st.markdown("Explore como diferentes gêneros se comportam em termos de batida e intensidade.")

# Carregar os dados
df = pd.read_csv('dataset.csv')

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros")
generos_disponiveis = df['track_genre'].unique()
selecao_generos = st.sidebar.multiselect(
    "Escolha os gêneros para comparar:",
    options=generos_disponiveis,
    default=['rock', 'pop', 'hip-hop', 'reggaeton', 'kids']
)

# --- FILTRAGEM ---
df_filtrado = df[df['track_genre'].isin(selecao_generos)]
resumo = df_filtrado.groupby('track_genre')[['danceability', 'energy', 'valence']].mean().reset_index()

# --- VISUALIZAÇÃO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Dançabilidade por Gênero")
    fig1 = px.bar(resumo, x='track_genre', y='danceability', color='energy',
                  color_continuous_scale='Viridis')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Vibe: Energia vs Positividade (Valence)")
    # Valence mede se a música é alegre (perto de 1) ou triste (perto de 0)
    fig2 = px.scatter(resumo, x='valence', y='energy', text='track_genre',
                      size='danceability', color='track_genre')
    st.plotly_chart(fig2, use_container_width=True)
    # --- TABELA DE DESTAQUES ---
st.divider() # Cria uma linha divisória para organizar o visual
st.subheader(f"Top 5 Músicas Populares em: {', '.join(selecao_generos)}")

# Pegamos o dataframe filtrado, ordenamos pela popularidade e mostramos as colunas principais
top_musicas = df_filtrado.sort_values(by='popularity', ascending=False).head(5)

# Exibindo a tabela com colunas selecionadas para não poluir o site
st.table(top_musicas[['track_name', 'artists', 'popularity', 'track_genre']])

# --- CARDS DE RESUMO (KPIs) ---
st.divider()
st.subheader("Resumo Estatístico da Seleção")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total de Músicas", len(df_filtrado))
with kpi2:
    st.metric("Média de Dançabilidade", f"{df_filtrado['danceability'].mean():.2f}")
with kpi3:
    st.metric("Média de Energia", f"{df_filtrado['energy'].mean():.2f}")

# --- BOTÃO DE DOWNLOAD (NA BARRA LATERAL) ---
# Prepara o arquivo para baixar
csv = df_filtrado.to_csv(index=False).encode('utf-8')

st.sidebar.markdown("---") # Adiciona uma linha na lateral para separar
st.sidebar.download_button(
    label="📥 Baixar dados filtrados (CSV)",
    data=csv,
    file_name='meu_relatorio_musical.csv',
    mime='text/csv',

)

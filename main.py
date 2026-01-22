import pandas as pd

df = pd.read_csv('dataset.csv')

# 1. Agrupar por gênero e calcular a média de Dançabilidade e Energia
resumo_generos = df.groupby('track_genre')[['danceability', 'energy']].mean().reset_index()

# 2. Ordenar para ver os 10 mais "dançáveis"
mais_dancaveis = resumo_generos.sort_values(by='danceability', ascending=False).head(10)

print("--- OS 10 GÊNEROS MAIS DANÇÁVEIS ---")
print(mais_dancaveis)

# 3. Ver a média geral de Energia de todo o arquivo
media_energia = df['energy'].mean()
print(f"\nA energia média de todas as músicas é: {media_energia:.2f}")
import plotly.express as px

# Criar um gráfico de barras com os 10 mais dançáveis
fig = px.bar(mais_dancaveis, 
             x='track_genre', 
             y='danceability',
             color='energy', # As cores vão mostrar quem tem mais energia
             title='Top 10 Gêneros Mais Dançáveis e sua Energia',
             labels={'track_genre': 'Gênero', 'danceability': 'Dançabilidade'})

# Isso vai abrir uma aba no navegador com o gráfico!

fig.show()

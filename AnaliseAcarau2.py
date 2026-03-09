import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyhomogeneity as hg

# 1. Preparação (Agrupando dados de Acaraú)
df = pd.read_csv('acarau.txt', sep=';', encoding='latin1')
df_anual = df.groupby('Anos')['Total'].sum().reset_index()
df_anual = df_anual[df_anual['Anos'] < 2025] # Removendo ano incompleto

# 2. Execução do Teste de Pettitt
res_pet = hg.pettitt_test(df_anual['Total'])
cp = res_pet.cp # Índice da quebra
ano_quebra = df_anual.iloc[cp]['Anos'] # Ano exato do degrau

# Médias antes e depois
media_antes = df_anual.iloc[:cp]['Total'].mean()
media_depois = df_anual.iloc[cp:]['Total'].mean()

# 3. Gráfico do Degrau
plt.figure(figsize=(12, 6))
plt.plot(df_anual['Anos'], df_anual['Total'], color='#1f77b4', alpha=0.4, label='Precipitação Real')

# Desenhando o Degrau (Linhas Verdes Tracejadas)
# Período A
plt.hlines(y=media_antes, xmin=df_anual['Anos'].min(), xmax=ano_quebra, 
           colors='green', linestyles='--', linewidth=2.5, label=f'Média 1: {media_antes:.1f}mm')

# Período B (Começa onde termina o A)
plt.hlines(y=media_depois, xmin=ano_quebra, xmax=df_anual['Anos'].max(), 
           colors='green', linestyles='--', linewidth=2.5, label=f'Média 2: {media_depois:.1f}mm')

# Linha Vertical no Ano da Quebra
plt.axvline(x=ano_quebra, color='red', linestyle='-', alpha=0.7, linewidth=1.5)

# Anotação do Ano da Quebra
plt.annotate(f'Quebra em {ano_quebra}', xy=(ano_quebra, media_depois), xytext=(ano_quebra+2, media_depois+200),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))

plt.title(f'Detecção de Quebra de Regime Pluviométrico - Acaraú/CE', fontsize=14)
plt.ylabel('Precipitação Anual (mm)')
plt.legend()
plt.grid(True, alpha=0.2)
plt.show()

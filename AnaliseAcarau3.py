import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
import pyhomogeneity as hg

# 1. Carregamento e Agrupamento (Acaraú)
df = pd.read_csv('acarau.txt', sep=';', encoding='latin1')
df_anual = df.groupby('Anos')['Total'].sum().reset_index()
df_anual = df_anual[df_anual['Anos'] < 2025] # Evitar ano incompleto

# 2. Cálculos Estatísticos
res_mk = mk.original_test(df_anual['Total'])
res_pet = hg.pettitt_test(df_anual['Total'])

# Parâmetros do Pettitt (O Degrau)
cp = res_pet.cp
ano_quebra = df_anual.iloc[cp]['Anos']
media_antes = df_anual.iloc[:cp]['Total'].mean()
media_depois = df_anual.iloc[cp:]['Total'].mean()

# Parâmetros do Mann-Kendall (A Rampa)
# Usamos o Sen's Slope para desenhar a inclinação correta
slope = res_mk.slope
intercept = np.mean(df_anual['Total']) - slope * np.mean(df_anual['Anos'])
linha_mk = slope * df_anual['Anos'] + intercept

# 3. Visualização Dupla
plt.figure(figsize=(14, 7))
plt.plot(df_anual['Anos'], df_anual['Total'], color='silver', label='Precipitação Real', marker='o', alpha=0.5)

# --- LINHA TRACEJADA 1: MANN-KENDALL (RAMPA) ---
plt.plot(df_anual['Anos'], linha_mk, color='red', linestyle='--', linewidth=2, 
         label=f'Tendência Mann-Kendall (Slope: {slope:.2f})')

# --- LINHA TRACEJADA 2: PETTITT (DEGRAU VERDE) ---
# Parte A do degrau
plt.hlines(y=media_antes, xmin=df_anual['Anos'].min(), xmax=ano_quebra, 
           colors='green', linestyles='--', linewidth=3, label=f'Média Pré-{ano_quebra}')
# Parte B do degrau
plt.hlines(y=media_depois, xmin=ano_quebra, xmax=df_anual['Anos'].max(), 
           colors='green', linestyles='--', linewidth=3, label=f'Média Pós-{ano_quebra}')

# Marcação vertical do ponto de mudança
plt.axvline(x=ano_quebra, color='black', alpha=0.3, label='Ponto de Ruptura')

# Ajustes Finais
plt.title(f'Análise de Estacionariedade e Tendência: Posto Acaraú/CE', fontsize=14)
plt.xlabel('Ano')
plt.ylabel('Precipitação Acumulada (mm)')
plt.legend(loc='upper right', frameon=True)
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

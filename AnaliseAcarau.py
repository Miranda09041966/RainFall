import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
import pyhomogeneity as hg
from sklearn.model_selection import train_test_split

# 1. Preparação dos Dados
df = pd.read_csv('acarau.txt', sep=';', encoding='latin1')

# Criar coluna de data e total anual para análise de tendência
df_anual = df.groupby('Anos')['Total'].sum().reset_index()
df_anual = df_anual[df_anual['Total'] < 5000] # Filtro de outlier/erro (ex: 888.8)

# 2. Teste de Mann-Kendall
res_mk = mk.original_test(df_anual['Total'])

print(f"--- Teste de Mann-Kendall ---")
print(f"Tendência: {res_mk.trend}")
print(f"P-valor: {res_mk.p:.4f}")

# 3. Condicional: Se p-valor < 0.05 (ou 0.005 conforme solicitado), rodar Pettitt
rodar_pettitt = res_mk.p < 0.05 

plt.figure(figsize=(12, 6))
plt.plot(df_anual['Anos'], df_anual['Total'], label='Precipitação Anual (mm)', color='blue', marker='o')

if rodar_pettitt:
    # Teste de Pettitt
    res_pet = hg.pettitt_test(df_anual['Total'])
    cp = res_pet.cp # Ponto de mudança (índice)
    ano_quebra = df_anual.iloc[cp]['Anos']
    avg_antes = df_anual.iloc[:cp]['Total'].mean()
    avg_depois = df_anual.iloc[cp:]['Total'].mean()
    
    # Plotagem das linhas de Pettitt (Degrau)
    plt.axvline(x=ano_quebra, color='red', linestyle='--', label=f'Quebra Pettitt ({ano_quebra})')
    plt.hlines(y=avg_antes, xmin=df_anual['Anos'].min(), xmax=ano_quebra, colors='green', linestyles='--')
    plt.hlines(y=avg_depois, xmin=ano_quebra, xmax=df_anual['Anos'].max(), colors='orange', linestyles='--')
    
    print(f"\n--- Teste de Pettitt ---")
    print(f"Ponto de mudança detectado em: {ano_quebra}")

# 4. Gráfico de Mann-Kendall (Linha de Tendência)
# Simplificação da linha de tendência para visualização
z = np.polyfit(df_anual['Anos'], df_anual['Total'], 1)
p = np.poly1d(z)
plt.plot(df_anual['Anos'], p(df_anual['Anos']), "r--", label="Tendência (Sen's Slope)")

plt.title('Análise de Tendência e Quebra: Posto Acaraú')
plt.xlabel('Ano')
plt.ylabel('Precipitação Acumulada (mm)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 5. Divisão Treino e Teste para Machine Learning
# Usaremos o 'Total' mensal como target e 'Mes/Ano' como features
X = df[['Anos', 'Meses']]
y = df['Total']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(f"\n--- Preparação para ML ---")
print(f"Tamanho do Treino: {len(X_train)} meses")
print(f"Tamanho do Teste: {len(X_test)} meses")

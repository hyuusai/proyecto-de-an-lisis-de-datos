# Importación de las librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carga del dataset con manejo de excepciones
try:
    df = pd.read_csv('2019.csv')
    df.columns = df.columns.str.strip()  # Eliminar espacios innecesarios en nombres de columnas
except FileNotFoundError:
    print("Archivo '2019.csv' no encontrado.")
    exit()
except Exception as e:
    print("Error al cargar el archivo:", e)
    exit()

# Información básica del dataset
print("=== Información general del dataset ===")
print(df.info())             # Información general: columnas, tipo de datos, nulos
print("\n=== Estadísticas descriptivas ===")
print(df.describe())         # Estadísticas básicas
print("\n=== Dimensiones del dataset (filas, columnas) ===")
print(df.shape)

# Valores nulos
print("\n=== Valores nulos por columna ===")
print(df.isnull().sum())

# Primeras 10 filas
print("\n=== Primeras 10 filas ===")
print(df.head(10))

# Tipos de datos por columna
print("\n=== Tipos de datos por columna ===")
print(df.dtypes)

#Visualización exploratoria básica: Gráfico de barras agrupadas
# Seleccionar los 12 países con mayor felicidad
top_12 = df.sort_values(by='Score', ascending=False).head(12)

# Preparar datos para el gráfico de barras
countries = top_12['Country or region'].values
gdp = top_12['GDP per capita'].values
score = top_12['Score'].values
x = np.arange(len(countries))
width = 0.35
multiplier = 0

# Crear gráfico de barras agrupadas
fig, ax = plt.subplots(figsize=(14, 7), layout='constrained')
data = {'PIB per cápita': gdp, 'Felicidad': score}

for label, values in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, values, width, label=label)
    ax.bar_label(rects, padding=3, fontsize=8)
    multiplier += 1

ax.set_ylabel('Valor')
ax.set_title('Comparación: PIB per cápita vs. Puntaje de Felicidad (Top 12 países)')
ax.set_xticks(x + width / 2)
ax.set_xticklabels(countries, rotation=45, ha='right')
ax.legend(loc='upper left')
ax.set_ylim(0, max(gdp.max(), score.max()) + 1)

# Segunda visualización: gráfico de los 12 países más felices
labels = top_12['Country or region']
sizes = top_12['Score']
explode = [0.05] * len(labels)

fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
       shadow=True, startangle=90)
ax.set_title("Top 12 países según nivel de felicidad (2019)")
ax.axis('equal')
plt.tight_layout()

plt.show()


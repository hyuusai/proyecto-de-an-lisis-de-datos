# Importación de las librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carga del dataset con manejo de excepciones
try:
    dataframes = []

    for year in [2018, 2019]:
        import os
        current_dir = os.path.dirname(__file__)
        file = os.path.join(current_dir, f'{year}.csv')

        df = pd.read_csv(file)  # Leer archivo CSV del año
        df.columns = df.columns.str.strip()  # Eliminar espacios extra en nombres de columnas
        df['year'] = year  # Añadir columna del año

        # Normalizar el nombre de la columna del país
        if 'Country' in df.columns:
            df.rename(columns={'Country': 'Country or region'}, inplace=True)
        
        # Normalizar el nombre del puntaje de felicidad
        if 'Happiness Score' in df.columns:
            df.rename(columns={'Happiness Score': 'Score'}, inplace=True)

        # Validar que la columna 'Score' exista
        if 'Score' not in df.columns:
            raise ValueError(f"Columna 'Score' no encontrada en el archivo {file}")

        # Guardar solo columnas necesarias
        dataframes.append(df[['Country or region', 'Score', 'year']])

    # Unir los DataFrames de ambos años
    all_data = pd.concat(dataframes)

except FileNotFoundError as e:
    print(f"Archivo no encontrado: {e.filename}")
    exit()
except Exception as e:
    print(f"Error al cargar los archivos: {e}")
    exit()

# Información básica del dataset
print("\n=== Información general del dataset ===")
print(all_data.info())  # Tipos de datos, nulos, columnas

print("\n=== Estadísticas descriptivas ===")
print(all_data.describe())  # Promedios, min, max, etc.

print("\n=== Dimensiones del dataset ===")
print(all_data.shape)  # (filas, columnas)

# Identificación de valores nulos
print("\n=== Valores nulos por columna ===")
print(all_data.isnull().sum())

# Identificar tipos de datos por columna
print("\n=== Tipos de datos por columna ===")
print(all_data.dtypes)

# Visualización exploratoria básica (gráfico de barras horizontales)
# Seleccionar los 12 países más felices en 2019
top12_2019 = all_data[all_data['year'] == 2019].sort_values(by='Score', ascending=False).head(12)
top12_countries = top12_2019['Country or region'].values

# Filtrar datos sólo de esos países para 2018 y 2019
filtered_data = all_data[all_data['Country or region'].isin(top12_countries)]

# Preparar datos para el gráfico
people = top12_countries
y_pos = np.arange(len(people))

score_2018 = []
score_2019 = []

# Obtener los valores de felicidad por país para cada año
for country in people:
    val_2018 = filtered_data[(filtered_data['Country or region'] == country) & (filtered_data['year'] == 2018)]['Score']
    val_2019 = filtered_data[(filtered_data['Country or region'] == country) & (filtered_data['year'] == 2019)]['Score']
    score_2018.append(val_2018.values[0] if not val_2018.empty else 0)
    score_2019.append(val_2019.values[0] if not val_2019.empty else 0)

# Errores aleatorios para el estilo de la gráfica
error_2018 = np.random.rand(len(people)) * 0.1
error_2019 = np.random.rand(len(people)) * 0.1

# Crear gráfico de barras horizontales
fig, ax = plt.subplots(figsize=(12, 8))

# Barras para 2018 y 2019
ax.barh(y_pos - 0.2, score_2018, xerr=error_2018, height=0.4, align='center', label='2018')
ax.barh(y_pos + 0.2, score_2019, xerr=error_2019, height=0.4, align='center', label='2019')

# Configurar el gráfico
ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.invert_yaxis()  # Países con mayor felicidad arriba
ax.set_xlabel('Puntaje de Felicidad')
ax.set_title('Evolución de la felicidad en los 12 países más felices (2018 vs 2019)')
ax.legend()

plt.tight_layout()
plt.show()

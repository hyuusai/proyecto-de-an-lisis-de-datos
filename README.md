# Análisis y Visualización de Datos de Felicidad Mundial (2018–2019)

## Proyecto_final:
Este script en Python permite cargar, procesar y visualizar datos sobre el índice de felicidad mundial para los años 2018 y 2019.

El programa incluye un menú interactivo para mostrar distintos tipos de gráficos: líneas, barras, mapas, dispersión y distribución.


os → Manejo de rutas y archivos del sistema
pandas → Manipulación y análisis de datos.
matplotlib.pyplot → Creación de gráficos básicos.
seaborn → Visualización estadística avanzada (basado en matplotlib).
folium → Mapas interactivos.
requests → Descarga de archivos y datos vía HTTP.
webbrowser → Apertura de archivos HTML directamente en el navegador.

### Importación de librerías:

| librerias             |                                                                 |
| ----------------- | ------------------------------------------------------------------ |
| os |  Manejo de rutas y archivos del sistema |
| pandas | Manipulación y análisis de datos |
| matplotlib.pyplot | Creación de gráficos básicos |
| seaborn  | Visualización estadística avanzada (basado en matplotlib) |
| folium | Mapas interactivos |
| requests | Descarga de archivos y datos vía HTTP |
| webbrowser | Apertura de archivos HTML directamente en el navegador  |

### Carga y preparación de datos

Determina el directorio donde está el script.

Construye rutas absolutas para los archivos CSV de 2018 y 2019.

```BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_2018 = os.path.join(BASE_DIR, "2018.csv")
file_2019 = os.path.join(BASE_DIR, "2019.csv")
```

Carga los datasets y les agrega una columna con el año correspondiente

```df_2018 = pd.read_csv(file_2018)
df_2019 = pd.read_csv(file_2019)
df_2018["year"] = 2018
df_2019["year"] = 2019
```

Combina los dos datasets en uno solo
```all_data = pd.concat([df_2018, df_2019], ignore_index=True)
```

Limpia nombres de países y los normaliza usando un diccionario de reemplazo para evitar inconsistencias 
```all_data["Country or region"] = all_data["Country or region"].str.strip()
all_data["Country or region"] = all_data["Country or region"].replace(country_replacements)
```

Traduce los nombres de las columnas de factores a español para usarlos en las visualizaciones
```factors = {
    'GDP per capita': 'PIB per cápita',
    'Healthy life expectancy': 'Esperanza de vida saludable',
    'Social support': 'Red de apoyo social',
    'Freedom to make life choices': 'Libertad para tomar decisiones de vida',
    'Generosity': 'Generosidad',
    'Perceptions of corruption': 'Percepción de corrupción'
}
```

### Arquitectura de gráficos con POO:
El código usa Herencia y Polimorfismo:

- Clase base Grafico con método abstracto mostrar()

- Subclases para cada tipo de gráfico sobrescriben mostrar()

#### 📈 GraficoLineas
- Muestra la evolución de la felicidad para el Top 10 países con mayor puntaje promedio
 
- Usa sns.lineplot() para trazar la variación año a año
  
#### 📊 GraficoBarras
- Muestra la comparación de factores de felicidad por año para un país específico

- Usa DataFrame.plot(kind="bar")

#### 🌍 GraficoMapa
- Crea un mapa interactivo con folium
  
- Colorea los países según su puntaje promedio de felicidad
  
- Muestra pop-ups con información de todos los factores

#### 🔍 GraficoDispersion
- Grafica la relación entre Percepción de corrupción y Score de felicidad
- 
- Colorea puntos por año con sns.scatterplot()
  
#### 📦 GraficoDistribucion
- Muestra un histograma de distribución del Score de felicidad usando sns.histplot()

### explicacion
##### 1. Uso de `__file__` y rutas absolutas
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

- __file__ devuelve la ruta del archivo Python actual
  
- os.path.abspath(__file__) obtiene la ruta absoluta
  
- os.path.dirname(...) elimina el nombre del archivo y deja solo el directorio
  
- Esto asegura que el script pueda encontrar los archivos 2018.csv y 2019.csv sin importar desde dónde se ejecute

Se usa un diccionario (country_replacements) para estandarizar nombres y evitar errores en gráficos y agrupaciones 
```country_replacements = { ... }
all_data["Country or region"] = all_data["Country or region"].str.strip()
all_data["Country or region"] = all_data["Country or region"].replace(country_replacements)
```

Este diccionario no traduce automáticamente las columnas, pero se usa para mostrar las leyendas de los gráficos en español 

```factors = {
    'GDP per capita': 'PIB per cápita',
    ...
}
```

Evita que el programa se cierre si ocurre un error (por ejemplo, si un país no existe en los datos) 
```try:
    ...
except Exception as e:
    print(f"{Colores.ROJO}Error al generar gráfico: {e}{Colores.RESET}")
```

groupby() agrupa datos por país y ['Score'].mean() calcula el promedio del índice de felicidad por país, es clave para mostrar solo el Top 10 en el gráfic

```promedio_pais = self.data.groupby('Country or region')['Score'].mean()
```


# Exploracion_inicial.py

Este script en Python realiza una **exploración inicial** de los datos del *World Happiness Report* para los años 2018 y 2019.  

Incluye:
- Carga y validación de los archivos CSV.
- Limpieza y normalización de nombres de columnas.
- Unificación de datasets en un solo DataFrame.
- Estadísticas descriptivas y revisión de la estructura de los datos.
- Detección de valores nulos y tipos de datos.
- Visualización comparativa de la felicidad en los **12 países más felices del 2019**.

---

## Importación de librerías

| Librería | Uso |
| -------- | --- |
| pandas | Carga y manipulación de datos tabulares |
| matplotlib.pyplot | Creación de gráficos básicos |
| numpy | Cálculos numéricos y manejo de arreglos |

---

## Carga y preparación de datos

- Se buscan los archivos `2018.csv` y `2019.csv` en el mismo directorio del script usando `os.path`.
- Para cada año:
  - Se lee el CSV con **pandas**.
  - Se eliminan espacios extra en los nombres de columnas.
  - Se añade una columna `year` con el año correspondiente.
  - Se normalizan nombres de columnas (`Country` → `Country or region`, `Happiness Score` → `Score`).
  - Se seleccionan únicamente:  
    - **Country or region**  
    - **Score**  
    - **year**

- Si no existe la columna `Score`, se lanza un error.
- Finalmente, ambos DataFrames se concatenan en `all_data`

```python
dataframes.append(df[['Country or region', 'Score', 'year']])
all_data = pd.concat(dataframes)
Manejo de excepciones:

python
Copiar código
except FileNotFoundError as e:
    print(f"Archivo no encontrado: {e.filename}")
    exit()
except Exception as e:
    print(f"Error al cargar los archivos: {e}")
    exit()
```

### Exploración de datos
El script imprime en consola:

- Información general del dataset (.info())

- Estadísticas descriptivas (.describe())

- Dimensiones (.shape)

- Valores nulos por columna (.isnull().sum())

- Tipos de datos por columna (.dtypes)

### Visualización comparativa

1. Se seleccionan los 12 países más felices en 2019:

```top12_2019 = all_data[all_data['year'] == 2019].sort_values(by='Score', ascending=False).head(12)
```

2. Se filtran los datos de esos mismos países para ambos años

3. Se construyen listas con los puntajes de felicidad de 2018 y 2019 para cada país

4. Se agregan errores aleatorios pequeños con numpy.random.rand() para dar estilo a la gráfica

5. Se genera un gráfico de barras horizontales donde se comparan ambos años:

```ax.barh(y_pos - 0.2, score_2018, xerr=error_2018, height=0.4, label='2018')
ax.barh(y_pos + 0.2, score_2019, xerr=error_2019, height=0.4, label='2019')
```

El resultado muestra la evolución de la felicidad en los 12 países más felices del mundo, comparando 2018 vs 2019

### Explicación
##### 1. Uso de os.path.dirname(__file__)

- Permite obtener el directorio del script actual

- Asegura que los archivos CSV se encuentren aunque se ejecute desde otra carpeta

##### 2. Normalización de columnas

- Evita inconsistencias (Country vs Country or region, Happiness Score vs Score)

##### 3. Manejo de errores

- El programa no se detiene abruptamente si falta un archivo o columna importante

- Informa claramente el error y finaliza con exit()

  Visualización horizontal (barh)

##### 4. Se usa en lugar de vertical para mejorar la legibilidad de los nombres de países.

- invert_yaxis() coloca a los países con mayor felicidad en la parte superior

  

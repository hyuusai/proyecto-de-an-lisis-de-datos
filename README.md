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
``` all_data = pd.concat([df_2018, df_2019], ignore_index=True)
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
  

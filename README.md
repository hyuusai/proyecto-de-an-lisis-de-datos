 
# Análisis  Reporte Mundial de la Felicidad (World Happiness Repor

<p>
  Este proyecto tiene como objetivo principal analizar los datos del Reporte Mundial de la Felicidad y través de este análisis se busca identificar los factores que más influyen en la felicidad de las personas en diferentes países.
</p>

### Librerías Utilizadas
<li>pandas: Para la carga, limpieza y manipulación de los datos.</li>
<li>matplotlib.pyplot: Para la creación de gráficos y visualizaciones.</li>
<li>numpy: Para realizar operaciones numéricas y manejar los datos de manera eficiente.</li>

### Explicación
<p>El script está diseñado para cargar, limpiar y realizar un análisis exploratorio básico de los datos del Reporte Mundial de la Felicidad de 2018 y 2019
</p>

#####  Carga y Limpieza de Datos:
<p>Se usa un bucle for para iterar sobre los años 2018 y 2019
Se leen los archivos CSV y se normalizan los nombres de las columnas para asegurar la consistencia. Por ejemplo, Country y Happiness Score se renombran a Country or region y Score
Finalmente, los DataFrames de ambos años se combinan en un único DataFrame llamado all_data usando pd.concat()
Se añade una nueva columna llamada year a cada DataFrame para identificar a qué año corresponden los datos
</p>

#####  El código imprime informaciónsobre el conjunto de datos combinado, incluyendo:
<p>all_data.info(): Proporciona el tipo de datos de cada columna y si hay valores nulos
all_data.describe(): Muestra estadísticas descriptivas como la media, la desviación estándar y los valores mínimo y máximo de las columnas
all_data.shape: Indica el número de filas y columnas del DataFrame
all_data.isnull().sum(): Cuenta la cantidad de valores nulos por columna
all_data.dtypes: Muestra el tipo de dato de cada columna
</p>

###### proxima ...

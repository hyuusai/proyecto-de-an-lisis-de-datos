# =============================
# IMPORTACIONES DE LIBRERÍAS
# =============================
import os               # Para manejar rutas y archivos del sistema
import pandas as pd     # Para manipulación y análisis de datos
import matplotlib.pyplot as plt  # Para gráficos básicos
import seaborn as sns   # Para gráficos estadísticos avanzados
import folium           # Para mapas interactivos
import requests         # Para descargar archivos desde la web
import webbrowser       # Para abrir archivos HTML en el navegador

# =============================
# 1. COLORES PARA EL MENÚ Y ERRORES
# =============================
class Colores:
    # Códigos de color para la terminal
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    ROJO = "\033[91m"
    RESET = "\033[0m"      # Reinicia color
    NEGRITA = "\033[1m"    # Texto en negrita

# =============================
# 2. CARGA DE DATOS
# =============================
# Definir directorio base del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas de los archivos CSV
file_2018 = os.path.join(BASE_DIR, "2018.csv")
file_2019 = os.path.join(BASE_DIR, "2019.csv")

# Cargar datasets
df_2018 = pd.read_csv(file_2018)
df_2019 = pd.read_csv(file_2019)

# Agregar columna de año
df_2018["year"] = 2018
df_2019["year"] = 2019

# Combinar datasets en uno solo
all_data = pd.concat([df_2018, df_2019], ignore_index=True)

# Normalización de nombres de países para consistencia
country_replacements = {
    "United States": "United States of America",
    "Tanzania": "United Republic of Tanzania",
    "Congo (Brazzaville)": "Republic of the Congo",
    "Congo (Kinshasa)": "Democratic Republic of the Congo",
    "Papua New Guinea": "Independent State of Papua New Guinea",
    "Eritrea": "State of Eritrea",
    "Palestinian Territories": "West Bank",
    "Hong Kong S.A.R. of China": "Hong Kong",
    "North Macedonia": "Macedonia",
    "Republic of Kosovo": "Kosovo",
    "Serbia": "Republic of Serbia",
    "Trinidad & Tobago": "Trinidad and Tobago"
}
# Elimina espacios y reemplaza nombres según el diccionario
all_data["Country or region"] = all_data["Country or region"].str.strip()
all_data["Country or region"] = all_data["Country or region"].replace(country_replacements)

# Traducción de factores de felicidad
factors = {
    'GDP per capita': 'PIB per cápita',
    'Healthy life expectancy': 'Esperanza de vida saludable',
    'Social support': 'Red de apoyo social',
    'Freedom to make life choices': 'Libertad para tomar decisiones de vida',
    'Generosity': 'Generosidad',
    'Perceptions of corruption': 'Percepción de corrupción'
}

# =============================
# 3. CLASES DE GRÁFICOS (HERENCIA Y POLIMORFISMO)
# =============================
class Grafico:
    """Clase base para todos los gráficos"""
    def __init__(self, titulo):
        self.titulo = titulo  # Título del gráfico

    def mostrar(self):
        """Método genérico que debe sobrescribirse en subclases"""
        raise NotImplementedError("El método mostrar() debe implementarse en la subclase")

# -----------------------------
# GRÁFICO DE LÍNEAS
# -----------------------------
class GraficoLineas(Grafico):
    """Gráfico de líneas para evolución de felicidad"""
    def __init__(self, data, titulo="Evolución de felicidad"):
        super().__init__(titulo)
        self.data = data

    def mostrar(self):
        try:
            # Calcular promedio de Score por país
            promedio_pais = self.data.groupby('Country or region')['Score'].mean().sort_values(ascending=False)
            top10_countries = promedio_pais.head(10).index  # Seleccionar top 10
            filtered_data = self.data[self.data['Country or region'].isin(top10_countries)]

            # Crear gráfico de líneas
            plt.figure(figsize=(12, 8))
            sns.lineplot(
                data=filtered_data,
                x="year",
                y="Score",
                hue="Country or region",
                marker="o",
                linewidth=2.5,
                alpha=0.85
            )
            plt.title(self.titulo, fontsize=14, fontweight='bold')
            plt.xlabel("Año")
            plt.ylabel("Puntaje de Felicidad")
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend(title="País", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"{Colores.ROJO}Error al generar gráfico de líneas: {e}{Colores.RESET}")

# -----------------------------
# GRÁFICO DE BARRAS
# -----------------------------
class GraficoBarras(Grafico):
    """Gráfico de barras de factores de felicidad por país"""
    def __init__(self, data, pais, titulo=None):
        if titulo is None:
            titulo = f"Factores de felicidad en {pais} por año"
        super().__init__(titulo)
        self.data = data
        self.pais = pais

    def mostrar(self):
        try:
            # Verifica si el país existe en los datos
            if self.pais not in self.data["Country or region"].values:
                print(f"{Colores.ROJO}El país '{self.pais}' no se encuentra en los datos.{Colores.RESET}")
                return
            # Agrupar por año y calcular promedio de factores
            data_pais = self.data[self.data["Country or region"] == self.pais].groupby("year")[list(factors.keys())].mean()
            # Crear gráfico de barras
            data_pais.plot(kind="bar", figsize=(10,6))
            plt.title(self.titulo, fontsize=14, fontweight='bold')
            plt.ylabel("Valor promedio")
            plt.xlabel("Año")
            plt.xticks(rotation=0)
            plt.legend([factors[k] for k in factors.keys()], bbox_to_anchor=(1,1))
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"{Colores.ROJO}Error al generar gráfico de barras: {e}{Colores.RESET}")

# -----------------------------
# GRÁFICO DE MAPA
# -----------------------------
class GraficoMapa(Grafico):
    """Mapa de felicidad usando Folium"""
    def __init__(self, data, titulo="Mapa de felicidad"):
        super().__init__(titulo)
        self.data = data

    def mostrar(self):
        try:
            # Promedio de Score y factores por país
            avg_factors = self.data.groupby("Country or region")[['Score'] + list(factors.keys())].mean().reset_index()
            geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
            geo_json_data = requests.get(geo_url).json()

            # Crear mapa base
            m = folium.Map(location=[20,0], zoom_start=2, tiles="cartodb positron")
            folium.Choropleth(
                geo_data=geo_url,
                name="choropleth",
                data=avg_factors,
                columns=["Country or region", "Score"],
                key_on="feature.properties.name",
                fill_color="YlGnBu",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="Puntaje promedio de felicidad (2018-2019)"
            ).add_to(m)

            # Agregar popups con información de factores
            info_dict = avg_factors.set_index('Country or region').to_dict(orient='index')
            for feature in geo_json_data['features']:
                country_name = feature['properties']['name']
                if country_name in info_dict:
                    data = info_dict[country_name]
                    html = f"<b>{country_name}</b><br><b>Felicidad (Score):</b> {data['Score']:.2f}<br><br>"
                    for key, label in factors.items():
                        val = data.get(key)
                        if pd.isna(val):
                            html += f"<b>{label}:</b> No disponible<br>"
                        else:
                            html += f"<b>{label}:</b> {val:.3f}<br>"
                    iframe = folium.IFrame(html=html, width=320, height=280)
                    popup = folium.Popup(iframe, max_width=320)
                    folium.GeoJson(
                        feature,
                        popup=popup,
                        style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent'}
                    ).add_to(m)

            # Guardar y abrir mapa en navegador
            map_filename = os.path.join(BASE_DIR, "mapa_felicidad_con_factores.html")
            m.save(map_filename)
            print(f"{Colores.VERDE}Mapa guardado como '{map_filename}'{Colores.RESET}")
            webbrowser.open(f"file://{map_filename}")
        except Exception as e:
            print(f"{Colores.ROJO}Error al generar mapa de felicidad: {e}{Colores.RESET}")

# -----------------------------
# GRÁFICO DE DISPERSIÓN
# -----------------------------
class GraficoDispersion(Grafico):
    """Corrupción vs Felicidad"""
    def __init__(self, data, titulo="Corrupción vs Felicidad"):
        super().__init__(titulo)
        self.data = data

    def mostrar(self):
        try:
            plt.figure(figsize=(10,6))
            sns.scatterplot(data=self.data, x="Perceptions of corruption", y="Score", hue="year", alpha=0.7)
            plt.title(self.titulo, fontsize=14, fontweight='bold')
            plt.xlabel("Percepción de corrupción")
            plt.ylabel("Score de felicidad")
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.show()
        except Exception as e:
            print(f"{Colores.ROJO}Error al generar gráfico de dispersión: {e}{Colores.RESET}")

# -----------------------------
# GRÁFICO DE DISTRIBUCIÓN
# -----------------------------
class GraficoDistribucion(Grafico):
    """Distribución del Score de felicidad"""
    def __init__(self, data, titulo="Distribución del Score de felicidad"):
        super().__init__(titulo)
        self.data = data

    def mostrar(self):
        try:
            plt.figure(figsize=(8,5))
            sns.histplot(data=self.data, x="Score", bins=20, kde=True, color="purple")
            plt.title(self.titulo, fontsize=14, fontweight='bold')
            plt.xlabel("Score")
            plt.ylabel("Frecuencia")
            plt.show()
        except Exception as e:
            print(f"{Colores.ROJO}Error al generar gráfico de distribución: {e}{Colores.RESET}")

# =============================
# 4. MENÚ INTERACTIVO
# =============================
def menu():
    while True:
        # Mostrar opciones del menú con colores
        print(f"\n{Colores.AZUL}{Colores.NEGRITA}===== MENÚ DE OPCIONES ====={Colores.RESET}")
        print(f"{Colores.VERDE}1.{Colores.RESET} Gráfico de líneas: Evolución de felicidad (Top 10 países)")
        print(f"{Colores.VERDE}2.{Colores.RESET} Gráfico de barras: Factores de felicidad por país")
        print(f"{Colores.VERDE}3.{Colores.RESET} Gráfico geográfico: Mapa de felicidad y factores")
        print(f"{Colores.VERDE}4.{Colores.RESET} Gráfico de dispersión: Corrupción vs felicidad")
        print(f"{Colores.VERDE}5.{Colores.RESET} Gráfico de distribución: Score de felicidad")
        print(f"{Colores.ROJO}0.{Colores.RESET} Salir")

        opcion = input(f"{Colores.AMARILLO}Selecciona una opción: {Colores.RESET}")

        # Llamada a la clase correspondiente según la opción
        if opcion == "1":
            g = GraficoLineas(all_data)
            g.mostrar()
        elif opcion == "2":
            pais = input("Ingrese el país a analizar (por ejemplo Finland): ")
            g = GraficoBarras(all_data, pais)
            g.mostrar()
        elif opcion == "3":
            g = GraficoMapa(all_data)
            g.mostrar()
        elif opcion == "4":
            g = GraficoDispersion(all_data)
            g.mostrar()
        elif opcion == "5":
            g = GraficoDistribucion(all_data)
            g.mostrar()
        elif opcion == "0":
            print(f"{Colores.ROJO}Saliendo del programa...{Colores.RESET}")
            break
        else:
            print(f"{Colores.ROJO}Opción no válida. Intenta de nuevo.{Colores.RESET}")

# =============================
# 5. EJECUCIÓN PRINCIPAL
# =============================
if __name__ == "__main__":
    menu()  # Inicia el menú interactivo




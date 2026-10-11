
# Proyecto Mistral AI
# Graficos de rendimiento del modelo Ministral 3 8B
# Se utilizan los resultados obtenidos en las 10 pruebas.

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Ubicamos la carpeta principal del proyecto.
BASE = Path(__file__).resolve().parent.parent

# Archivo que contiene las estadisticas.
ARCHIVO = BASE / "results" / "estadisticas_por_categoria.csv"

# Carpeta donde guardaremos los graficos.
CARPETA_GRAFICOS = BASE / "docs" / "graficos"
CARPETA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# Leemos los resultados.
datos = pd.read_csv(ARCHIVO, encoding="utf-8-sig")

# Nombres para mostrar en los graficos.
nombres = {
    "generacion": "Generacion",
    "resumen": "Resumen",
    "correccion_traduccion": "Correccion y traduccion",
    "codigo": "Codigo",
    "razonamiento_veracidad": "Razonamiento"
}

datos["Nombre"] = datos["Categoria"].replace(nombres)


# Funcion para crear y guardar los graficos.
def crear_grafico(columna, titulo, etiqueta, archivo, color):
    plt.figure(figsize=(11, 6))

    barras = plt.bar(
        datos["Nombre"],
        datos[columna],
        color=color
    )

    plt.title(titulo, fontsize=15, fontweight="bold")
    plt.ylabel(etiqueta)
    plt.xlabel("Categoria de evaluacion")

    plt.xticks(rotation=15, ha="right")
    plt.grid(axis="y", alpha=0.25)

    # Agregamos el valor encima de cada barra.
    for barra in barras:
        valor = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            valor,
            f"{valor:.2f}",
            ha="center",
            va="bottom"
        )

    plt.ylim(0, datos[columna].max() * 1.18)
    plt.tight_layout()

    ruta = CARPETA_GRAFICOS / archivo
    plt.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close()

    print("Grafico guardado:", ruta)


# Grafico 1: tiempo promedio de respuesta.
crear_grafico(
    "Tiempo_Promedio",
    "Tiempo promedio de respuesta por categoria",
    "Tiempo en segundos",
    "01_tiempo_promedio.png",
    "#2874A6"
)

# Grafico 2: velocidad de generacion.
crear_grafico(
    "Velocidad_Promedio",
    "Velocidad promedio de generacion por categoria",
    "Tokens por segundo",
    "02_velocidad_promedio.png",
    "#239B56"
)

# Grafico 3: cantidad promedio de tokens.
crear_grafico(
    "Tokens_Promedio",
    "Tokens promedio generados por categoria",
    "Cantidad de tokens",
    "03_tokens_promedio.png",
    "#CA6F1E"
)

print("\nLos tres graficos se generaron correctamente.")

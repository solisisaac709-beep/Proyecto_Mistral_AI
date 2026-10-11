
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


# ------------------------------------------------------------
# Comparacion de rendimiento entre Windows y Docker
# Se utilizan tres ejecuciones completas por configuracion.
# ------------------------------------------------------------

import json
import statistics

archivos_pruebas = {
    "Windows": [
        "resultados_20261011_151650_913926.json",
        "resultados_20261011_152651_308671.json",
        "resultados_20261011_153006_320986.json"
    ],
    "Docker": [
        "resultados_20261011_220322_432084.json",
        "resultados_20261011_220533_422600.json",
        "resultados_20261011_220859_524549.json"
    ]
}

# Cargamos las 30 respuestas de cada configuracion.
resultados_comparacion = {}

for configuracion, archivos in archivos_pruebas.items():
    respuestas = []

    for nombre_archivo in archivos:
        ruta = BASE / "results" / nombre_archivo

        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)

        if isinstance(contenido, dict):
            contenido = [contenido]

        respuestas.extend(contenido)

    resultados_comparacion[configuracion] = respuestas
    print(configuracion, ":", len(respuestas), "respuestas")



# Funcion para crear graficos comparativos mas claros.
def grafico_comparativo(campo, titulo, unidad, archivo_salida):
    configuraciones = ["Windows", "Docker"]

    promedios = []
    desviaciones = []

    for configuracion in configuraciones:
        valores = [
            float(respuesta[campo])
            for respuesta in resultados_comparacion[configuracion]
        ]

        promedios.append(statistics.mean(valores))
        desviaciones.append(statistics.stdev(valores))

    fig, ax = plt.subplots(figsize=(9, 5.5))

    colores = ["#2874A6", "#239B56"]

    barras = ax.bar(
        configuraciones,
        promedios,
        color=colores,
        width=0.48
    )

    ax.set_title(titulo, fontsize=15, fontweight="bold", pad=18)
    ax.set_ylabel(unidad, fontsize=11)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    # Mostramos el promedio encima de cada barra.
    for barra, promedio in zip(barras, promedios):
        ax.annotate(
            f"{promedio:.2f}",
            xy=(
                barra.get_x() + barra.get_width() / 2,
                promedio
            ),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=12,
            fontweight="bold"
        )

    # Dejamos espacio para los valores superiores.
    ax.set_ylim(0, max(promedios) * 1.25)

    # La desviacion estandar se muestra debajo del grafico.
    informacion = (
        f"Windows: desviacion estandar = {desviaciones[0]:.2f}   |   "
        f"Docker: desviacion estandar = {desviaciones[1]:.2f}"
    )

    fig.text(
        0.5, 0.02,
        informacion,
        ha="center",
        fontsize=9,
        color="#555555"
    )

    fig.subplots_adjust(bottom=0.17, top=0.87)

    ruta = CARPETA_GRAFICOS / archivo_salida
    fig.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("Grafico comparativo guardado:", ruta)


# Grafico 4: comparacion de TTFT.
grafico_comparativo(
    "ttft_segundos",
    "TTFT promedio: Windows vs Docker",
    "Segundos",
    "04_comparacion_ttft.png"
)

# Grafico 5: comparacion de velocidad.
grafico_comparativo(
    "tokens_por_segundo",
    "Velocidad de generacion: Windows vs Docker",
    "Tokens por segundo",
    "05_comparacion_velocidad.png"
)

# Grafico 6: comparacion del tiempo total.
grafico_comparativo(
    "tiempo_total",
    "Tiempo total: Windows vs Docker",
    "Segundos",
    "06_comparacion_tiempo_total.png"
)

# Grafico 7: comparacion de tokens.
grafico_comparativo(
    "tokens",
    "Tokens generados: Windows vs Docker",
    "Cantidad de tokens",
    "07_comparacion_tokens.png"
)

print("\nLos cuatro graficos comparativos se generaron correctamente.")

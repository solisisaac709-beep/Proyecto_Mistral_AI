# Proyecto Mistral AI
# Graficos de rendimiento del modelo Ministral 3 8B
# Utiliza los CSV y JSON ya guardados en results/.
# Cada bloque genera figuras distintas; no vuelve a ejecutar el modelo.

import json
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

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



# ------------------------------------------------------------
# Comparacion de rendimiento entre Windows y Docker
# Se utilizan tres ejecuciones completas por configuracion.
# ------------------------------------------------------------

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



# ------------------------------------------------------------
# Graficos 8 al 13: comparacion de recursos Windows vs Docker
# Se utilizan las tres mediciones de cada entorno.
# ------------------------------------------------------------

ARCHIVO_RECURSOS = (
    BASE / "results" / "comparacion_recursos_resumen.csv"
)

datos_recursos = pd.read_csv(
    ARCHIVO_RECURSOS,
    encoding="utf-8-sig"
)


def grafico_recursos(metrica, titulo, unidad, archivo_salida):
    # Seleccionamos la metrica y ordenamos los entornos.
    filtro = datos_recursos[
        datos_recursos["Metrica"] == metrica
    ].copy()

    filtro = filtro.set_index("Entorno").reindex(
        ["Windows", "Docker"]
    )

    if filtro["Promedio_3_ejecuciones"].isna().any():
        raise ValueError(
            f"No se encontraron los datos de: {metrica}"
        )

    promedios = filtro["Promedio_3_ejecuciones"].tolist()
    desviaciones = filtro[
        "Desviacion_entre_ejecuciones"
    ].tolist()

    fig, ax = plt.subplots(figsize=(9, 5.5))

    barras = ax.bar(
        ["Windows", "Docker"],
        promedios,
        color=["#2874A6", "#239B56"],
        width=0.48
    )

    ax.set_title(
        titulo,
        fontsize=15,
        fontweight="bold",
        pad=18
    )

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

    ax.set_ylim(0, max(promedios) * 1.25)

    # Mostramos la desviacion entre las tres ejecuciones.
    informacion = (
        f"Windows: desviacion = {desviaciones[0]:.2f}   |   "
        f"Docker: desviacion = {desviaciones[1]:.2f}"
    )

    fig.text(
        0.5,
        0.055,
        informacion,
        ha="center",
        fontsize=9,
        color="#555555"
    )

    # Aclaramos que se mide el equipo anfitrion.
    fig.text(
        0.5,
        0.025,
        "Ambos entornos utilizan Ollama en Windows",
        ha="center",
        fontsize=8,
        color="#777777"
    )

    fig.subplots_adjust(bottom=0.20, top=0.87)

    ruta = CARPETA_GRAFICOS / archivo_salida

    fig.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Grafico de recursos guardado:", ruta)


# Grafico 8: CPU del sistema.
grafico_recursos(
    "CPU sistema (%)",
    "Uso promedio de CPU del sistema",
    "Porcentaje (%)",
    "08_cpu_sistema.png"
)

# Grafico 9: CPU del proceso llama-server.
grafico_recursos(
    "CPU proceso (%)",
    "Uso promedio de CPU del proceso de inferencia",
    "Porcentaje (%)",
    "09_cpu_modelo.png"
)

# Grafico 10: RAM del sistema.
grafico_recursos(
    "RAM sistema (GiB)",
    "Consumo promedio de RAM del sistema",
    "Memoria (GiB)",
    "10_ram_sistema.png"
)

# Grafico 11: RAM del modelo.
grafico_recursos(
    "RAM modelo (GiB)",
    "Consumo promedio de RAM del proceso de inferencia",
    "Memoria (GiB)",
    "11_ram_modelo.png"
)

# Grafico 12: actividad de GPU.
grafico_recursos(
    "Actividad motor GPU (%)",
    "Actividad promedio del motor GPU mas ocupado",
    "Porcentaje (%)",
    "12_actividad_gpu.png"
)

# Grafico 13: VRAM dedicada.
grafico_recursos(
    "VRAM dedicada (GiB)",
    "Consumo promedio de VRAM dedicada",
    "Memoria (GiB)",
    "13_vram.png"
)



# ------------------------------------------------------------
# Graficos 14 y 15: comparacion de temperaturas 0.2 y 0.9
# ------------------------------------------------------------

ARCHIVO_TEMPERATURAS = (
    BASE / "results" / "comparacion_temperaturas.csv"
)

datos_temperaturas = pd.read_csv(
    ARCHIVO_TEMPERATURAS,
    encoding="utf-8-sig"
)


def grafico_temperaturas(metrica, titulo, unidad, archivo_salida):
    filtro = datos_temperaturas[
        datos_temperaturas["Metrica"] == metrica
    ].copy()

    filtro["Temperatura"] = filtro["Temperatura"].astype(float)

    filtro = filtro.set_index("Temperatura").reindex(
        [0.2, 0.9]
    )

    promedios = filtro["Promedio"].tolist()
    desviaciones = filtro["Desviacion"].tolist()

    if any(pd.isna(valor) for valor in promedios):
        raise ValueError(f"Faltan datos para: {metrica}")

    fig, ax = plt.subplots(figsize=(9, 5.5))

    barras = ax.bar(
        ["0.2", "0.9"],
        promedios,
        color=["#2874A6", "#CA6F1E"],
        width=0.48
    )

    ax.set_title(titulo, fontsize=15, fontweight="bold")
    ax.set_xlabel("Temperatura")
    ax.set_ylabel(unidad)
    ax.set_ylim(0, max(promedios) * 1.25)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    for barra, valor in zip(barras, promedios):
        ax.annotate(
            f"{valor:.2f}",
            xy=(
                barra.get_x() + barra.get_width() / 2,
                valor
            ),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=12,
            fontweight="bold"
        )

    fig.text(
        0.5,
        0.04,
        (
            f"Desviacion: 0.2 = {desviaciones[0]:.2f} | "
            f"0.9 = {desviaciones[1]:.2f}"
        ),
        ha="center",
        fontsize=9
    )

    fig.subplots_adjust(bottom=0.17)

    ruta = CARPETA_GRAFICOS / archivo_salida
    fig.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("Grafico de temperaturas guardado:", ruta)


# Grafico 14: velocidad por temperatura.
grafico_temperaturas(
    "Velocidad (tokens/s)",
    "Velocidad promedio por temperatura",
    "Tokens por segundo",
    "14_temperatura_velocidad.png"
)

# Grafico 15: tiempo de respuesta por temperatura.
grafico_temperaturas(
    "Tiempo total (segundos)",
    "Tiempo total promedio por temperatura",
    "Segundos",
    "15_temperatura_tiempo.png"
)



# ------------------------------------------------------------
# Graficos 16 y 17: evaluacion de calidad de las respuestas
# Comparacion entre temperaturas 0.2 y 0.9
# ------------------------------------------------------------

ARCHIVO_CALIDAD = BASE / "results" / "evaluacion_calidad_revisada.csv"

calidad = pd.read_csv(ARCHIVO_CALIDAD, encoding="utf-8-sig")

# Convertimos las temperaturas a numeros para evitar diferencias
# entre valores como 0.2 y "0.2".
calidad["Temperatura"] = pd.to_numeric(calidad["Temperatura"])

criterios = [
    "Precision_1_5",
    "Claridad_1_5",
    "Cumplimiento_1_5",
    "Coherencia_1_5"
]

# Calculamos los promedios directamente desde las calificaciones.
for criterio in criterios:
    calidad[criterio] = pd.to_numeric(
        calidad[criterio],
        errors="raise"
    )

promedios_calidad = (
    calidad.groupby("Temperatura")[criterios]
    .mean()
    .reindex([0.2, 0.9])
)

if promedios_calidad.isna().any().any():
    raise ValueError("Faltan calificaciones de calidad.")

# Grafico 16: comparacion de los cuatro criterios.
ax = promedios_calidad.T.plot(
    kind="bar",
    figsize=(11, 6),
    color=["#2874A6", "#CA6F1E"],
    width=0.7
)

ax.set_title(
    "Calidad de respuestas por criterio y temperatura",
    fontsize=14,
    fontweight="bold"
)
ax.set_ylabel("Calificacion promedio (1 a 5)")
ax.set_xlabel("Criterio evaluado")
ax.set_xticklabels(
    ["Precision", "Claridad", "Cumplimiento", "Coherencia"],
    rotation=0
)
ax.set_ylim(0, 5.5)
ax.legend(["Temperatura 0.2", "Temperatura 0.9"])
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
ruta = CARPETA_GRAFICOS / "16_calidad_por_criterio.png"
plt.savefig(ruta, dpi=300, bbox_inches="tight")
plt.close()

print("Grafico guardado:", ruta)

# Grafico 17: promedio general de calidad.
promedio_general = promedios_calidad.mean(axis=1)

fig, ax = plt.subplots(figsize=(9, 5.5))

barras = ax.bar(
    ["0.2", "0.9"],
    promedio_general.values,
    color=["#2874A6", "#CA6F1E"],
    width=0.48
)

ax.set_title(
    "Calidad general de respuestas por temperatura",
    fontsize=14,
    fontweight="bold"
)
ax.set_xlabel("Temperatura")
ax.set_ylabel("Calificacion promedio (1 a 5)")
ax.set_ylim(0, 5.5)
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

for barra, valor in zip(barras, promedio_general.values):
    ax.annotate(
        f"{valor:.2f} / 5",
        xy=(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height()
        ),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

fig.tight_layout()
ruta = CARPETA_GRAFICOS / "17_calidad_general.png"
fig.savefig(ruta, dpi=300, bbox_inches="tight")
plt.close(fig)

print("Grafico guardado:", ruta)
print("\nListo: se generaron los 17 graficos en docs/graficos.")

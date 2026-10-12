
# Proyecto Mistral AI
# Preparacion de la evaluacion de calidad de respuestas

from pathlib import Path
import json
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "results"

archivos = {
    "0.2": "resultados_20261011_151650_913926.json",
    "0.9": "resultados_20261011_183330_778413.json"
}

respuestas = {}

for temperatura, nombre in archivos.items():
    ruta = CARPETA / nombre

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    respuestas[temperatura] = {
        int(item["id"]): item
        for item in datos
    }

filas = []

for identificador in sorted(respuestas["0.2"]):
    if identificador not in respuestas["0.9"]:
        raise ValueError(
            f"Falta la pregunta {identificador} en temperatura 0.9"
        )

    baja = respuestas["0.2"][identificador]
    alta = respuestas["0.9"][identificador]

    if baja["prompt"] != alta["prompt"]:
        raise ValueError(
            f"Las preguntas no coinciden en el ID {identificador}"
        )

    for temperatura, item in [("0.2", baja), ("0.9", alta)]:
        filas.append({
            "ID": identificador,
            "Categoria": item["categoria"],
            "Temperatura": temperatura,
            "Pregunta": item["prompt"],
            "Respuesta": item["respuesta"],
            "Precision_1_5": "",
            "Claridad_1_5": "",
            "Cumplimiento_1_5": "",
            "Coherencia_1_5": "",
            "Observaciones": ""
        })

tabla = pd.DataFrame(filas)

salida = CARPETA / "evaluacion_calidad.csv"

tabla.to_csv(
    salida,
    index=False,
    encoding="utf-8-sig"
)

print("\nTABLA DE EVALUACION GENERADA")
print("Respuestas:", len(tabla))
print("Preguntas diferentes:", tabla["ID"].nunique())
print("Archivo:", salida)
print("\nLas calificaciones quedan vacias para revision.")

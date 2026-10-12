
# Proyecto Mistral AI
# Comparacion de resultados con temperaturas 0.2 y 0.9

from pathlib import Path
import json
import statistics
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CARPETA = BASE / "results"

archivos = {
    "0.2": "resultados_20261011_151650_913926.json",
    "0.9": "resultados_20261011_183330_778413.json"
}

metricas = {
    "tokens": "Tokens generados",
    "ttft_segundos": "TTFT (segundos)",
    "tokens_por_segundo": "Velocidad (tokens/s)",
    "tiempo_total": "Tiempo total (segundos)"
}

resultados = []

for temperatura, nombre_archivo in archivos.items():
    ruta = CARPETA / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        respuestas = json.load(archivo)

    if isinstance(respuestas, dict):
        respuestas = [respuestas]

    print(
        f"Temperatura {temperatura}: "
        f"{len(respuestas)} respuestas"
    )

    for campo, nombre in metricas.items():
        valores = [
            float(respuesta[campo])
            for respuesta in respuestas
        ]

        resultados.append({
            "Temperatura": temperatura,
            "Metrica": nombre,
            "Promedio": statistics.mean(valores),
            "Desviacion": statistics.stdev(valores),
            "Minimo": min(valores),
            "Maximo": max(valores),
            "Cantidad": len(valores)
        })

resumen = pd.DataFrame(resultados)

salida = CARPETA / "comparacion_temperaturas.csv"
resumen.to_csv(salida, index=False, encoding="utf-8-sig")

print("\nCOMPARACION DE TEMPERATURAS")
print(resumen.round(2).to_string(index=False))

print("\nArchivo generado:")
print(salida)


# Comparacion de recursos: Windows y Docker
# Proyecto Mistral AI - Programacion IV

from pathlib import Path
import pandas as pd

carpeta = Path("results")

metricas = {
    "cpu_sistema_pct": "CPU sistema (%)",
    "ram_sistema_gib": "RAM sistema (GiB)",
    "ram_modelo_gib": "RAM modelo (GiB)",
    "cpu_modelo_pct": "CPU proceso (%)",
    "gpu_motor_max_pct": "Actividad motor GPU (%)",
    "vram_dedicada_gib": "VRAM dedicada (GiB)"
}

resultados = []

for entorno in ["windows", "docker"]:
    for numero in range(1, 4):
        archivo = carpeta / f"recursos_{entorno}_{numero:02d}.csv"

        if not archivo.exists():
            raise FileNotFoundError(f"Falta el archivo: {archivo}")

        datos = pd.read_csv(archivo)

        for columna, nombre in metricas.items():
            valores = pd.to_numeric(
                datos[columna], errors="coerce"
            ).dropna()

            if valores.empty:
                continue

            resultados.append({
                "Entorno": entorno.capitalize(),
                "Ejecucion": numero,
                "Metrica": nombre,
                "Promedio": valores.mean(),
                "Maximo": valores.max(),
                "Muestras": len(valores)
            })

detalle = pd.DataFrame(resultados)

# Cada ejecucion tiene el mismo peso en el resumen.
resumen = (
    detalle.groupby(["Entorno", "Metrica"])
    .agg(
        Promedio_3_ejecuciones=("Promedio", "mean"),
        Desviacion_entre_ejecuciones=("Promedio", "std"),
        Maximo_observado=("Maximo", "max"),
        Muestras_totales=("Muestras", "sum")
    )
    .reset_index()
)

detalle.to_csv(
    carpeta / "comparacion_recursos_detalle.csv",
    index=False
)

resumen.to_csv(
    carpeta / "comparacion_recursos_resumen.csv",
    index=False
)

print("\nCOMPARACION WINDOWS VS DOCKER")
print(resumen.round(2).to_string(index=False))

print("\nArchivos generados:")
print("results/comparacion_recursos_detalle.csv")
print("results/comparacion_recursos_resumen.csv")

print("\nNOTAS:")
print("- Ambos entornos utilizan Ollama en Windows.")
print("- Las metricas del sistema incluyen otros procesos.")
print("- GPU representa el motor mas activo de cada muestra.")
print("- Los valores de GPU mayores a 100% son anomalias.")
print("- La desviacion se calcula entre tres promedios.")

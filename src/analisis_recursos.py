
# Analisis de recursos de Mistral AI
# Compara las tres ejecuciones realizadas en Windows.

import pandas as pd
from pathlib import Path

carpeta = Path("results")

archivos = [
    carpeta / "recursos_windows_01.csv",
    carpeta / "recursos_windows_02.csv",
    carpeta / "recursos_windows_03.csv"
]

metricas = {
    "cpu_sistema_pct": "CPU sistema (%)",
    "ram_sistema_gib": "RAM sistema (GiB)",
    "ram_modelo_gib": "RAM modelo (GiB)",
    "cpu_modelo_pct": "CPU proceso (%)",
    "gpu_motor_max_pct": "GPU motor max (%)",
    "vram_dedicada_gib": "VRAM dedicada (GiB)"
}

resultados = []

for numero, archivo in enumerate(archivos, start=1):
    datos = pd.read_csv(archivo)

    for columna, nombre in metricas.items():
        valores = pd.to_numeric(
            datos[columna], errors="coerce"
        ).dropna()

        resultados.append({
            "Ejecucion": numero,
            "Metrica": nombre,
            "Promedio": valores.mean(),
            "Maximo": valores.max(),
            "Desviacion": valores.std(),
            "Muestras": len(valores)
        })

tabla = pd.DataFrame(resultados)

# Resumen entre ejecuciones:
# Promedio de los promedios de cada ejecucion.
# Desviacion entre los tres promedios.
# Maximo observado en cualquiera de las ejecuciones.
consolidado = (
    tabla.groupby("Metrica")
    .agg(
        Promedio_3_ejecuciones=("Promedio", "mean"),
        Desviacion_entre_ejecuciones=("Promedio", "std"),
        Maximo_observado=("Maximo", "max")
    )
    .reset_index()
)

salida_detalle = carpeta / "analisis_recursos_windows.csv"
salida_resumen = carpeta / "resumen_recursos_windows.csv"

tabla.to_csv(salida_detalle, index=False)
consolidado.to_csv(salida_resumen, index=False)

print("\nRESUMEN DE LAS TRES EJECUCIONES")
print(consolidado.round(2).to_string(index=False))

print("\nArchivos generados:")
print(salida_detalle)
print(salida_resumen)

print(
    "\nNota: GPU motor max es una lectura de los "
    "contadores de Windows, no el uso global de GPU."
)



# Monitor de recursos para el proyecto Mistral AI
# Registra CPU, RAM, proceso llama-server, GPU y VRAM.

import csv
import json
import subprocess
import time
import statistics
from datetime import datetime
from pathlib import Path

import psutil


CARPETA = Path("results")
CARPETA.mkdir(exist_ok=True)

# Identificador de GPU observado en Windows.
GPU_LUID = "luid_0x00000000_0x00015108"


def leer_gpu():
    """Consulta los contadores de GPU de Windows."""

    script = r"""
    $ErrorActionPreference = 'Stop'

    $muestras = (Get-Counter -Counter @(
        '\GPU Engine(*)\Utilization Percentage',
        '\GPU Adapter Memory(*)\Dedicated Usage'
    ) -ErrorAction Stop).CounterSamples

    $datos = foreach ($m in $muestras) {
        [PSCustomObject]@{
            nombre = $m.InstanceName
            ruta = $m.Path
            valor = $m.CookedValue
        }
    }

    ConvertTo-Json -InputObject @($datos) -Compress -Depth 3
    """

    try:
        resultado = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=15,
            check=True
        )

        datos = json.loads(resultado.stdout)

        if isinstance(datos, dict):
            datos = [datos]

        vram = []
        motores = []

        for dato in datos:
            nombre = str(dato.get("nombre", "")).lower()
            ruta = str(dato.get("ruta", "")).lower()
            valor = float(dato.get("valor", 0))

            if GPU_LUID not in nombre:
                continue

            if "dedicated usage" in ruta:
                vram.append(valor / (1024 ** 3))

            elif "utilization percentage" in ruta:
                motores.append(valor)

        # Se toma el motor con mayor actividad.
        # No equivale necesariamente al uso global de GPU.
        gpu_motor_max = max(motores) if motores else None
        vram_gib = max(vram) if vram else None

        return gpu_motor_max, vram_gib

    except (
        subprocess.SubprocessError,
        ValueError,
        json.JSONDecodeError,
        OSError
    ):
        return None, None


def buscar_llama():
    """Busca el proceso que ejecuta el modelo."""

    for proceso in psutil.process_iter(["name"]):
        try:
            nombre = (proceso.info["name"] or "").lower()

            if "llama-server" in nombre:
                return proceso

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return None


def resumen(valores):
    valores = [v for v in valores if v is not None]

    if not valores:
        return None, None, None

    promedio = statistics.mean(valores)
    maximo = max(valores)

    desviacion = (
        statistics.stdev(valores)
        if len(valores) > 1
        else 0
    )

    return promedio, maximo, desviacion


def main():
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo = CARPETA / f"monitoreo_completo_{fecha}.csv"

    mediciones = []

    print("Monitor de recursos de Mistral AI")
    print("Presione Ctrl+C para finalizar.")
    print("")

    psutil.cpu_percent(interval=None)

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            memoria = psutil.virtual_memory()

            proceso = buscar_llama()

            ram_modelo = None
            cpu_modelo = None

            if proceso:
                try:
                    ram_modelo = (
                        proceso.memory_info().rss / (1024 ** 3)
                    )

                    # Porcentaje del proceso desde su lectura previa.
                    cpu_modelo = proceso.cpu_percent(interval=None)

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied
                ):
                    pass

            gpu_motor, vram = leer_gpu()

            registro = {
                "fecha_hora": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "cpu_sistema_pct": round(cpu, 2),
                "ram_sistema_gib": round(
                    memoria.used / (1024 ** 3), 3
                ),
                "ram_modelo_gib": (
                    round(ram_modelo, 3)
                    if ram_modelo is not None else None
                ),
                "cpu_modelo_pct": (
                    round(cpu_modelo, 2)
                    if cpu_modelo is not None else None
                ),
                "gpu_motor_max_pct": (
                    round(gpu_motor, 2)
                    if gpu_motor is not None else None
                ),
                "vram_dedicada_gib": (
                    round(vram, 3)
                    if vram is not None else None
                )
            }

            mediciones.append(registro)

            print(
                f"CPU: {registro['cpu_sistema_pct']}% | "
                f"RAM: {registro['ram_sistema_gib']} GiB | "
                f"RAM modelo: {registro['ram_modelo_gib']} GiB | "
                f"GPU motor: {registro['gpu_motor_max_pct']}% | "
                f"VRAM: {registro['vram_dedicada_gib']} GiB"
            )

    except KeyboardInterrupt:
        print("\nFinalizando monitoreo...")

    if not mediciones:
        print("No se registraron datos.")
        return

    with open(archivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(
            f,
            fieldnames=mediciones[0].keys()
        )
        escritor.writeheader()
        escritor.writerows(mediciones)

    print("\nRESUMEN DE RECURSOS")

    campos = {
        "CPU sistema (%)": "cpu_sistema_pct",
        "RAM sistema (GiB)": "ram_sistema_gib",
        "RAM modelo (GiB)": "ram_modelo_gib",
        "CPU proceso (%)": "cpu_modelo_pct",
        "GPU motor max (%)": "gpu_motor_max_pct",
        "VRAM dedicada (GiB)": "vram_dedicada_gib"
    }

    for etiqueta, campo in campos.items():
        valores = [m[campo] for m in mediciones]
        promedio, maximo, desviacion = resumen(valores)

        if promedio is None:
            print(f"{etiqueta}: sin datos")
        else:
            print(
                f"{etiqueta}: "
                f"promedio={promedio:.2f}, "
                f"maximo={maximo:.2f}, "
                f"desviacion={desviacion:.2f}"
            )

    print(f"\nMuestras: {len(mediciones)}")
    print(f"Archivo: {archivo}")


if __name__ == "__main__":
    main()

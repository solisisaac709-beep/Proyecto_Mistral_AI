
# Proyecto de Investigacion - Programacion IV
# Pruebas de inteligencia artificial con Mistral AI
# Este programa envia preguntas a Ollama y guarda los resultados.

import argparse
import csv
import json
import time
import os
from datetime import datetime
from pathlib import Path

import requests


# Se obtiene la carpeta principal del proyecto.
BASE = Path(__file__).resolve().parent.parent

# Direccion del servidor local de Ollama.
URL = os.environ.get(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

def consultar_modelo(modelo, pregunta, temperatura, max_tokens):
    """Envia una pregunta al modelo y mide su rendimiento."""

    datos = {
        "model": modelo,
        "prompt": pregunta,
        "stream": True,
        "options": {
            "temperature": temperatura,
            "num_predict": max_tokens
        }
    }

    respuesta_texto = ""
    tokens = 0
    primer_token = None
    inicio = time.perf_counter()

    try:
        with requests.post(
            URL,
            json=datos,
            stream=True,
            timeout=(10, 300)
        ) as respuesta:

            respuesta.raise_for_status()

            for linea in respuesta.iter_lines():
                if not linea:
                    continue

                evento = json.loads(linea.decode("utf-8"))

                # Cada fragmento contiene una parte de la respuesta.
                fragmento = evento.get("response", "")

                if fragmento:
                    if primer_token is None:
                        primer_token = time.perf_counter()

                    respuesta_texto += fragmento

                # El ultimo evento contiene las metricas de Ollama.
                if evento.get("done", False):
                    tokens = evento.get("eval_count", 0)

                    # Tiempo de generacion informado por Ollama.
                    duracion_ns = evento.get("eval_duration", 0)

                    if duracion_ns > 0:
                        velocidad = tokens / (duracion_ns / 1e9)
                    else:
                        velocidad = 0

                    break
            else:
                raise ValueError(
                    "Ollama termino la conexion sin enviar el evento final."
                )

        fin = time.perf_counter()

        # Tiempo hasta recibir el primer fragmento de respuesta.
        if primer_token is not None:
            ttft = primer_token - inicio
        else:
            ttft = 0

        return {
            "respuesta": respuesta_texto,
            "tokens": tokens,
            "ttft_segundos": round(ttft, 4),
            "tokens_por_segundo": round(velocidad, 4),
            "tiempo_total": round(fin - inicio, 4)
        }

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "No se pudo conectar con Ollama. "
            "Verifique que el servidor este funcionando."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "La solicitud tardo demasiado tiempo."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Error HTTP al consultar Ollama: {error}"
        )

    except (json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(
            f"Error al procesar la respuesta: {error}"
        )


def cargar_prompts(ruta):
    """Lee las preguntas guardadas en el archivo JSON."""

    with open(ruta, "r", encoding="utf-8") as archivo:
        preguntas = json.load(archivo)

    if not isinstance(preguntas, list):
        raise ValueError("El archivo debe contener una lista de prompts.")

    for pregunta in preguntas:
        if not isinstance(pregunta, dict) or not pregunta.get("prompt"):
            raise ValueError("Se encontro un prompt sin contenido.")

    return preguntas


def guardar_resultados(resultados):
    """Guarda las respuestas y metricas en archivos CSV y JSON."""

    carpeta = BASE / "results"
    carpeta.mkdir(exist_ok=True)

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    archivo_csv = carpeta / f"resultados_{fecha}.csv"
    archivo_json = carpeta / f"resultados_{fecha}.json"

    columnas = [
        "id",
        "categoria",
        "modelo",
        "temperatura",
        "max_tokens",
        "prompt",
        "respuesta",
        "tokens",
        "ttft_segundos",
        "tokens_por_segundo",
        "tiempo_total"
    ]

    with open(archivo_csv, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)

    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(resultados, archivo, ensure_ascii=False, indent=4)

    print("\nResultados guardados correctamente.")
    print("CSV:", archivo_csv)
    print("JSON:", archivo_json)


def main():
    """Funcion principal del programa."""

    parser = argparse.ArgumentParser(
        description="Pruebas de inferencia con Mistral AI y Ollama"
    )

    parser.add_argument(
        "--model",
        default="ministral-3:8b",
        help="Modelo que se utilizara"
    )

    grupo = parser.add_mutually_exclusive_group(required=True)

    grupo.add_argument(
        "--prompt",
        help="Pregunta individual"
    )

    grupo.add_argument(
        "--file",
        help="Archivo JSON con las preguntas"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperatura de muestreo"
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=500,
        help="Cantidad maxima de tokens generados"
    )

    args = parser.parse_args()

    if not 0 <= args.temperature <= 2:
        parser.error("La temperatura debe estar entre 0 y 2.")

    if args.max_tokens < 1:
        parser.error("max-tokens debe ser mayor que cero.")

    try:
        if args.prompt:
            preguntas = [{
                "id": 1,
                "categoria": "individual",
                "prompt": args.prompt
            }]
        else:
            ruta = Path(args.file)
            preguntas = cargar_prompts(ruta)

        resultados = []

        print("\nIniciando pruebas con:", args.model)
        print("Cantidad de preguntas:", len(preguntas))

        for numero, pregunta in enumerate(preguntas, start=1):
            print(f"\nEjecutando pregunta {numero}/{len(preguntas)}")

            resultado = consultar_modelo(
                args.model,
                pregunta["prompt"],
                args.temperature,
                args.max_tokens
            )

            registro = {
                "id": pregunta.get("id", numero),
                "categoria": pregunta.get("categoria", "sin_categoria"),
                "modelo": args.model,
                "temperatura": args.temperature,
                "max_tokens": args.max_tokens,
                "prompt": pregunta["prompt"],
                **resultado
            }

            resultados.append(registro)

            print("Respuesta:", resultado["respuesta"])
            print("Tokens generados:", resultado["tokens"])
            print("TTFT:", resultado["ttft_segundos"], "segundos")
            print("Velocidad:", resultado["tokens_por_segundo"], "tokens/s")
            print("Tiempo total:", resultado["tiempo_total"], "segundos")

        guardar_resultados(resultados)

    except (
        RuntimeError,
        OSError,
        ValueError,
        json.JSONDecodeError
    ) as error:
        print("\nError durante la ejecucion:")
        print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

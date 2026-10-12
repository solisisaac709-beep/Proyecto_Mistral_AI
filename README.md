# Proyecto Mistral AI — Ministral 3 8B

Este es mi proyecto de investigación para Programación IV. Instalé Ministral 3 8B con Ollama y creé un cliente Python para enviar preguntas, guardar respuestas y medir tiempos. Después comparé la ejecución desde Windows y desde Docker, además de analizar recursos y calidad de respuestas.

## Equipo utilizado

- Windows 11, 64 bits.
- AMD Ryzen 7 5700X; 32 GB de RAM.
- AMD Radeon RX 6700 con 10 GB de VRAM reportados.
- Python 3.13, Ollama y Docker Desktop.

## Cómo funciona

**Ollama y el modelo corren en Windows.** El contenedor Docker tiene el cliente Python y se conecta al mismo Ollama por HTTP. Por esta razón, Docker no ejecuta el modelo en otra GPU ni sus límites de CPU y RAM limitan a Ollama.

## Carpetas y archivos principales

- `src/inference.py`: envía las preguntas y registra TTFT, tokens y tiempo total.
- `src/monitor_recursos.py`: monitorea CPU, RAM, proceso de Ollama y contadores de GPU **en Windows**.
- `src/analisis_recursos.py`, `src/comparar_recursos.py`, `src/comparar_temperaturas.py`: analizan los CSV/JSON.
- `src/evaluar_calidad.py`: prepara una plantilla para puntuar respuestas; **no las califica automáticamente**.
- `src/graficos.py`: genera los 17 gráficos a partir de los resultados guardados.
- `prompts/suite.json`: diez preguntas en cinco categorías.
- `results/`: archivos de pruebas y métricas.
- `docs/graficos/`: gráficos generados; `docs/`: evidencias y documentación.
- `Dockerfile`, `.dockerignore`, `requirements.txt`: configuración del contenedor y dependencias.

## Preparación inicial (PowerShell en la carpeta del proyecto)

Instalar Ollama y Docker Desktop antes de comenzar. Luego ejecutar:

```powershell
ollama pull ministral-3:8b
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No hace falta activar el entorno virtual; los comandos utilizan directamente su `python.exe`, lo que evita problemas con la política de ejecución de PowerShell.

## Ejecución en Windows

Un solo prompt:

```powershell
.\.venv\Scripts\python.exe src/inference.py --model ministral-3:8b --prompt "Explica que es la inteligencia artificial" --temperature 0.2 --max-tokens 100
```

Los diez prompts:

```powershell
.\.venv\Scripts\python.exe src/inference.py --model ministral-3:8b --file prompts/suite.json --temperature 0.2 --max-tokens 500
```

El programa muestra la respuesta, TTFT, tokens por segundo y tiempo total; además crea archivos CSV y JSON en `results/`.

## Ejecución mediante Docker

Ollama debe estar ejecutándose en Windows y su API debe ser accesible desde Docker Desktop.

Construir la imagen y verificar el usuario:

```powershell
docker build -t mistral-ai-proyecto:latest .
docker run --rm --entrypoint id mistral-ai-proyecto:latest
```

Ejecutar un prompt con límites para el **cliente**:

```powershell
docker run --rm --cpus="2" --memory="2g" --add-host=host.docker.internal:host-gateway -e OLLAMA_URL=http://host.docker.internal:11434/api/generate -v "${PWD}/results:/app/results" -v "${PWD}/prompts:/app/prompts:ro" mistral-ai-proyecto:latest --model ministral-3:8b --prompt "Explica brevemente que es la inteligencia artificial." --temperature 0.2 --max-tokens 100
```

Para las diez preguntas, utilizar el mismo comando y reemplazar `--prompt "..."` por `--file prompts/suite.json` y `--max-tokens 500`.

Los parámetros `--cpus` y `--memory` limitan el contenedor Python, **no** el servidor Ollama de Windows. El modelo no se copia dentro de la imagen Docker.

## Archivos oficiales de la comparación Windows / Docker

Las seis corridas principales, de diez respuestas cada una, son:

| Entorno | JSON de las tres corridas |
| --- | --- |
| Windows | `resultados_20261011_151650_913926.json`, `resultados_20261011_152651_308671.json`, `resultados_20261011_153006_320986.json` |
| Docker | `resultados_20261011_220322_432084.json`, `resultados_20261011_220533_422600.json`, `resultados_20261011_220859_524549.json` |

Se usó el mismo modelo (`ministral-3:8b`), la misma suite de diez prompts, temperatura 0.2 y máximo de 500 tokens.

La comparación de temperatura 0.2 frente a 0.9 usa:

- `resultados_20261011_151650_913926.json` (0.2).
- `resultados_20261011_183330_778413.json` (0.9).

Los demás archivos `resultados_*.csv/json` son pruebas preliminares, ejecuciones complementarias o verificaciones individuales. **No se mezclan con las seis corridas principales del informe.**

## Análisis y gráficos

Una vez que existen los archivos de resultados, se pueden generar o actualizar los resúmenes:

```powershell
.\.venv\Scripts\python.exe src/analisis_recursos.py
.\.venv\Scripts\python.exe src/comparar_recursos.py
.\.venv\Scripts\python.exe src/comparar_temperaturas.py
.\.venv\Scripts\python.exe src/graficos.py
```

Los scripts de recursos utilizan los archivos `recursos_windows_01.csv` hasta `03.csv` y `recursos_docker_01.csv` hasta `03.csv`. Para usar el monitor en otro equipo de Windows podría ser necesario cambiar `GPU_LUID` en `src/monitor_recursos.py`. Ese contador identifica el **motor GPU más activo**, no el porcentaje global de uso de la tarjeta.

La evaluación de calidad usa dos archivos distintos:

- `results/evaluacion_calidad.csv`: plantilla con espacios vacíos para revisar respuestas.
- `results/evaluacion_calidad_revisada.csv`: valoraciones registradas y utilizadas en los gráficos 16 y 17; son subjetivas y deben justificarse con las respuestas originales.

**Cuidado:** ejecutar `src/evaluar_calidad.py` vuelve a generar la plantilla `evaluacion_calidad.csv`. No modifica el archivo `evaluacion_calidad_revisada.csv`.

## Prueba adicional solo con CPU

El requisito de inferencia únicamente con CPU **aún necesita una ejecución y evidencia propias**. No debe confundirse con ejecutar el cliente Docker con `--cpus=2`: Ollama seguiría usando la GPU de Windows. Esta prueba se incorporará cuando se haya realizado realmente.

## Resultados y limitaciones

- Velocidad media de las corridas principales: Windows 24.56 tokens/s y Docker 24.44 tokens/s.
- Ambos clientes usan el mismo Ollama en Windows. No se puede atribuir una mejora de inferencia a Docker con estas mediciones.
- Los promedios de CPU/RAM describen el equipo completo y pueden incluir otros programas abiertos.
- Los resultados de electricidad del informe son estimaciones, no consumos medidos con vatímetro.

## Autor

Proyecto académico individual desarrollado con pruebas locales y resultados disponibles en este repositorio.

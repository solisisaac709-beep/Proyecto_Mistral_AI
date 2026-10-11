
# Proyecto Mistral AI

## Descripción

Proyecto universitario de evaluación de inteligencia artificial
utilizando el modelo Ministral 3 8B, ejecutado localmente
mediante Ollama.

El proyecto permite realizar consultas al modelo desde Python,
medir su rendimiento y guardar los resultados en archivos
CSV y JSON.

También se utiliza Docker para ejecutar el programa en
un entorno aislado.

## Tecnologías utilizadas

- Python 3.13
- Ministral 3 8B
- Ollama
- Docker
- Git
- Visual Studio Code
- Biblioteca Requests

## Equipo utilizado

- Sistema operativo: Windows 11 de 64 bits
- Procesador: AMD Ryzen 7 5700X
- Memoria RAM: 32 GB
- Tarjeta gráfica: AMD Radeon RX 6700
- VRAM reportada: 10 GB

## Estructura del proyecto

Proyecto_Mistral_AI/
- src/
  - inference.py
- prompts/
  - suite.json
- results/
- docs/
- Dockerfile
- .dockerignore
- .gitignore
- requirements.txt
- README.md

## Modelo utilizado

Modelo: ministral-3:8b

El modelo se ejecuta localmente con Ollama.

Comando para descargarlo:

ollama pull ministral-3:8b

## Instalación de dependencias

Crear el entorno virtual:

py -3.13 -m venv .venv

Activar el entorno en PowerShell:

.\.venv\Scripts\Activate.ps1

Instalar dependencias:

python -m pip install -r requirements.txt

## Ejecución local

Para ejecutar una pregunta individual:

python src/inference.py --prompt "Que es la inteligencia artificial?" --temperature 0.2 --max-tokens 500

Para ejecutar los diez prompts:

python src/inference.py --file prompts/suite.json --temperature 0.2 --max-tokens 500

## Ejecución con Docker

Construir la imagen:

docker build -t mistral-ai-proyecto .

Ejecutar las diez preguntas desde PowerShell:

docker run --rm -e OLLAMA_URL=http://host.docker.internal:11434/api/generate -v "${PWD}\results:/app/results" mistral-ai-proyecto --file prompts/suite.json --temperature 0.2 --max-tokens 500

Docker ejecuta el programa Python y utiliza el servidor
Ollama instalado en Windows.

## Evaluación

Se realizaron pruebas en cinco categorías:

1. Generación de texto.
2. Resumen de información.
3. Corrección y traducción.
4. Generación de código.
5. Razonamiento y veracidad.

Se utilizaron diez prompts.

Las pruebas se realizaron con temperatura 0.2 y límites
de generación de 250 y 500 tokens.

## Métricas

Primera ejecución:

- TTFT promedio: 3.2749 segundos
- Velocidad promedio: 24.373 tokens/s
- Tiempo total promedio: 9.3174 segundos
- Tokens generados: 1461

Segunda ejecución:

- TTFT promedio: 3.9663 segundos
- Velocidad promedio: 24.5916 tokens/s
- Tiempo total promedio: 13.3038 segundos
- Tokens generados: 2270

## Resultados

El modelo presentó resultados favorables en tareas de
traducción, corrección, programación y razonamiento.

También se identificaron limitaciones en respuestas
extensas y afirmaciones cuantitativas sin respaldo.

Los resultados se almacenan en archivos CSV y JSON.

## Autor

Proyecto académico individual.

## Consideraciones

Los resultados dependen del hardware, la configuración
del modelo y las características de las preguntas.

Las respuestas generadas por inteligencia artificial
deben verificarse antes de utilizarse como información
definitiva.

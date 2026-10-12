
# Configuración y pruebas de Docker

## Proyecto Mistral AI — Programación IV

### 1. Objetivo

Implementar un contenedor Docker para ejecutar el cliente Python
que se comunica con el modelo Ministral 3 8B mediante Ollama.

El servidor Ollama se ejecuta en Windows. Por lo tanto, el
contenedor no ejecuta directamente el modelo de inteligencia
artificial ni administra su memoria GPU.

### 2. Imagen utilizada

- Nombre: mistral-ai-proyecto:latest
- Imagen base: python:3.13-slim
- Tamaño reportado: 513572986 bytes
- Tamaño aproximado: 513.57 MB
- Usuario configurado: mistral

### 3. Seguridad

Se creó un usuario sin privilegios administrativos llamado
mistral y se configuró mediante la instrucción USER.

La comprobación se realizó con:

docker run --rm --entrypoint id mistral-ai-proyecto:latest

Resultado:

uid=999(mistral) gid=999(mistral) groups=999(mistral)

Esto confirma que el proceso principal del contenedor se
ejecuta sin utilizar el usuario root.

### 4. Optimización de construcción

El Dockerfile copia requirements.txt e instala las dependencias
antes de copiar el código fuente.

Esta organización permite reutilizar las capas de instalación
cuando se modifica el código sin cambiar las dependencias.

Se utiliza pip install --no-cache-dir para evitar conservar
la caché de paquetes de pip dentro de la imagen.

La construcción se completó correctamente mediante docker build.

### 5. Límites de recursos

Se ejecutó una prueba utilizando los siguientes parámetros:

- --cpus="2"
- --memory="2g"

Estos parámetros establecen límites para el contenedor que
ejecuta Python, no para el servidor Ollama de Windows.

### 6. Resultados de la prueba

Modelo: ministral-3:8b
Temperatura: 0.2
Límite de generación: 100 tokens

- Tokens generados: 100
- TTFT: 10.5988 segundos
- Velocidad: 24.682 tokens por segundo
- Tiempo total: 14.6518 segundos

La prueba terminó correctamente y generó archivos CSV y JSON.

### 7. Comunicación con Ollama

El contenedor se conecta al servidor Ollama mediante:

http://host.docker.internal:11434/api/generate

La dirección se proporciona mediante la variable de entorno
OLLAMA_URL.

### 8. Limitaciones de la comparación

Las pruebas de Windows y Docker utilizan el mismo servidor
Ollama y el mismo hardware de inferencia.

Por eso, los resultados comparan principalmente la ejecución
del cliente Python en dos entornos, no el rendimiento de dos
servidores de inferencia independientes.

Las mediciones de RAM y CPU del sistema también incluyen otros
procesos que estaban activos durante las pruebas.

### 9. Conclusión

Se comprobó que el cliente Python puede ejecutarse en Docker
con un usuario sin privilegios y con límites de CPU y memoria,
manteniendo la comunicación con Ollama.

La configuración mejora el aislamiento del cliente y permite
documentar las condiciones de ejecución. Sin embargo, no se
ha demostrado una reducción de recursos ni una mejora de
rendimiento atribuible exclusivamente a Docker.

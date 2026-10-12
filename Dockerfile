
# Proyecto Mistral AI - Programacion IV
# Imagen ligera de Python
FROM python:3.13-slim

# Carpeta principal del proyecto
WORKDIR /app

# Copiamos primero las dependencias para aprovechar la cache
COPY requirements.txt .

# Instalamos las bibliotecas necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Creamos un usuario sin privilegios de administrador
RUN groupadd --system mistral && \
    useradd --system --gid mistral --create-home mistral

# Copiamos los archivos del proyecto
COPY --chown=mistral:mistral src/ ./src/
COPY --chown=mistral:mistral prompts/ ./prompts/

# Creamos la carpeta de resultados con los permisos correctos
RUN mkdir -p /app/results && \
    chown -R mistral:mistral /app/results

# Ejecutamos el contenedor sin privilegios de root
USER mistral

# Ejecutamos el programa principal
ENTRYPOINT ["python", "src/inference.py"]

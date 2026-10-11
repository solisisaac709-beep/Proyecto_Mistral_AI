
# Imagen base de Python para ejecutar el proyecto
FROM python:3.13-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos las dependencias del proyecto
COPY requirements.txt .

# Instalamos las bibliotecas necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el programa y las preguntas
COPY src/ ./src/
COPY prompts/ ./prompts/

# Creamos la carpeta donde se guardan los resultados
RUN mkdir -p results

# Comando principal del contenedor
ENTRYPOINT ["python", "src/inference.py"]

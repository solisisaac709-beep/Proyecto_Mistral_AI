
# Análisis de rendimiento de Ministral 3 8B

## 1. Descripción de las pruebas

Para evaluar el rendimiento del modelo Ministral 3 8B, se realizaron pruebas utilizando Ollama y un programa desarrollado en Python.

Primero se ejecutó una suite de 10 preguntas en tres ocasiones directamente desde Windows, obteniendo 30 respuestas. Posteriormente, se realizaron otras tres ejecuciones de la misma suite utilizando Docker, para un total de 60 respuestas evaluadas.

En ambas configuraciones se utilizó una temperatura de muestreo de 0.2 y un límite máximo de 500 tokens por respuesta.

El objetivo fue analizar el rendimiento del modelo y determinar si existían diferencias al ejecutar el programa directamente en Windows o dentro de un contenedor Docker.

## 2. Resultados estadísticos en Windows

Se realizaron tres ejecuciones de la suite de 10 preguntas, obteniendo 30 respuestas.

| Métrica | Promedio | Desviación estándar |
|---|---:|---:|
| Tokens generados | 241.5333 | 187.7046 |
| TTFT (segundos) | 3.4474 | 2.6644 |
| Velocidad (tokens/s) | 24.5579 | 0.5888 |
| Tiempo total (segundos) | 13.4111 | 9.3814 |

## 3. Interpretación de los resultados de Windows

Durante las pruebas, el modelo alcanzó una velocidad promedio de 24.56 tokens por segundo, con una desviación estándar de 0.59 tokens/s.

Esto muestra que la velocidad de generación se mantuvo relativamente estable entre las respuestas evaluadas.

El tiempo promedio hasta la generación del primer token (TTFT) fue de 3.45 segundos, mientras que el tiempo total promedio por respuesta fue de 13.41 segundos.

La cantidad de tokens generados presentó una variación mayor, debido a que las preguntas pertenecían a diferentes categorías y requerían respuestas de distintas extensiones.

## 4. Consumo de recursos del equipo

Durante una ejecución local de Ministral 3 8B, se observó el comportamiento del hardware mediante el Administrador de tareas de Windows.

El equipo utilizado cuenta con una tarjeta gráfica AMD Radeon RX 6700 de 10 GB de memoria gráfica y aproximadamente 32 GB de memoria RAM.

En la captura realizada durante la prueba se observaron los siguientes valores:

| Recurso | Valor observado |
|---|---|
| Tarjeta gráfica | AMD Radeon RX 6700 |
| Utilización de GPU | 95% |
| Memoria gráfica utilizada | 8.3 GB de 10 GB |
| Temperatura de GPU | 53 °C |
| Utilización de CPU | 16% |
| Memoria RAM utilizada | 22.0 GB de 31.9 GB |
| Utilización de RAM | 69% |

Los resultados muestran que la GPU presentó una carga importante durante la ejecución del modelo, mientras que la utilización del procesador fue considerablemente menor.

Además, mediante el comando `ollama ps`, se comprobó que Ollama reportaba el modelo cargado completamente en la GPU, con una ventana de contexto de 4096 tokens y un tamaño cargado de 5.6 GB.

Es importante aclarar que los valores obtenidos mediante el Administrador de tareas corresponden a una observación puntual. No representan necesariamente el consumo máximo de toda la ejecución ni el consumo exclusivo del modelo.

La captura de esta prueba se encuentra documentada en el archivo `docs/21_gpu_rendimiento_mistral.png`.

## 5. Comparación de rendimiento entre Windows y Docker

Para comparar dos configuraciones de ejecución, se realizaron tres pruebas utilizando Python directamente en Windows y otras tres ejecutando el programa dentro de Docker.

En ambas configuraciones se utilizó Ministral 3 8B mediante Ollama, con los mismos parámetros y la misma suite de 10 preguntas.

En total se analizaron 60 respuestas.

### 5.1 Resultados comparativos

| Métrica | Windows | Docker |
|---|---:|---:|
| Respuestas evaluadas | 30 | 30 |
| Tokens promedio | 241.5333 | 237.7667 |
| Desviación estándar de tokens | 187.7046 | 184.0891 |
| TTFT promedio (s) | 3.4474 | 0.6450 |
| Desviación estándar de TTFT | 2.6644 | 1.1592 |
| Velocidad promedio (tokens/s) | 24.5579 | 24.4449 |
| Desviación estándar de velocidad | 0.5888 | 0.6278 |
| Tiempo total promedio (s) | 13.4111 | 10.5075 |
| Desviación estándar del tiempo total | 9.3814 | 8.1912 |

### 5.2 Análisis de los resultados

La velocidad de generación fue muy similar en ambas configuraciones.

Windows alcanzó una velocidad promedio de 24.56 tokens por segundo, mientras que Docker obtuvo 24.44 tokens por segundo.

La diferencia fue de aproximadamente un 0.46%, por lo que no se observó una variación importante en la velocidad de generación.

Por otra parte, Docker presentó un TTFT promedio de 0.65 segundos, frente a los 3.45 segundos registrados en Windows.

También se observó un menor tiempo total promedio en Docker.

Sin embargo, estos resultados no permiten afirmar que Docker acelere el modelo, ya que en ambas configuraciones la inferencia se realizó mediante Ollama en el mismo equipo.

Factores como el estado de carga del modelo, el calentamiento inicial y las condiciones del sistema pueden influir en los resultados.

### 5.3 Ventajas observadas del uso de Docker

La ejecución del programa dentro de Docker permitió comprobar que el proyecto puede funcionar en un entorno de software aislado.

Entre sus ventajas se encuentran la organización de las dependencias, la portabilidad y la posibilidad de reproducir el entorno de ejecución.

Durante las pruebas se utilizó una imagen denominada `mistral-ai-proyecto:latest`, mientras que Ollama continuó ejecutándose en Windows.

Por lo tanto, la comparación realizada corresponde a la ejecución del cliente Python dentro y fuera del contenedor, no a dos motores de inferencia diferentes.

## 6. Conclusiones generales

Las pruebas permitieron comprobar que Ministral 3 8B puede ejecutarse localmente y responder preguntas de generación de texto, resumen, traducción, programación y razonamiento.

El modelo mantuvo una velocidad de generación relativamente estable durante las 60 respuestas evaluadas.

La comparación entre Windows y Docker mostró resultados prácticamente equivalentes en cuanto a la velocidad de generación.

Aunque Docker registró menores tiempos promedio de respuesta, no se puede atribuir esa diferencia únicamente al uso de contenedores.

También se comprobó que la tarjeta gráfica AMD Radeon RX 6700 tuvo una participación importante durante la ejecución del modelo.

Los resultados obtenidos corresponden al hardware y las condiciones específicas utilizadas durante las pruebas, por lo que podrían variar en otros equipos.

Las desviaciones estándar presentadas se calcularon a partir de las respuestas individuales. Para evaluar específicamente la variación entre las tres corridas completas de cada configuración, se requieren estadísticas adicionales por ejecución.

Como mejora del análisis, queda pendiente realizar un registro automatizado de los picos de memoria RAM, memoria gráfica y utilización de CPU/GPU durante las pruebas.

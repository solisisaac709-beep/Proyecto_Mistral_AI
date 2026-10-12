
# Análisis de costos de ejecución de Mistral AI

## 1. Escenario de uso

Se analiza el funcionamiento del modelo Ministral 3 8B
durante 4 horas diarias, 22 días al mes.

Horas mensuales = 4 × 22 = 88 horas.

## 2. Ejecución local

El proyecto utiliza una computadora con una GPU AMD
Radeon RX 6700 de 10 GB y el servidor Ollama.

Para estimar el consumo eléctrico se supone una potencia
promedio de 350 W para la computadora completa.

Este valor es una hipótesis de cálculo y no una medición
realizada con un instrumento.

Consumo mensual:
0.350 kW × 88 horas = 30.8 kWh.

## 3. Costo eléctrico en Costa Rica

Distribuidora: CNFL.
Modalidad considerada: residencial ordinaria T-RE.
Vigencia de las tarifas: año 2026.

Tarifas de referencia:
- Primeros 30 kWh: cargo fijo de ₡1,744.80.
- Bloque 31-200 kWh: ₡58.16/kWh.
- Bloque 201-300 kWh: ₡89.24/kWh.
- Bloque superior a 300 kWh: ₡92.27/kWh adicional.

Costo incremental estimado para 30.8 kWh:
- A ₡58.16/kWh: ₡1,791.33.
- A ₡89.24/kWh: ₡2,748.59.
- A ₡92.27/kWh: ₡2,841.92.

Los resultados dependen del consumo habitual de la
vivienda. Si se cruzan bloques, debe aplicarse el
cálculo escalonado.

No se incluyen otros cargos de la factura.

## 4. Alternativa de infraestructura en la nube

Proveedor de referencia: Runpod.

Tarifas por hora publicadas:
- RTX A5000: US$0.27/h.
- RTX 3090: US$0.50/h.
- RTX 4090: US$0.89/h.

Costos para 88 horas:
- RTX A5000: US$23.76.
- RTX 3090: US$44.00.
- RTX 4090: US$78.32.

Los precios pueden cambiar y dependen de la
disponibilidad y modalidad de contratación.

No se incluyen almacenamiento, transferencia de datos,
impuestos ni otros posibles cargos.

## 5. Consideraciones técnicas

En la ejecución local, Docker contiene el cliente Python,
mientras que Ollama ejecuta el modelo en Windows.

Los límites de CPU y RAM configurados en Docker no
representan límites para el servidor Ollama.

Las GPU de nube analizadas no son equivalentes a la
GPU local. Por lo tanto, la comparación corresponde a
costos de infraestructura y no a rendimiento idéntico.

## 6. Conclusión

Para 88 horas mensuales, la ejecución local puede tener
un costo eléctrico incremental menor que el alquiler
de una GPU en la nube, especialmente cuando ya se
dispone del equipo.

No obstante, una comparación completa debe considerar
la compra o depreciación del hardware, el mantenimiento,
el consumo eléctrico medido y los cargos adicionales
de los servicios de nube.

## 7. Fuentes consultadas

Compañía Nacional de Fuerza y Luz. (2026).
Tarifa residencial T-RE vigente para 2026.
Publicación tarifaria en La Gaceta.
https://www.icafe.cr/wp-content/uploads/informacion_mercado/costos_actividad/unitarios_insumos/CNFL%20Tarifa%20Actual.pdf

Runpod. (s. f.). GPU cloud pricing.
https://www.runpod.io/pricing

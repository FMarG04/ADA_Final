# ADA\_Final

---

Este proyecto realiza análisis sobre grafos de gran escala (con ubicaciones geográficas), incluyendo el cálculo del camino promedio más corto, el árbol de expansión mínima (MST) y la detección de comunidades mediante un enfoque simplificado del algoritmo de Louvain.

Además, incluye una interfaz gráfica moderna para facilitar la ejecución e inspección visual de resultados.



## Características

* Carga eficiente de archivos masivos usando bloques y manejo de errores.
* Análisis de redes:

  * Longitud promedio del camino más corto (con Dijkstra).
  * Árbol de expansión mínima (MST con Prim).
  * Detección de comunidades (Louvain simplificado).
* Visualización interactiva de comunidades sobre mapa mundial (Plotly).
* Interfaz gráfica con consola embebida usando `customtkinter`.
* Limpieza automática de memoria tras la ejecución.



## Estructura esperada de archivos de entrada

* `10_million_user.txt`: Cada línea contiene las conexiones (IDs) de un usuario, separadas por comas.
* `10_million_location.txt`: Cada línea contiene la ubicación (latitud, longitud) del usuario correspondiente en la misma línea del archivo de usuarios.

Ambos archivos deben estar alineados línea por línea y ubicados en la misma carpeta que el programa.



## Requisitos

Instala las siguientes dependencias antes de ejecutar el programa:

```bash
pip install customtkinter plotly
```



## Ejecución

Ejecuta la interfaz gráfica con:

```bash
python interfaz.py
```

Aparecerá una ventana con los siguientes controles:

* Botón "Ejecutar Análisis": Inicia el análisis completo sobre una muestra.
* Botón "Ver Comunidades": Visualiza las comunidades detectadas sobre un mapa interactivo.
* Botón "Salir": Libera recursos y cierra la aplicación.

Toda la salida del análisis se muestra en vivo dentro de la interfaz.



## Flujo del Programa

### 1. Carga (`cargar` en `ADA_Proyecto.py`)

* Lee ambos archivos por bloques (configurable con `tam_bloque`).
* Extrae ubicaciones válidas y relaciones entre usuarios.
* Selecciona una muestra (`tam_muestra`) para análisis.
* Maneja errores por línea, ubicaciones faltantes o malformadas.

### 2. Análisis (también en `ADA_Proyecto.py`)

* `promedio`: Calcula la longitud promedio de caminos más cortos con Dijkstra.
* `expansion`: Calcula un Árbol de Expansión Mínima (MST) con Prim.
* `louvain`: Agrupa nodos en comunidades basándose en las conexiones.

### 3. Visualización (`interfaz.py`)

* Consola integrada muestra los resultados de forma textual.
* El botón “Ver Comunidades” lanza un mapa Plotly con colores por comunidad.

### 4. Limpieza (`liberar`)

* Borra variables que no sean críticas.
* Ejecuta el recolector de basura (`gc.collect()`).
* Termina el programa con `sys.exit()`.



## Visualización de Comunidades

* Cada comunidad detectada se representa en un color distinto.
* Se usa un gráfico tipo `Scattergeo` con `plotly.graph_objects`.
* Se valida que las coordenadas sean válidas para evitar errores de visualización.
* No se requiere imagen de fondo (`world_map.png`), ya que Plotly genera el mapa de forma automática.



## Archivos incluidos

| Archivo                   | Descripción                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `ADA_Proyecto.py`         | Código de análisis principal: carga, procesamiento y lógica de grafo. |
| `interfaz.py`             | Interfaz gráfica para ejecutar y visualizar el análisis.              |
| `10_million_user.txt`     | (No incluido) Archivo de conexiones entre usuarios.                   |
| `10_million_location.txt` | (No incluido) Archivo de ubicaciones de cada usuario.                 |


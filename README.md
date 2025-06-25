# ADA_Final

---


Este proyecto realiza análisis sobre grafos grandes (con ubicaciones geográficas), incluyendo cálculo de caminos más cortos, árboles de expansión mínima y detección de comunidades con el algoritmo de Louvain.



##  Características

* Carga eficiente desde archivos grandes de usuarios y ubicaciones.
* Cálculo de:

  * Camino promedio más corto.
  * Árbol de expansión mínima (MST).
  * Detección de comunidades con el Algoritmo de Louvain.
* Visualización interactiva de comunidades usando Plotly.
* Interfaz moderna y ligera con CustomTkinter.
* Limpieza automática de memoria tras ejecución.



##  Estructura esperada de archivos de entrada

* `10_million_user.txt`: Cada línea representa las conexiones de un usuario (IDs separados por comas).
* `10_million_location.txt`: Cada línea contiene la ubicación (latitud, longitud) correspondiente al usuario en la misma línea del archivo de conexiones.

>  Ambos archivos deben estar alineados línea por línea y en la misma carpeta que el programa.


##  Cómo ejecutar

### 1. Requisitos

Asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install customtkinter plotly
```

### 2. Ejecución

Corre el archivo de la interfaz gráfica:

```bash
python interfaz.py
```

(Usualmente algo como `main_gui.py`)

La ventana mostrará:

* **Botón "Ejecutar Análisis"**: Carga los archivos, toma una muestra y ejecuta los análisis.
* **Botón "Ver Comunidades"**: Muestra un mapa con las comunidades detectadas.
* **Botón "Salir"**: Limpia recursos y cierra la aplicación.


##  Flujo del Programa

1. **Carga (`cargar`)**:

   * Lee usuarios y ubicaciones por bloques.
   * Toma una muestra de tamaño definido (ej. 1000 usuarios).
   * Maneja errores y valores nulos.

2. **Análisis**:

   * `promedio`: Usa Dijkstra para calcular la longitud promedio de los caminos más cortos.
   * `expansion`: Aplica Prim para calcular el árbol de expansión mínima (MST).
   * `louvain`: Detecta comunidades en la muestra usando el algoritmo de Louvain.

3. **Visualización**:

   * Los resultados se muestran en consola embebida.
   * Las comunidades se grafican sobre un mapa, si se incluye `world_map.png`.

4. **Limpieza (`liberar`)**:

   * Borra variables innecesarias, fuerza el recolector de basura y termina el programa.


## Visualización de Comunidades

* Cada comunidad se muestra con un color diferente en el mapa.
* Si se encuentra `world_map.png`, se utiliza como fondo.


import time
import gc
import sys
import math
import heapq
import random  

muestra_prim = {}  # Muestra secundaria global para expansión

def liberar():
    protegidas = {
        '__name__', '__file__', '__doc__', '__package__', '__builtins__',
        'gc', 'sys', 'liberar', 'cargar', 'math', 'heapq', 'random', 'muestra_prim'
    }
    for var in list(globals().keys()):
        if var not in protegidas:
            globals().pop(var, None)
    gc.collect()
    print("Memoria liberada. Cerrando...")
    sys.exit()

def distancia(p1, p2):
    if None in p1 or None in p2:
        return float('inf')
    lat1, lon1 = p1
    lat2, lon2 = p2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def dijkstra(grafo, ubicaciones, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    heap = [(0, inicio)]

    while heap:
        d_actual, actual = heapq.heappop(heap)
        if d_actual > distancias[actual]:
            continue

        for vecino in grafo[actual]:
    
            if vecino not in ubicaciones or ubicaciones[vecino] is None or \
               actual not in ubicaciones or ubicaciones[actual] is None:
                continue  
            peso = distancia(ubicaciones[actual], ubicaciones[vecino])
            
            nueva_d = d_actual + peso
            if nueva_d < distancias[vecino]:
                distancias[vecino] = nueva_d
                heapq.heappush(heap, (nueva_d, vecino))

    return distancias

def promedio(muestra):
 
    nodos_validos = {u for u, info in muestra.items() if info['ubicacion'] is not None and None not in info['ubicacion']}
    
    ubic = {u: info['ubicacion'] for u, info in muestra.items() if u in nodos_validos}
 
    grafo_filtrado = {u: [v for v in info['conexiones'] if v in nodos_validos] for u, info in muestra.items() if u in nodos_validos}
    
    if not grafo_filtrado:
        print("Advertencia: No hay nodos con ubicaciones validas o conexiones para calcular el promedio del camino mas corto.")
        return 0

    total = 0
    conteo = 0
    for nodo_inicio in grafo_filtrado: 
        distancias = dijkstra(grafo_filtrado, ubic, nodo_inicio)
        for nodo_destino, d in distancias.items():
            if nodo_destino != nodo_inicio and d < float('inf'):
                total += d
                conteo += 1
    return total / conteo if conteo > 0 else 0

def expansion(muestra):
    global muestra_prim

    print("\n--- Arbol de expansion minima usando muestra_prim ---")
    muestra = muestra_prim  # Usa la muestra secundaria

    ubic = {u: info['ubicacion'] for u, info in muestra.items() if info['ubicacion'] is not None and None not in info['ubicacion']}

    grafo = {u: [v for v in info['conexiones'] if v in ubic] for u, info in muestra.items() if u in ubic}

    grafo = {u: connections for u, connections in grafo.items() if connections}

    if not grafo:
        print("No hay suficientes nodos con ubicaciones validas para construir un MST.")
        return

    try:
        inicio = next(iter(grafo))
    except StopIteration:
        print("El grafo filtrado esta vacio, no se puede iniciar el MST.")
        return

    visitado = set()
    mst_orden = []  
    heap = []
    peso_total = 0

    visitado.add(inicio)
    mst_orden.append(inicio)  

    for vecino in grafo[inicio]:
        if vecino in ubic and ubic[vecino] is not None: 
            peso = distancia(ubic[inicio], ubic[vecino])
            if peso < float('inf'):
                heapq.heappush(heap, (peso, inicio, vecino))

    while heap and len(visitado) < len(grafo):
        peso, desde, hacia = heapq.heappop(heap)

        if hacia in visitado:
            continue

        visitado.add(hacia)
        mst_orden.append(hacia)
        peso_total += peso

        for vecino_de_hacia in grafo[hacia]:  
            if vecino_de_hacia not in visitado and vecino_de_hacia in ubic and ubic[vecino_de_hacia] is not None:
                p_vecino = distancia(ubic[hacia], ubic[vecino_de_hacia])
                if p_vecino < float('inf'):
                    heapq.heappush(heap, (p_vecino, hacia, vecino_de_hacia))

    print("\nArbol de expansion minima (orden de nodos visitados):")
    print(', '.join(map(str, mst_orden)))
    print(f"Peso total del arbol de expansion minima: {peso_total:.4f}")

def louvain(muestra):
    print("\n--- Detectando comunidades (simplificado) ---")

    # Construir grafo válido
    grafo = {
        u: set(v for v in data['conexiones'] if v in muestra and muestra[v]['ubicacion'] is not None and None not in muestra[v]['ubicacion'])
        for u, data in muestra.items()
        if data['ubicacion'] is not None and None not in data['ubicacion']
    }

    etiquetas = {nodo: nodo for nodo in grafo}
    cambiaron = True

    while cambiaron:
        cambiaron = False
        nodos = list(grafo.keys())
        random.shuffle(nodos)
        for nodo in nodos:
            conteo = {}
            for vecino in grafo[nodo]:
                etiqueta = etiquetas[vecino]
                conteo[etiqueta] = conteo.get(etiqueta, 0) + 1
            if conteo:
                nueva = max(conteo.items(), key=lambda x: (x[1], -x[0]))[0]
                if etiquetas[nodo] != nueva:
                    etiquetas[nodo] = nueva
                    cambiaron = True

    # Agrupar por etiqueta
    comunidades = {}
    for nodo, etiqueta in etiquetas.items():
        comunidades.setdefault(etiqueta, []).append(nodo)

    # Imprimir resultados
    for i, (cid, miembros) in enumerate(sorted(comunidades.items()), 1):
        print(f"\nComunidad {i}:")
        print(f"Cantidad de usuarios: {len(miembros)}")
        print("Usuarios:", ', '.join(map(str, sorted(miembros))))

    return comunidades


def cargar(ruta_grafo, ruta_ubic, max_usuarios=None, tam_bloque=10000, tam_muestra=0):
    global muestra_prim
    total = 0
    aristas = 0
    usuarios = set()
    conexiones = {}  
    ubicaciones = {}
    muestra = {}  
    muestra_prim = {}  # Inicializa la muestra secundaria
    t0 = time.time()
    var_glob = 0
    prim_count = 0
    try:
        with open(ruta_grafo, 'r') as f_grafo, open(ruta_ubic, 'r') as f_ubic:
            while True:
                lineas_g, lineas_u = [], [] 
                for _ in range(tam_bloque):
                    lg = f_grafo.readline()
                    lu = f_ubic.readline()
                    if not lg or not lu: break  
                    if max_usuarios and total >= max_usuarios: break  
                    
                    lineas_g.append(lg)
                    lineas_u.append(lu)
                    total += 1
                
                if not lineas_g: break  

                base = total - len(lineas_g)  
                block_connections_raw = {} 

                print(f"\n--- Procesando bloque desde linea {base + 1} hasta {total} ---")
                t_bloque = time.time()
                
                for i, (lg, lu) in enumerate(zip(lineas_g, lineas_u)):
                    u = base + i  
                    try:
                        vecinos = [int(x) for x in lg.strip().split(',') if x.strip()]
                    except ValueError:
                        print(f"Advertencia: Conexiones invalidas para usuario {u} en linea de grafo. Saltando.")
                        vecinos = [] 
                    try:
                        ubicaciones[u] = tuple(map(float, lu.strip().split(',')))
                    except ValueError:
                        print(f"Advertencia: Ubicacion invalida para usuario {u} en linea de ubicacion. Estableciendo a (None, None).")
                        ubicaciones[u] = (None, None) 
                    block_connections_raw[u] = set(vecinos)

                for u_block, current_vecinos in block_connections_raw.items():
                    usuarios.add(u_block)
                    if u_block in conexiones:  
                        conexiones[u_block] += len(current_vecinos) 
                    else:
                        conexiones[u_block] = len(current_vecinos)
                    aristas += len(current_vecinos)

                users_in_block = sorted(block_connections_raw.keys()) 
                var_loc = 0
                for u_sample in users_in_block:
                    if var_glob < tam_muestra: 
                        if var_loc < 3:
                            muestra[u_sample] = { 
                                'conexiones': list(block_connections_raw.get(u_sample, set())),
                                'ubicacion': ubicaciones.get(u_sample, (None, None))
                            }
                            var_loc += 1
                            var_glob += 1

                    if prim_count <  1000:
                        muestra_prim[u_sample] = {
                            'conexiones': list(block_connections_raw.get(u_sample, set())),
                            'ubicacion': ubicaciones.get(u_sample, (None, None))
                        }
                        prim_count += 1

                del block_connections_raw, lineas_g, lineas_u
                gc.collect()
                print(f"Tiempo de bloque: {time.time() - t_bloque:.2f}s")
                
                if max_usuarios and total >= max_usuarios:
                    break  

    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {e}. Asegurate de que '10_million_user.txt' y '10_million_location.txt' existan.")
        return {}
    except Exception as e:
        print(f"Ocurrio un error inesperado durante la carga: {e}")
        return {}

    duracion = time.time() - t0
    print(f"\n--- PROCESO DE CARGA COMPLETADO ---")
    print(f"Tiempo total de carga: {duracion:.2f}s")
    print(f"Usuarios cargados: {len(usuarios)}")
    print(f"Aristas totales (estimado): {aristas}")
    print(f"Total de lineas procesadas del archivo: {total}")

    if conexiones:  
        if usuarios:
            max_conn_user = max(conexiones, key=conexiones.get)
            min_conn_user = min(conexiones, key=conexiones.get)
            print(f"Usuario con mas conexiones: {max_conn_user} ({conexiones[max_conn_user]})")
            print(f"Usuario con menos conexiones: {min_conn_user} ({conexiones[min_conn_user]})")
    else:
        print("No se encontraron conexiones para analizar.")

    print(f"Tamano de la muestra para analisis: {len(muestra)} usuarios")

    return muestra

def main():
    muestra = cargar('10_million_user.txt', '10_million_location.txt', 10000000, 10000 , 3000 )

    print("\n--- Analisis en la muestra ---") 
    print("\nCalculando longitud promedio del camino mas corto...")
    prom = promedio(muestra)
    print(f"Longitud promedio del camino mas corto en la muestra: {prom:.4f}") 
    print("\nCalculando arbol de expansion minima...")
    expansion(muestra)  # Usa muestra_prim por dentro

    comunidades = louvain(muestra)

    return {}, muestra, comunidades  # Puedes devolver más si lo necesitas


if __name__ == '__main__':
    main()
    liberar()

import time
import gc
import sys
import math
import heapq
import random  

def liberar():
    protegidas = {
        '__name__', '__file__', '__doc__', '__package__', '__builtins__',
        'gc', 'sys', 'liberar', 'cargar', 'math', 'heapq', 'random' 
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
 

def grafo(m):
    n = list(m.keys())
    g = {u: {} for u in n}
    t = 0.0
    for u in n:
        lu = m[u]['ubicacion']
        for v in m[u]['conexiones']:
            if v in m and u < v:
                lv = m[v]['ubicacion']
                d = distancia(lu, lv)
                p = 1000.0 if d == 0 else 1.0 / d
                g[u][v] = p
                g[v][u] = p
                t += p
    return g, t * 2

def grados(g):
    return {n: sum(v.values()) for n, v in g.items()}

def ganancia(g, n, c, info, t):
    if t == 0:
        return 0.0
    s = 0.0
    for v, p in g[n].items():
        if any(v in i['nodos'] and k == c for k, i in info.items()):
            s += p
    d = sum(g[n].values())
    st = info.get(c, {}).get('grado', 0.0)
    return (s - (d * st) / t) / (t / 2)

def estructura(n, com, deg):
    e = {}
    for u in n:
        c = com[u]
        if c not in e:
            e[c] = {'nodos': set(), 'grado': 0.0}
        e[c]['nodos'].add(u)
        e[c]['grado'] += deg.get(u, 0.0)
    return e

def louvain(m):
    print("\n--- Iniciando el Algoritmo de Louvain ---")
    f = {}
    for u, d in m.items():
        if d['ubicacion'] is not None and None not in d['ubicacion']:
            c = [v for v in d['conexiones'] if v in m and m[v]['ubicacion'] is not None and None not in m[v]['ubicacion']]
            f[u] = {'ubicacion': d['ubicacion'], 'conexiones': c}
    if not f:
        print("No hay nodos válidos.")
        return {}
    g, t = grafo(f)
    deg = grados(g)
    com = {n: i for i, n in enumerate(g)}
    nodos = list(g.keys())
    ite = 0
    while True:
        print(f"\n--- Iteración Louvain #{ite + 1} ---")
        mej = False
        a = nodos[:]
        random.shuffle(a)
        for n in a:
            c = com[n]
            inf = estructura(nodos, com, deg)
            if c in inf:
                inf[c]['nodos'].discard(n)
                inf[c]['grado'] -= deg[n]
                if not inf[c]['nodos']:
                    del inf[c]
            mejor = -float('inf')
            nuevo = c
            cs = set(com.get(v) for v in g[n])
            for cc in cs:
                g_mod = ganancia(g, n, cc, inf, t)
                if g_mod > mejor:
                    mejor = g_mod
                    nuevo = cc
            if nuevo != c:
                com[n] = nuevo
                mej = True
        if not mej:
            break
        mapa = {}
        for n, c in com.items():
            mapa.setdefault(c, []).append(n)
        nuevo_g = {}
        nuevo_m = {}
        for i, (c, m) in enumerate(mapa.items()):
            nuevo_m[c] = i
            nuevo_g[i] = {}
        for cu, mu in mapa.items():
            for u in mu:
                for v, p in g[u].items():
                    cv = com[v]
                    if cu == cv:
                        nuevo_g[nuevo_m[cu]][nuevo_m[cu]] = nuevo_g[nuevo_m[cu]].get(nuevo_m[cu], 0.0) + p
                    else:
                        a = nuevo_m[cu]
                        b = nuevo_m[cv]
                        nuevo_g[a][b] = nuevo_g[a].get(b, 0.0) + p
        g = nuevo_g
        com = {n: n for n in g}
        nodos = list(g.keys())
        t = sum(sum(v.values()) for v in g.values())
        ite += 1
    res = {}
    for n, c in com.items():
        res.setdefault(c, []).append(n)
    print("\n--- Comunidades detectadas ---")
    for c, m in res.items():
        print(f"Comunidad {c}: {sorted(m)}")
    return res

def cargar(ruta_grafo, ruta_ubic, max_usuarios=None, tam_bloque=10000, tam_muestra=0):
    total = 0
    aristas = 0
    usuarios = set()
    conexiones = {}  
    ubicaciones = {}
    muestra = {}  
    t0 = time.time()
    
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
                 
                for u_current, current_vecinos in block_connections_raw.items():
                    usuarios.add(u_current) 
                     
                    pass  
                 
                if u_current in block_connections_raw:
                      
                     pass  
                     
                for u_block, current_vecinos in block_connections_raw.items():
                     
                    if u_block in conexiones:  
                        conexiones[u_block] += len(current_vecinos) 
                    else:
                        conexiones[u_block] = len(current_vecinos)
                     
                    aristas += len(current_vecinos)
                 
                users_in_block = sorted(block_connections_raw.keys()) 
                for u_sample in users_in_block:
                    if len(muestra) < tam_muestra: 
                        muestra[u_sample] = {
                            'conexiones': list(block_connections_raw.get(u_sample, set())), # Use the raw connections for this user
                            'ubicacion': ubicaciones.get(u_sample, (None, None))
                        }
                    else:
                        break  

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

    aristas //= 2  
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
    muestra = cargar('10_million_user.txt', '10_million_location.txt', 10000, 1000 , 1000)

    print("\n--- Analisis en la muestra ---") 
    print("\nCalculando longitud promedio del camino mas corto...")
    prom = promedio(muestra)
    print(f"Longitud promedio del camino mas corto en la muestra: {prom:.4f}") 
    print("\nCalculando arbol de expansion minima...")
    expansion(muestra)

    comunidades = louvain(muestra)

    return {}, muestra, comunidades  # Puedes devolver más si lo necesitas


if __name__ == '__main__':
    main()
    liberar()

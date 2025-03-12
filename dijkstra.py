import heapq
from math import sqrt

def calculate_distance(p1, p2):
    """
    Calculeaza distanta euclidiana intre doua puncte.
    :param p1: Tuple (x1, y1)
    :param p2: Tuple (x2, y2)
    :return: Distanta euclidiana
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def dijkstra(nodes, edges, start_node, end_node):
    """
    Implementarea algoritmului Dijkstra pentru calculul celui mai scurt drum intr-un graf.
    :param nodes: Dictionar {nod_id: (x, y)} cu toate nodurile si coordonatele lor.
    :param edges: Lista de muchii (source, target, weight) care definesc graful.
    :param start_node: Nodul de start pentru algoritm.
    :param end_node: Nodul de final pentru care se calculeaza drumul minim.
    :return: O lista reprezentand drumul minim si distanta drumului.
    """

    # 1. Initializari
    d = {node: float('inf') for node in nodes}  # Initializam distantele nodurilor cu infinit
    p = {node: None for node in nodes}          # Initializam predecesorii nodurilor cu None
    d[start_node] = 0                           # Distanta nodului de start este 0

    # 2. Construirea grafului ca dictionar de adiacenta
    graph = {node: [] for node in nodes}        # Initializam lista de adiacenta
    for u, v, w in edges:
        graph[u].append((v, w))                 # Adaugam muchiile in lista de adiacenta
    
    # 3. Configurarea cozii de prioritati (heap)
    heap = [(0, start_node)]  # Adaugam nodul de start cu distanta 0 in heap
    visited = set()           # Multimea nodurilor vizitate

    # 4. Procesarea nodurilor folosind heap-ul
    while heap:
        dist, x = heapq.heappop(heap)  # Scoatem nodul cu distanta minima
        if x in visited:               # Daca nodul a fost deja vizitat, il ignoram
            continue
        visited.add(x)                 # Marcam nodul ca vizitat

        # Relaxarea muchiilor pentru vecinii nodului x
        for y, weight in graph[x]:
            if d[y] > d[x] + weight:   # Verificam daca putem obtine o distanta mai mica
                d[y] = d[x] + weight   # Actualizam distanta minima
                p[y] = x               # Actualizam predecesorul nodului y
                heapq.heappush(heap, (d[y], y))  # Adaugam vecinul in coada de prioritati
    
    # 5. Reconstruirea drumului minim
    path = []                 # Lista pentru drumul minim
    current = end_node        # Pornim de la nodul final
    while current is not None:
        path.append(current)  # Adaugam nodul curent in drum
        current = p[current]  # Trecem la predecesorul nodului curent
    path.reverse()            # Inversam ordinea pentru a obtine drumul de la start la final

    # 6. Returnarea drumului si a distantei minime
    return path, d[end_node]

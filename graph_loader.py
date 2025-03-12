import xml.etree.ElementTree as ET

def load_graph_from_xml(file_path):
    """
    Încarcă un graf dintr-un fișier XML.
    :param file_path: Calea către fișierul XML.
    :return: Un tuplu cu două componente:
             - nodes: Dictionar {nod_id: (longitude, latitude)} - coordonatele nodurilor.
             - edges: Listă de tupluri (source, target, weight) - muchiile cu greutățile lor.
    """
    nodes = {}  # Inițializăm un dicționar gol pentru noduri
    edges = []  # Inițializăm o listă goală pentru muchii

    # Parsăm fișierul XML
    tree = ET.parse(file_path)  # Parsează fișierul XML într-un arbore
    root = tree.getroot()       # Obține rădăcina arborelui XML

    # 1. Citirea nodurilor din tag-ul <nodes>
    for node in root.find("nodes"):  # Caută și iterează prin toate nodurile
        node_id = int(node.get("id"))              # Preia atributul 'id' al nodului
        longitude = int(node.get("longitude"))     # Preia atributul 'longitude' (x)
        latitude = int(node.get("latitude"))       # Preia atributul 'latitude' (y)
        nodes[node_id] = (longitude, latitude)     # Adaugă nodul în dicționar

    # 2. Citirea muchiilor din tag-ul <arcs>
    if root.find("arcs"):  # Verifică dacă există tag-ul <arcs> în fișier
        for arc in root.find("arcs"):  # Iterează prin fiecare muchie (arc)
            source = int(arc.get("from"))          # Nodul sursă al arcului
            target = int(arc.get("to"))            # Nodul destinație al arcului
            weight = float(arc.get("length", 1))   # Lungimea arcului (default = 1)
            edges.append((source, target, weight)) # Adaugă muchia în lista de muchii

    # 3. Returnează nodurile și muchiile
    return nodes, edges

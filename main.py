from graph_loader import load_graph_from_xml
from visualizer import MapVisualizer

def main():
    file_path = "luxembourg_map.xml"
    nodes, edges = load_graph_from_xml(file_path)

    visualizer = MapVisualizer(nodes, edges)
    visualizer.run()
    visualizer.close()

if __name__ == "__main__":
    main()

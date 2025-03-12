# 🗺️ Dijkstra Map Visualizer (Luxembourg) 

An interactive Python application that visualizes the shortest path between two points on a real-world map of Luxembourg using Dijkstra’s algorithm. Users can zoom, pan, and select nodes with clicks. The application reads the road network from an XML file and draws the graph on screen using Pygame.

## 🚀 Features

- Loads nodes and edges from `luxembourg_map.xml`
- Visualizes the full graph using Pygame
- Allows zoom and pan using on-screen buttons
- Users can select two nodes by clicking on the map
- Computes and displays the shortest path using Dijkstra’s algorithm

## 🧠 How It Works

- `graph_loader.py`: Loads the graph (nodes and edges) from XML
- `dijkstra.py`: Dijkstra’s shortest path algorithm implementation
- `visualizer.py`: Interactive map renderer using Pygame (supports zoom, pan, node selection)
- `main.py`: Entry point that wires everything together

## ▶️ Run the App

```bash
python main.py
```
- Click two nodes on the map to compute the shortest path
- Use on-screen buttons to zoom in/out or pan (← ↑ ↓ →)

## 📦 Requirements

- Python 3.8+
- Pygame: `pip install pygame`
- Make sure `luxembourg_map.xml` is in the same directory.

import matplotlib.pyplot as plt
import networkx as nx
import json
from pyvis.network import Network

def load_graph_from_json(filename) -> nx.DiGraph:
    with open(filename, 'r') as file:
        data = json.load(file)
    return nx.node_link_graph(data)


def visualize_and_save_graph_png(graph, filename):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(16, 16))
    nx.draw(graph, pos, with_labels=True, node_size=100, font_size=10, node_color='lightblue', edge_color='gray')
    plt.title('Wikipedia Graph Visualization')
    plt.savefig(filename)
    plt.close()

def visualize_and_save_graph_html(graph, filename):
    pos = nx.spring_layout(graph)
    net = Network(notebook=False)
    for node in graph.nodes():
        net.add_node(node, x=pos[node][0], y=pos[node][1])
    for edge in graph.edges():
        net.add_edge(edge[0], edge[1])
    net.write_html(filename)

if __name__ == '__main__':
    filename = "../EX00/wiki_graph.json"

    image_filename = 'wiki_graph.png'
    html_filename = 'wiki_graph.html'

    loading = load_graph_from_json(filename)
    print(loading)
    visualize_and_save_graph_png(loading, image_filename)
    visualize_and_save_graph_html(loading, html_filename)
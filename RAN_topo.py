import networkx as nx
import matplotlib.pyplot as plt

def create_topo(num_RUs, num_DUs, num_CUs):
    # Tạo đồ thị
    G = nx.Graph()

    # Thêm các nút RU, DU, CU
    RUs = [f'RU{i+1}' for i in range(num_RUs)]
    DUs = [f'DU{i+1}' for i in range(num_DUs)]
    CUs = [f'CU{i+1}' for i in range(num_CUs)]

    # Thêm các nút vào đồ thị
    G.add_nodes_from(RUs, type='RU')
    G.add_nodes_from(DUs, type='DU')
    G.add_nodes_from(CUs, type='CU')

    # Liên kết các DUs với CUs (fully connected)
    for du in DUs:
        for cu in CUs:
            G.add_edge(du, cu)

    # Liên kết RU1 và RU2 với DU1, RU3 và RU4 với DU2
    G.add_edge('RU1', 'DU1')
    G.add_edge('RU2', 'DU1')
    G.add_edge('RU3', 'DU2')
    G.add_edge('RU4', 'DU2')

    # Vị trí của các nút: RU, DU, CU xếp thành cột
    pos = {
        'RU1': (0, 3), 'RU2': (0, 2), 'RU3': (0, 1), 'RU4': (0, 0),
        'DU1': (1, 2.5), 'DU2': (1, 0.5),
        'CU1': (2, 2), 'CU2': (2, 1)
    }
    # print(G.edges)
    # print(G.nodes)
    # Vẽ đồ thị
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, 
            font_size=10, font_weight='bold', edge_color='gray')
    plt.title(f"Network Model: {num_RUs} RU, {num_DUs} DU, {num_CUs} CU (Column Layout)", fontsize=15)
    plt.show()


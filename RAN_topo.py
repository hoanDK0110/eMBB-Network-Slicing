import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_topo(num_RUs, num_DUs, num_CUs):
    # Tạo đồ thị
    G = nx.Graph()

    # Tạo danh sách các nút và dung lượng
    RUs = [f'RU{i+1}' for i in range(num_RUs)]
    DUs = [f'DU{i+1}' for i in range(num_DUs)]
    CUs = [f'CU{i+1}' for i in range(num_CUs)]

    # Thêm các nút vào đồ thị với dung lượng = 100
    for ru in RUs:
        G.add_node(ru, type='RU', capacity=100)
    for du in DUs:
        G.add_node(du, type='DU', capacity=100)
    for cu in CUs:
        G.add_node(cu, type='CU', capacity=100)

    # Liên kết các DUs với CUs (fully connected)
    for du in DUs:
        for cu in CUs:
            G.add_edge(du, cu)

    # Tính số lượng RU mỗi DU kết nối
    ru_per_du = max(1, num_RUs // num_DUs)  # Tránh chia cho 0

    # Kết nối RUs với DUs theo tỉ lệ đã cho
    for i in range(0, num_RUs, ru_per_du):
        du_index = i // ru_per_du
        if du_index < num_DUs:  # Kiểm tra chỉ số DU có hợp lệ không
            for j in range(ru_per_du):
                if i + j < num_RUs:  # Kiểm tra xem RU có tồn tại không
                    G.add_edge(RUs[i + j], DUs[du_index])  # Kết nối RU với DU tương ứng

    # Kết nối các RU dư với các DU cuối
    remainder = num_RUs % num_DUs
    if remainder > 0:
        for j in range(remainder):
            G.add_edge(RUs[-(j + 1)], DUs[-(j + 1)])  # Kết nối RU dư với DU cuối

    # Vị trí của các nút: RU, DU, CU xếp thành cột
    pos = {ru: (0, 3 - i) for i, ru in enumerate(RUs)}
    pos.update({du: (1, 2.5 - i * 2) for i, du in enumerate(DUs)})
    pos.update({cu: (2, 2 - i) for i, cu in enumerate(CUs)})

    # Vẽ đồ thị với các tùy chỉnh
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')

    # Vẽ các nút
    node_colors = ['lightblue' if 'RU' in node else 'lightgreen' if 'DU' in node else 'lightcoral' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, linewidths=2)

    # Hiển thị dung lượng mỗi nút trên đồ thị
    node_labels = {node: f"{node}\nCap: {data['capacity']}" for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_weight='bold', font_color='black')

    plt.title(f"Network Model: {num_RUs} RU, {num_DUs} DU, {num_CUs} CU (Column Layout)", fontsize=15)
    plt.axis('off')  # Tắt trục
    plt.tight_layout()  # Điều chỉnh bố cục
    plt.show()

    return G

def edge_detect(G,num_DUs,num_RUs, num_CUs):
    l_RU_DU = np.zeros((num_RUs, num_DUs), dtype=int)
    for edge in G.edges:
        node1, node2 = edge
    if node1 in num_RUs and node2 in num_DUs:
        i = num_RUs.index(node1) 
        j = num_DUs.index(node2)  
        l_RU_DU[i, j] = 1   
    l_DU_CU = np.ones((num_DUs, num_CUs), dtype=int)

def get_capacity_by_type(G, node_type):
    # Lấy ra các nút theo loại (type) yêu cầu và trả về mảng capacity tương ứng
    return [data['capacity'] for node, data in G.nodes(data=True) if data['type'] == node_type]

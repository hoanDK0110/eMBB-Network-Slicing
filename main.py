import gen_RU_UE
import wireless
import RAN_topo
import solving
import benmark
import numpy as np

num_RUs = 3             # Số lượng RU (bao gồm RU ở tâm)
num_DUs = 2             # Số lượng DU
num_CUs = 1             # Số lượng CU
num_UEs = 4             # Số lượng user eMBB
radius_in = 100         # Bán kính vòng tròn trong (km)
radius_out = 1000       # Bán kính vòng tròn ngoài (km)
num_RBs = 2           # Số lượng của RBs
num_antennas = 2        # Số lượng anntenas

rb_bandwidth = 180e3    # Băng thông
# Maximum transmission power
max_tx_power_dbm = 43   # dBm
max_tx_power_watts = 10**((max_tx_power_dbm)/10) # in mWatts  
noise_power_watts = 1e-10 # Công suất nhiễu (in mWatts)

path_loss_ref = 128.1
path_loss_exp = 37.6

D_j = 30                # yêu cầu tài nguyên của node DU j
D_m = 30                # yêu cầu tài nguyên của node CU m

R_min = 1e6              # Data rate ngưỡng yêu cầu


# Khởi tạo biến
# Khởi tạo ma trận z_bi_sk (biến nhị phân)
z_bi_sk = np.zeros((num_RUs, num_UEs, num_RBs), dtype=int)

# Khởi tạo ma trận phi_i_sk (biến nhị phân cho RU-UE)
phi_i_sk = np.zeros((num_RUs, num_UEs), dtype=int)

# Khởi tạo ma trận phi_j_sk (biến nhị phân cho DU-UE)
phi_j_sk = np.zeros((num_DUs, num_UEs), dtype=int)

# Khởi tạo ma trận phi_m_sk (biến nhị phân cho CU-UE)
phi_m_sk = np.zeros((num_CUs, num_UEs), dtype=int)


#Toạ toạ độ RU
coordinates_RU = gen_RU_UE.gen_coordinates_RU(num_RUs, radius_out)                  
#Toạ toạ độ UE
coordinates_UE = gen_RU_UE.gen_coordinates_UE(num_UEs, radius_in, radius_out) 

# Vẽ mạng wireless
#graph = gen_RU_UE.plot_save_network(coordinates_RU, coordinates_UE, radius_in, radius_out)

# Tạo mạng RAN
G = RAN_topo.create_topo(num_RUs, num_DUs, num_CUs)
#RAN_topo.draw_topo(G)

# Danh sách tập các liên kết trong mạng
l_ru_du, l_du_cu = RAN_topo.get_links(G)
#print("l_ru_du: ", l_ru_du)
#print("l_du_cu: ", l_du_cu)

# Tập các capacity của các node DU, CU
A_j, A_m = RAN_topo.get_node_cap(G)
#print("A_j: ", A_j)
#print("A_m: ", A_m)

# Tính khoảng cách giữa euclid RU-UE (km)
distances_RU_UE = gen_RU_UE.calculate_distances(coordinates_RU, coordinates_UE, num_RUs, num_UEs)
#print("distances_RU_UE: ", distances_RU_UE)

# Tính độ lợi của kênh truyền 
gain = wireless.channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas, path_loss_ref, path_loss_exp)

# Tính phân bổ công suất
P_bi_sk = wireless.allocate_power(num_RUs, num_UEs, num_RBs, max_tx_power_watts)

# Giải
a, b = solving.optimize(num_UEs, num_RUs, num_DUs, num_CUs, num_RBs, max_tx_power_watts, rb_bandwidth, D_j, D_m, R_min, gain, P_bi_sk, A_j, A_m, l_ru_du, l_du_cu)  
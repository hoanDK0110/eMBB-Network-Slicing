import gen_RU_UE
import wireless
import RAN_topo
import solving
import benmark
import numpy as np

num_RUs = 4                             # Số lượng RU (bao gồm RU ở tâm)
num_DUs = 2                             # Số lượng DU
num_CUs = 2                             # Số lượng CU
num_UEs = 20                             # Số lượng user
radius_in = 100                         # Bán kính vòng tròn trong (km)
radius_out = 1000                       # Bán kính vòng tròn ngoài (km)
num_RBs = 10                             # Số lượng của RBs
num_antennas = 8                        # Số lượng anntenas

capacity_node = 100                     # Tài nguyên node

rb_bandwidth = 180e3                    # Băng thông
# Maximum transmission power
max_tx_power_dbm = 43                   # dBm
max_tx_power_watts = 10**((max_tx_power_dbm)/10) # in mWatts  
noise_power_watts = 1e-10               # Công suất nhiễu (in mWatts)

path_loss_ref = 128.1
path_loss_exp = 37.6

D_j = 20                                 # yêu cầu tài nguyên của node DU j
D_m = 20                                 # yêu cầu tài nguyên của node CU m

R_min = 1e6                             # Data rate ngưỡng yêu cầu

epsilon = 1e-6

#Toạ toạ độ RU, UE
coordinates_RU = gen_RU_UE.gen_coordinates_RU(num_RUs, radius_out)                  
coordinates_UE = gen_RU_UE.gen_coordinates_UE(num_UEs, radius_in, radius_out) 

# Tính khoảng cách giữa euclid RU-UE (km)
distances_RU_UE = gen_RU_UE.calculate_distances(coordinates_RU, coordinates_UE, num_RUs, num_UEs)

# Vẽ mạng wireless
#graph = gen_RU_UE.plot_save_network(coordinates_RU, coordinates_UE, radius_in, radius_out)

# Tạo mạng RAN
G = RAN_topo.create_topo(num_RUs, num_DUs, num_CUs, capacity_node)
#RAN_topo.draw_topo(G)

# Danh sách tập các liên kết trong mạng
l_ru_du, l_du_cu = RAN_topo.get_links(G)

# Tập các capacity của các node DU, CU
A_j, A_m = RAN_topo.get_node_cap(G)

# Tính độ lợi của kênh truyền 
gain = wireless.channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas, path_loss_ref, path_loss_exp)

# Tính phân bổ công suất
P_bi_sk = wireless.allocate_power(num_RUs, num_UEs, num_RBs, max_tx_power_watts)

# Solve
pi_sk, z_bi_sk, phi_i_sk, phi_j_sk, phi_m_sk = solving.optimize(num_UEs, num_RUs, num_DUs, num_CUs, num_RBs, max_tx_power_watts, rb_bandwidth, D_j, D_m, R_min, gain, P_bi_sk, A_j, A_m, l_ru_du, l_du_cu, epsilon) 

# Show result
benmark.print_mapping(pi_sk, z_bi_sk, phi_i_sk, phi_j_sk, phi_m_sk)
import gen_RU_UE
import wireless
import RAN_topo
import solving
import benchmark
import numpy as np
import cvxpy as cp

num_RUs = 4                 # Số lượng RU (bao gồm RU ở tâm) I
num_DUs = 2                 # Số lượng DU                    J
num_CUs = 2                 # Số lượng CU                    M
num_UEs = 3                 # Số lượng user eMBB             k
radius_in = 100             # Bán kính vòng tròn trong
radius_out = 1000           # Bán kính vòng tròn ngoài
num_RBs = 100               # Số lượng của RBs              Bi
num_antennas = 8            # Số lượng anntenas             
noise_power_watts = 1e-10
max_tx_power_watts = 43     #Pi_max
R_sk = 1e6                  #minimum requirenment throughput (10mbps)
rb_bandwidth = 180e3 
z_ue = cp.Variable((num_RUs, num_UEs, num_RBs), boolean=True)
Phi_i_s_k = cp.Variable((num_RUs, 1, num_UEs), boolean=True)
Phi_j_s_k = cp.Variable((num_DUs, 1, num_UEs), boolean=True)
Phi_m_s_k = cp.Variable((num_CUs, 1, num_UEs), boolean=True)
pi_sk =  cp.Variable(integer=True)
#những biến chưa xác định giá trị
D_du = 20
D_cu = 20

# Tạo tọa độ
coordinates_RU = gen_RU_UE.gen_coordinates_RU(num_RUs, radius_out)                  #Toạ toạ độ RU
coordinates_UE = gen_RU_UE.gen_coordinates_UE(num_UEs, radius_in, radius_out)       #Toạ toạ độ UE

gen_RU_UE.plot_save_network(coordinates_RU, coordinates_UE, radius_in, radius_out)

#Tính khoảng cách giữa euclid RU-UE
distances_RU_UE = gen_RU_UE.calculate_distances(coordinates_RU, coordinates_UE, num_RUs, num_UEs)
#print("dis:", distances_RU_UE)

# Tính độ lợi của kênh truyền 
gain = wireless.channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas)

G = RAN_topo.create_topo(num_RUs, num_DUs, num_CUs)
l_RU_DU,l_DU_CU = RAN_topo.edge_detect(G,num_DUs,num_RUs, num_CUs)
print(G.nodes(data=True)) #A_j

# Sử dụng hàm cho DU và CU
A_j = RAN_topo.get_capacity_by_type(G, 'DU')
A_m = RAN_topo.get_capacity_by_type(G, 'CU')

pi_sk,p_ue_ur = solving(num_UEs, num_DUs, num_RUs, num_RBs, num_CUs, max_tx_power_watts, gain, R_sk, rb_bandwidth, A_j, A_m, D_du, D_cu, l_RU_DU, l_DU_CU,z_ue,pi_sk,Phi_i_s_k,Phi_j_s_k,Phi_m_s_k)
print(pi_sk)
print(p_ue_ur)



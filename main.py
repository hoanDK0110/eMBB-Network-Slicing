import gen_RU_UE
import wireless
import RAN_topo
import solving
import benchmark

num_RUs = 4         # Số lượng RU (bao gồm RU ở tâm)
num_DUs = 2         # Số lượng DU
num_CUs = 2         # Số lượng CU
num_UEs = 3         # Số lượng user eMBB
num_Slice = 3       # Số lượng slice s
radius_in = 100     # Bán kính vòng tròn trong
radius_out = 1000   # Bán kính vòng tròn ngoài
num_RBs = 100       # Số lượng của RBs
num_antennas = 8    # Số lượng anntenas
noise_power_watts = 1e-10
P_max = 100
R_min = 10

# Tạo tọa độ
coordinates_RU = gen_RU_UE.gen_coordinates_RU(num_RUs, radius_out)                  #Toạ toạ độ RU
coordinates_UE = gen_RU_UE.gen_coordinates_UE(num_UEs, radius_in, radius_out)       #Toạ toạ độ UE

gen_RU_UE.plot_save_network(coordinates_RU, coordinates_UE, radius_in, radius_out)

#Tính khoảng cách giữa euclid RU-UE
distances_RU_UE = gen_RU_UE.calculate_distances(coordinates_RU, coordinates_UE, num_RUs, num_UEs)
#print("dis:", distances_RU_UE)

# Tính độ lợi của kênh truyền 
gain = wireless.channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas)

RAN_topo.create_topo(num_RUs, num_DUs, num_CUs)




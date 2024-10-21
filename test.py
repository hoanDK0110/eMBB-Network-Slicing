import numpy as np
import cvxpy as cp
import wireless
import gen_RU_UE

# Các tham số đã được định nghĩa
num_RUs = 4                             # Số lượng RU (bao gồm RU ở tâm)
num_DUs = 2                             # Số lượng DU
num_CUs = 2                             # Số lượng CU
num_UEs = 10                             # Số lượng user
radius_in = 100                         # Bán kính vòng tròn trong (km)
radius_out = 1000                       # Bán kính vòng tròn ngoài (km)
num_RBs = 2                             # Số lượng của RBs
num_antennas = 8                        # Số lượng anntenas

rb_bandwidth = 180e3                    # Băng thông
# Maximum transmission power
max_tx_power_dbm = 43                   # dBm
max_tx_power_watts = 10**((max_tx_power_dbm)/10) # in mWatts  
noise_power_watts = 1e-10               # Công suất nhiễu (in mWatts)

path_loss_ref = 128.1
path_loss_exp = 37.6

D_j = 10                                 # yêu cầu tài nguyên của node DU j
D_m = 10                                 # yêu cầu tài nguyên của node CU m

R_min = 1e6                             # Data rate ngưỡng yêu cầu

# Biến đã có sẵn
pi_sk = cp.Variable((num_RUs, num_UEs), boolean=True)

# Tính phân bổ công suất
P_bi_sk = wireless.allocate_power(num_RUs, num_UEs, num_RBs, max_tx_power_watts)

#Toạ toạ độ RU, UE
coordinates_RU = gen_RU_UE.gen_coordinates_RU(num_RUs, radius_out)                  
coordinates_UE = gen_RU_UE.gen_coordinates_UE(num_UEs, radius_in, radius_out) 

# Tính khoảng cách giữa euclid RU-UE (km)
distances_RU_UE = gen_RU_UE.calculate_distances(coordinates_RU, coordinates_UE, num_RUs, num_UEs)

# Tính độ lợi của kênh truyền 
gain = wireless.channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas, path_loss_ref, path_loss_exp)


# Khởi tạo ma trận z_bi_sk (biến nhị phân)
z_bi_sk = {}
for i in range(num_RUs):
    for k in range(num_UEs):
        for b in range(num_RBs):
            z_bi_sk[(i, k, b)] = cp.Variable(boolean=True)

# Danh sách ràng buộc
constraints = []

# Ràng buộc (15b)
for k in range(num_UEs):
    R_sk = 0
    for b in range(num_RBs):
        SNR = 0
        for i in range(num_RUs): 
            SNR += P_bi_sk[i, k, b] * z_bi_sk[(i, k, b)] * gain[i, k, b]
        R_sk += rb_bandwidth * cp.log(1 + SNR) / np.log(2)
    constraints.append(R_sk >= R_min * cp.sum(pi_sk[k]))

# Thêm ràng buộc cho pi_sk: phải là nhị phân (0 hoặc 1)
constraints += [pi_sk >= 0, pi_sk <= 1]

# Tạo hàm mục tiêu (giả sử muốn tối ưu hóa throughput)
objective = cp.Maximize(cp.sum(pi_sk))  # Hoặc bạn có thể thay đổi mục tiêu tùy theo yêu cầu

# Tạo bài toán tối ưu
problem = cp.Problem(objective, constraints)

# Giải bài toán
result = problem.solve(solver=cp.MOSEK)


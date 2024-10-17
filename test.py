import numpy as np
import cvxpy as cp

# Các tham số đã được định nghĩa
num_RUs = 4  # Số lượng RU
num_DUs = 2  # Số lượng DU
num_CUs = 2  # Số lượng CU
num_UEs = 3  # Số lượng user eMBB
radius_in = 100
radius_out = 1000
num_RBs = 100  # Số lượng RBs
num_antennas = 8
noise_power_watts = 1e-10
max_tx_power_watts = 43  # Pi_max
R_sk = np.array([1e6, 1e6, 1e6])  # minimum requirement throughput (10 Mbps) for each UE
rb_bandwidth = 180e3  # Bandwidth of RB

# Biến đã có sẵn
pi_sk = cp.Variable((num_RUs, num_UEs), integer=True)
p_ue_ur = np.empty((num_RUs, num_UEs, num_RBs), dtype=object)

# Tạo biến công suất truyền
for i in range(num_RUs):
    for k in range(num_UEs):
        for b in range(num_RBs):
            p_ue_ur[i, k, b] = cp.Variable()

# Tạo các biến và ma trận nhị phân cho bài toán
z_ue = np.random.randint(0, 2, (num_RUs, num_UEs, num_RBs))  # z_ue là nhị phân
g_ue = np.random.rand(num_RUs, num_UEs, num_RBs)  # ma trận channel gain

# Danh sách ràng buộc
constraints = []

# Ràng buộc (15b)
for k in range(num_UEs):
    temp1 = 0
    for b in range(num_RBs):
        temp2 = 0
        # Thay vì thực hiện phép nhân toàn mảng, thực hiện nhân từng phần tử
        for i in range(num_RUs):
            temp2 += p_ue_ur[i, k, b] * z_ue[i, k, b] * g_ue[i, k, b]
        temp1 += rb_bandwidth * (cp.log(1 + temp2) / 0.3)  # tính throughput của UE k
    constraints.append(temp1 >= R_sk[k] * cp.sum(pi_sk[:, k]))

# Tạo hàm mục tiêu (giả sử muốn tối ưu hóa throughput)
objective = cp.Maximize(cp.sum(pi_sk))  # Hoặc bạn có thể thay đổi mục tiêu tùy theo yêu cầu

# Tạo bài toán tối ưu
problem = cp.Problem(objective, constraints)

# Giải bài toán
problem.solve(solver=cp.MOSEK)

# In kết quả
print("pi_sk:", pi_sk.value)
print("p_ue_ur:", [[p_ue_ur[i, k, b].value for b in range(num_RBs)] for i in range(num_RUs) for k in range(num_UEs)])

import cvxpy as cp
import numpy as np

def optimizing(num_UEs, num_DUs, num_RUs, num_CUs, num_RBs, max_tx_power_watts, z_ue, g_ue, R_sk, rb_bandwidth, D_du, A_j, Phi_i_s_k, Phi_j_s_k, Phi_m_s_k):
    # Khởi tạo biến
    pi_sk = cp.Variable((num_RUs, num_UEs), integer=True)  
    p_ue_ur = np.empty((num_RUs, num_UEs, num_RBs), dtype=object)

    # Tạo biến công suất truyền cho từng RU, user, RB
    for i in range(num_RUs):
        for b in range(num_RBs):
            for k in range(num_UEs):
                p_ue_ur[i,k,b] = cp.Variable()

    # Hàm mục tiêu 
    objective = cp.Maximize(cp.sum(pi_sk))

    # Danh sách ràng buộc
    constraints = []

    # Ràng buộc (15b)
    for k in range(num_UEs):
        temp1 = 0
        for b in range(num_RBs):
            temp2 = 0
            for i in range(num_RUs): 
                temp2 += p_ue_ur[i,k,b] * z_ue[(i,k,b)] * g_ue[i,k,b]
            temp1 += rb_bandwidth * (cp.log(1 + temp2) / 0.3)
        constraints.append(temp1 >= R_sk[k] * pi_sk[:, k])

    # Ràng buộc (15c)
    for i in range(num_RUs):
        temp0 = 0
        for b in range(num_RBs):
            for k in range(num_UEs):
                temp0 += p_ue_ur[i,k,b] * z_ue[i,k,b]
        constraints.append(temp0 <= max_tx_power_watts)

    # Ràng buộc (15d)
    for j in range(num_DUs):
        temp3 = 0
        for i in range(num_RUs):
            for b in range(num_RBs):
                for k in range(num_UEs):
                    temp3 += Phi_i_s_k[i, :, k] * D_du[k]
        constraints.append(temp3 <= A_j[j])

    # Ràng buộc (15f), (15g), (15h)
    for k in range(num_UEs):
        temp_ru = 0
        for i in range(num_RUs):
            temp_ru += cp.sum(Phi_i_s_k[i, :, k])
        constraints.append(temp_ru == pi_sk[:, k])

        temp_du = 0
        for j in range(num_DUs):
            temp_du += cp.sum(Phi_j_s_k[j, :, k])
        constraints.append(temp_du == pi_sk[:, k])

        temp_cu = 0
        for m in range(num_CUs):
            temp_cu += cp.sum(Phi_m_s_k[m, :, k])
        constraints.append(temp_cu == pi_sk[:, k])

    # Ràng buộc (15i)
    for i in range(num_RUs):
        for k in range(num_UEs):
            for b in range(num_RBs):
                constraints.append(z_ue[i,k,b] <= Phi_i_s_k[i, :, k])
                constraints.append(z_ue[i,k,b] >= Phi_i_s_k[i, :, k] - 1)

    # Ràng buộc (15j)
    connection_ij = cp.Variable((num_RUs, num_DUs), boolean=True)
    for i in range(num_RUs):
        for j in range(num_DUs):
            # Ràng buộc 15j
            constraints.append(Phi_j_s_k[j, :, :] <= connection_ij[i, j] - Phi_i_s_k[i, :, :] + 1)
            # Tạo và kiểm tra sự liên kết
            constraints.append(connection_ij[i, j] <= 1)
            constraints.append(connection_ij[i, j] >= 0)

    # Ràng buộc (15k)
    connection_jm = cp.Variable((num_DUs, num_CUs), boolean=True)
    for j in range(num_DUs):
        for m in range(num_CUs):
            # Ràng buộc 15k
            constraints.append(Phi_m_s_k[m, :, :] <= connection_jm[j, m] - Phi_j_s_k[j, :, :] + 1)
            # Tạo và kiểm tra sự liên kết
            constraints.append(connection_jm[j, m] <= 1)
            constraints.append(connection_jm[j, m] >= 0)

    # Giải bài toán tối ưu
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.MOSEK)

    return pi_sk.value, p_ue_ur, connection_ij.value, connection_jm.value

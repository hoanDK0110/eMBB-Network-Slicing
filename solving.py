import cvxpy as cp
import numpy as np

def optimizing(pi_sk, num_UEs, num_DUs, num_RUs, num_CUs, num_RBs, max_tx_power_watts, z_ue, g_ue, p_ue_ur, R_sk, rb_bandwidth, D_du, D_cu, A_j, A_m, Phi_i_s_k, Phi_j_s_k, Phi_m_s_k, l_RU_DU, l_DU_CU):


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
        for k in range(num_UEs):
            temp3 += Phi_j_s_k[j, :, k] * D_du[k]
        constraints.append(temp3 <= A_j[j])
        
    # Ràng buộc (15e)
    for m in range(num_CUs):
        temp4 = 0
        for k in range(num_UEs):
            temp4 += Phi_m_s_k[m, :, k] * D_cu[k]
        constraints.append(temp4 <= A_m[m])    

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
    for i in range(num_RUs):
        for j in range(num_DUs):
            constraints.append(Phi_j_s_k[j, :, :] <= l_RU_DU[i, j] - Phi_i_s_k[i, :, :] + 1)

    # Ràng buộc (15k)
    for j in range(num_DUs):
        for m in range(num_CUs):
            constraints.append(Phi_m_s_k[m, :, :] <= l_DU_CU[j, m] - Phi_j_s_k[j, :, :] + 1)
            
    # Giải bài toán tối ưu
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.MOSEK)

    return pi_sk.value, p_ue_ur

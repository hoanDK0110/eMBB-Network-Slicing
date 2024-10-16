import cvxpy as cp
import numpy as np

def optimizing(num_UE, num_DU, num_RU, num_RB, num_CU, max_tx_power_watts, g_ue, R_sk, rb_bandwidth, A_j, D_du,l_RU_DU,l_DU_CU):
    z_ue = cp.Variable((num_RU, num_UE, num_RB), boolean=True)
    Phi_i_s_k = cp.Variable((num_RU, 1, num_UE), boolean=True)
    Phi_j_s_k = cp.Variable((num_DU, 1, num_UE), boolean=True)
    Phi_m_s_k = cp.Variable((num_CU, 1, num_UE), boolean=True)
    pi_sk =  cp.Variable(integer=True)
    obj = cp.Variable
    objective = cp.maximum
    constraint= []
    constraint.append( obj >= 0)
    p_ue_ur = np.empty((num_RU,num_UE,num_RB), dtype=object)
    for i in range(num_RU):
        for b in range(num_RB):
            for k in range(num_UE):
                p_ue_ur[i,k,b] = cp.Variable()
                constraint.append(p_ue_ur[i,k,b] >=0)
    #constraint 15c
    for i in range(num_RU):
        temp0 = 0
        for b in range(num_RB):
            for k in range(num_UE):
                temp0 += p_ue_ur[i,k,b]*z_ue[i,k,b]
        constraint.append(temp0 <= max_tx_power_watts)
    for i in range(num_RU):
        for b in range(num_RB): 
            for k in range(num_UE):
                constraint.append(z_ue[(i,k,b)] >= 0)
                constraint.append(z_ue[(i,k,b)] <= 1)
    #constraint 15b
    for k in range(num_UE):
            temp1 = 0
            for b in range(num_RB):
                temp2 = 0
                for i in range(num_RU): 
                    temp2 += p_ue_ur[i,k,b]*z_ue[(i,k,b)]*g_ue[i,k,b]
                temp1 += rb_bandwidth*(cp.log(1+ temp2)/0.3)
            constraint.append(temp1 >= R_sk*pi_sk)
    #constraint 15d
    for j in range(num_DU):
        temp3 = 0
        for i in range(num_RU):
            for b in range(num_RB):
                for k in range(num_UE):
                    temp3 += Phi_i_s_k[i, :, k] * D_du[k]
        constraint.append(temp3 <= A_j[j])
    # contraints (15f), (15g), (15h)
    for k in range(num_UE):
        temp_ru = 0
        for i in range(num_RU):
            temp_ru += cp.sum(Phi_i_s_k[i, :, k])
        constraint.append(temp_ru == pi_sk[:, k])

        temp_du = 0
        for j in range(num_DU):
            temp_du += cp.sum(Phi_j_s_k[j, :, k])
        constraint.append(temp_du == pi_sk[:, k])

        temp_cu = 0
        for m in range(num_CU):
            temp_cu += cp.sum(Phi_m_s_k[m, :, k])
        constraint.append(temp_cu == pi_sk[:, k])
    # contraint (15i)
    for i in range(num_RU):
        for k in range(num_UE):
            for b in range(num_RB):
                constraint.append(z_ue[i,k,b] <= Phi_i_s_k[i, :, k])
                constraint.append(z_ue[i,k,b] >= Phi_i_s_k[i, :, k] - 1)
    #contraint (15j)
    for j in range(num_DU):
        for i in range(num_RU):
            for k in range(num_UE):
                constraint.append(Phi_j_s_k[j, :, k] <= l_RU_DU[i,j] - Phi_i_s_k[i, :, k] + 1)
    #contraint (15k)
    for m in range(num_CU):
        for j in range(num_DU):
            for k in range(num_UE):
                constraint.append(Phi_m_s_k[m, :, k] <= l_DU_CU[j,m] - Phi_j_s_k[j, :, k] + 1)

    # Giải bài toán tối ưu
    problem = cp.Problem(objective, constraint)
    problem.solve(solver=cp.MOSEK)

    return pi_sk.value, p_ue_ur

# This is the constraint to ensure that we do not allocate RBs that have already been allocated and are currently being used by other users 
# (meaning that all RBs are an array of resource blocks for all RUs). 
# However, the paper shows that RBs are an array of resource blocks for a single RU, so I am really confused about this.
    # for b in range(num_RB): 
    #     for k in range(num_UE):
    #         for i in range(num_RU):
    #             for j in range (i,num_RU):
    #                 constraint.append(z_ue[(i,k,b)] == z_ue[(j,k,b)])
    

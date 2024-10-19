import numpy as np
import cvxpy as cp

def optimize(num_UEs, num_RUs, num_DUs, num_CUs, num_RBs, max_tx_power_watts, rb_bandwidth, D_j, D_m, R_min, gain, P_bi_sk, A_j, A_m, l_ru_du, l_du_cu):
    try:
        z_bi_sk, phi_i_sk, phi_j_sk, phi_m_sk = {}, {}, {}, {}
        # Biến phẩn bổ UE
        for i in range(num_RUs):
            for b in range(num_UEs):
                for k in range(num_RBs):
                    z_bi_sk[(i,k,b)]= cp.Variable(integer=True)

        # Biến phẩn bổ RU
        for i in range(num_RUs):
            for k in range(num_UEs):
                phi_i_sk[(i,k)]= cp.Variable(integer=True)

        # Biến phẩn bổ E
        for j in range(num_DUs):
            for k in range(num_UEs):
                phi_j_sk[(j, k)] = cp.Variable(integer=True) 

        # Biến phẩn bổ CE
        for m in range(num_CUs):
            for k in range(num_UEs):
                phi_m_sk[(m, k)] = cp.Variable(integer=True)  

        # Biến tối ưu cho việc phân bổ
        pi_sk = cp.Variable((num_RUs, num_UEs), integer=True)
        # Hàm mục tiêu 
        objective = cp.Maximize(cp.sum(pi_sk))

        # Danh sách ràng buộc
        constraints = []
        
        # Ràng buộc (15b)
        for k in range(num_UEs):
            R_sk = 0
            for b in range(num_RBs):
                SNR = 0
                for i in range(num_RUs): 
                    SNR += P_bi_sk[i, k, b] * z_bi_sk[i, k, b] * gain[i, k, b]
                R_sk += rb_bandwidth * cp.log(1 + SNR) / cp.log(2)
            constraints.append(R_sk >= R_min * cp.sum(pi_sk[:, k]))

        # Ràng buộc (15c)
        for i in range(num_RUs):
            total_power = 0
            for b in range(num_RBs):
                for k in range(num_UEs):
                    total_power += P_bi_sk[i, k, b] * z_bi_sk[i, k, b]
            constraints.append(total_power <= max_tx_power_watts)

        # Ràng buộc (15d)
        for j in range(num_DUs):
            count_du = cp.sum(phi_j_sk[j, :] * D_j)
            constraints.append(count_du <= A_j[j])
        
        # Ràng buộc (15e)
        for m in range(num_CUs):
            count_cu = cp.sum(phi_m_sk[m, :] * D_m)  
            constraints.append(count_cu <= A_m[m]) 

        # Ràng buộc (15f + 15g + 15h)
        for k in range(num_UEs):
            constraints.append(cp.sum(phi_i_sk[:, k]) == cp.sum(pi_sk[:, k]))
            constraints.append(cp.sum(phi_j_sk[:, k]) == cp.sum(pi_sk[:, k]))
            constraints.append(cp.sum(phi_m_sk[:, k]) == cp.sum(pi_sk[:, k]))

        # Ràng buộc (15i)
        for i in range(num_RUs):
            for k in range(num_UEs):
                constraints.append(cp.sum(z_bi_sk[i, k, :]) <= phi_i_sk[i, k])  
                constraints.append(cp.sum(z_bi_sk[i, k, :]) >= phi_i_sk[i, k])  

        # Ràng buộc (15j)
        for i in range(num_RUs):
            for j in range(num_DUs):
                constraints.append(phi_j_sk[j, :] <= l_ru_du[i, j] - phi_i_sk[i, :] + 1)

        # Ràng buộc (15k)
        for j in range(num_DUs):
            for m in range(num_CUs):
                constraints.append(phi_m_sk[m, :] <= l_du_cu[j, m] - phi_j_sk[j, :] + 1)

        # Giải bài toán tối ưu
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.MOSEK)

        # Lưu trữ giá trị công suất sau khi tối ưu
        P_bi_sk_values = np.zeros((num_RUs, num_UEs, num_RBs))
        for i in range(num_RUs):
            for b in range(num_RBs):
                for k in range(num_UEs):
                    P_bi_sk_values[i, k, b] = P_bi_sk[i, k, b].value

        return P_bi_sk_values, pi_sk.value

    except cp.SolverError:
        print('Solver error: non_feasible')
        return None, None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None

import numpy as np
import cvxpy as cp

def optimize(num_UEs, num_RUs, num_DUs, num_CUs, num_RBs, max_tx_power_watts, rb_bandwidth, D_j, D_m, R_min, gain, P_bi_sk, A_j, A_m, l_ru_du, l_du_cu, epsilon):
    try:
        # Khởi tạo ma trận z_bi_sk (biến nhị phân)
        z_bi_sk = {}
        for i in range(num_RUs):
            for k in range(num_UEs):
                for b in range(num_RBs):
                    z_bi_sk[(i, k, b)] = cp.Variable(boolean=True)

        # Khởi tạo các biến phi_i_sk, phi_j_sk, phi_m_sk
        phi_i_sk = cp.Variable((num_RUs, num_UEs), boolean=True)
        phi_j_sk = cp.Variable((num_DUs, num_UEs), boolean=True)
        phi_m_sk = cp.Variable((num_CUs, num_UEs), boolean=True)

        # Biến tối ưu cho việc phân bổ
        pi_sk = cp.Variable((num_UEs))

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
                    SNR += P_bi_sk[i, k, b] * z_bi_sk[(i, k, b)] * gain[i, k, b]
                R_sk += rb_bandwidth * cp.log(1 + SNR) / np.log(2)
            constraints.append(R_sk >= R_min * cp.sum(pi_sk[k]))

        # Ràng buộc (15c)
        for i in range(num_RUs):
            total_power = 0
            for b in range(num_RBs):
                for k in range(num_UEs):
                    total_power += P_bi_sk[i, k, b] * z_bi_sk[(i, k, b)]
            constraints.append(total_power <= max_tx_power_watts)

        # Ràng buộc (15d)
        for j in range(num_DUs):
            count_du = cp.sum(phi_j_sk[j, :]) * D_j
            constraints.append(count_du <= A_j[j])

        # Ràng buộc (15e)
        for m in range(num_CUs):
            count_cu = cp.sum(phi_m_sk[m, :]) * D_m
            constraints.append(count_cu <= A_m[m])

        # Ràng buộc (15f + 15g + 15h)
        for k in range(num_UEs):
            constraints.append(cp.sum(phi_i_sk[:, k]) == cp.sum(pi_sk[k]))
            constraints.append(cp.sum(phi_j_sk[:, k]) == cp.sum(pi_sk[k]))
            constraints.append(cp.sum(phi_m_sk[:, k]) == cp.sum(pi_sk[k]))

        # Ràng buộc (15i)
        for i in range(num_RUs):
            for k in range(num_UEs):
                for b in range(num_RBs):
                    constraints.append(z_bi_sk[(i, k, b)] <= phi_i_sk[i, k])
                    constraints.append(phi_i_sk[i, k] <= z_bi_sk[(i, k, b)] + (1 - epsilon))

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

        return pi_sk, z_bi_sk, phi_i_sk, phi_j_sk, phi_m_sk

    except cp.SolverError:
        print('Solver error: non_feasible')
        return None, None, None, None, None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None, None, None, None


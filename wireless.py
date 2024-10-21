import numpy as np
from numpy.linalg import norm

import numpy as np
from numpy.linalg import norm

def channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas, path_loss_ref, path_loss_exp):

    gain = np.zeros((num_RUs, num_UEs, num_RBs), dtype=np.float64)
    
    # Tính toán mất mát đường truyền (path loss)
    path_loss_db = path_loss_ref + path_loss_exp * np.log10(distances_RU_UE * 1e-3)
    
    # Chuyển đổi Path Loss từ dB sang hệ số tuyến tính
    path_loss_linear = 10 ** (-path_loss_db / 10)
    
    #print("path_loss_linear:", path_loss_linear)
    
    # Tính độ lợi kênh cho từng RU, UE và RB
    for i in range(num_RUs):  
        for k in range(num_UEs):  
            for b in range(num_RBs):  
                # Lấy độ lợi kênh cho cặp (RU, UE)
                channel_gain = path_loss_linear[i, k] / noise_power_watts
                
                # Tạo ma trận kênh với số lượng anten cho mỗi UE-RU
                h = np.sqrt(channel_gain) * np.sqrt(1/2) * (np.random.randn(num_antennas) + 1j * np.random.randn(num_antennas))
                #print("h:", h)
                # Tính norm của ma trận h
                gain[i, k, b] = norm(h, 2) ** 2  
    return gain

def allocate_power(num_RUs, U_em, num_RBs, max_tx_power_watts):

    # Khởi tạo ma trận công suất
    p_bi_sk = np.zeros((num_RUs, U_em, num_RBs))

    # Tính toán công suất tối đa phân bổ cho mỗi RB
    pp = max_tx_power_watts / num_RBs

    # Phân bổ công suất cho từng RU cho dịch vụ eMBB
    for i in range(num_RUs):
        p_bi_sk[i, :, :] = pp * np.ones((U_em, num_RBs))

    return p_bi_sk
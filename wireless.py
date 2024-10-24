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

def allocate_power(num_RUs, num_UEs, num_RBs, max_tx_power_watts, gain, user_requests):

    # Khởi tạo ma trận công suất
    p_bi_sk = np.zeros((num_RUs, num_UEs, num_RBs))

    # Tính tổng yêu cầu tài nguyên của tất cả các user
    total_user_request = np.sum(user_requests)

    # Tính toán công suất cấp phát dựa trên yêu cầu của user và điều kiện kênh truyền
    for i in range(num_RUs):
        for k in range(num_UEs):
            # Tính tổng độ lợi kênh cho tất cả các RB giữa RU và UE
            total_gain = np.sum(gain[i, k, :])

            # Điều chỉnh công suất theo độ lợi kênh và yêu cầu của user
            if total_gain > 0 and user_requests[k] > 0:
                # Công suất phân bổ cho mỗi RB theo yêu cầu tài nguyên và độ lợi kênh
                power_allocation_factor = (user_requests[k] / total_user_request) * (gain[i, k, :] / total_gain)
                p_bi_sk[i, k, :] = max_tx_power_watts * power_allocation_factor

    return p_bi_sk
import numpy as np
from numpy.linalg import norm


def channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas):
    gain = np.zeros((num_RUs, num_UEs, num_RBs), dtype=np.float64)
    
    # Tính toán mất mát đường truyền
    path_loss = 128.1 + 37.6 * np.log10(distances_RU_UE * 1e-3)

    # Tính độ lợi kênh
    for i in range(num_RUs):
        for b in range(num_RBs):
            for k in range(num_UEs):
                channel_gain = 10 ** (-path_loss[i, k] / 10) / noise_power_watts
                h = np.sqrt(channel_gain) * np.sqrt(1 / 2) * (np.random.rand(num_antennas) + 1j * np.random.rand(num_antennas))
                gain[i, k, b] = norm(h, 2) ** 2  # Lưu giá trị vào mảng gain

    return gain


# Gọi hàm và in kết quả
#gain = channel_gain(distances_RU_UE, num_RUs, num_UEs, num_RBs, noise_power_watts, num_antennas)
#print("gain: ", gain)

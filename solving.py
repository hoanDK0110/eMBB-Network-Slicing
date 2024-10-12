import cvxpy as cp
import numpy as np

def optimizing(num_UE, num_UR, num_DU, num_RU, num_RB, max_tx_power_watts, z_ue, g_ue, R_sk, rb_bandwidth):
    z_ue = {}
    pi_sk = {}
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
    for k in range(num_UE):
            temp1 = 0
            for b in range(num_RB):
                temp2 = 0
                for i in range(num_RU): 
                    temp2 += p_ue_ur[i,k,b]*z_ue[(i,k,b)]*g_ue[i,k,b]
                temp1 += rb_bandwidth*(cp.log(1+ temp2)/0.3)
            constraint.append(temp1 >= R_sk*pi_sk)

# This is the constraint to ensure that we do not allocate RBs that have already been allocated and are currently being used by other users 
# (meaning that all RBs are an array of resource blocks for all RUs). 
# However, the paper shows that RBs are an array of resource blocks for a single RU, so I am really confused about this.
    # for b in range(num_RB): 
    #     for k in range(num_UE):
    #         for i in range(num_RU):
    #             for j in range (i,num_RU):
    #                 constraint.append(z_ue[(i,k,b)] == z_ue[(j,k,b)])
    

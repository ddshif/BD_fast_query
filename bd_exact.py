import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def bd_exact1(u,v):
    b = np.zeros(N); b[u]=1; b[v]=-1
    f, *_ = np.linalg.lstsq(L, b, rcond=None)
    return np.sqrt(f@f)
def bd_exact2(u,v):
    b = np.zeros(N); b[u]=1; b[v]=-1
    L_pinv = np.linalg.pinv(L)  # 直接计算伪逆
    BD_2 = b.T @ L_pinv@ L_pinv @ b
    return np.sqrt(BD_2)
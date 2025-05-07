
import numpy as np


# 2. 完整 BackPush 实现（双残差 + X/Y/Z 校正）
def backpush_bd_full(G, s, t, r_max=1e-3):
    n = G.number_of_nodes()
    d = np.array([G.degree(i) for i in range(n)], dtype=float)
    beta_s = np.zeros(n); beta_t = np.zeros(n)
    r_s = np.zeros(n); r_t = np.zeros(n)
    r_s[s]=1.0; r_t[t]=1.0
    X = Y = Z = 0.0
    active = {s, t}
    while active:
        y = active.pop()
        deg_y = d[y]
        # push r_s
        if r_s[y]/deg_y >= r_max:
            rs = r_s[y]
            beta_s[y] += rs/deg_y
            X += (rs/deg_y)**2
            r_s[y] = 0.0
            inc = rs/deg_y
            for nbr in G[y]:
                if inc/d[nbr] >= r_max: active.add(nbr)
                r_s[nbr] += inc
        # push r_t
        if r_t[y]/deg_y >= r_max:
            rt = r_t[y]
            beta_t[y] += rt/deg_y
            Y += (rt/deg_y)**2
            r_t[y] = 0.0
            inc = rt/deg_y
            for nbr in G[y]:
                if inc/d[nbr] >= r_max: active.add(nbr)
                r_t[nbr] += inc
    # 计算 Z
    Z = np.sum((r_s - r_t)**2 / d)
    # β 校正
    denom = 1.0 + X + Y + Z
    bs = (beta_s + r_s/d - r_t/d) / denom
    bt = (beta_t + r_t/d - r_s/d) / denom
    diff = bs - bt
    bd2 = np.dot(d, diff*diff)
    return np.sqrt(bd2)
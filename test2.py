import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from backpush import backpush_bd_full
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")



# 1. 构造树结构
G = nx.Graph()
# 根节点
root = 0
G.add_node(root)
node_id = 1

# 第一层：6 个子节点
layer1 = []
for _ in range(3):
    G.add_node(node_id)
    G.add_edge(root, node_id)
    layer1.append(node_id)
    node_id += 1

# 第二层：每个第一层节点连 3 个子节点
layer2 = []
for parent in layer1:
    for _ in range(3):
        G.add_node(node_id)
        G.add_edge(parent, node_id)
        layer2.append(node_id)
        node_id += 1

# 第三层：每个第二层节点连 2 个叶节点
layer3 = []
for parent in layer2:
    for _ in range(3):
        G.add_node(node_id)
        G.add_edge(parent, node_id)
        layer3.append(node_id)
        node_id += 1

# 确认节点总数
assert node_id == 1 + 3 + 9 + 27, f"节点数不对: {node_id}"

layer1=[1, 2, 3]
layer2=[6, 7, 8, 9, 10, 11, 12,4, 5]
layer3=[23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

# 2. 同心布局
shells = [
    [root],
    layer1,
    layer2,
    layer3
]

pos = nx.shell_layout(G, shells)
N = G.number_of_nodes()





# 3. 精确 & 近似 BD 计算
L = nx.laplacian_matrix(G).toarray()
print('L:', L)

def bd_exact(u,v):
    b = np.zeros(N); b[u]=1; b[v]=-1
    f, *_ = np.linalg.lstsq(L, b, rcond=None)
    return np.sqrt(f@f)
def bd_exact2(u,v):
    b = np.zeros(N); b[u]=1; b[v]=-1
    L_pinv = np.linalg.pinv(L)  # 直接计算伪逆
    BD_2 = b.T @ L_pinv@ L_pinv @ b
    return np.sqrt(BD_2)
def rd_exact(u,v):
    b = np.zeros(N); b[u]=1; b[v]=-1
    L_pinv = np.linalg.pinv(L)  # 直接计算伪逆
    rd = b.T @ L_pinv @ b
    return rd

def bd_backpush(u,v):
    return backpush_bd_full(G, u, v, r_max=1e-3)




edge_bd = {}
for u, v in G.edges():
    # 计算精确解
    d = rd_exact(u, v)
    edge_bd[(u, v)] = d
    
for (u, v), d in sorted(edge_bd.items(), key=lambda kv: kv[1]):
    print(f"边 ({u:2d},{v:2d}) 的 BD = {d:.6f}")

# 提取距离数组并归一化到 [0,1]
ds = np.array(list(edge_bd.values()))
norm = (ds - ds.min()) / (ds.max() - ds.min() + 1e-12)

# —— 4. 构造 “红—橙—黄” 渐变色图谱 ——
cmap = LinearSegmentedColormap.from_list(
    "red_orange_yellow", ["red", "orange", "yellow"]
)

# 每条边的颜色
edge_colors = [cmap(norm[i]) for i in range(len(ds))]

# —— 5. 绘图 ——  
plt.figure(figsize=(7,7))

# 5.1 节点
nx.draw_networkx_nodes(
    G, pos,
    node_size=200,
    node_color="white",
    edgecolors="black",
    linewidths=1
)

# 5.2 边
# 需要保证 edge_colors 对应 G.edges() 的遍历顺序
for ( (u, v), color ) in zip(edge_bd.keys(), edge_colors):
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    plt.plot(
        [x1, x2], [y1, y2],
        color=color, linewidth=2
    )

# 5.3 节点编号
labels = {n: str(n) for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

# 美化
plt.axis("off")
plt.title("BD of edges", pad=10)
plt.tight_layout()
plt.show()
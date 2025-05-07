import networkx as nx
import matplotlib.pyplot as plt
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
print('layer1:', layer1)
print('layer2:', layer2)
print('layer3:', layer3)

pos = nx.shell_layout(G, shells)

# 3. 绘图
plt.figure(figsize=(6,6))
nx.draw_networkx_edges(G, pos,
                       edge_color='tab:blue',
                       width=2)
nx.draw_networkx_nodes(G, pos,
                       node_size=200,
                       node_color='white',
                       edgecolors='black',
                       linewidths=1)

# 4. 标注节点编号
labels = {n: str(n) for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.axis('off')
plt.tight_layout()
plt.show()
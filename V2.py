import time
import tracemalloc
from typing import List, Any

# 状态映射: -2: 0, -1: 1, 0: 2, 1: 3
# 2bits表示一个格子: 00(-2), 01(-1), 10(0), 11(1)
val_map = {-2: 0, -1: 1, 0: 2, 1: 3}


def generate_neighbors(rows, cols, puzzle_1d):
    neighbors = {}
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if puzzle_1d[index] == 0:  # 跳过空位(假设0是不参与交换的障碍)
                continue
            adj = []
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= ni < rows and 0 <= nj < cols:
                    n_index = ni * cols + nj
                    if puzzle_1d[n_index] != 0:
                        adj.append(n_index)
            neighbors[index] = tuple(adj)
    return neighbors


def solve_puzzle(board: List[List[int]], target_board: List[List[int]]) -> tuple:
    rows, cols = len(board), len(board[0])
    board_1d_lst = [val_map[x] for row in board for x in row]
    target_1d_lst = [val_map[x] for row in target_board for x in row]

    # 初始状态位运算化
    init_state = 0
    for i, v in enumerate(board_1d_lst):
        init_state |= (v << (i * 2))

    neighbors = generate_neighbors(rows, cols, board_1d_lst)

    # 预计算掩码
    adj_masks = [[] for _ in range(rows * cols)]
    for i in range(rows * cols):
        if i in neighbors:
            idx_shift = i * 2
            for ng in neighbors[i]:
                ng_shift = ng * 2
                # 当目标格(ng)是 1(01) 时，异或 3(11) 变 2(10)；
                # 当目标格(ng)是 3(11) 时，异或 1(01) 变 2(10)；
                # 这种位运算技巧实现了 0(空位) 与相邻格子的快速交换
                mask_1 = (3 << idx_shift) | (3 << ng_shift)
                mask_3 = (1 << idx_shift) | (1 << ng_shift)
                adj_masks[i].append((ng, ng_shift, mask_1, mask_3))

    # 目标状态可能由于“空位”在不同位置而有多个
    valid_targets = []
    for i, val in enumerate(target_1d_lst):
        if val == 1:  # 假设值1可以被空位占据
            t_state = 0
            for j, v in enumerate(target_1d_lst):
                t_state |= ((2 if j == i else v) << (j * 2))
            valid_targets.append((t_state, i))

    init_idx = board_1d_lst.index(2)

    # 双向 BFS 核心数据结构
    front_f = {init_state: init_idx}
    front_b = {t_state: t_idx for t_state, t_idx in valid_targets}
    tree_f = {init_state: (None, -1)}
    tree_b = {t_state: (None, -1) for t_state, t_idx in valid_targets}

    if init_state in tree_b:
        return 0, [], 1

    while front_f and front_b:
        # 选择较小的一端进行扩展
        if len(front_f) <= len(front_b):
            next_front = {}
            for curr, idx in front_f.items():
                for ng, ng_shift, mask_1, mask_3 in adj_masks[idx]:
                    # 提取邻居格子的当前值
                    ng_val = (curr >> ng_shift) & 3
                    new_b = curr ^ (mask_1 if ng_val == 1 else mask_3)

                    if new_b in tree_b:
                        tree_f[new_b] = (curr, ng)
                        return _reconstruct_path(tree_f, tree_b, new_b, True)

                    if new_b not in tree_f:
                        tree_f[new_b] = (curr, ng)
                        next_front[new_b] = ng
            front_f = next_front
        else:
            next_front = {}
            for curr, idx in front_b.items():
                for ng, ng_shift, mask_1, mask_3 in adj_masks[idx]:
                    ng_val = (curr >> ng_shift) & 3
                    new_b = curr ^ (mask_1 if ng_val == 1 else mask_3)

                    if new_b in tree_f:
                        tree_b[new_b] = (curr, idx)
                        return _reconstruct_path(tree_f, tree_b, new_b, False)

                    if new_b not in tree_b:
                        tree_b[new_b] = (curr, idx)
                        next_front[new_b] = ng
            front_b = next_front

    return -1, [], len(tree_f) + len(tree_b)


def _reconstruct_path(tree_f, tree_b, meeting_point, f_pushed_last):
    # 回溯正向路径
    path_f, c = [], meeting_point
    while tree_f[c][0] is not None:
        path_f.append(tree_f[c][1])
        c = tree_f[c][0]
    # 回溯反向路径
    path_b, c = [], meeting_point
    while tree_b[c][0] is not None:
        path_b.append(tree_b[c][1])
        c = tree_b[c][0]

    total_nodes = len(tree_f) + len(tree_b)
    # 如果是反向扩展碰到的正向，路径顺序需要微调
    return len(path_f) + len(path_b), path_f[::-1] + path_b, total_nodes


if __name__ == '__main__':
    board_hard = [
        [1, 1, 1, -2, -2],
        [1, -1, -1, -1, -2],
        [0, 1, 1, -1, -1],
        [-1, -1, -1, -1, -1],
        [1, 1, -1, 1, -1]
    ]
    target_board_ = [
        [-1, -1, -1, -2, -2],
        [-1, -1, 1, 1, -2],
        [-1, -1, -1, 1, 1],
        [1, 1, 1, 1, -1],
        [-1, -1, 1, -1, -1]
    ]

    # 启动内存监控
    tracemalloc.start()

    start_time = time.time()

    count, path, nodes = solve_puzzle(board_hard, target_board_)

    end_time = time.time()

    # 获取内存统计
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("--- 求解结果 ---")
    print(f"移动步数: {count}")
    print(f"移动路径: {path}")
    print(f"探索的唯一节点数: {nodes}")
    print(f"耗时: {end_time - start_time:.4f} 秒")
    print(f"当前内存消耗: {current / 1024 / 1024:.2f} MB")
    print(f"峰值内存消耗: {peak / 1024 / 1024:.2f} MB")

'''
hard 第一步（获取时间 + 节点数）：
探索的唯一节点数: 1685505
耗时: 3.8950 秒
探索的唯一节点数: 1685505
耗时: 2.7581 秒
探索的唯一节点数: 1685505
耗时: 3.1084 秒
探索的唯一节点数: 1685505
耗时: 2.8766 秒
探索的唯一节点数: 1685505
耗时: 2.7970 秒

峰值内存消耗: 242.33 MB
'''
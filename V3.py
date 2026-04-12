import time
import heapq
import tracemalloc
from typing import List, Any


def solve_puzzle_pdb_astar(board: List[List[int]], target_board: List[List[int]]) -> tuple[int, List[int]]:
    rows, cols = len(board), len(board[0])

    # 1. 提取有效格子并建立索引映射 (剔除 -2 障碍物)
    valid_cells = []
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != -2:
                valid_cells.append((i, j))

    cell_to_idx = {cell: idx for idx, cell in enumerate(valid_cells)}
    idx_to_cell = {idx: cell for cell, idx in cell_to_idx.items()}
    num_bits = len(valid_cells)

    # 2. 建立位运算邻接表和边集
    adj = [[] for _ in range(num_bits)]
    edges = []
    for i, j in valid_cells:
        idx = cell_to_idx[(i, j)]
        for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if (ni, nj) in cell_to_idx:
                adj[idx].append(cell_to_idx[(ni, nj)])
                if idx < cell_to_idx[(ni, nj)]:
                    edges.append((1 << idx) | (1 << cell_to_idx[(ni, nj)]))

    # 3. 极速 PDB (模式数据库) 生成器
    def build_pdb(start_masks):
        pdb = bytearray([255] * (1 << num_bits))
        q = [0] * 1000000
        head = 0
        tail = 0
        for mask in start_masks:
            pdb[mask] = 0
            q[tail] = mask
            tail += 1

        while head < tail:
            mask = q[head]
            head += 1
            d = pdb[mask] + 1

            for edge in edges:
                overlap = mask & edge
                if overlap and overlap != edge:
                    new_mask = mask ^ edge
                    if pdb[new_mask] == 255:
                        pdb[new_mask] = d
                        q[tail] = new_mask
                        tail += 1
        return pdb

    # 4. 解析目标状态，生成 PDB
    target_1_mask = 0
    target_minus_1_masks = []
    target_minus_1_positions = []

    for i in range(rows):
        for j in range(cols):
            if target_board[i][j] == 1:
                target_1_mask |= (1 << cell_to_idx[(i, j)])
            elif target_board[i][j] == -1:
                target_minus_1_positions.append(cell_to_idx[(i, j)])

    for skip_idx in range(len(target_minus_1_positions)):
        mask = 0
        for idx, pos in enumerate(target_minus_1_positions):
            if idx != skip_idx:
                mask |= (1 << pos)
        target_minus_1_masks.append(mask)

    print("正在预计算 1 的模式数据库 (PDB)...")
    t0 = time.time()
    pdb_1 = build_pdb([target_1_mask])
    t_pdb1 = time.time() - t0
    print(f"完成! 耗时: {t_pdb1:.2f}s")

    print("正在预计算 -1 的模式数据库 (PDB)...")
    t0 = time.time()
    pdb_minus_1 = build_pdb(target_minus_1_masks)
    t_pdb_minus1 = time.time() - t0
    print(f"完成! 耗时: {t_pdb_minus1:.2f}s")

    # 5. 解析初始状态
    start_1_mask = 0
    start_minus_1_mask = 0
    start_0_idx = -1

    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 1:
                start_1_mask |= (1 << cell_to_idx[(i, j)])
            elif board[i][j] == -1:
                start_minus_1_mask |= (1 << cell_to_idx[(i, j)])
            elif board[i][j] == 0:
                start_0_idx = cell_to_idx[(i, j)]

    init_h = pdb_1[start_1_mask] + pdb_minus_1[start_minus_1_mask]
    print(f"初始状态的完美启发式距离 H = {init_h}")

    start_state = (start_1_mask << 22) | start_minus_1_mask

    pq = [(init_h, 0, start_state, start_0_idx)]
    g_score = {start_state: 0}
    came_from = {start_state: (None, -1)}

    print("开始 A* 搜索...")
    t0 = time.time()
    nodes_expanded = 0  # 节点计数器

    while pq:
        f, g, state, idx_0 = heapq.heappop(pq)

        if g > g_score.get(state, float('inf')):
            continue

        nodes_expanded += 1  # 每次弹出并准备扩展时计数

        m1 = state >> 22
        m_minus_1 = state & 0x3FFFFF

        # 到达目标
        if pdb_1[m1] == 0 and pdb_minus_1[m_minus_1] == 0:
            t_astar = time.time() - t0
            print(f"A* 搜索完成! 耗时: {t_astar:.2f}s")
            print(f"扩展节点数: {nodes_expanded}")

            # 回溯路径
            path = []
            curr = state
            while True:
                prev, move = came_from[curr]
                if prev is None:
                    break
                path.append(move)
                curr = prev

            path = path[::-1]
            original_path = []
            for move_idx in path:
                r, c = idx_to_cell[move_idx]
                original_path.append(r * cols + c)

            # 返回步数和路径，同时额外返回测量信息供主程序使用
            return g, original_path, {
                't_pdb1': t_pdb1,
                't_pdb_minus1': t_pdb_minus1,
                't_astar': t_astar,
                'nodes_expanded': nodes_expanded
            }

        for nxt in adj[idx_0]:
            nxt_bit = 1 << nxt
            idx_0_bit = 1 << idx_0

            if m1 & nxt_bit:
                new_m1 = (m1 ^ nxt_bit) | idx_0_bit
                new_m_minus_1 = m_minus_1
            else:
                new_m1 = m1
                new_m_minus_1 = (m_minus_1 ^ nxt_bit) | idx_0_bit

            new_state = (new_m1 << 22) | new_m_minus_1
            new_g = g + 1

            if new_g < g_score.get(new_state, float('inf')):
                g_score[new_state] = new_g
                came_from[new_state] = (state, nxt)
                h = pdb_1[new_m1] + pdb_minus_1[new_m_minus_1]
                heapq.heappush(pq, (new_g + h, new_g, new_state, nxt))

    return -1, [], {}


if __name__ == '__main__':
    # 启动内存跟踪
    #tracemalloc.start()

    board_hard = [
        [1, 1, 1, -2, -2], [1, -1, -1, -1, -2], [0, 1, 1, -1, -1],
        [-1, -1, -1, -1, -1], [1, 1, -1, 1, -1],
    ]
    board_ultimate_hard = [
        [1, 1, 1, -2, -2],
        [1, 1, -1, -1, -2],
        [1, 1, -1, -1, -1],
        [1, -1, -1, -1, -1],
        [1, -1, -1, -1, 0],
    ]
    target_board = [[-1, -1, -1, -2, -2], [-1, -1, 1, 1, -2],
                    [-1, -1, -1, 1, 1],
                    [1, 1, 1, 1, -1], [-1, -1, 1, -1, -1],
                    ]

    # 记录初始内存快照
    snapshot_before = tracemalloc.take_snapshot()

    steps, path, metrics = solve_puzzle_pdb_astar(board_hard, target_board)

    # 记录结束内存快照并计算峰值
    snapshot_after = tracemalloc.take_snapshot()
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n========== 性能测量报告 ==========")
    print(f"PDB 1 构建时间:       {metrics['t_pdb1']:.2f} s")
    print(f"PDB -1 构建时间:      {metrics['t_pdb_minus1']:.2f} s")
    print(f"A* 搜索时间:          {metrics['t_astar']:.2f} s")
    print(f"总运行时间:           {metrics['t_pdb1'] + metrics['t_pdb_minus1'] + metrics['t_astar']:.2f} s")
    print(f"扩展节点总数:         {metrics['nodes_expanded']}")
    print(f"峰值内存使用:         {peak / 1024 / 1024:.2f} MB")
    print(f"当前内存使用:         {current / 1024 / 1024:.2f} MB")
    print("\n移动步数:", steps)
    print("移动路径 (一维索引):", path)
    print("==================================\n")

'''
hard 第一步（获取时间 + 节点数）：
PDB 1 构建时间:       1.66 s
PDB -1 构建时间:      3.22 s
A* 搜索时间:          2.45 s
总运行时间:           7.32 s
扩展节点总数:         469526

PDB 1 构建时间:       2.29 s
PDB -1 构建时间:      3.45 s
A* 搜索时间:          2.42 s
总运行时间:           8.16 s
扩展节点总数:         469526

PDB 1 构建时间:       1.94 s
PDB -1 构建时间:      3.16 s
A* 搜索时间:          3.44 s
总运行时间:           8.54 s
扩展节点总数:         469526

PDB 1 构建时间:       1.87 s
PDB -1 构建时间:      2.20 s
A* 搜索时间:          2.64 s
总运行时间:           6.71 s
扩展节点总数:         469526

PDB 1 构建时间:       2.01 s
PDB -1 构建时间:      2.25 s
A* 搜索时间:          2.33 s
总运行时间:           6.59 s
扩展节点总数:         469526

峰值内存使用:         119.70 MB
'''
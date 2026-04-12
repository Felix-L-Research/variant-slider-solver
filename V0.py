import heapq
import time
import tracemalloc  # Python 内置的内存跟踪库，专门用于获取真实峰值内存
from typing import List, Any
import copy

# 定义常量
move_grid = 0
fixed_grid = -2
attr_grid = 1
var_grid = -1


def generate_neighbors(rows, cols, puzzle_1d):
    neighbors = {}
    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if puzzle_1d[index] == fixed_grid:
                continue
            neighbor_indices = []
            for ni, nj in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= ni < rows and 0 <= nj < cols:
                    n_index = ni * cols + nj
                    if puzzle_1d[n_index] != fixed_grid:
                        neighbor_indices.append(n_index)
            neighbors[index] = tuple(neighbor_indices)
    return neighbors


class Solution:
    neighbors = None
    target_board = None   # 二维列表
    rows = 0
    cols = 0

    class State:
        def __init__(self, board: List[List[int]], cost: int, parent: 'Solution.State', move: int):
            self.board = board
            self.g = cost
            self.parent = parent
            self.move = move
            self.h = self.heuristic()
            self.f = self.h + self.g

        def __lt__(self, other):
            return self.f < other.f

        def heuristic(self):
            displacement = 0
            for i in range(Solution.rows):
                for j in range(Solution.cols):
                    board_val = self.board[i][j]
                    if board_val != fixed_grid and board_val != 0:
                        if board_val != Solution.target_board[i][j]:
                            displacement += 1
            return displacement

        def successor(self):
            # 找到0的位置
            i0 = j0 = -1
            for i in range(Solution.rows):
                for j in range(Solution.cols):
                    if self.board[i][j] == 0:
                        i0, j0 = i, j
                        break
                if i0 != -1:
                    break

            idx0 = i0 * Solution.cols + j0
            successors = []
            for ng in Solution.neighbors[idx0]:
                ni, nj = divmod(ng, Solution.cols)
                # 深拷贝当前棋盘
                new_board = [row[:] for row in self.board]
                # 交换0和邻居
                new_board[i0][j0], new_board[ni][nj] = new_board[ni][nj], new_board[i0][j0]
                successors.append(Solution.State(new_board, self.g + 1, self, ng))
            return successors


def is_target(board: List[List[int]], target: List[List[int]]) -> bool:
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        for j in range(cols):
            b = board[i][j]
            t = target[i][j]
            if b == 0:
                if t != var_grid:
                    return False
            else:
                if b != t:
                    return False
    return True


def get_path(state: Solution.State) -> List[int]:
    path = []
    while state.parent is not None:
        path.append(state.move)
        state = state.parent
    return path[::-1]


def solve_puzzle(board: List[List[int]], target_board: List[List[int]]) -> tuple[Any, Any, int]:
    rows, cols = len(board), len(board[0])
    Solution.rows = rows
    Solution.cols = cols
    Solution.target_board = target_board

    # 生成邻居信息（基于一维索引，但棋盘已转换为二维）
    board_1d = tuple(val for row in board for val in row)
    Solution.neighbors = generate_neighbors(rows, cols, board_1d)

    init_state = Solution.State(board, 0, None, -1)

    pq = [init_state]
    # 存储已访问状态的可哈希表示（元组的元组）
    explored = {tuple(tuple(row) for row in board)}

    nodes_expanded = 0

    while pq:
        state = heapq.heappop(pq)
        nodes_expanded += 1

        if is_target(state.board, Solution.target_board):
            return state.g, get_path(state), nodes_expanded

        for successor in state.successor():
            succ_key = tuple(tuple(row) for row in successor.board)
            if succ_key not in explored:
                explored.add(succ_key)
                heapq.heappush(pq, successor)

    return -1, [], nodes_expanded


if __name__ == '__main__':
    board_easy = [[1, -1, 1, -2, -2], [-1, 1, -1, -1, -2], [-1, 1, 0, 1, 1], [-1, 1, 1, -1, -1], [-1, -1, 1, -1, -1]]

    board_medium = [  # 34
        [-1, -1, 1, -2, -2],
        [1, -1, -1, 0, -2],
        [1, 1, -1, -1, -1],
        [-1, -1, -1, 1, 1],
        [1, 1, -1, -1, 1],
    ]
    board_hard = [  # 46
        [1, 1, 1, -2, -2],
        [1, -1, -1, -1, -2],
        [0, 1, 1, -1, -1],
        [-1, -1, -1, -1, -1],
        [1, 1, -1, 1, -1],
    ]
    target_board_ = [[-1, -1, -1, -2, -2], [-1, -1, 1, 1, -2], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1],
                     [-1, -1, 1, -1, -1]]

    # 开始追踪内存与时间
    tracemalloc.start()
    start_time = time.time()

    count, path, nodes = solve_puzzle(board_hard, target_board_)

    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("=== 实验结果 ===")
    print(f"移动步数 (最少代价): {count}")
    print(f"CPU 耗时: {end_time - start_time:.4f} 秒")
    print(f"节点扩展数 (Expanded Nodes): {nodes} 个")
    print(f"峰值内存占用: {peak_mem / 1024 / 1024:.2f} MB")



'''
easy 第一步（获取时间 + 节点数）：
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 8.6446 秒
节点扩展数 (Expanded Nodes): 178264 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 7.7364 秒
节点扩展数 (Expanded Nodes): 178264 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 8.1254 秒
节点扩展数 (Expanded Nodes): 178264 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 7.7237 秒
节点扩展数 (Expanded Nodes): 178264 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 8.8729 秒
节点扩展数 (Expanded Nodes): 178264 个

峰值内存占用: 302.20 MB
'''


'''
medium 第一步（获取时间 + 节点数）：
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 67.6426 秒
节点扩展数 (Expanded Nodes): 1368635 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 62.5169 秒
节点扩展数 (Expanded Nodes): 1368635 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 63.8778 秒
节点扩展数 (Expanded Nodes): 1368635 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 62.5228 秒
节点扩展数 (Expanded Nodes): 1368635 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 62.9823 秒
节点扩展数 (Expanded Nodes): 1368635 个

峰值内存占用: 1862.45 MB
'''

'''
hard 第一步（获取时间 + 节点数）：
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 168.4614 秒
节点扩展数 (Expanded Nodes): 3547878 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 162.9685 秒
节点扩展数 (Expanded Nodes): 3547878 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 162.2291 秒
节点扩展数 (Expanded Nodes): 3547878 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 161.5846 秒
节点扩展数 (Expanded Nodes): 3547878 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 162.2511 秒
节点扩展数 (Expanded Nodes): 3547878 个


峰值内存占用: 2929.59 MB
'''
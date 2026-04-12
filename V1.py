import heapq
import time
import tracemalloc  # Python 内置的内存跟踪库，专门用于获取真实峰值内存
from typing import List, Any

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
            neighbor_indices =[]
            for ni, nj in[(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= ni < rows and 0 <= nj < cols:
                    n_index = ni * cols + nj
                    if puzzle_1d[n_index] != fixed_grid:
                        neighbor_indices.append(n_index)
            neighbors[index] = tuple(neighbor_indices)
    return neighbors

class Solution:
    neighbors = None
    target_board_1d = None
    cols = 0

    class State:
        # 【控制变量点 1】：__slots__ 内存限制
        __slots__ =['board', 'g', 'h', 'f', 'parent', 'move']

        def __init__(self, board: tuple, cost: int, parent: 'Solution.State', move: int):
            self.board = board
            self.g = cost
            self.parent = parent
            self.move = move
            self.h = self.heuristic()
            self.f = self.h + self.g

        def __lt__(self, other):
            # 【控制变量点 2】：Tie-breaker 机制
            if self.f == other.f:
                return self.g > other.g
            return self.f < other.f

        def heuristic(self):
            displacement = 0
            for board_val, target_val in zip(self.board, Solution.target_board_1d):
                if board_val != fixed_grid and board_val != 0:
                    if board_val != target_val:
                        displacement += 1
            return displacement

        def successor(self):
            idx = self.board.index(0)
            successors =[]
            board_list = list(self.board)
            for ng in Solution.neighbors[idx]:
                board_list[idx], board_list[ng] = board_list[ng], board_list[idx]
                successors.append(Solution.State(tuple(board_list), self.g + 1, self, ng))
                board_list[idx], board_list[ng] = board_list[ng], board_list[idx]
            return successors

def is_target(board_1d, target_1d):
    for b, t in zip(board_1d, target_1d):
        if b == 0:
            if t != var_grid: return False
        else:
            if b != t: return False
    return True

def get_path(state: Solution.State) -> List[int]:
    path =[]
    while state.parent is not None:
        path.append(state.move)
        state = state.parent
    return path[::-1]

def solve_puzzle(board: List[List[int]], target_board: List[List[int]]) -> tuple[Any, Any, int]:
    rows, cols = len(board), len(board[0])
    board_1d = tuple(element for sublist in board for element in sublist)
    target_1d = tuple(element for sublist in target_board for element in sublist)
    Solution.cols = cols
    Solution.target_board_1d = target_1d
    Solution.neighbors = generate_neighbors(rows, cols, board_1d)
    init_state = Solution.State(board_1d, 0, None, -1)
    pq = [init_state]
    explored = {board_1d}

    nodes_expanded = 0  # 新增：记录弹出的节点总数

    while pq:
        state = heapq.heappop(pq)
        nodes_expanded += 1  # 每次真正处理一个节点时，计数器 +1

        if is_target(state.board, Solution.target_board_1d):
            return state.g, get_path(state), nodes_expanded

        for successor in state.successor():
            if successor.board not in explored:
                explored.add(successor.board)
                heapq.heappush(pq, successor)

    return -1,[], nodes_expanded

if __name__ == '__main__':
    board_easy = [[1, -1, 1, -2, -2],[-1, 1, -1, -1, -2],[-1, 1, 0, 1, 1],[-1, 1, 1, -1, -1],[-1, -1, 1, -1, -1]]
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
    target_board_ = [[-1, -1, -1, -2, -2],[-1, -1, 1, 1, -2],[-1, -1, -1, 1, 1],[1, 1, 1, 1, -1],[-1, -1, 1, -1, -1]]

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
CPU 耗时: 2.5284 秒
节点扩展数 (Expanded Nodes): 153636 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 2.6625 秒
节点扩展数 (Expanded Nodes): 153636 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 2.8372 秒
节点扩展数 (Expanded Nodes): 153636 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 2.7062 秒
节点扩展数 (Expanded Nodes): 153636 个
=== 实验结果 ===
移动步数 (最少代价): 26
CPU 耗时: 2.7111 秒
节点扩展数 (Expanded Nodes): 153636 个

第二步（仅获取峰值内存）:
峰值内存占用: 79.97 MB
'''


'''
medium 第一步（获取时间 + 节点数）：
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 20.0933 秒
节点扩展数 (Expanded Nodes): 984113 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 19.6960 秒
节点扩展数 (Expanded Nodes): 984113 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 19.6212 秒
节点扩展数 (Expanded Nodes): 984113 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 19.8816 秒
节点扩展数 (Expanded Nodes): 984113 个
=== 实验结果 ===
移动步数 (最少代价): 34
CPU 耗时: 19.8082 秒
节点扩展数 (Expanded Nodes): 984113 个

第二步（仅获取峰值内存）:
峰值内存占用: 465.63 MB
'''

'''
hard 第一步（获取时间 + 节点数）：
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 66.9971 秒
节点扩展数 (Expanded Nodes): 3341754 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 64.6021 秒
节点扩展数 (Expanded Nodes): 3341754 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 64.7642 秒
节点扩展数 (Expanded Nodes): 3341754 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 62.9834 秒
节点扩展数 (Expanded Nodes): 3341754 个
=== 实验结果 ===
移动步数 (最少代价): 46
CPU 耗时: 63.5652 秒
节点扩展数 (Expanded Nodes): 3341754 个

第二步（仅获取峰值内存）:
峰值内存占用: 1092.11 MB
'''
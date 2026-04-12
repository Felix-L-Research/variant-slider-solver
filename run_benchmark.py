import sys
import time
import tracemalloc
import importlib
import gc
import argparse
from cases import CASES  # 导入刚才定义的字典


def run_benchmark():
    parser = argparse.ArgumentParser(description="Variant Slider Solver Benchmark")
    parser.add_argument("version", choices=["V0", "V1", "V2", "V3"], help="算法版本")
    parser.add_argument("--mode", choices=["perf", "mem"], required=True, help="perf:测速, mem:测内存")
    parser.add_argument("--case", choices=["easy", "medium", "hard"], default="easy", help="难度等级")

    args = parser.parse_args()

    # 1. 获取数据：这里 CASES 是字典，args.case 是键（'easy'/'medium'/'hard'）
    # 返回的结果 case_data 也是一个字典 {"start": ..., "target": ...}
    case_data = CASES[args.case]
    start_board = case_data["start"]
    target_board = case_data["target"]

    # 2. 动态加载模块
    try:
        module = importlib.import_module(args.version)
    except ImportError:
        print(f"找不到模块 {args.version}.py")
        return

    if args.mode == "perf":
        gc.collect()
        start_time = time.perf_counter()

        # 调用 solve
        count, path, nodes = module.solve_puzzle(start_board, target_board)

        end_time = time.perf_counter()
        print(f"\n[{args.version} | {args.case.upper()}]")
        print(f"Time: {end_time - start_time:.4f}s")
        print(f"Nodes: {nodes}")
        print(f"Steps: {count}")
        print(f"Solution Path: {path}")

    elif args.mode == "mem":
        gc.collect()
        tracemalloc.start()

        module.solve_puzzle(start_board, target_board)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"\n[{args.version} | {args.case.upper()} Memory]")
        print(f"Peak Memory: {peak / (1024 * 1024):.2f} MB") # 建议统一用 1024


if __name__ == "__main__":
    run_benchmark()


# 📦 variant-slider-solver

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Speedup-61x-orange?style=flat-square" alt="Speedup">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=flat-square" alt="Status">
</p>

> **🎓 本科毕业论文配套实现** | 针对高维、多同质目标、通配块约束的工业调度抽象模型。通过位运算状态压缩与启发式演进，在普通微机上实现 **46 步极限难度谜题的秒级求解**。

---

## 🌟 核心特性

本框架记录了从 **面向对象初学版** 到 **硬件级底层优化版** 的完整进化轨迹：

*   **⚡ 极致压榨：** 利用 64-bit Bitboard 与双掩码拼接（44-bit）彻底消除 Python 对象开销与 GC 停顿。
*   **🧠 智能决策：** 引入可容许（Admissible）的**加法模式数据库 (PDB)**，将搜索空间的评估转化为 $O(1)$ 的查表操作。
*   **🛠️ 工程闭环：** 提供从 `V0` 到 `V3` 的迭代源码，直观展现 **内存对齐、零拷贝转移、分支预测友好** 等优化思路。
*   **📊 数据驱动：** 相比基线版本，节点搜索量减少 **87%**，内存占用降低 **96%**，综合耗时缩短 **61 倍**。

---

## 🚀 算法演进路线

| 阶段 | 核心实现 | 优化手段 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **V0 (Baseline)** | `List[List]` | 错位计数法 (Hamming) | 原型验证，逻辑跑通 |
| **V1 (Memory)** | `Tuple` + `__slots__` | 内存对齐 + Tie-breaker | 降低碎片化，优化对象存储 |
| **V2 (Bitwise)** | `64-bit Bitboard` | 双向 BFS + 静态掩码异或 | 状态空间压缩，消除指针开销 |
| **V3 (Ultimate)** | `PDB + A*` | 离线预计算 + 启发式修剪 | 极限搜索，40步以上复杂解 |

---

## 📂 项目结构

```bash
variant-slider-solver/
├── V0.py                # 基线版：二维列表 + 弱启发式
├── V1.py                # 工程优化：一维元组 + 状态打散优化
├── V2.py                # 算力压榨：位运算核心 + 双向搜索
├── V3.py                # 终极版：双掩码 PDB 引导的 A* 算法 (含预计算逻辑)
├── run_benchmark.py     # 自动化评测工具 (性能、内存、路径验证)
├── cases.py             # 存放不同难度的变种滑块棋盘
└── LICENSE              # MIT 开源协议
```

---

## 📊 实验数据对比
> **测试环境：** 普通微机 (Inter i7) | **测试用例：** Hard (46步最优解)

| 版本 | 核心技术 | 扩展节点数 | 峰值内存 | 寻路耗时 | 综合加速比 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **V0** | 二维列表 + Hamming | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (Base) |
| **V1** | 一维元组优化 | 3,341,754 | 1,092 MB | 64.58 s | **2.53×** |
| **V2** | Bitboard + 双向 BFS | 1,685,505 | 242 MB | 3.09 s | **52.91×** |
| **V3** | **PDB + 异或 A\*** | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

> 💡 **注：** V3 的 `2.66s` 为在线搜索时间。系统启动时需一次性进行 `4.8s` 的 PDB 预计算。

---

## 🛠️ 快速上手

本项目内置自动化评测工具 `util.py`，支持多维度性能测试。

### 1. 搜索性能测试
测试 V3 版本在 Hard 难度下的表现：
```bash
python util.py V3 --mode perf --case hard
```

### 2. 内存消耗分析
对比 V0 版本的内存峰值（需在文件头部开启 `tracemalloc`）：
```bash
python util.py V0 --mode mem --case easy
```

### 3. 参数说明
- `--mode`: `perf` (性能耗时) / `mem` (内存追踪)
- `--case`: `easy` (26步) / `medium` (34步) / `hard` (46步)

---

## 🎓 学术说明

本仓库为中南林业科技大学本科毕业论文配套实现。

*   **论文题目：** 《基于位运算状态压缩与模式数据库的变体滑块谜题求解算法研究》
*   **核心贡献：** 证明了针对多同质目标的 PDB 可容许性，并设计了基于 XOR 自反方程的状态转移模型，实现了在 Python 这一高层语言上的硬件级性能压榨。

---

## 📜 许可证与致谢

- **License:** [MIT License](LICENSE)
- **Mentor:** 感谢 **刘蓉老师** 对算法严谨性与论文架构的悉心指导。
- **Community:** 感谢开源社区在启发式搜索领域提供的理论支持。



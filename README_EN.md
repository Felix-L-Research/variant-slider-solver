
# 📦 variant-slider-solver

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Speedup-61x-orange?style=flat-square" alt="Speedup">
  <img src="https://img.shields.io/badge/Thesis-Undergraduate-red?style=flat-square" alt="Thesis">
</p>

<p align="center">
  <b><a href="README.md">中文版</a></b> | <b>English Version</b>
</p>

> **🎓 Thesis Implementation** | *An optimized solver for high-dimensional variant slider puzzles, achieving sub-second solving for 46-step puzzles on a standard laptop (Intel i5-9300H, 32GB RAM) via bitwise state compression and heuristic evolution.*

---

## 🌟 Key Features

*   **⚡ Hardware-Level Optimization:** Utilizing 64-bit Bitboards and dual-masking (44-bit) to eliminate Python object overhead and GC latency.
*   **🧠 Intelligent Heuristics:** Implementation of an **Admissible Additive Pattern Database (PDB)**, reducing state evaluation to $O(1)$ table lookups.
*   **🛠️ Engineering Evolution:** A step-by-step codebase from `V0` to `V3` demonstrating the path from OOP patterns to memory-aligned, hardware-friendly logic.
*   **📊 Performance:** Compared to the baseline, node expansion is reduced by **87%**, memory by **96%**, and execution time by **61x**.

---

## 🚀 Algorithm Evolution

| Phase | Core Implementation | Optimization Strategy | Use Case |
| :--- | :--- | :--- | :--- |
| **V0 (Baseline)** | `List[List]` | Hamming Distance | Prototype & Logic Verification |
| **V1 (Memory)** | `Tuple` + `__slots__` | Alignment & Tie-breaking | Reducing heap fragmentation |
| **V2 (Bitwise)** | `64-bit Bitboard` | Bi-BFS + Static XOR Mask | Eliminating pointer overhead |
| **V3 (Ultimate)** | **PDB + A\*** | Precomputation + Pruning | Extreme cases (46+ steps) |

---

## 📂 Project Structure

```bash
variant-slider-solver/
├── V0.py                # Baseline: 2D List + Weak Heuristic
├── V1.py                # Engineering: 1D Tuple + Memory Tuning
├── V2.py                # Performance: Bitboard + Bidirectional BFS
├── V3.py                # Ultimate: Dual-mask PDB-guided A*
├── run_benchmark.py     # Evaluation Tool (Time, Memory, Path)
├── cases.py             # Predefined test cases (Easy/Medium/Hard)
└── LICENSE              # MIT License
```

---

## 📊 Experimental Results (Hard Case / 46 Steps)

| Version | Core Technology | Nodes Expanded | Peak Memory | Search Time | Speedup |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **V0** | 2D List + Hamming | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (Base) |
| **V1** | 1D Tuple Optimization | 3,341,754 | 1,092 MB | 64.58 s | 2.53× |
| **V2** | Bitboard + Bi-BFS | 1,685,505 | 242 MB | 3.09 s | 52.91× |
| **V3** | **PDB + XOR A\*** | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

---

## 🛠️ Usage

### 1. Command Examples
```bash
# Performance Test (V3 Hard Case)
python run_benchmark.py V3 --mode perf --case hard

# Memory Analysis (V0 Easy Case)
python run_benchmark.py V0 --mode mem --case easy
```

### 2. Argument Details
*   `--mode`: Benchmark mode. Options: `perf` (time & path) or `mem` (peak memory tracking).
*   `--case`: Predefined difficulty level.
    *   `easy`: 26-step solution, ideal for V0/V1 tests.
    *   `medium`: 34-step solution, medium complexity.
    *   `hard`: 46-step solution, showcases the extreme speedup of V2/V3.

---

## 🎓 Academic Statement

This repository is the official implementation of the undergraduate thesis:
*   **Title:** *Research on High-performance Solving Algorithms for Variant Slider Puzzles based on Bitwise State Compression and Pattern Databases*
*   **Institution:** Zhongnan University of Forestry and Technology (ZNUFT)
*   **Core Contribution:** Proven the admissibility of PDBs for multi-homogeneous targets and designed a state transition model based on XOR reflexive equations.

---

## 📜 License & Acknowledgments
*   **License:** [MIT License](LICENSE)
*   **Mentor:** Special thanks to **Mentor Rong Liu** for the guidance on algorithm rigor and thesis structure.

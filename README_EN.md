

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

> **🎓 Undergraduate Thesis Implementation** | An optimized solver for high-dimensional variant slider puzzles with multi-homogeneous targets and wildcard constraints.
> Achieves **near‑instant solving of 46‑step puzzles** on a standard laptop (Intel i5‑9300H, 32GB RAM) through bitwise state compression and heuristic evolution.

---

## 🌟 Key Features

This repository records the complete evolution from a **naïve OOP implementation** to a **hardware‑optimized low‑level version**:

- ⚡ **Hardware‑Level Optimization**: Uses 64‑bit Bitboards with dual‑mask concatenation (44‑bit) to eliminate Python object overhead and GC pauses.
- 🧠 **Intelligent Heuristics**: Implements an **admissible additive Pattern Database (PDB)**, reducing state evaluation to $O(1)$ table lookups.
- 🛠️ **Engineering Evolution**: Iterative code from `V0` to `V3`, demonstrating the transition from OOP patterns to memory‑aligned, hardware‑friendly logic.
- 📊 **Data‑Driven Performance**: Compared to the baseline, nodes expanded are reduced by **87%**, peak memory by **96%**, and total execution time by **61×**.

---

## 🚀 Algorithm Evolution

| Phase | Core Implementation | Optimization Strategy | Use Case |
| :--- | :--- | :--- | :--- |
| **V0 (Baseline)** | `List[List]` | Hamming Distance | Prototype & Logic Verification |
| **V1 (Memory)**  | `Tuple` + `__slots__` | Memory Alignment & Tie‑breaker | Reducing Heap Fragmentation |
| **V2 (Bitwise)** | `64‑bit Bitboard` | Bidirectional BFS + Static XOR Mask | State Compression, Eliminating Pointer Overhead |
| **V3 (Ultimate)**| **PDB + A\*** | Off‑line Precomputation + Heuristic Pruning | Extreme Cases (40+ Steps) |

---

## 📂 Project Structure

```
variant-slider-solver/
├── V0.py                # Baseline: 2D List + Weak Heuristic
├── V1.py                # Engineering: 1D Tuple + Memory Tuning
├── V2.py                # Performance: Bitboard + Bidirectional BFS
├── V3.py                # Ultimate: Dual‑mask PDB‑guided A*
├── run_benchmark.py     # Evaluation Tool (Time, Memory, Path Verification)
├── cases.py             # Predefined Test Cases (Easy / Medium / Hard)
└── LICENSE              # MIT License
```

---

## 📊 Experimental Results (Hard Case / 46 Steps)

| Version | Core Technology | Nodes Expanded | Peak Memory | Search Time | Speedup |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **V0** | 2D List + Hamming | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (Base) |
| **V1** | 1D Tuple + `__slots__` | 3,341,754 | 1,092 MB | 64.58 s | 2.53× |
| **V2** | Bitboard + Bi‑BFS | 1,685,505 | 242 MB | 3.09 s | 52.91× |
| **V3** | **PDB + XOR A\*** | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

---

## 🛠️ Quick Start

Use `run_benchmark.py` to test different versions and difficulty levels.

### 1. Command Examples

```bash
# Performance Test (V3 Hard Case)
python run_benchmark.py V3 --mode perf --case hard

# Memory Analysis (V0 Easy Case)
python run_benchmark.py V0 --mode mem --case easy
```

### 2. Argument Details

| Argument | Description | Options |
| :--- | :--- | :--- |
| `--mode` | Benchmark mode | `perf` (time & path) / `mem` (peak memory tracking) |
| `--case` | Predefined difficulty | `easy` (26‑step solution, suitable for V0/V1) / `medium` (34 steps) / `hard` (46 steps, showcases V2/V3 extreme speedup) |

---

## 🎓 Academic Statement

This repository is the official implementation of the undergraduate thesis at **Central South University of Forestry and Technology**.

- **Title**: *Research on High‑performance Solving Algorithms for Variant Slider Puzzles based on Bitwise State Compression and Pattern Databases*
- **Core Contributions**:
  - Proved the admissibility of PDBs for multi‑homogeneous targets.
  - Designed a state transition model based on XOR reflexive equations.
  - Achieved hardware‑level performance within the Python environment.

---

## 📌 Errata — On Algorithm 4‑1 Pseudocode in the Thesis

**Regarding the pseudocode of Algorithm 4‑1 in the companion thesis:**

Section 2.3 of the thesis mathematically defines the multi‑goal relaxed matching rule for the cursor (`0`) and wildcard blocks (`-1`). The pseudocode in lines 7‑8 of Algorithm 4‑1 is a simplified schematic representation. In actual extreme‑difficulty solving, because the cursor can legally remain on any wildcard position, a single‑mask comparison cannot precisely cover all legitimate goal states.

The actual engineering implementation in this repository (see `V3.py`, lines 61–76) adopts a **PDB multi‑source initialization** strategy: during PDB construction for wildcard blocks, the set of all legal goal masks is treated as the zero‑cost starting states for BFS. Consequently, the termination check becomes a constant‑time table lookup (`PDB[mask] == 0`). This design preserves the admissibility of the heuristic while completely solving the multi‑goal matching problem, and it contributes the critical performance improvement.

We provide this clarification for readers who cross‑reference the thesis with the code.

---

## 📜 License & Acknowledgments

- **License**: [MIT License](LICENSE)
- **Mentor**: Special thanks to **Prof. Rong Liu** for her rigorous guidance on algorithm correctness and thesis structure.


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

> **🎓 Companion Implementation for Undergraduate Thesis** | A heuristic-evolved, bitwise-compressed solver for an industrial scheduling abstraction model featuring high-dimensional spaces, multiple homogeneous targets, and wildcard constraints. Achieves **sub-3-second solutions for 46-step extreme-difficulty puzzles** on a standard laptop (Intel i5 9300H, 32GB RAM).

---

## 🌟 Core Features

This framework documents the complete evolutionary trajectory from an **Object-Oriented beginner version** to a **hardware-level optimized version**:

*   **⚡ Extreme Squeezing:** Utilizes 64-bit Bitboards and dual-mask concatenation (44-bit) to completely eliminate Python object overhead and Garbage Collection (GC) pauses.
*   **🧠 Intelligent Decision-Making:** Introduces an admissible **Additive Pattern Database (PDB)**, transforming search space evaluation into $O(1)$ table lookups.
*   **🛠️ Engineering Loop:** Provides iterative source code from `V0` to `V3`, intuitively demonstrating the optimization path from OOP to hardware-friendly algorithms.
*   **📊 Data-Driven:** Compared to the baseline, node expansions are reduced by **87%**, memory footprint by **96%**, and overall execution time is sped up by **61x**.

---

## 🚀 Algorithm Evolution Route

| Phase | Core Implementation | Optimization Method | Applicable Scenario |
| :--- | :--- | :--- | :--- |
| **V0 (Baseline)** | `List[List]` | Misplaced Tiles (Hamming) | Prototype validation, logic verification |
| **V1 (Memory)** | `Tuple` + `__slots__` | Memory alignment + Tie-breaker | Reduce fragmentation, optimize object storage |
| **V2 (Bitwise)** | `64-bit Bitboard` | Bidirectional BFS + Static mask XOR | State space compression, eliminate pointer overhead |
| **V3 (Ultimate)** | `PDB + A*` | Offline pre-computation + Heuristic pruning | Extreme search, complex solutions > 40 steps |

---

## 📂 Project Structure

```bash
variant-slider-solver/
├── V0.py                # Baseline: 2D List + Weak Heuristic
├── V1.py                # Engineering Opt: 1D Tuple + State flattening
├── V2.py                # Bitwise Opt: Bitboard core + Bidirectional BFS
├── V3.py                # Ultimate: Dual-mask PDB guided A* algorithm
├── run_benchmark.py     # Automated benchmarking tool (Perf, Mem, Path)
├── cases.py             # Preset puzzle boards (Easy/Medium/Hard)
├── REFERENCES.md        # Core references & theoretical origins (with DOIs)
└── LICENSE              # MIT License
```

---

## 📊 Experimental Data Comparison (Hard / 46-step optimal)

| Version | Core Technology | Expanded Nodes | Peak Memory | CPU Time | Speedup |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **V0** | 2D List + Hamming | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (Baseline) |
| **V1** | 1D Tuple + `__slots__` | 3,341,754 | 1,092 MB | 64.58 s | 2.53× |
| **V2** | Bitboard + Bi-BFS | 1,685,505 | 242 MB | 3.09 s | 52.91× |
| **V3** | **PDB + XOR A\*** | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

---

## 🛠️ Quick Start

Use `run_benchmark.py` to easily test the algorithm across different versions and difficulties.

### 1. Command Examples
```bash
# Performance test (e.g., V3 version, Hard difficulty)
python run_benchmark.py V3 --mode perf --case hard

# Memory tracking (e.g., V0 version, Easy difficulty)
python run_benchmark.py V0 --mode mem --case easy
```

### 2. Parameter Details
*   `--mode`: Evaluation mode. Options are `perf` (execution time and path) or `mem` (peak memory tracking).
*   `--case`: Preset use case difficulty.
    *   `easy`: 26-step solution, suitable for validating V0/V1.
    *   `medium`: 34-step solution, medium difficulty.
    *   `hard`: 46-step solution, used to demonstrate the extreme acceleration capabilities of V2/V3.

---

## 🎓 Academic Note

This repository is the companion implementation for an undergraduate thesis at Central South University of Forestry and Technology.
*   **Thesis Title:** *Research on a Solving Algorithm for Variant Sliding-Tile Puzzles Based on Bitwise State Compression and Pattern Databases*
*   **Core Contributions:** Proved the admissibility of PDB for multiple homogeneous targets, designed a state transition model based on XOR reflexive equations, and achieved hardware-level performance squeezing in a Python environment.

---

## 📚 References & Theoretical Origins

To practice the spirit of Open Science and facilitate subsequent developers and researchers in tracing the theoretical foundations of this project, a complete set of digital retrieval links for all references is provided. All references have undergone strict cross-validation and include official DOIs or permanent Google Scholar links.

👉 **[Click to view the full reference list (REFERENCES.md)](./REFERENCES.md)**

---

## 📌 Errata & Addendum

Adhering to a rigorous academic attitude, the author conducted a secondary in-depth verification of the details in the paper after finalization and archiving. The following errata and addendums are provided to ensure citation accuracy for future researchers:

**1. Clarification on Algorithm 4-1 Pseudocode:**
Section 2.3 of the paper strictly defines the multi-target relaxed matching rules for the cursor (0) and wildcards (-1) mathematically. The pseudocode in lines 7–8 of Algorithm 4-1 is a simplified schematic representation. In actual extreme-difficulty solving, since the cursor can legally stay at any wildcard position, a direct single-mask comparison cannot accurately cover all legal target states.
The actual engineering implementation in this repository (see `V3.py` lines 61–76) adopts a **PDB multi-start initialization** strategy: when building the wildcard pattern database, the set of all legal target masks is used as the zero-cost starting point for BFS. This transforms the termination condition into a constant-time table lookup `PDB[mask] == 0`. This design completely solves the multi-target matching problem while maintaining heuristic admissibility, contributing to a crucial performance boost.

**2. Errata and Link Addendum for References:**
| Location      | Original Content                                             | Corrected & Supplemented Content                             | Errata & Addendum Note                                       |
| :------------ | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Reference [3] | Pearl J. Heuristics... [M]. **Reading**: Addison-Wesley, 1984: 50-81. | Pearl J. Heuristics... [M]. **Reading, MA**: Addison-Wesley, 1984: 50-81. | **1. Location Completion:** Added the state abbreviation (MA) to eliminate geographical ambiguity. |
| Reference [8] | Korf R E. Sliding-tile puzzles... 1999, 14(6): **8-14**.     | Korf R E. Sliding-tile puzzles... 1999, 14(6): **8-12**.     | **1. Page Errata:** The actual page range is 8-12. Corrected a typographical error. |

*(Note: The above errata only involve the simplified expression of pseudocode and typographical errors in references, and do not affect the core algorithm logic, experimental data, or the validity of any theoretical derivations in the paper.)*

---

## 📜 License & Acknowledgements
*   **License:** [MIT License](LICENSE)
*   **Mentor:** Special thanks to **Prof. Rong Liu** for her meticulous guidance on algorithm rigor and thesis architecture.

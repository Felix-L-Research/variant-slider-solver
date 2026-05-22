# 📦 variant-slider-solver

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Speedup-61x-orange?style=flat-square" alt="Speedup">
  <img src="https://img.shields.io/badge/Thesis-Undergraduate-red?style=flat-square" alt="Thesis">
</p>

<p align="center">
  <b>中文版</b> | <b><a href="README_EN.md">English Version</a></b>
</p>

> **🎓 Undergraduate Thesis Companion Implementation** | An abstract model for industrial scheduling with high dimensionality, multiple homogeneous objectives, and wildcard block constraints. Through bitwise state compression and heuristic evolution, it achieves **second-level solving of 46-step extreme-difficulty puzzles** on a laptop (Intel i5 9300H, 32GB RAM).

---

## 🌟 Core Features

This framework documents the complete evolutionary trajectory from an **object-oriented beginner version** to a **hardware-level low-level optimized version**:

*   **⚡ Extreme Optimization:** Utilizes 64-bit Bitboard and dual-mask concatenation (44-bit) to completely eliminate Python object overhead and GC pauses.
*   **🧠 Intelligent Decision-Making:** Introduces an admissible **additive pattern database (PDB)**, transforming search space evaluation into an $O(1)$ table lookup operation.
*   **🛠️ Engineering Closure:** Provides iterative source code from `V0` to `V3`, intuitively demonstrating the optimization path from object-oriented to hardware-friendly algorithms.
*   **📊 Data-Driven:** Compared to the baseline version, node search volume is reduced by **87%**, memory usage is reduced by **96%**, and total time consumption is shortened by **61 times**.

---

## 🚀 Algorithm Evolution Roadmap

| Phase | Core Implementation | Optimization Method | Applicable Scenario |
| :--- | :--- | :--- | :--- |
| **V0 (Baseline)** | `List[List]` | Hamming Distance (Misplaced Count) | Prototype verification, logic validation |
| **V1 (Memory)** | `Tuple` + `__slots__` | Memory Alignment + Tie-breaker | Reduce fragmentation, optimize object storage |
| **V2 (Bitwise)** | `64-bit Bitboard` | Bidirectional BFS + Static Mask XOR | State space compression, eliminate pointer overhead |
| **V3 (Ultimate)** | `PDB + A*` | Offline Precomputation + Heuristic Pruning | Extreme search, complex solutions with 40+ steps |

---

## 📂 Project Structure

```bash
variant-slider-solver/
├── V0.py                # Baseline version: 2D list + weak heuristic
├── V1.py                # Engineering optimization: 1D tuple + state scattering optimization
├── V2.py                # Computational power optimization: bitwise core + bidirectional search
├── V3.py                # Ultimate version: dual-mask PDB-guided A* algorithm
├── run_benchmark.py     # Automated evaluation tool (performance, memory, path verification)
├── cases.py             # Contains preset boards (Easy/Medium/Hard)
├── README_EN.md            # Project documentation (Chinese version: includes quick start and errata summary)
├── README_EN.md         # Project documentation (English version)
├── ERRATA_EN.md            # Academic errata and theoretical supplementary notes (Chinese version: rigorous theoretical derivations)
├── ERRATA_EN.md         # Academic errata and theoretical supplementary notes (English version)
├── REFERENCES.md        # Core references and theoretical sources (includes DOIs and direct links)
└── LICENSE              # MIT open-source license
```

---

## 📊 Experimental Data Comparison (Hard Difficulty / 46-step Optimal Solution)

| Version | Core Technology | Expanded Nodes | Peak Memory | Pathfinding Time | Overall Speedup |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **V0** | 2D List + Hamming | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (Baseline) |
| **V1** | 1D Tuple + `__slots__` | 3,341,754 | 1,092 MB | 64.58 s | 2.53× |
| **V2** | Bitboard + Bidirectional BFS | 1,685,505 | 242 MB | 3.09 s | 52.91× |
| **V3** | **PDB + XOR A\*** | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

---

## 🛠️ Quick Start

Using `run_benchmark.py`, you can conveniently test the algorithm across different versions and difficulty levels.

### 1. Example Run Commands
```bash
# Performance test (using V3 version, Hard difficulty as an example)
python run_benchmark.py V3 --mode perf --case hard

# Memory tracking (using V0 version, Easy difficulty as an example)
python run_benchmark.py V0 --mode mem --case easy
```

### 2. Parameter Details
*   `--mode`: Evaluation mode. Options are `perf` (execution time and path) or `mem` (peak memory tracking).
*   `--case`: Preset case difficulty.
    *   `easy`: 26-step solution, suitable for verifying V0/V1.
    *   `medium`: 34-step solution, medium difficulty.
    *   `hard`: 46-step solution, used to demonstrate the extreme acceleration capability of V2/V3.

---

## 🎓 Academic Note

This repository is the companion implementation for an undergraduate thesis at Central South University of Forestry and Technology.
*   **Thesis Title:** "Research on Solving Algorithms for Variant Slider Puzzles Based on Bitwise State Compression and Pattern Databases"
*   **Core Contributions:** Proved the admissibility of PDB for multiple homogeneous objectives and designed a state transition model based on the XOR involution equation, achieving hardware-level performance optimization within the Python environment.

---

## 📚 References and Theoretical Sources (References)

In the spirit of open science, and to facilitate subsequent developers and researchers in tracing the theoretical foundations of this project (the variant slider puzzle solving engine), a complete set of digital retrieval links for the references is provided here. All references have undergone rigorous cross-verification and include official DOIs or permanent Google Scholar retrieval addresses.

👉 **[Click to view the complete reference list (REFERENCES.md)](./REFERENCES.md)**

---

## 📌 Academic Errata and Theoretical Supplement (Errata & Addendum)

Adhering to a rigorous academic attitude, after the finalization of the undergraduate thesis, the author conducted an in-depth review and extreme stress testing of the engineering implementation details and the underlying discrete mathematics theory presented in the text.

To ensure the accuracy of citations for subsequent researchers and to refine the theoretical boundaries of this algorithm in generalized industrial scenarios, this project has compiled a detailed supplementary documentation. It primarily covers deepening in the following three dimensions:

1. **Engineering Implementation Notes**: Supplements the explanation of the $O(1)$ ultra-fast relaxation matching strategy based on `PDB multi-start initialization` in the actual source code (an engineering deepening of the pseudocode in Algorithm 4-1 of the thesis).
2. **Formatting and Reference Errata**: Corrects typographical errors in page numbers and publication locations for some references.
3. **Theoretical Boundary Derivation (Core)**:
   - Supplements the **topological connectivity prerequisite** (connected component detection) required for the validity of the generalized state space formula.
   - Reveals the underlying algebraic principle of **"topological folding of parity isolation"** by the wildcard block relaxation matching mechanism.
   - Rigorously derives the **absolute mathematical boundary** ($N_{\text{valid}} \le 3$) for parity deadlock recovery under extreme obstacle density.

*(Note: The above supplements only involve the expansion of theoretical boundaries and corrections of formatting errors; they do not affect the core algorithm logic of the thesis or the experimental conclusion of a 61-fold performance improvement.)*

👉 **Please refer to the detailed derivation and explanation in: [Academic Errata and Theoretical Supplement Notes (ERRATA_EN.md)](./ERRATA_EN.md)**

---

## 📜 License and Acknowledgements
*   **License:** [MIT License](LICENSE)
*   **Mentor:** Special thanks to **Professor Liu Rong** for her meticulous guidance on the algorithmic rigor and thesis structure.
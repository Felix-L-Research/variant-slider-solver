### 📌 Academic Errata and Addendum

Adhering to a rigorous academic standard, the author conducted an in-depth verification and extreme stress testing of the engineering details and underlying discrete mathematics theory following the finalization and archiving of the paper. The following errata and supplementary explanations are provided to ensure the accuracy of citations for subsequent researchers.

*(Note: The following explanations pertain only to the simplified representation of pseudocode, typographical numbering, and theoretical deepening under extreme boundary conditions. They do not affect the core algorithmic logic, experimental data, or the validity of the final 61× performance improvement of the paper.)*

### I. Engineering Implementation and Typographical Errata

**1. Explanation of Pseudocode in Algorithm 4-1 of the Companion Paper:**
Section 2.3 of the paper has already rigorously defined the multi-objective relaxed matching rules for the cursor (0) and wildcard blocks (-1) from a mathematical perspective. The pseudocode in lines 7–8 of Algorithm 4-1 is a simplified, illustrative representation. In actual extreme-difficulty solving, because the cursor can legally reside at any wildcard position, a direct single-mask comparison cannot precisely cover all legal target states.
The actual engineering implementation in this repository (see lines 61–76 of `V3.py`) adopts a **PDB Multi-Start Initialization** strategy: when constructing the wildcard block pattern database, the set of all legal target masks is used as the zero-cost starting point for BFS. This transforms the termination condition into a constant-time table lookup operation of `PDB[mask] == 0`. This design completely resolves the multi-target matching problem while maintaining heuristic admissibility and contributes to the key performance improvement.

**2. Errata and Link Supplements for References:**
| Location | Original Content | Corrected and Supplemented Content | Errata and Supplementary Explanation |
| :--- | :--- | :--- | :--- |
| Reference [3] | Pearl J. Heuristics... [M]. **Reading**: Addison-Wesley, 1984: 50-81. | Pearl J. Heuristics... [M]. **Reading, MA**: Addison-Wesley, 1984: 50-81. | **Place of Publication Supplement:** Added the state abbreviation (MA) to eliminate geographic ambiguity. |
| Reference [8] | Korf R E. Sliding-tile puzzles... 1999, 14(6): **8-14**. | Korf R E. Sliding-tile puzzles... 1999, 14(6): **8-12**. | **Page Number Erratum:** The actual start and end pages are 8-12; this was a typographical error. |

---

### II. Theoretical Boundary and Mathematical Rigor Addendum

**1. The "Topological Connectivity" Prerequisite for the Generalized State Space Formula**
In Section 2.1.1 of the paper, the total theoretical number of states for the effective grid $N_{valid} = 22$ is calculated as 6,466,460 using the multiset permutation formula. The validity of this combinatorial formula relies on an implicit graph theory prerequisite: **the effective grid after removing obstacles must constitute a single connected component.**
*   **For the Test Cases in This Paper:** Topological detection confirms that the coordinates of the three fixed obstacles (`-2`) defined in this paper do not form a closed enclosure, and the effective grid graph indeed constitutes a single connected component. Therefore, the state space calculation and the conclusion of 100% reachability in the paper are entirely correct.
*   **For Generalized Industrial Scenarios:** If the density of obstacles is extremely high, completely surrounding some grids to form "isolated islands," the surrounded grids will become deadlock states. Consequently, when generalizing this pathfinding engine to universal scenarios, the system initialization phase must introduce **Component Detection**. State space estimation and pathfinding should only be performed for the connected component containing the cursor.

**2. The Underlying Topological and Algebraic Mechanisms of "Parity Constraint Failure"**
Page 6 of the paper states: "The 'internal permutation' characteristic of homogeneous blocks effectively collapses parity isolation." In the theoretical review after finalization, the author further clarified the **dual underlying mathematical mechanisms** that break the classical parity deadlock of sliding puzzles:
*   **Invisible Swapping of Homogeneous Blocks:** Based on the pigeonhole principle, the board inevitably contains a large number of homogeneous blocks (e.g., 9 `1`s and 12 `-1`s). A transposition of homogeneous blocks at the underlying level changes the parity of the microscopic permutation, but the macroscopic physical state remains unchanged. In the mapping to the quotient space, this causes a topological folding of the parity subspaces.
*   **Parity Toggle Switch of Wildcard Blocks (Core Mechanism):** According to the matching logic in Section 2.3 of the paper, the cursor (`0`) can legally reside at any target position of a wildcard block (`-1`). If a parity deadlock is encountered, the cursor only needs to move one additional step to an adjacent wildcard block. This instantly reverses the global parity at the mathematical foundation while maintaining the legality of the macroscopic match. The relaxed matching of wildcard blocks fundamentally tears apart the parity barrier of classical graph search.

**3. Absolute Mathematical Boundary Derivation Under Extreme Obstacle Density**
Given that homogeneous blocks and wildcard blocks can break parity, under what extreme conditions would the parity isolation of this variant sliding puzzle be restored (i.e., an absolute deadlock occurs)?
Let $N_{valid}$ be the number of connected effective grids in the component containing the cursor after removing obstacles. This region contains 1 cursor (`0`), $N_1$ attribute blocks (`1`), and $N_{-1}$ wildcard blocks (`-1`). The spatial equation is: $N_1 + N_{-1} = N_{valid} - 1$.
The **sole mathematical condition** for the restoration of parity isolation is: the quantity of all movable homogeneous blocks is strictly $\le 1$ (i.e., losing the ability for invisible swapping, and the cursor lacks extra wildcard blocks to serve as a parity toggle switch).
That is: $N_1 \le 1$ and $N_{-1} \le 1$. Adding these two inequalities and substituting the spatial equation yields: **$N_{valid} \le 3$**.
*   **Absolute Robustness:** As long as the number of connected effective grids $N_{valid} \ge 4$ (e.g., any $2 \times 2$ connected region), there must exist at least one type of homogeneous block with a quantity $\ge 2$. Parity isolation is absolutely broken, and 100% of macroscopic states are reachable.
*   **Theoretical Singularity:** Parity will only lock when a massive number of obstacles force the cursor into an extreme dead-end where $N_{valid} \le 3$ (e.g., a $1 \times 3$ single chain, losing topological cycles and algebraic surrogates). However, in this case, the state space is extremely small (on the order of $O(1)$), and the algorithm can complete the determination in microseconds, never causing a curse of dimensionality.
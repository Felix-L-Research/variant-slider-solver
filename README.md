# 📦 variant-slider-solver
> 🎓 本科毕业设计配套实现 | 🐍 Pure Python | ⚡ 位运算状态压缩 | 🧠 模式数据库(PDB) | 📊 61× 综合加速

针对高维、多同质目标、通配块约束的工业调度抽象模型，本项目提供了一套从基线到终极优化的递进式求解框架。通过形式化建模、启发式演进与底层硬件压榨，在普通微机上实现 46 步极限难度谜题的秒级求解。

## 🚀 核心特性
| 维度 | 实现方案 | 工程价值 |
|:---|:---|:---|
| **算法演进** | `V0 → V1 → V2 → V3` 四版本递进对照 | 完整记录从 OOP 陷阱 → 内存优化 → 双向盲搜 → PDB 启发式的优化路径 |
| **状态压缩** | 64-bit Bitboard / 双掩码拼接 (44-bit) | 彻底消除高级语言对象开销与 GC 停顿 |
| **零拷贝转移** | 位异或 `(⊕)` 自反方程 | 单节点扩展锁定为 `O(1)` 常数时间 |
| **启发式设计** | 加法模式数据库 (Additive PDB) | 可容许性数学证明 + `O(1)` 查表评估 |
| **实验复现** | Hard 用例 (46步) 节点↓87% / 内存↓96% / 耗时↓61倍 | 数据真实可验，严格区分离线构建与在线搜索 |

## 📂 项目结构
```text
variant-slider-solver/
├── V0.py              # 基线版：二维列表 + 错位计数法弱启发式
├── V1.py              # 工程优化：一维元组 + __slots__ + Tie-breaker
├── V2.py              # 算力压榨：64位Bitboard + 双向BFS + 静态掩码异或
├── V3.py              # 终极版：双掩码PDB + 异或转移 A* (含离线预计算)
└── README.md          # 项目说明与复现指南
```

## ⚙️ 快速运行
> 💡 本仓库仅依赖 Python 标准库 (`heapq`, `time`, `tracemalloc`)，无需 `pip install`。

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/variant-slider-solver.git
cd variant-slider-solver

# 2. 运行终极版 (V3: PDB A*)
python V3.py
# 输出包含：PDB构建耗时、A*搜索耗时、扩展节点数、最优步数与路径

# 3. 运行基线对照 (V0/V1/V2)
python V0.py
python V1.py
python V2.py
```

> 📌 **内存测量说明**：默认关闭 `tracemalloc` 以保证 CPU 耗时纯净。如需采集峰值内存，请在对应文件顶部取消注释 `tracemalloc.start()` 相关代码段。

## 📊 实验数据 (Hard 难度 / 46步最优解)
| 版本 | 核心技术 | 扩展节点数 | 峰值内存 | 寻路耗时 | 综合加速比 |
|:---|:---|:---|:---|:---|:---|
| **V0** | 二维列表 + 弱启发式 | 3,547,878 | 2,929 MB | 163.50 s | 1.0× (基线) |
| **V1** | 一维元组 + `__slots__` | 3,341,754 | 1,092 MB | 64.58 s | 2.53× |
| **V2** | 64-bit Bitboard + 双向BFS | 1,685,505 | 242 MB | 3.09 s | 52.91× |
| **V3** | 双掩码 PDB + 异或 A* | **469,526** | **120 MB** | **2.66 s** | **61.47×** |

> ⏱️ 注：V3 `2.66s` 仅为在线 A* 搜索时间。PDB 离线预计算约需 `4.8s`（仅需系统启动时执行一次）。

## 🎓 学术说明
本仓库为中南林业科技大学本科毕业论文《**基于位运算状态压缩与模式数据库的变体滑块谜题求解算法研究**》的配套开源实现。
- 完整理论推导、可容许性证明与工程演进分析详见论文正文。
- 代码严格遵循“单一职责”与“可复现”原则，保留各版本核心逻辑供交叉验证。
- 实验数据采用分步独立测量法（Decoupled Measurement）规避性能分析工具干扰。

📄 [下载完整论文 PDF]（[可替换为你的学校仓库链接或附件路径](https://wps3.cldisk.com/weboffice/office/w/4995b0c590225eba0dead3f326a9cb6e?_w_appid=DOEJSZFNQSTHSITO&_w_third_appid=DOEJSZFNQSTHSITO&_w_third_file_id=4995b0c590225eba0dead3f326a9cb6e&_w_third_param_obj=NEWAESCODE_3ff24df414e9c52938e179316681c3441d9b1f8ad8760483cc89f592b77ecb0e8e7ada83ff5c22037b9690483ca804b9fdc303d7471ec65278dfac092b6cbb0d23fe885f4556e8b53b29e434c9213dc12f0ae76c2ee3b72054f839a3797887ed1865aa74782c9a5c401be06d7261855fdf0328dce4b8dea1358f049e8272c41ab48a5b79c6f2e158c627f1ffb5dd9c22a8a68793419ab2605f5a2132b5e4a1bd842060ded5ea8bd833783cef2aadd90da8a477f0dd38f383f0e78b6ad17f89deea6d7584a6ffd445a9c37b44a095877373727bb1039219a72f281cbd3d0d29f06dbb4a67f91bde52e5a18693c1fb31bae98f5e85426062137af854baea49b595c885dacf29e97cdacca137a3347ecdda22ff9a0912d36190c3fe228e64a3f8841d9dd5a9cfeeea00ab1b895bc8bd56e2650303362df0b4ec91065947b5b575c7c75f02e28ffebfa4eac696309f0699bceca52fae351cb6e7c80199b95585540ba528afe058f0b5e2b372f3fe581e116a334999ac9ddfbbcbc9fcf0d147f58b80ef9b12df32315f1f471aed6ef4cdb1c0ec67241f07f86ea3766072ff1c025536&preview_mode=ordinary&route_key=14&__doc_route_key=14)）

## 📜 许可证
本项目采用 [MIT License](LICENSE) 开源，仅供学术研究、教学演示与工程参考。商业使用请联系作者。

## 🤝 致谢
感谢导师刘蓉老师在算法严谨性与工程规范上的指导。感谢开源社区在启发式搜索与位运算优化领域的深厚积累。


# 🚀 **AntibioticEnv System**

[![License](https://img.shields.io/badge/License-Academic%20Use-blue?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-green?style=flat-square)](#)
[![Language](https://img.shields.io/badge/Language-Python%203.10+-orange?style=flat-square)](#)
[![Version](https://img.shields.io/badge/Version-v1.1-yellow?style=flat-square)](#)
[![Author](https://img.shields.io/badge/Author-Lingzhi%20Huang-lightgrey?style=flat-square)](#)

---

## 🧬 **Overview**

**AntibioticEnv System**（环境抗生素污染分析系统）  
是一款专为科研人员设计的 **抗生素时空分布与生态风险评估平台**，  
集成数据分析、可视化与不确定性模拟于一体。

该系统支持：
- 📈 **抗生素时空分布特征分析**  
- ☣️ **生态风险评估（RQ、PI、RRQ）**  
- 🎲 **不确定性分析（Monte Carlo Simulation）**  
- 🌏 **双语界面（中 / 英）**  
- 💾 **自动报告导出（Excel + Markdown）**

---

## 🧩 **Key Features**

| 模块 | 功能 |
|------|------|
| 🎨 GUI 界面 | 可视化操作与交互数据导入 |
| 📊 图表分析 | 自动绘制风险矩阵与分布图 |
| 🧮 风险计算 | 内置 RQ、PI、RRQ 模块 |
| 🎲 Monte Carlo | 支持随机抽样与不确定性模拟 |
| 🌐 双语支持 | 中文 / English 切换 |
| 💾 报告导出 | 生成 `.xlsx` 与 `.md` 文件 |

---

## 💻 **Installation**

<div align="center">

### 🪟 **Windows (v1.1)**
[![Download for Windows](https://img.shields.io/badge/⬇️%20Download-Windows%20Installer-blue?style=for-the-badge&logo=windows)](https://github.com/FrazierHuang/AntibioticEnvSystem/releases/download/v1.1-windows/AntibioticEnvSystem.exe)

### 🍎 **macOS (v1.0)**
[![Download for macOS](https://img.shields.io/badge/⬇️%20Download-macOS%20Installer-silver?style=for-the-badge&logo=apple)](https://github.com/FrazierHuang/AntibioticEnvSystem/releases/download/v1.0-macos/AntibioticEnvSystem.dmg)

</div>

---

## 🧭 **Quick Start**

1️⃣ 打开软件，点击 **“导入数据”** 选择 CSV / Excel 文件。  
2️⃣ 选择所需的分析模块（RQ / PI / RRQ）。  
3️⃣ 点击 **“生成分析结果”**。  
4️⃣ 输出文件自动保存在 `outputs/` 目录，包括：  
   - `outputs.xlsx` → 结果数据  
   - `outputs_report.md` → Markdown 报告  
   - `.png` → 各类图表  

---

## 📘 **Citation**

> Huang, L.Z. (2025). *AntibioticEnv System: A platform for spatial-temporal and ecological risk assessment of antibiotics in aquatic environments.* Version 1.1.

📄 **DOI (pending)**: `10.xxxx/AntibioticEnvSystem.v1.1`  
📚 如在科研论文中使用，请注明版本号与作者。

---

## 🧑‍💻 **Author**

| Name | Lingzhi Huang (黄凌志) |
|------|------------------------|
| Field | Environmental Science & Engineering |
| Contact | [GitHub Profile →](https://github.com/FrazierHuang) |

---

## 📂 **Project Structure**

```bash
AntibioticEnvSystem/
├── antibiotic_env/          # Core computation modules
├── main_gui.py              # GUI main interface
├── run_all.py               # Batch processing entry
├── lang/                    # Language files
├── outputs/                 # Generated outputs
└── installer/               # Build scripts (.dmg / .exe)
```

---

## ⚖️ **License**

> 本软件仅限科研与教学用途。  
> 禁止商业传播或二次销售。  
>
> © 2025 Lingzhi Huang — All Rights Reserved.

---

## ⭐ **Support**

如果本项目对你的科研工作有帮助，请考虑：
- 点亮 ⭐ **Star** 支持项目  
- 提交 **Issue / PR** 改进功能  
- 分享给你的科研同伴 🌿  

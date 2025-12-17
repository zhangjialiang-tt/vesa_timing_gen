# 项目目录结构说明

## 概览

本项目采用清晰的目录结构，将源代码、测试、文档和示例分离，便于维护和使用。

## 目录结构

```
vesa_timing_gen/
├── src/                              # 源代码目录
│   ├── vesa_timing_calculator.py    # 主应用程序
│   │   ├── TimingParameters         # 时序参数数据模型
│   │   ├── VesaCalculator          # CVT 计算器核心类
│   │   └── MainWindow              # PyQt5 GUI 主窗口
│   └── vesa_timing_rtl_template.py  # RTL 代码生成模板
│       ├── generate_verilog_rtl()  # 生成 Verilog RTL 模块
│       └── generate_testbench()    # 生成测试平台
│
├── tests/                            # 测试文件目录
│   ├── test_ui_basic.py             # UI 基础功能测试
│   ├── test_event_handling.py       # 事件处理测试
│   ├── test_error_display.py        # 错误显示测试
│   ├── test_reverse_calculation.py  # 反向计算功能测试
│   ├── test_rtl_generation.py       # RTL 代码生成测试
│   ├── test_requirements_verification.py  # 需求验证测试
│   ├── test_new_feature.py          # 新功能测试
│   └── test_calculator_only.py      # 计算器独立测试
│
├── examples/                         # 示例脚本目录
│   └── demo_rtl_generation.py       # RTL 批量生成演示
│       └── 演示如何批量生成多个分辨率的 RTL 代码
│
├── docs/                             # 文档目录
│   ├── QUICK_START.md               # 快速开始指南
│   ├── FEATURE_SUMMARY.md           # 功能总结文档
│   ├── README_PIXEL_CLOCK_MODE.md   # 像素时钟模式详细说明
│   ├── README_RTL_GENERATION.md     # RTL 生成功能详细说明
│   ├── IFLOW.md                     # 工作流程说明
│   └── PROJECT_STRUCTURE.md         # 项目结构说明（本文件）
│
├── output/                           # RTL 代码输出目录
│   ├── vesa_timing_*.v              # 生成的 RTL 模块文件
│   └── tb_vesa_timing_*.v           # 生成的测试平台文件
│
├── .kiro/                            # Kiro IDE 配置目录
│   └── specs/                        # 规格文档
│       └── vesa-timing-calculator/
│           ├── requirements.md       # 需求文档（中文）
│           ├── design.md            # 设计文档（中文）
│           └── tasks.md             # 任务列表（中文）
│
├── .git/                             # Git 版本控制目录
├── .vscode/                          # VS Code 配置目录
├── __pycache__/                      # Python 缓存目录
│
├── README.md                         # 项目主说明文档
└── .gitignore                        # Git 忽略配置文件
```

## 目录说明

### 📁 src/ - 源代码目录

包含所有核心源代码文件。

**文件说明**:
- `vesa_timing_calculator.py`: 主应用程序，包含 GUI 和计算逻辑
  - 约 800 行代码
  - 实现双向时序计算
  - 支持 CVT 和 CVT-RB 模式
  - 提供完整的 PyQt5 GUI

- `vesa_timing_rtl_template.py`: RTL 代码生成模板
  - 约 300 行代码
  - 生成 Verilog RTL 模块
  - 生成测试平台代码
  - 自动计算位宽和参数

### 📁 tests/ - 测试目录

包含所有测试脚本，用于验证功能正确性。

**测试分类**:

1. **UI 测试**
   - `test_ui_basic.py`: 测试 UI 基本功能
   - `test_event_handling.py`: 测试事件处理
   - `test_error_display.py`: 测试错误显示

2. **功能测试**
   - `test_reverse_calculation.py`: 测试反向计算
   - `test_rtl_generation.py`: 测试 RTL 生成
   - `test_calculator_only.py`: 测试计算器核心

3. **验证测试**
   - `test_requirements_verification.py`: 验证需求实现
   - `test_new_feature.py`: 测试新增功能

**运行测试**:
```bash
# 运行单个测试
python tests/test_reverse_calculation.py

# 运行所有测试
python -m pytest tests/
```

### 📁 examples/ - 示例目录

包含使用示例和演示脚本。

**示例说明**:
- `demo_rtl_generation.py`: 批量生成 RTL 代码演示
  - 生成 6 个常见分辨率配置
  - 展示完整的使用流程
  - 输出详细的生成信息

**运行示例**:
```bash
python examples/demo_rtl_generation.py
```

### 📁 docs/ - 文档目录

包含所有项目文档和使用说明。

**文档分类**:

1. **入门文档**
   - `QUICK_START.md`: 5 分钟快速上手指南
   - `PROJECT_STRUCTURE.md`: 项目结构说明（本文件）

2. **功能文档**
   - `FEATURE_SUMMARY.md`: 完整功能总结
   - `README_PIXEL_CLOCK_MODE.md`: 像素时钟模式详解
   - `README_RTL_GENERATION.md`: RTL 生成功能详解

3. **开发文档**
   - `IFLOW.md`: 工作流程和开发指南

### 📁 output/ - 输出目录

存放生成的 RTL 代码文件。

**文件命名规则**:
- RTL 模块: `vesa_timing_<分辨率>_<刷新率>hz[_rb].v`
- 测试平台: `tb_vesa_timing_<分辨率>_<刷新率>hz[_rb].v`

**示例**:
- `vesa_timing_1920x1080_60hz.v`
- `tb_vesa_timing_1920x1080_60hz.v`
- `vesa_timing_1920x1080_60hz_rb.v` (Reduced Blanking)

### 📁 .kiro/ - Kiro IDE 配置

包含 Kiro IDE 的项目配置和规格文档。

**规格文档**:
- `requirements.md`: 详细的需求文档（中文）
- `design.md`: 完整的设计文档（中文）
- `tasks.md`: 实施任务列表（中文）

## 文件依赖关系

```
主应用程序启动流程:
src/vesa_timing_calculator.py
    ├── 导入 TimingParameters (数据模型)
    ├── 导入 VesaCalculator (计算引擎)
    └── 导入 MainWindow (GUI)
        └── 调用 vesa_timing_rtl_template.py (RTL 生成)

测试文件依赖:
tests/*.py
    └── sys.path.insert(0, '../src')
        └── 导入 src/ 中的模块

示例文件依赖:
examples/*.py
    └── sys.path.insert(0, '../src')
        └── 导入 src/ 中的模块
```

## 导入路径说明

由于源代码位于 `src/` 目录，测试和示例文件需要添加路径：

```python
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 现在可以导入模块
from vesa_timing_calculator import VesaCalculator
```

## 使用指南

### 启动应用程序

```bash
# 从项目根目录
python src/vesa_timing_calculator.py

# 或从 src 目录
cd src
python vesa_timing_calculator.py
```

### 运行测试

```bash
# 从项目根目录运行单个测试
python tests/test_reverse_calculation.py

# 运行所有测试（需要 pytest）
python -m pytest tests/
```

### 运行示例

```bash
# 从项目根目录
python examples/demo_rtl_generation.py
```

### 生成 RTL 代码

1. 启动应用程序
2. 输入参数或选择预设
3. 点击"生成 RTL 代码"按钮
4. 查看 `output/` 目录

## 开发建议

### 添加新功能

1. 在 `src/` 目录添加源代码
2. 在 `tests/` 目录添加测试
3. 在 `docs/` 目录更新文档
4. 在 `examples/` 目录添加示例（可选）

### 代码组织原则

- **单一职责**: 每个文件专注于一个功能
- **清晰分离**: 源码、测试、文档分离
- **易于导航**: 目录结构清晰，命名规范
- **便于维护**: 相关文件集中管理

### 命名规范

- **源文件**: 小写字母 + 下划线 (`vesa_timing_calculator.py`)
- **测试文件**: `test_` 前缀 (`test_reverse_calculation.py`)
- **示例文件**: `demo_` 前缀 (`demo_rtl_generation.py`)
- **文档文件**: 大写字母 + 下划线 (`QUICK_START.md`)

## 维护建议

### 定期清理

```bash
# 清理 Python 缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 清理输出文件（可选）
rm -rf output/*.v
```

### 版本控制

`.gitignore` 已配置忽略：
- `__pycache__/` - Python 缓存
- `*.pyc` - 编译的 Python 文件
- `.vscode/` - VS Code 配置
- `output/*.v` - 生成的 RTL 文件（可选）

## 常见问题

**Q: 为什么要分离 src、tests、docs 目录？**
A: 这是标准的 Python 项目结构，便于：
- 代码组织和维护
- 测试和部署
- 文档管理
- 团队协作

**Q: 如何在其他项目中使用这些模块？**
A: 可以将 `src/` 目录添加到 Python 路径，或者安装为包：
```bash
pip install -e .  # 开发模式安装
```

**Q: 输出目录可以修改吗？**
A: 可以，在代码中修改 `output_dir` 变量即可。

**Q: 如何添加新的测试？**
A: 在 `tests/` 目录创建新文件，按照现有测试的格式编写。

## 总结

本项目采用清晰的目录结构，将不同类型的文件分类管理：

- ✅ **src/**: 核心源代码
- ✅ **tests/**: 测试脚本
- ✅ **examples/**: 使用示例
- ✅ **docs/**: 项目文档
- ✅ **output/**: 生成文件

这种结构使项目易于理解、维护和扩展。

---

**最后更新**: 2025-12-17

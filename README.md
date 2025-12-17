# VESA 视频时序计算器

一个功能完整的桌面应用程序，用于计算和生成符合 VESA CVT 标准的视频时序参数和 RTL 代码。

## 主要特性

- ✅ **双向时序计算**: 支持从刷新率计算像素时钟，或从像素时钟计算刷新率
- ✅ **CVT 标准支持**: 完整实现 VESA CVT 1.2 标准和 CVT-RB 模式
- ✅ **RTL 代码生成**: 自动生成 Verilog RTL 模块和测试平台
- ✅ **图形用户界面**: 直观易用的 PyQt5 界面
- ✅ **预设功能**: 内置常见分辨率快速选择
- ✅ **实时计算**: 参数修改后自动更新结果

## 快速开始

### 安装依赖

```bash
pip install PyQt5
```

### 启动应用程序

```bash
python src/vesa_timing_calculator.py
```

### 基本使用

1. 选择计算模式（正向/反向）
2. 输入分辨率和刷新率（或像素时钟）
3. 查看计算结果
4. 可选：生成 RTL 代码

详细使用说明请参考 [快速开始指南](docs/QUICK_START.md)

## 项目结构

```
vesa_timing_gen/
├── src/                              # 源代码
│   ├── vesa_timing_calculator.py    # 主应用程序
│   └── vesa_timing_rtl_template.py  # RTL 代码生成模板
├── tests/                            # 测试文件
│   ├── test_ui_basic.py             # UI 基础测试
│   ├── test_event_handling.py       # 事件处理测试
│   ├── test_error_display.py        # 错误显示测试
│   ├── test_reverse_calculation.py  # 反向计算测试
│   ├── test_rtl_generation.py       # RTL 生成测试
│   └── test_requirements_verification.py  # 需求验证测试
├── examples/                         # 示例脚本
│   └── demo_rtl_generation.py       # RTL 批量生成演示
├── docs/                             # 文档
│   ├── QUICK_START.md               # 快速开始指南
│   ├── FEATURE_SUMMARY.md           # 功能总结
│   ├── README_PIXEL_CLOCK_MODE.md   # 像素时钟模式说明
│   ├── README_RTL_GENERATION.md     # RTL 生成功能说明
│   └── IFLOW.md                     # 工作流程说明
├── output/                           # RTL 代码输出目录
├── .kiro/                            # Kiro IDE 配置
│   └── specs/                        # 规格文档
│       └── vesa-timing-calculator/
│           ├── requirements.md       # 需求文档
│           ├── design.md            # 设计文档
│           └── tasks.md             # 任务列表
├── README.md                         # 本文件
└── .gitignore                        # Git 忽略配置
```

## 功能概览

### 1. 时序参数计算

支持两种计算模式：

**正向计算**（从刷新率计算像素时钟）
- 输入：分辨率 + 刷新率
- 输出：像素时钟 + 完整时序参数

**反向计算**（从像素时钟计算刷新率）
- 输入：分辨率 + 像素时钟
- 输出：刷新率 + 完整时序参数

### 2. CVT 标准模式

- **标准 CVT**: 完整的 VESA CVT 1.2 标准实现
- **CVT-RB**: Reduced Blanking 模式，减少带宽需求

### 3. RTL 代码生成

自动生成：
- Verilog RTL 时序生成器模块
- 完整的测试平台（testbench）
- 详细的参数注释和文档

### 4. 支持的分辨率

- **HD**: 1280x720
- **Full HD**: 1920x1080, 1920x1200
- **QHD**: 2560x1440
- **4K UHD**: 3840x2160
- **8K UHD**: 7680x4320
- 刷新率范围: 24-240 Hz

## 使用示例

### 示例 1: 计算 1080p60 时序

```bash
python src/vesa_timing_calculator.py
# 在 GUI 中选择预设 "1920x1080@60Hz"
# 查看计算结果：像素时钟 ≈ 147.84 MHz
```

### 示例 2: 批量生成 RTL 代码

```bash
python examples/demo_rtl_generation.py
# 自动生成 6 个常见分辨率的 RTL 代码
# 输出到 ./output 目录
```

### 示例 3: 运行测试

```bash
# 测试反向计算功能
python tests/test_reverse_calculation.py

# 测试 RTL 生成功能
python tests/test_rtl_generation.py
```

## 生成的 RTL 代码

生成的 Verilog 模块包含：

```verilog
module vesa_timing_gen (
    input  wire        clk,           // 像素时钟
    input  wire        rst_n,         // 异步复位
    output reg         hsync,         // 水平同步
    output reg         vsync,         // 垂直同步
    output reg         de,            // 数据使能
    output reg         frame_valid,   // 帧有效
    output reg  [N:0]  h_count,       // 水平计数器
    output reg  [M:0]  v_count        // 垂直计数器
);
```

## 文档

- [快速开始指南](docs/QUICK_START.md) - 5 分钟上手教程
- [功能总结](docs/FEATURE_SUMMARY.md) - 完整功能说明
- [像素时钟模式](docs/README_PIXEL_CLOCK_MODE.md) - 双向计算详解
- [RTL 生成功能](docs/README_RTL_GENERATION.md) - RTL 代码生成指南
- [工作流程](docs/IFLOW.md) - 开发流程说明

## 技术栈

- **Python 3.7+**: 主要编程语言
- **PyQt5**: GUI 框架
- **Verilog**: RTL 代码生成目标语言

## 应用场景

1. **显示器开发**: 设计和验证显示时序
2. **FPGA 项目**: 快速生成时序模块
3. **硬件调试**: 分析现有时序参数
4. **教学演示**: 学习视频时序原理

## 测试

运行所有测试：

```bash
# UI 测试
python tests/test_ui_basic.py
python tests/test_event_handling.py
python tests/test_error_display.py

# 功能测试
python tests/test_reverse_calculation.py
python tests/test_rtl_generation.py
python tests/test_requirements_verification.py
```

## 贡献

欢迎提交问题和改进建议！

## 许可

本项目遵循 VESA CVT 1.2 标准规范。
生成的 RTL 代码可自由用于商业和非商业项目。

## 联系

- VESA 官方网站: https://vesa.org
- CVT 标准文档: VESA Coordinated Video Timings (CVT) Standard Version 1.2

---

**版本**: 1.0  
**最后更新**: 2025-12-17

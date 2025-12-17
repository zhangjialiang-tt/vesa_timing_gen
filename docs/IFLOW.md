# VESA 视频时序计算器 - 项目上下文

## 项目概述

这是一个基于 PyQt5 的桌面应用程序，用于根据 VESA CVT (Coordinated Video Timing) 标准计算视频时序参数。面向显示器工程师、硬件开发人员和技术人员，提供精确的视频时序计算功能。

**主要功能：**
- 支持标准 CVT 和 CVT-RB (Reduced Blanking) 两种计算模式
- 实时参数验证和自动计算
- 常见分辨率预设快速选择
- 计算结果复制功能
- 双面板专业界面布局

## 项目结构

```
vesa_timing_gen/
├── vesa_timing_calculator.py    # 主应用程序文件（核心逻辑 + UI）
├── test_*.py                    # 测试文件（UI、计算、错误处理等）
├── README.md                    # 项目简介
├── README_PIXEL_CLOCK_MODE.md   # 像素时钟反向计算模式说明
└── .kiro/specs/vesa-timing-calculator/  # 设计文档和需求规格
    ├── requirements.md          # 详细需求文档
    ├── design.md               # 架构设计和实现计划
    └── tasks.md                # 任务清单
```

## 核心组件

### 1. VesaCalculator 类
- **位置**：`vesa_timing_calculator.py`
- **职责**：封装 VESA CVT 标准计算算法
- **关键方法**：
  - `calculate()` - 主计算方法，支持正向和反向计算
  - `_calculate_standard_cvt()` - 标准 CVT 算法
  - `_calculate_reduced_blanking()` - CVT-RB 算法
  - `_calculate_from_pixel_clock()` - 反向计算（从像素时钟计算刷新率）

### 2. MainWindow 类
- **位置**：`vesa_timing_calculator.py`
- **职责**：管理所有 UI 组件和用户交互
- **关键方法**：
  - `_create_input_panel()` - 创建左侧输入面板
  - `_create_output_panel()` - 创建右侧输出面板
  - `_on_calculate()` - 计算按钮事件处理
  - `_on_input_changed()` - 实时计算（输入变化触发）
  - `_on_preset_selected()` - 预设选择处理
  - `_copy_results()` - 复制结果到剪贴板

### 3. TimingParameters 数据类
- **位置**：`vesa_timing_calculator.py`
- **职责**：存储输入和输出参数，提供验证功能
- **字段**：包含 4 个输入参数和 11 个输出参数

## 技术栈

- **GUI 框架**：PyQt5
- **编程语言**：Python 3
- **测试框架**：pytest + pytest-qt
- **属性测试**：Hypothesis（计划中）
- **代码规范**：PEP 8

## 运行方式

### 启动应用程序
```bash
python vesa_timing_calculator.py
```

### 运行测试
```bash
# 运行所有测试
pytest test_*.py

# 运行特定测试
pytest test_ui_basic.py
pytest test_reverse_calculation.py
```

## 计算模式

### 模式 1：从刷新率计算像素时钟（正向计算）
- **输入**：水平分辨率、垂直分辨率、刷新率
- **输出**：像素时钟 + 所有时序参数
- **用途**：设计新的显示时序

### 模式 2：从像素时钟计算刷新率（反向计算）
- **输入**：水平分辨率、垂直分辨率、像素时钟
- **输出**：刷新率 + 所有时序参数
- **用途**：分析现有的显示时序

## 输入参数范围

- **水平分辨率**：640-7680 像素
- **垂直分辨率**：480-4320 行
- **刷新率**：24-240 Hz
- **像素时钟**：10-1000 MHz

## 输出参数

共 11 个时序参数：
1. 像素时钟 (MHz)
2. 水平总像素
3. 水平消隐区
4. 水平前廊
5. 水平同步脉冲
6. 水平后廊
7. 垂直总行数
8. 垂直消隐区
9. 垂直前廊
10. 垂直同步脉冲
11. 垂直后廊

## 预设选项

- 1280x720@60Hz
- 1920x1080@60Hz
- 2560x1440@60Hz
- 3840x2160@60Hz
- 1920x1200@60Hz

## 关键算法常量

### 标准 CVT 模式
- `H_SYNC_PERCENT = 8.0` - 水平同步脉冲占比
- `MIN_V_SYNC_BP = 550.0` - 最小垂直同步+后廊时间 (μs)
- `MIN_V_PORCH = 3` - 最小垂直前廊行数
- `CELL_GRAN = 8` - 像素粒度

### CVT-RB 模式
- `RB_H_BLANK = 160` - 固定水平消隐像素
- `RB_V_BLANK = 460.0` - 固定垂直消隐时间 (μs)
- `RB_H_SYNC = 32` - 固定水平同步脉冲
- `RB_V_SYNC = 8` - 固定垂直同步脉冲行数

## 测试策略

### 单元测试
- UI 组件测试（`test_ui_basic.py`）
- 计算逻辑测试（`test_reverse_calculation.py`）
- 错误处理测试（`test_error_display.py`）
- 事件处理测试（`test_event_handling.py`）
- 需求验证测试（`test_requirements_verification.py`）

### 属性测试（计划中）
使用 Hypothesis 库进行基于属性的测试，验证：
- 输入参数存储一致性
- 时序参数数学一致性
- CVT-RB 模式消隐时间减少
- 输出完整性
- 无效输入错误处理

### 参考测试用例
- **标准 1080p60**：1920x1080@60Hz → 像素时钟 ≈ 173.00 MHz
- **CVT-RB 1080p60**：1920x1080@60Hz RB → 像素时钟 ≈ 138.50 MHz
- **HDMI 标准**：1920x1080, 148.5 MHz → 刷新率 ≈ 60.21 Hz

## 代码规范

- 遵循 PEP 8 命名规范
- 关键函数和类包含详细文档字符串
- CVT 算法部分有详细注释说明
- 使用类型提示（Type Hints）
- 中文界面和错误消息

## 开发注意事项

1. **精度控制**：浮点数输出保留两位小数
2. **错误处理**：输入验证 + 异常捕获 + 友好错误提示
3. **实时计算**：输入变化自动触发（500ms 内响应）
4. **布局适配**：窗口大小调整时保持合理布局
5. **代码分离**：计算逻辑与 UI 完全分离，便于测试

## 相关文档

- `README.md` - 项目简介
- `README_PIXEL_CLOCK_MODE.md` - 反向计算模式详细说明
- `.kiro/specs/vesa-timing-calculator/requirements.md` - 详细需求规格
- `.kiro/specs/vesa-timing-calculator/design.md` - 架构设计和测试策略
- `.kiro/specs/vesa-timing-calculator/tasks.md` - 实施任务清单

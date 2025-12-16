# 设计文档

## 概述

VESA 视频时序计算器是一个基于 PyQt5/6 的桌面应用程序，实现 VESA CVT (Coordinated Video Timing) 标准的视频时序参数计算。应用程序采用 MVC 架构模式，将计算逻辑与 UI 完全分离，确保代码的可维护性和可测试性。

核心功能包括：
- 基于 VESA CVT 和 CVT-RB 标准的精确时序计算
- 实时参数验证和结果更新
- 常见分辨率预设快速选择
- 计算结果的格式化复制功能
- 清晰专业的双面板界面布局

## 架构

应用程序采用分层架构：

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│         (MainWindow - UI)           │
├─────────────────────────────────────┤
│         Business Logic Layer        │
│       (VesaCalculator - CVT)        │
├─────────────────────────────────────┤
│         Data Layer                  │
│    (TimingParameters - Models)      │
└─────────────────────────────────────┘
```

### 架构组件

1. **Presentation Layer (表示层)**
   - `MainWindow` 类：管理所有 UI 组件和用户交互
   - 负责输入验证、事件处理和结果显示
   - 使用 Qt 信号槽机制实现响应式更新

2. **Business Logic Layer (业务逻辑层)**
   - `VesaCalculator` 类：封装 CVT 标准计算算法
   - 完全独立于 UI，可单独测试
   - 提供标准 CVT 和 CVT-RB 两种计算模式

3. **Data Layer (数据层)**
   - `TimingParameters` 数据类：存储输入和输出参数
   - 提供参数验证和序列化功能

## 组件和接口

### VesaCalculator 类

```python
class VesaCalculator:
    """VESA CVT 标准时序计算器"""
    
    def calculate(self, h_active: int, v_active: int, 
                  refresh_rate: float, reduced_blanking: bool = False) -> dict:
        """
        计算 CVT 时序参数
        
        参数:
            h_active: 水平有效像素 (640-7680)
            v_active: 垂直有效行数 (480-4320)
            refresh_rate: 刷新率 Hz (24-240)
            reduced_blanking: 是否使用 CVT-RB 模式
            
        返回:
            包含所有时序参数的字典
        """
        pass
    
    def _calculate_standard_cvt(self, ...) -> dict:
        """标准 CVT 计算"""
        pass
    
    def _calculate_reduced_blanking(self, ...) -> dict:
        """CVT-RB 计算"""
        pass
```

### MainWindow 类

```python
class MainWindow(QMainWindow):
    """主窗口 UI 类"""
    
    def __init__(self):
        """初始化 UI 组件和布局"""
        pass
    
    def _create_input_panel(self) -> QGroupBox:
        """创建左侧输入面板"""
        pass
    
    def _create_output_panel(self) -> QGroupBox:
        """创建右侧输出面板"""
        pass
    
    def _on_calculate(self):
        """计算按钮点击事件处理"""
        pass
    
    def _on_input_changed(self):
        """输入参数变化事件处理（实时计算）"""
        pass
    
    def _on_preset_selected(self, index: int):
        """预设选择事件处理"""
        pass
    
    def _copy_results(self):
        """复制结果到剪贴板"""
        pass
    
    def _update_results_table(self, results: dict):
        """更新结果表格显示"""
        pass
    
    def _show_error(self, message: str):
        """显示错误消息"""
        pass
```

### TimingParameters 数据类

```python
@dataclass
class TimingParameters:
    """时序参数数据模型"""
    
    # 输入参数
    h_active: int
    v_active: int
    refresh_rate: float
    reduced_blanking: bool
    
    # 输出参数
    pixel_clock: float = 0.0
    h_total: int = 0
    h_blanking: int = 0
    h_front_porch: int = 0
    h_sync_pulse: int = 0
    h_back_porch: int = 0
    v_total: int = 0
    v_blanking: int = 0
    v_front_porch: int = 0
    v_sync_pulse: int = 0
    v_back_porch: int = 0
    
    def validate_input(self) -> tuple[bool, str]:
        """验证输入参数有效性"""
        pass
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        pass
```

## 数据模型

### 输入数据模型

| 字段 | 类型 | 范围 | 默认值 | 描述 |
|------|------|------|--------|------|
| h_active | int | 640-7680 | 1920 | 水平有效像素 |
| v_active | int | 480-4320 | 1080 | 垂直有效行数 |
| refresh_rate | float | 24-240 | 60.0 | 刷新率 (Hz) |
| reduced_blanking | bool | - | False | CVT-RB 模式开关 |

### 输出数据模型

| 字段 | 类型 | 单位 | 描述 |
|------|------|------|------|
| pixel_clock | float | MHz | 像素时钟频率 |
| h_total | int | pixels | 水平总像素数 |
| h_blanking | int | pixels | 水平消隐区 |
| h_front_porch | int | pixels | 水平前廊 |
| h_sync_pulse | int | pixels | 水平同步脉冲宽度 |
| h_back_porch | int | pixels | 水平后廊 |
| v_total | int | lines | 垂直总行数 |
| v_blanking | int | lines | 垂直消隐区 |
| v_front_porch | int | lines | 垂直前廊 |
| v_sync_pulse | int | lines | 垂直同步脉冲宽度 |
| v_back_porch | int | lines | 垂直后廊 |

### CVT 算法常量

标准 CVT 模式：
- `H_SYNC_PERCENT = 8.0`  # 水平同步脉冲占比
- `MIN_V_SYNC_BP = 550.0`  # 最小垂直同步+后廊时间 (μs)
- `MIN_V_PORCH = 3`  # 最小垂直前廊行数
- `CELL_GRAN = 8`  # 像素粒度（必须是 8 的倍数）

CVT-RB 模式：
- `RB_H_BLANK = 160`  # 固定水平消隐像素
- `RB_V_BLANK = 460.0`  # 固定垂直消隐时间 (μs)
- `RB_H_SYNC = 32`  # 固定水平同步脉冲
- `RB_V_SYNC = 8`  # 固定垂直同步脉冲行数


## 正确性属性

*属性是一个特征或行为，应该在系统的所有有效执行中保持为真——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*

### Property 1: 输入参数存储一致性
*对于任何*有效的输入参数（水平分辨率、垂直分辨率、刷新率、reduced_blanking），当这些参数被传递给应用程序时，应用程序应该能够正确存储并在后续检索时返回相同的值。
**验证需求: Requirements 1.1**

### Property 2: 水平时序参数数学一致性
*对于任何*有效的输入参数，计算得到的水平时序参数必须满足以下关系：h_total = h_active + h_blanking，且 h_blanking = h_front_porch + h_sync_pulse + h_back_porch。
**验证需求: Requirements 2.2**

### Property 3: 垂直时序参数数学一致性
*对于任何*有效的输入参数，计算得到的垂直时序参数必须满足以下关系：v_total = v_active + v_blanking，且 v_blanking = v_front_porch + v_sync_pulse + v_back_porch。
**验证需求: Requirements 2.3**

### Property 4: CVT-RB 模式消隐时间减少
*对于任何*有效的输入参数，当使用 CVT-RB 模式计算时，总消隐时间（h_blanking + v_blanking）应该小于使用标准 CVT 模式计算的消隐时间。
**验证需求: Requirements 2.4**

### Property 5: 输出精度保证
*对于任何*计算结果，所有浮点数类型的输出参数（如 pixel_clock）在格式化显示时应该至少保留两位小数。
**验证需求: Requirements 2.6**

### Property 6: 输出完整性
*对于任何*有效的输入参数，计算结果字典必须包含所有 11 个必需的时序参数键：pixel_clock, h_total, h_blanking, h_front_porch, h_sync_pulse, h_back_porch, v_total, v_blanking, v_front_porch, v_sync_pulse, v_back_porch。
**验证需求: Requirements 3.3**

### Property 7: 无效输入错误处理
*对于任何*无效的输入参数（分辨率或刷新率 <= 0，或超出允许范围），应用程序应该返回错误状态而不是计算结果，并提供错误消息。
**验证需求: Requirements 3.4, 8.1**

### Property 8: 预设参数映射正确性
*对于任何*预设选项，选择该预设后填充的参数值（h_active, v_active, refresh_rate）应该与预设定义中的值完全匹配。
**验证需求: Requirements 4.2**

### Property 9: 复制结果格式正确性
*对于任何*计算结果，复制到剪贴板的文本应该包含所有 11 个参数，每个参数占一行，格式为"参数名称: 数值 单位"。
**验证需求: Requirements 5.1, 5.2**

### Property 10: VesaCalculator 接口契约
*对于任何*调用 VesaCalculator.calculate() 方法的情况，该方法应该接受四个参数（h_active: int, v_active: int, refresh_rate: float, reduced_blanking: bool）并返回一个字典类型的结果。
**验证需求: Requirements 7.3**

## 错误处理

### 输入验证错误

1. **范围验证**
   - 水平分辨率不在 640-7680 范围内
   - 垂直分辨率不在 480-4320 范围内
   - 刷新率不在 24-240 Hz 范围内
   - 处理方式：自动限制到边界值或显示错误提示

2. **类型验证**
   - 输入非数字字符
   - 处理方式：Qt SpinBox 自动处理，只允许数字输入

3. **零值或负值**
   - 分辨率或刷新率 <= 0
   - 处理方式：清空结果区域，显示红色错误消息

### 计算错误

1. **算法异常**
   - CVT 计算过程中的数学错误（如除零）
   - 处理方式：捕获异常，显示友好错误消息，记录日志

2. **精度问题**
   - 浮点数计算精度损失
   - 处理方式：使用 Decimal 类型或适当的舍入策略

### UI 错误

1. **剪贴板访问失败**
   - 系统剪贴板不可用
   - 处理方式：捕获异常，显示"复制失败"提示

2. **窗口初始化失败**
   - Qt 组件创建失败
   - 处理方式：显示错误对话框，安全退出应用

### 错误显示策略

- 使用状态栏显示临时错误消息（3-5 秒自动消失）
- 严重错误使用 QMessageBox 对话框
- 输入验证错误在输出区域用红色文本显示
- 所有错误消息使用中文，清晰描述问题和建议操作

## 测试策略

### 单元测试

使用 `pytest` 框架进行单元测试，重点测试：

1. **VesaCalculator 类测试**
   - 使用 VESA 官方标准测试用例验证计算准确性
   - 测试标准 CVT 模式：1920x1080@60Hz 的已知结果
   - 测试 CVT-RB 模式：1920x1080@60Hz 的已知结果
   - 边界值测试：最小分辨率 640x480@24Hz
   - 边界值测试：最大分辨率 7680x4320@240Hz

2. **TimingParameters 类测试**
   - 输入验证逻辑测试
   - 数据序列化和反序列化测试

3. **UI 组件测试**
   - 预设列表完整性测试（验证包含所有必需预设）
   - 复制功能格式测试（验证输出格式正确）
   - 错误消息显示测试

### 属性测试

使用 `Hypothesis` 库进行基于属性的测试，配置每个测试运行至少 100 次迭代。

每个属性测试必须使用以下格式标注：
```python
# Feature: vesa-timing-calculator, Property {number}: {property_text}
```

1. **Property 1: 输入参数存储一致性**
   ```python
   # Feature: vesa-timing-calculator, Property 1: 输入参数存储一致性
   @given(h_active=integers(640, 7680), 
          v_active=integers(480, 4320),
          refresh_rate=floats(24.0, 240.0),
          reduced_blanking=booleans())
   def test_input_storage_consistency(h_active, v_active, refresh_rate, reduced_blanking):
       # 测试输入存储和检索的一致性
   ```

2. **Property 2 & 3: 时序参数数学一致性**
   ```python
   # Feature: vesa-timing-calculator, Property 2: 水平时序参数数学一致性
   # Feature: vesa-timing-calculator, Property 3: 垂直时序参数数学一致性
   @given(h_active=integers(640, 7680), 
          v_active=integers(480, 4320),
          refresh_rate=floats(24.0, 240.0),
          reduced_blanking=booleans())
   def test_timing_parameters_consistency(h_active, v_active, refresh_rate, reduced_blanking):
       # 验证 h_total = h_active + h_blanking
       # 验证 h_blanking = h_front_porch + h_sync_pulse + h_back_porch
       # 验证垂直参数的相同关系
   ```

3. **Property 4: CVT-RB 模式消隐时间减少**
   ```python
   # Feature: vesa-timing-calculator, Property 4: CVT-RB 模式消隐时间减少
   @given(h_active=integers(640, 7680), 
          v_active=integers(480, 4320),
          refresh_rate=floats(24.0, 240.0))
   def test_reduced_blanking_reduces_blanking_time(h_active, v_active, refresh_rate):
       # 比较标准模式和 RB 模式的消隐时间
   ```

4. **Property 6: 输出完整性**
   ```python
   # Feature: vesa-timing-calculator, Property 6: 输出完整性
   @given(h_active=integers(640, 7680), 
          v_active=integers(480, 4320),
          refresh_rate=floats(24.0, 240.0),
          reduced_blanking=booleans())
   def test_output_completeness(h_active, v_active, refresh_rate, reduced_blanking):
       # 验证结果包含所有 11 个必需键
   ```

5. **Property 7: 无效输入错误处理**
   ```python
   # Feature: vesa-timing-calculator, Property 7: 无效输入错误处理
   @given(h_active=integers(-1000, 0) | integers(7681, 10000),
          v_active=integers(-1000, 0) | integers(4321, 10000),
          refresh_rate=floats(-100.0, 0.0) | floats(241.0, 1000.0))
   def test_invalid_input_error_handling(h_active, v_active, refresh_rate):
       # 验证无效输入返回错误而不是结果
   ```

### 集成测试

1. **端到端工作流测试**
   - 启动应用 → 选择预设 → 验证自动计算 → 复制结果
   - 启动应用 → 手动输入 → 点击计算 → 验证结果显示

2. **UI 交互测试**
   - 使用 `pytest-qt` 测试 Qt 信号槽机制
   - 测试输入变化触发自动计算
   - 测试预设选择触发参数填充

### 测试覆盖率目标

- 代码覆盖率：>= 85%
- VesaCalculator 类：100%（核心计算逻辑必须完全覆盖）
- 错误处理路径：>= 90%

### CVT 算法验证

使用以下 VESA 标准参考值进行验证：

**标准 CVT 模式 - 1920x1080@60Hz**
- 预期像素时钟：≈ 173.00 MHz
- 预期 h_total：≈ 2576 pixels
- 预期 v_total：≈ 1120 lines

**CVT-RB 模式 - 1920x1080@60Hz**
- 预期像素时钟：≈ 138.50 MHz
- 预期 h_total：2080 pixels
- 预期 v_total：1111 lines

这些参考值将用于单元测试中验证算法实现的正确性。

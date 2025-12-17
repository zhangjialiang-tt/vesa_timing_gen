# VESA 时序计算器 - RTL 代码生成功能

## 功能概述

VESA 时序计算器现在支持自动生成 Verilog RTL 代码，可以根据计算出的时序参数生成完整的硬件描述代码和测试平台。

## 主要特性

### 1. 自动生成 RTL 模块
- 完整的 Verilog 时序生成器模块
- 包含详细的参数注释和文档
- 自动计算计数器位宽
- 生成标准的同步信号（hsync, vsync, de）

### 2. 自动生成测试平台
- 完整的 Verilog testbench
- 自动配置时钟周期
- 包含帧计数和监控逻辑
- 支持波形转储（VCD 格式）

### 3. 输出文件管理
- 自动创建 `./output` 目录
- 文件名包含分辨率和刷新率信息
- 同时生成模块和测试平台文件

## 使用方法

### 步骤 1: 计算时序参数
1. 启动应用程序：`python vesa_timing_calculator.py`
2. 输入分辨率和刷新率（或像素时钟）
3. 选择计算模式（标准 CVT 或 CVT-RB）
4. 等待计算完成

### 步骤 2: 生成 RTL 代码
1. 点击"生成 RTL 代码"按钮（绿色按钮）
2. 等待生成完成
3. 查看成功提示对话框

### 步骤 3: 查看生成的文件
生成的文件位于 `./output` 目录：
- `vesa_timing_<分辨率>_<刷新率>hz.v` - RTL 模块
- `tb_vesa_timing_<分辨率>_<刷新率>hz.v` - 测试平台

## 生成的 RTL 模块接口

### 端口定义

```verilog
module vesa_timing_gen (
    input  wire        clk,           // 像素时钟
    input  wire        rst_n,         // 异步复位，低电平有效
    
    output reg         hsync,         // 水平同步信号
    output reg         vsync,         // 垂直同步信号
    output reg         de,            // 数据使能信号
    output reg         frame_valid,   // 帧有效信号
    
    output reg  [N:0]  h_count,       // 水平计数器
    output reg  [M:0]  v_count        // 垂直计数器
);
```

### 信号说明

| 信号 | 方向 | 描述 |
|------|------|------|
| clk | 输入 | 像素时钟，频率根据计算结果确定 |
| rst_n | 输入 | 异步复位信号，低电平有效 |
| hsync | 输出 | 水平同步信号，同步脉冲期间为低电平 |
| vsync | 输出 | 垂直同步信号，同步脉冲期间为低电平 |
| de | 输出 | 数据使能信号，有效显示区域为高电平 |
| frame_valid | 输出 | 帧有效信号，有效帧期间为高电平 |
| h_count | 输出 | 水平像素计数器，范围 0 到 H_TOTAL-1 |
| v_count | 输出 | 垂直行计数器，范围 0 到 V_TOTAL-1 |

## 使用示例

### 示例 1: 生成 1920x1080@60Hz 时序

**输入参数**:
- 水平分辨率: 1920
- 垂直分辨率: 1080
- 刷新率: 60 Hz
- Reduced Blanking: 否

**生成的文件**:
- `output/vesa_timing_1920x1080_60hz.v`
- `output/tb_vesa_timing_1920x1080_60hz.v`

**关键参数**:
```verilog
localparam H_ACTIVE      = 1920;
localparam H_FRONT_PORCH = 128;
localparam H_SYNC_PULSE  = 24;
localparam H_BACK_PORCH  = 128;
localparam H_TOTAL       = 2200;

localparam V_ACTIVE      = 1080;
localparam V_FRONT_PORCH = 3;
localparam V_SYNC_PULSE  = 4;
localparam V_BACK_PORCH  = 33;
localparam V_TOTAL       = 1120;
```

### 示例 2: 生成 3840x2160@60Hz 时序（4K）

**输入参数**:
- 水平分辨率: 3840
- 垂直分辨率: 2160
- 刷新率: 60 Hz
- Reduced Blanking: 是

**生成的文件**:
- `output/vesa_timing_3840x2160_60hz.v`
- `output/tb_vesa_timing_3840x2160_60hz.v`

## 仿真和验证

### 使用 Icarus Verilog 仿真

```bash
# 编译
iverilog -o sim output/vesa_timing_1920x1080_60hz.v output/tb_vesa_timing_1920x1080_60hz.v

# 运行仿真
vvp sim

# 查看波形（使用 GTKWave）
gtkwave tb_vesa_timing_1920x1080_60hz.vcd
```

### 使用 ModelSim 仿真

```tcl
# 创建工作库
vlib work

# 编译源文件
vlog output/vesa_timing_1920x1080_60hz.v
vlog output/tb_vesa_timing_1920x1080_60hz.v

# 启动仿真
vsim tb_vesa_timing_1920x1080_60hz

# 添加波形
add wave -radix unsigned sim:/tb_vesa_timing_1920x1080_60hz/*

# 运行仿真
run -all
```

### 使用 Vivado 仿真

```tcl
# 创建项目
create_project timing_sim ./timing_sim -part xc7a35tcpg236-1

# 添加源文件
add_files output/vesa_timing_1920x1080_60hz.v
add_files -fileset sim_1 output/tb_vesa_timing_1920x1080_60hz.v

# 设置顶层模块
set_property top tb_vesa_timing_1920x1080_60hz [get_filesets sim_1]

# 运行仿真
launch_simulation
run all
```

## 集成到 FPGA 项目

### 步骤 1: 添加到项目
将生成的 `.v` 文件添加到您的 FPGA 项目中。

### 步骤 2: 实例化模块
```verilog
// 实例化时序生成器
vesa_timing_1920x1080_60hz u_timing_gen (
    .clk         (pixel_clk),      // 147.84 MHz
    .rst_n       (rst_n),
    .hsync       (hdmi_hsync),
    .vsync       (hdmi_vsync),
    .de          (hdmi_de),
    .frame_valid (frame_valid),
    .h_count     (h_pos),
    .v_count     (v_pos)
);
```

### 步骤 3: 连接显示接口
根据您的显示接口（HDMI、DisplayPort 等）连接相应的信号。

## 时序图

### 水平时序
```
        |<------- H_TOTAL ------->|
        |                         |
        |<- H_ACTIVE ->|          |
        |              |          |
    ----+              +----------+
        |              | FP | SP | BP |
        |              |    |    |    |
hsync   ----------------+    +----+    +----
                        |<-->|    |<->|
                         FP   SP   BP

de      ----------------+         +----
                        |         |
```

### 垂直时序
```
        |<------- V_TOTAL ------->|
        |                         |
        |<- V_ACTIVE ->|          |
        |              |          |
    ----+              +----------+
        |              | FP | SP | BP |
        |              |    |    |    |
vsync   ----------------+    +----+    +----
                        |<-->|    |<->|
                         FP   SP   BP

frame   ----------------+         +----
_valid                  |         |
```

## 注意事项

1. **时钟频率**: 确保 FPGA 能够生成所需的像素时钟频率
2. **时序约束**: 在综合时添加适当的时序约束
3. **信号极性**: 默认生成的同步信号为负极性（低电平有效）
4. **计数器位宽**: 自动根据分辨率计算，无需手动调整
5. **复位策略**: 使用异步复位，低电平有效

## 常见问题

**Q: 生成的代码可以直接用于 FPGA 吗？**
A: 是的，生成的代码是标准的 Verilog RTL，可以直接用于 FPGA 综合。

**Q: 如何修改同步信号极性？**
A: 在生成的代码中，将 `hsync <= 1'b0` 改为 `hsync <= 1'b1`（反之亦然）。

**Q: 支持哪些 FPGA 平台？**
A: 生成的代码是通用的 Verilog，支持所有主流 FPGA 平台（Xilinx、Intel/Altera、Lattice 等）。

**Q: 如何验证生成的时序是否正确？**
A: 使用提供的测试平台进行仿真，检查同步信号和数据使能信号的时序关系。

**Q: 可以生成 VHDL 代码吗？**
A: 当前版本只支持 Verilog，VHDL 支持可能在未来版本中添加。

## 技术支持

如有问题或建议，请参考：
- VESA CVT 1.2 标准文档
- 项目 GitHub 仓库
- 相关 FPGA 开发文档

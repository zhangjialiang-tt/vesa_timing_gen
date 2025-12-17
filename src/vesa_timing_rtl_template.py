"""
VESA 时序 RTL 代码生成模板

根据计算出的时序参数生成 Verilog RTL 代码
"""

from datetime import datetime


def generate_verilog_rtl(timing_params: dict, module_name: str = "vesa_timing_gen") -> str:
    """
    生成 Verilog RTL 代码
    
    参数:
        timing_params: 时序参数字典，包含所有计算结果
        module_name: 模块名称
        
    返回:
        生成的 Verilog 代码字符串
    """
    
    # 提取参数
    h_active = timing_params.get('h_active', 1920)
    v_active = timing_params.get('v_active', 1080)
    pixel_clock = timing_params.get('pixel_clock', 148.5)
    refresh_rate = timing_params.get('refresh_rate', 60.0)
    
    h_total = timing_params.get('h_total', 2200)
    h_front_porch = timing_params.get('h_front_porch', 88)
    h_sync_pulse = timing_params.get('h_sync_pulse', 44)
    h_back_porch = timing_params.get('h_back_porch', 148)
    
    v_total = timing_params.get('v_total', 1125)
    v_front_porch = timing_params.get('v_front_porch', 4)
    v_sync_pulse = timing_params.get('v_sync_pulse', 5)
    v_back_porch = timing_params.get('v_back_porch', 36)
    
    # 计算同步信号的起始和结束位置
    h_sync_start = h_active + h_front_porch
    h_sync_end = h_sync_start + h_sync_pulse
    
    v_sync_start = v_active + v_front_porch
    v_sync_end = v_sync_start + v_sync_pulse
    
    # 计算计数器位宽
    h_counter_width = (h_total - 1).bit_length()
    v_counter_width = (v_total - 1).bit_length()
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成 Verilog 代码
    verilog_code = f"""//==============================================================================
// VESA Timing Generator
// 
// 自动生成时间: {timestamp}
// 生成工具: VESA 视频时序计算器
//
// 时序参数:
//   分辨率: {h_active}x{v_active}
//   刷新率: {refresh_rate:.2f} Hz
//   像素时钟: {pixel_clock:.2f} MHz
//
// 水平时序:
//   H_ACTIVE      = {h_active}
//   H_FRONT_PORCH = {h_front_porch}
//   H_SYNC_PULSE  = {h_sync_pulse}
//   H_BACK_PORCH  = {h_back_porch}
//   H_TOTAL       = {h_total}
//
// 垂直时序:
//   V_ACTIVE      = {v_active}
//   V_FRONT_PORCH = {v_front_porch}
//   V_SYNC_PULSE  = {v_sync_pulse}
//   V_BACK_PORCH  = {v_back_porch}
//   V_TOTAL       = {v_total}
//==============================================================================

module {module_name} (
    input  wire        clk,           // 像素时钟 ({pixel_clock:.2f} MHz)
    input  wire        rst_n,         // 异步复位，低电平有效
    
    output reg         hsync,         // 水平同步信号
    output reg         vsync,         // 垂直同步信号
    output reg         de,            // 数据使能信号
    output reg         frame_valid,   // 帧有效信号
    
    output reg  [{h_counter_width-1}:0]  h_count,      // 水平计数器
    output reg  [{v_counter_width-1}:0]  v_count       // 垂直计数器
);

//==============================================================================
// 参数定义
//==============================================================================

// 水平时序参数
localparam H_ACTIVE      = {h_active};
localparam H_FRONT_PORCH = {h_front_porch};
localparam H_SYNC_PULSE  = {h_sync_pulse};
localparam H_BACK_PORCH  = {h_back_porch};
localparam H_TOTAL       = {h_total};

// 垂直时序参数
localparam V_ACTIVE      = {v_active};
localparam V_FRONT_PORCH = {v_front_porch};
localparam V_SYNC_PULSE  = {v_sync_pulse};
localparam V_BACK_PORCH  = {v_back_porch};
localparam V_TOTAL       = {v_total};

// 同步信号边界
localparam H_SYNC_START  = H_ACTIVE + H_FRONT_PORCH;
localparam H_SYNC_END    = H_SYNC_START + H_SYNC_PULSE;

localparam V_SYNC_START  = V_ACTIVE + V_FRONT_PORCH;
localparam V_SYNC_END    = V_SYNC_START + V_SYNC_PULSE;

//==============================================================================
// 水平计数器
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        h_count <= {h_counter_width}'d0;
    end else begin
        if (h_count == H_TOTAL - 1) begin
            h_count <= {h_counter_width}'d0;
        end else begin
            h_count <= h_count + 1'b1;
        end
    end
end

//==============================================================================
// 垂直计数器
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        v_count <= {v_counter_width}'d0;
    end else begin
        if (h_count == H_TOTAL - 1) begin
            if (v_count == V_TOTAL - 1) begin
                v_count <= {v_counter_width}'d0;
            end else begin
                v_count <= v_count + 1'b1;
            end
        end
    end
end

//==============================================================================
// 水平同步信号生成
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        hsync <= 1'b1;
    end else begin
        if (h_count >= H_SYNC_START && h_count < H_SYNC_END) begin
            hsync <= 1'b0;  // 同步脉冲为低电平
        end else begin
            hsync <= 1'b1;
        end
    end
end

//==============================================================================
// 垂直同步信号生成
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        vsync <= 1'b1;
    end else begin
        if (v_count >= V_SYNC_START && v_count < V_SYNC_END) begin
            vsync <= 1'b0;  // 同步脉冲为低电平
        end else begin
            vsync <= 1'b1;
        end
    end
end

//==============================================================================
// 数据使能信号生成
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        de <= 1'b0;
    end else begin
        if (h_count < H_ACTIVE && v_count < V_ACTIVE) begin
            de <= 1'b1;  // 在有效显示区域内
        end else begin
            de <= 1'b0;
        end
    end
end

//==============================================================================
// 帧有效信号生成
//==============================================================================

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        frame_valid <= 1'b0;
    end else begin
        if (v_count < V_ACTIVE) begin
            frame_valid <= 1'b1;  // 在有效帧内
        end else begin
            frame_valid <= 1'b0;
        end
    end
end

endmodule
"""
    
    return verilog_code


def generate_testbench(timing_params: dict, module_name: str = "vesa_timing_gen") -> str:
    """
    生成 Verilog 测试平台代码
    
    参数:
        timing_params: 时序参数字典
        module_name: 被测模块名称
        
    返回:
        生成的测试平台代码字符串
    """
    
    pixel_clock = timing_params.get('pixel_clock', 148.5)
    h_total = timing_params.get('h_total', 2200)
    v_total = timing_params.get('v_total', 1125)
    
    # 计算时钟周期 (ns)
    clk_period = 1000.0 / pixel_clock  # MHz to ns
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    testbench_code = f"""//==============================================================================
// VESA Timing Generator Testbench
// 
// 自动生成时间: {timestamp}
// 生成工具: VESA 视频时序计算器
//==============================================================================

`timescale 1ns / 1ps

module tb_{module_name};

//==============================================================================
// 参数定义
//==============================================================================

localparam CLK_PERIOD = {clk_period:.3f};  // 时钟周期 (ns)
localparam H_TOTAL = {h_total};
localparam V_TOTAL = {v_total};

//==============================================================================
// 信号声明
//==============================================================================

reg         clk;
reg         rst_n;

wire        hsync;
wire        vsync;
wire        de;
wire        frame_valid;
wire [15:0] h_count;
wire [15:0] v_count;

//==============================================================================
// 时钟生成
//==============================================================================

initial begin
    clk = 1'b0;
    forever #(CLK_PERIOD/2) clk = ~clk;
end

//==============================================================================
// 复位生成
//==============================================================================

initial begin
    rst_n = 1'b0;
    #(CLK_PERIOD * 10);
    rst_n = 1'b1;
end

//==============================================================================
// 实例化被测模块
//==============================================================================

{module_name} u_{module_name} (
    .clk         (clk),
    .rst_n       (rst_n),
    .hsync       (hsync),
    .vsync       (vsync),
    .de          (de),
    .frame_valid (frame_valid),
    .h_count     (h_count),
    .v_count     (v_count)
);

//==============================================================================
// 监控和显示
//==============================================================================

integer frame_count;

initial begin
    frame_count = 0;
    
    // 等待复位完成
    @(posedge rst_n);
    
    // 监控帧同步信号
    forever begin
        @(negedge vsync);
        frame_count = frame_count + 1;
        $display("Time: %t ns - Frame %0d started", $time, frame_count);
        
        // 模拟 3 帧后停止
        if (frame_count >= 3) begin
            #(CLK_PERIOD * H_TOTAL * 10);
            $display("\\nSimulation completed successfully!");
            $display("Total frames simulated: %0d", frame_count);
            $finish;
        end
    end
end

//==============================================================================
// 波形转储 (可选)
//==============================================================================

initial begin
    $dumpfile("tb_{module_name}.vcd");
    $dumpvars(0, tb_{module_name});
end

//==============================================================================
// 超时保护
//==============================================================================

initial begin
    #(CLK_PERIOD * H_TOTAL * V_TOTAL * 5);  // 5 帧的时间
    $display("ERROR: Simulation timeout!");
    $finish;
end

endmodule
"""
    
    return testbench_code

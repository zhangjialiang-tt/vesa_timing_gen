//==============================================================================
// VESA Timing Generator
// 
// 自动生成时间: 2025-12-17 09:39:56
// 生成工具: VESA 视频时序计算器
//
// 时序参数:
//   分辨率: 3840x2160
//   刷新率: 60.00 Hz
//   像素时钟: 533.04 MHz
//
// 水平时序:
//   H_ACTIVE      = 3840
//   H_FRONT_PORCH = 48
//   H_SYNC_PULSE  = 32
//   H_BACK_PORCH  = 80
//   H_TOTAL       = 4000
//
// 垂直时序:
//   V_ACTIVE      = 2160
//   V_FRONT_PORCH = 3
//   V_SYNC_PULSE  = 8
//   V_BACK_PORCH  = 50
//   V_TOTAL       = 2221
//==============================================================================

module vesa_timing_3840x2160_60hz_rb (
    input  wire        clk,           // 像素时钟 (533.04 MHz)
    input  wire        rst_n,         // 异步复位，低电平有效
    
    output reg         hsync,         // 水平同步信号
    output reg         vsync,         // 垂直同步信号
    output reg         de,            // 数据使能信号
    output reg         frame_valid,   // 帧有效信号
    
    output reg  [11:0]  h_count,      // 水平计数器
    output reg  [11:0]  v_count       // 垂直计数器
);

//==============================================================================
// 参数定义
//==============================================================================

// 水平时序参数
localparam H_ACTIVE      = 3840;
localparam H_FRONT_PORCH = 48;
localparam H_SYNC_PULSE  = 32;
localparam H_BACK_PORCH  = 80;
localparam H_TOTAL       = 4000;

// 垂直时序参数
localparam V_ACTIVE      = 2160;
localparam V_FRONT_PORCH = 3;
localparam V_SYNC_PULSE  = 8;
localparam V_BACK_PORCH  = 50;
localparam V_TOTAL       = 2221;

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
        h_count <= 12'd0;
    end else begin
        if (h_count == H_TOTAL - 1) begin
            h_count <= 12'd0;
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
        v_count <= 12'd0;
    end else begin
        if (h_count == H_TOTAL - 1) begin
            if (v_count == V_TOTAL - 1) begin
                v_count <= 12'd0;
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

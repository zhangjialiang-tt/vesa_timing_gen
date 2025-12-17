"""
RTL 代码生成功能演示

演示如何使用 VESA 时序计算器生成不同分辨率的 RTL 代码
"""

import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import VesaCalculator
from vesa_timing_rtl_template import generate_verilog_rtl, generate_testbench


def generate_timing_rtl(h_active, v_active, refresh_rate, reduced_blanking=False):
    """
    生成指定分辨率和刷新率的 RTL 代码
    
    参数:
        h_active: 水平分辨率
        v_active: 垂直分辨率
        refresh_rate: 刷新率
        reduced_blanking: 是否使用 CVT-RB 模式
    """
    calculator = VesaCalculator()
    
    print(f"\n{'='*70}")
    print(f"生成 {h_active}x{v_active}@{refresh_rate}Hz 时序 RTL 代码")
    if reduced_blanking:
        print("模式: CVT Reduced Blanking")
    else:
        print("模式: 标准 CVT")
    print('='*70)
    
    # 计算时序参数
    results = calculator.calculate(
        h_active=h_active,
        v_active=v_active,
        refresh_rate=refresh_rate,
        reduced_blanking=reduced_blanking
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
        return False
    
    # 添加基本参数
    results['h_active'] = h_active
    results['v_active'] = v_active
    results['refresh_rate'] = refresh_rate
    
    # 显示计算结果
    print(f"\n时序参数:")
    print(f"  像素时钟:     {results['pixel_clock']:8.2f} MHz")
    print(f"  水平总像素:   {results['h_total']:8d} pixels")
    print(f"  水平消隐区:   {results['h_blanking']:8d} pixels")
    print(f"  垂直总行数:   {results['v_total']:8d} lines")
    print(f"  垂直消隐区:   {results['v_blanking']:8d} lines")
    
    # 创建输出目录
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成文件名
    rb_suffix = "_rb" if reduced_blanking else ""
    module_name = f"vesa_timing_{h_active}x{v_active}_{int(refresh_rate)}hz{rb_suffix}"
    
    # 生成 RTL 代码
    rtl_code = generate_verilog_rtl(results, module_name)
    rtl_filename = os.path.join(output_dir, f"{module_name}.v")
    
    with open(rtl_filename, 'w', encoding='utf-8') as f:
        f.write(rtl_code)
    
    # 生成测试平台
    tb_code = generate_testbench(results, module_name)
    tb_filename = os.path.join(output_dir, f"tb_{module_name}.v")
    
    with open(tb_filename, 'w', encoding='utf-8') as f:
        f.write(tb_code)
    
    print(f"\n生成的文件:")
    print(f"  ✓ {rtl_filename}")
    print(f"  ✓ {tb_filename}")
    
    return True


def main():
    """主函数：生成多个常见分辨率的 RTL 代码"""
    
    print("="*70)
    print("VESA 时序 RTL 代码生成演示")
    print("="*70)
    
    # 定义要生成的时序配置
    configs = [
        # (h_active, v_active, refresh_rate, reduced_blanking, description)
        (1280, 720, 60.0, False, "HD 720p60"),
        (1920, 1080, 60.0, False, "Full HD 1080p60"),
        (1920, 1080, 60.0, True, "Full HD 1080p60 RB"),
        (2560, 1440, 60.0, False, "QHD 1440p60"),
        (3840, 2160, 30.0, False, "4K UHD 2160p30"),
        (3840, 2160, 60.0, True, "4K UHD 2160p60 RB"),
    ]
    
    success_count = 0
    total_count = len(configs)
    
    for h_active, v_active, refresh_rate, reduced_blanking, description in configs:
        print(f"\n处理: {description}")
        if generate_timing_rtl(h_active, v_active, refresh_rate, reduced_blanking):
            success_count += 1
    
    # 总结
    print("\n" + "="*70)
    print("生成完成！")
    print("="*70)
    print(f"成功生成: {success_count}/{total_count} 个配置")
    print(f"输出目录: ./output")
    
    # 列出所有生成的文件
    output_dir = "./output"
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith('.v')]
        print(f"\n生成的文件列表 ({len(files)} 个文件):")
        for i, filename in enumerate(sorted(files), 1):
            filepath = os.path.join(output_dir, filename)
            size = os.path.getsize(filepath)
            print(f"  {i:2d}. {filename:50s} ({size:6d} bytes)")
    
    print("\n" + "="*70)
    print("使用说明:")
    print("  1. 查看生成的 RTL 代码: cat output/<文件名>.v")
    print("  2. 使用 Icarus Verilog 仿真:")
    print("     iverilog -o sim output/<模块名>.v output/tb_<模块名>.v")
    print("     vvp sim")
    print("  3. 查看波形: gtkwave tb_<模块名>.vcd")
    print("="*70)


if __name__ == "__main__":
    main()

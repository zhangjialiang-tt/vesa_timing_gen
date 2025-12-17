"""
测试 RTL 代码生成功能
"""

import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import VesaCalculator
from vesa_timing_rtl_template import generate_verilog_rtl, generate_testbench


def test_rtl_generation():
    """测试 RTL 代码生成"""
    
    print("=" * 60)
    print("测试 RTL 代码生成功能")
    print("=" * 60)
    
    # 创建计算器实例
    calculator = VesaCalculator()
    
    # 计算 1920x1080@60Hz 的时序参数
    print("\n计算 1920x1080@60Hz 时序参数...")
    results = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        reduced_blanking=False
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
        return
    
    # 添加基本参数到结果中
    results['h_active'] = 1920
    results['v_active'] = 1080
    results['refresh_rate'] = 60.0
    
    print("时序参数计算完成:")
    print(f"  像素时钟: {results['pixel_clock']:.2f} MHz")
    print(f"  水平总像素: {results['h_total']}")
    print(f"  垂直总行数: {results['v_total']}")
    
    # 创建输出目录
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\n创建输出目录: {output_dir}")
    
    # 生成 RTL 代码
    print("\n生成 RTL 代码...")
    module_name = "vesa_timing_1920x1080_60hz"
    
    rtl_code = generate_verilog_rtl(results, module_name)
    rtl_filename = os.path.join(output_dir, f"{module_name}.v")
    
    with open(rtl_filename, 'w', encoding='utf-8') as f:
        f.write(rtl_code)
    
    print(f"RTL 代码已保存: {rtl_filename}")
    
    # 生成测试平台
    print("生成测试平台...")
    tb_code = generate_testbench(results, module_name)
    tb_filename = os.path.join(output_dir, f"tb_{module_name}.v")
    
    with open(tb_filename, 'w', encoding='utf-8') as f:
        f.write(tb_code)
    
    print(f"测试平台已保存: {tb_filename}")
    
    # 显示生成的文件信息
    print("\n生成的文件:")
    print(f"  1. {rtl_filename} ({os.path.getsize(rtl_filename)} bytes)")
    print(f"  2. {tb_filename} ({os.path.getsize(tb_filename)} bytes)")
    
    # 显示 RTL 代码的前几行
    print("\nRTL 代码预览 (前 30 行):")
    print("-" * 60)
    with open(rtl_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:30], 1):
            print(f"{i:3d}: {line}", end='')
    print("-" * 60)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_rtl_generation()

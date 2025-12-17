#!/usr/bin/env python3
"""
测试新增的双参数计算模式
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import VesaCalculator

def test_dual_parameter_mode():
    """测试双参数计算模式"""
    print("测试新增的双参数计算模式...")
    
    # 创建计算器实例
    calculator = VesaCalculator()
    
    # 测试用例1: 1920x1080@60Hz，像素时钟 148.5MHz
    print("\n测试用例1: 1920x1080@60Hz，像素时钟 148.5MHz")
    results1 = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        pixel_clock=148.5,
        reduced_blanking=False
    )
    
    if 'error' in results1 and results1['error']:
        print(f"错误: {results1['message']}")
    else:
        print("计算结果:")
        for key, value in results1.items():
            if key != 'error':
                print(f"  {key}: {value}")
    
    # 测试用例2: 1920x1080@60Hz，像素时钟 148.5MHz，Reduced Blanking
    print("\n测试用例2: 1920x1080@60Hz，像素时钟 148.5MHz，Reduced Blanking")
    results2 = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        pixel_clock=148.5,
        reduced_blanking=True
    )
    
    if 'error' in results2 and results2['error']:
        print(f"错误: {results2['message']}")
    else:
        print("计算结果:")
        for key, value in results2.items():
            if key != 'error':
                print(f"  {key}: {value}")
    
    # 测试用例3: 3840x2160@60Hz，像素时钟 533.25MHz
    print("\n测试用例3: 3840x2160@60Hz，像素时钟 533.25MHz")
    results3 = calculator.calculate(
        h_active=3840,
        v_active=2160,
        refresh_rate=60.0,
        pixel_clock=533.25,
        reduced_blanking=False
    )
    
    if 'error' in results3 and results3['error']:
        print(f"错误: {results3['message']}")
    else:
        print("计算结果:")
        for key, value in results3.items():
            if key != 'error':
                print(f"  {key}: {value}")
    
    # 测试用例4: 验证错误处理 - 无效的刷新率
    print("\n测试用例4: 验证错误处理 - 无效的刷新率")
    results4 = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=300.0,  # 超出范围
        pixel_clock=148.5,
        reduced_blanking=False
    )
    
    if 'error' in results4 and results4['error']:
        print(f"预期错误: {results4['message']}")
    else:
        print("错误: 应该报告刷新率超出范围")
    
    # 测试用例5: 验证错误处理 - 无效的像素时钟
    print("\n测试用例5: 验证错误处理 - 无效的像素时钟")
    results5 = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        pixel_clock=-10.0,  # 无效值
        reduced_blanking=False
    )
    
    if 'error' in results5 and results5['error']:
        print(f"预期错误: {results5['message']}")
    else:
        print("错误: 应该报告像素时钟无效")

def test_comparison_with_existing_modes():
    """比较新模式与现有模式的一致性"""
    print("\n\n比较新模式与现有模式的一致性...")
    
    calculator = VesaCalculator()
    
    # 使用模式1计算: 从刷新率计算像素时钟
    print("\n使用模式1计算: 从刷新率计算像素时钟")
    results_mode1 = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        reduced_blanking=False
    )
    
    if 'error' not in results_mode1 or not results_mode1['error']:
        pixel_clock_from_mode1 = results_mode1['pixel_clock']
        print(f"计算出的像素时钟: {pixel_clock_from_mode1} MHz")
        
        # 使用新模式计算: 同时设置像素时钟和刷新率
        print("\n使用新模式计算: 同时设置像素时钟和刷新率")
        results_mode3 = calculator.calculate(
            h_active=1920,
            v_active=1080,
            refresh_rate=60.0,
            pixel_clock=pixel_clock_from_mode1,
            reduced_blanking=False
        )
        
        if 'error' not in results_mode3 or not results_mode3['error']:
            print("比较结果:")
            print(f"  模式1像素时钟: {pixel_clock_from_mode1} MHz")
            print(f"  模式3像素时钟: {results_mode3['pixel_clock']} MHz")
            print(f"  模式1刷新率: {results_mode1.get('refresh_rate', 'N/A')} Hz")
            print(f"  模式3刷新率: {results_mode3['refresh_rate']} Hz")
            
            # 比较时序参数
            timing_params = ['h_total', 'h_blanking', 'h_front_porch', 'h_sync_pulse', 
                          'h_back_porch', 'v_total', 'v_blanking', 'v_front_porch', 
                          'v_sync_pulse', 'v_back_porch']
            
            all_match = True
            for param in timing_params:
                if param in results_mode1 and param in results_mode3:
                    if results_mode1[param] != results_mode3[param]:
                        print(f"  警告: {param} 不匹配 - 模式1: {results_mode1[param]}, 模式3: {results_mode3[param]}")
                        all_match = False
            
            if all_match:
                print("  所有时序参数匹配!")
            else:
                print("  部分时序参数不匹配。")
        else:
            print(f"新模式计算错误: {results_mode3.get('message', '未知错误')}")
    else:
        print(f"模式1计算错误: {results_mode1.get('message', '未知错误')}")

if __name__ == "__main__":
    print("VESA 时序计算器 - 新功能测试")
    print("=" * 50)
    
    test_dual_parameter_mode()
    test_comparison_with_existing_modes()
    
    print("\n" + "=" * 50)
    print("测试完成!")
"""
测试反向计算功能：从像素时钟计算刷新率
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import VesaCalculator

def test_reverse_calculation():
    """测试从像素时钟反向计算"""
    calculator = VesaCalculator()
    
    print("=" * 60)
    print("测试反向计算：从像素时钟计算刷新率")
    print("=" * 60)
    
    # 测试 1: 1920x1080, 148.5 MHz (标准 HDMI 1080p60)
    print("\n测试 1: 1920x1080 @ 148.5 MHz")
    results = calculator.calculate(
        h_active=1920,
        v_active=1080,
        pixel_clock=148.5,
        reduced_blanking=False
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
    else:
        print(f"计算出的刷新率: {results['refresh_rate']:.2f} Hz")
        print(f"像素时钟: {results['pixel_clock']:.2f} MHz")
        print(f"水平总像素: {results['h_total']}")
        print(f"垂直总行数: {results['v_total']}")
    
    # 测试 2: 1920x1080, 138.5 MHz (CVT-RB)
    print("\n测试 2: 1920x1080 @ 138.5 MHz (Reduced Blanking)")
    results = calculator.calculate(
        h_active=1920,
        v_active=1080,
        pixel_clock=138.5,
        reduced_blanking=True
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
    else:
        print(f"计算出的刷新率: {results['refresh_rate']:.2f} Hz")
        print(f"像素时钟: {results['pixel_clock']:.2f} MHz")
        print(f"水平总像素: {results['h_total']}")
        print(f"垂直总行数: {results['v_total']}")
    
    # 测试 3: 3840x2160, 297 MHz (4K60)
    print("\n测试 3: 3840x2160 @ 297 MHz")
    results = calculator.calculate(
        h_active=3840,
        v_active=2160,
        pixel_clock=297.0,
        reduced_blanking=False
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
    else:
        print(f"计算出的刷新率: {results['refresh_rate']:.2f} Hz")
        print(f"像素时钟: {results['pixel_clock']:.2f} MHz")
        print(f"水平总像素: {results['h_total']}")
        print(f"垂直总行数: {results['v_total']}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

def test_forward_calculation():
    """测试正向计算（验证原有功能仍然正常）"""
    calculator = VesaCalculator()
    
    print("\n" + "=" * 60)
    print("测试正向计算：从刷新率计算像素时钟")
    print("=" * 60)
    
    # 测试: 1920x1080 @ 60Hz
    print("\n测试: 1920x1080 @ 60Hz")
    results = calculator.calculate(
        h_active=1920,
        v_active=1080,
        refresh_rate=60.0,
        reduced_blanking=False
    )
    
    if 'error' in results:
        print(f"错误: {results['message']}")
    else:
        print(f"像素时钟: {results['pixel_clock']:.2f} MHz")
        print(f"水平总像素: {results['h_total']}")
        print(f"垂直总行数: {results['v_total']}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_reverse_calculation()
    test_forward_calculation()

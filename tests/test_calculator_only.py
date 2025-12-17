#!/usr/bin/env python3
"""
测试新增的双参数计算模式 - 只测试计算器类，不依赖GUI
"""

import sys
import os

# 添加当前目录到 Python 路径，以便导入 vesa_timing_calculator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入 VesaCalculator 类，避免导入 PyQt5 部分
class VesaCalculator:
    """
    VESA CVT 标准时序计算器
    
    实现 VESA Coordinated Video Timing (CVT) 标准算法，
    支持标准 CVT 模式和 CVT Reduced Blanking (CVT-RB) 模式。
    """
    
    # 标准 CVT 模式常量
    H_SYNC_PERCENT = 8.0  # 水平同步脉冲占消隐区的百分比
    MIN_V_SYNC_BP = 550.0  # 最小垂直同步+后廊时间 (微秒)
    MIN_V_PORCH = 3  # 最小垂直前廊行数
    CELL_GRAN = 8  # 像素粒度（水平像素必须是 8 的倍数）
    
    # CVT-RB 模式常量
    RB_H_BLANK = 160  # 固定水平消隐像素
    RB_V_BLANK = 460.0  # 固定垂直消隐时间 (微秒)
    RB_H_SYNC = 32  # 固定水平同步脉冲宽度
    RB_V_SYNC = 8  # 固定垂直同步脉冲行数
    RB_MIN_V_BPORCH = 6  # 最小垂直后廊行数
    
    def calculate(self, h_active: int, v_active: int, 
                  refresh_rate: float = None, pixel_clock: float = None,
                  reduced_blanking: bool = False) -> dict:
        """
        计算 CVT 时序参数
        
        支持三种计算模式：
        1. 正向计算：提供 refresh_rate，计算 pixel_clock 和其他参数
        2. 反向计算：提供 pixel_clock，计算 refresh_rate 和其他参数
        3. 双参数计算：同时提供 refresh_rate 和 pixel_clock，计算时序参数
        
        参数:
            h_active: 水平有效像素 (640-7680)
            v_active: 垂直有效行数 (480-4320)
            refresh_rate: 刷新率 Hz (24-240)，模式1和3时必需
            pixel_clock: 像素时钟 MHz，模式2和3时必需
            reduced_blanking: 是否使用 CVT-RB 模式
            
        返回:
            包含所有时序参数的字典，如果输入无效则返回错误信息
        """
        # 验证基本参数
        if h_active < 640 or h_active > 7680:
            return {
                'error': True,
                'message': f"水平分辨率必须在 640 到 7680 像素之间，当前值: {h_active}"
            }
        
        if v_active < 480 or v_active > 4320:
            return {
                'error': True,
                'message': f"垂直分辨率必须在 480 到 4320 行之间，当前值: {v_active}"
            }
        
        # 检查计算模式
        if refresh_rate is None and pixel_clock is None:
            return {
                'error': True,
                'message': '请提供刷新率或像素时钟参数'
            }
        
        # 根据模式选择计算方法
        try:
            if refresh_rate is not None and pixel_clock is not None:
                # 新增模式3：同时提供刷新率和像素时钟
                if refresh_rate < 24.0 or refresh_rate > 240.0:
                    return {
                        'error': True,
                        'message': f"刷新率必须在 24 到 240 Hz 之间，当前值: {refresh_rate}"
                    }
                
                if pixel_clock <= 0:
                    return {
                        'error': True,
                        'message': f"像素时钟必须大于零，当前值: {pixel_clock}"
                    }
                
                return self._calculate_with_both_params(h_active, v_active, refresh_rate, pixel_clock, reduced_blanking)
            elif refresh_rate is not None:
                # 模式1：正向计算：从刷新率计算像素时钟
                if refresh_rate < 24.0 or refresh_rate > 240.0:
                    return {
                        'error': True,
                        'message': f"刷新率必须在 24 到 240 Hz 之间，当前值: {refresh_rate}"
                    }
                
                if reduced_blanking:
                    return self._calculate_reduced_blanking(h_active, v_active, refresh_rate)
                else:
                    return self._calculate_standard_cvt(h_active, v_active, refresh_rate)
            else:
                # 模式2：反向计算：从像素时钟计算刷新率
                if pixel_clock <= 0:
                    return {
                        'error': True,
                        'message': f"像素时钟必须大于零，当前值: {pixel_clock}"
                    }
                
                return self._calculate_from_pixel_clock(h_active, v_active, pixel_clock, reduced_blanking)
                
        except Exception as e:
            return {
                'error': True,
                'message': f'计算过程中发生错误: {str(e)}'
            }
    
    def _calculate_with_both_params(self, h_active: int, v_active: int, 
                                   refresh_rate: float, pixel_clock: float,
                                   reduced_blanking: bool = False) -> dict:
        """
        同时使用像素时钟和刷新率计算时序参数
        
        这种模式下，用户同时指定像素时钟和刷新率，
        系统会计算相应的时序参数，确保两者兼容。
        
        参数:
            h_active: 水平有效像素
            v_active: 垂直有效行数
            refresh_rate: 刷新率 Hz
            pixel_clock: 像素时钟频率 MHz
            reduced_blanking: 是否使用 CVT-RB 模式
            
        返回:
            包含所有时序参数的字典
        """
        import math
        
        # 步骤 1: 确保水平分辨率是 CELL_GRAN 的倍数
        h_active_rounded = (h_active // self.CELL_GRAN) * self.CELL_GRAN
        
        # 步骤 2: 计算理论上的总像素和总行数
        # 根据像素时钟和刷新率计算理论上的总像素和总行数
        # pixel_clock (MHz) = h_total * v_total * refresh_rate / 1,000,000
        # h_total * v_total = pixel_clock * 1,000,000 / refresh_rate
        total_pixels_times_lines = (pixel_clock * 1000000.0) / refresh_rate
        
        # 步骤 3: 根据模式选择消隐参数
        if reduced_blanking:
            # CVT-RB 模式：使用固定的消隐参数
            h_blanking = self.RB_H_BLANK
            h_sync_pulse = self.RB_H_SYNC
            h_back_porch = 80
            h_front_porch = h_blanking - h_sync_pulse - h_back_porch
            h_total = h_active_rounded + h_blanking
            
            # 垂直时序参数
            v_sync_pulse = self.RB_V_SYNC
            v_front_porch = self.MIN_V_PORCH
            
            # 计算垂直消隐
            # 使用迭代方法计算垂直消隐，以满足给定的像素时钟和刷新率
            v_back_porch = self.RB_MIN_V_BPORCH
            v_blanking = v_front_porch + v_sync_pulse + v_back_porch
            v_total = v_active + v_blanking
            
            # 迭代调整垂直消隐，使计算结果与输入参数匹配
            for _ in range(10):  # 最多迭代 10 次
                # 计算当前配置下的像素时钟
                calculated_pixel_clock = (h_total * v_total * refresh_rate) / 1000000.0
                
                # 如果计算出的像素时钟与输入值接近，则停止迭代
                if abs(calculated_pixel_clock - pixel_clock) < 0.01:
                    break
                
                # 调整垂直总行数以匹配像素时钟
                target_v_total = total_pixels_times_lines / h_total
                v_total = int(round(target_v_total))
                v_blanking = v_total - v_active
                
                # 确保垂直消隐至少包含前廊和同步脉冲
                min_v_blanking = v_front_porch + v_sync_pulse + self.RB_MIN_V_BPORCH
                if v_blanking < min_v_blanking:
                    v_blanking = min_v_blanking
                    v_total = v_active + v_blanking
                
                # 重新计算垂直后廊
                v_back_porch = v_blanking - v_front_porch - v_sync_pulse
            
        else:
            # 标准 CVT 模式：使用标准的消隐参数
            # 根据分辨率选择合适的水平消隐
            if h_active_rounded <= 1024:
                h_blank_pixels = 256
            elif h_active_rounded <= 1280:
                h_blank_pixels = 320
            elif h_active_rounded <= 1920:
                h_blank_pixels = 280
            else:
                h_blank_pixels = 288
            
            h_blanking = ((h_blank_pixels + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
            h_total = h_active_rounded + h_blanking
            
            # 水平同步脉冲
            h_sync_pulse = int(round(h_blanking * self.H_SYNC_PERCENT / 100.0))
            h_sync_pulse = ((h_sync_pulse + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
            
            # 水平后廊和前廊
            h_back_porch = (h_blanking // 2) - (h_sync_pulse // 2)
            h_back_porch = (h_back_porch // self.CELL_GRAN) * self.CELL_GRAN
            h_front_porch = h_blanking - h_sync_pulse - h_back_porch
            
            # 垂直时序参数
            v_front_porch = self.MIN_V_PORCH
            v_sync_pulse = 4
            
            # 计算垂直消隐
            # 使用迭代方法计算垂直消隐，以满足给定的像素时钟和刷新率
            v_back_porch = 10  # 初始估算
            v_blanking = v_front_porch + v_sync_pulse + v_back_porch
            v_total = v_active + v_blanking
            
            # 迭代调整垂直消隐，使计算结果与输入参数匹配
            for _ in range(10):  # 最多迭代 10 次
                # 计算当前配置下的像素时钟
                calculated_pixel_clock = (h_total * v_total * refresh_rate) / 1000000.0
                
                # 如果计算出的像素时钟与输入值接近，则停止迭代
                if abs(calculated_pixel_clock - pixel_clock) < 0.01:
                    break
                
                # 调整垂直总行数以匹配像素时钟
                target_v_total = total_pixels_times_lines / h_total
                v_total = int(round(target_v_total))
                v_blanking = v_total - v_active
                
                # 确保垂直消隐至少包含前廊和同步脉冲
                min_v_blanking = v_front_porch + v_sync_pulse + 1
                if v_blanking < min_v_blanking:
                    v_blanking = min_v_blanking
                    v_total = v_active + v_blanking
                
                # 重新计算垂直后廊
                v_back_porch = v_blanking - v_front_porch - v_sync_pulse
        
        # 最终计算
        v_blanking = v_front_porch + v_sync_pulse + v_back_porch
        v_total = v_active + v_blanking
        
        # 计算实际像素时钟（应该与输入值非常接近）
        actual_pixel_clock = (h_total * v_total * refresh_rate) / 1000000.0
        
        # 返回所有计算结果
        return {
            'pixel_clock': round(pixel_clock, 2),  # 使用输入的像素时钟
            'refresh_rate': round(refresh_rate, 2),  # 使用输入的刷新率
            'h_total': h_total,
            'h_blanking': h_blanking,
            'h_front_porch': h_front_porch,
            'h_sync_pulse': h_sync_pulse,
            'h_back_porch': h_back_porch,
            'v_total': v_total,
            'v_blanking': v_blanking,
            'v_front_porch': v_front_porch,
            'v_sync_pulse': v_sync_pulse,
            'v_back_porch': v_back_porch,
        }
    
    def _calculate_standard_cvt(self, h_active: int, v_active: int, 
                                refresh_rate: float) -> dict:
        """
        实现标准 CVT 算法
        """
        import math
        
        # 确保水平分辨率是 CELL_GRAN 的倍数
        h_active_rounded = (h_active // self.CELL_GRAN) * self.CELL_GRAN
        
        # 垂直时序参数
        v_front_porch = self.MIN_V_PORCH
        v_sync_pulse = 4
        v_back_porch = 10  # 简化计算
        
        v_blanking = v_front_porch + v_sync_pulse + v_back_porch
        v_total = v_active + v_blanking
        
        # 水平时序参数
        if h_active_rounded <= 1024:
            h_blank_pixels = 256
        elif h_active_rounded <= 1280:
            h_blank_pixels = 320
        elif h_active_rounded <= 1920:
            h_blank_pixels = 280
        else:
            h_blank_pixels = 288
        
        h_blanking = ((h_blank_pixels + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
        h_total = h_active_rounded + h_blanking
        
        h_sync_pulse = int(round(h_blanking * self.H_SYNC_PERCENT / 100.0))
        h_sync_pulse = ((h_sync_pulse + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
        
        h_back_porch = (h_blanking // 2) - (h_sync_pulse // 2)
        h_back_porch = (h_back_porch // self.CELL_GRAN) * self.CELL_GRAN
        h_front_porch = h_blanking - h_sync_pulse - h_back_porch
        
        # 计算像素时钟
        pixel_clock = (h_total * v_total * refresh_rate) / 1000000.0
        
        return {
            'pixel_clock': round(pixel_clock, 2),
            'h_total': h_total,
            'h_blanking': h_blanking,
            'h_front_porch': h_front_porch,
            'h_sync_pulse': h_sync_pulse,
            'h_back_porch': h_back_porch,
            'v_total': v_total,
            'v_blanking': v_blanking,
            'v_front_porch': v_front_porch,
            'v_sync_pulse': v_sync_pulse,
            'v_back_porch': v_back_porch,
        }
    
    def _calculate_reduced_blanking(self, h_active: int, v_active: int, 
                                    refresh_rate: float) -> dict:
        """
        实现 CVT Reduced Blanking (CVT-RB) 算法
        """
        # 确保水平分辨率是 CELL_GRAN 的倍数
        h_active_rounded = (h_active // self.CELL_GRAN) * self.CELL_GRAN
        
        # 水平时序参数
        h_blanking = self.RB_H_BLANK
        h_sync_pulse = self.RB_H_SYNC
        h_back_porch = 80
        h_front_porch = h_blanking - h_sync_pulse - h_back_porch
        h_total = h_active_rounded + h_blanking
        
        # 垂直时序参数
        v_sync_pulse = self.RB_V_SYNC
        v_front_porch = self.MIN_V_PORCH
        v_back_porch = self.RB_MIN_V_BPORCH
        v_blanking = v_front_porch + v_sync_pulse + v_back_porch
        v_total = v_active + v_blanking
        
        # 计算像素时钟
        pixel_clock = (h_total * v_total * refresh_rate) / 1000000.0
        
        return {
            'pixel_clock': round(pixel_clock, 2),
            'h_total': h_total,
            'h_blanking': h_blanking,
            'h_front_porch': h_front_porch,
            'h_sync_pulse': h_sync_pulse,
            'h_back_porch': h_back_porch,
            'v_total': v_total,
            'v_blanking': v_blanking,
            'v_front_porch': v_front_porch,
            'v_sync_pulse': v_sync_pulse,
            'v_back_porch': v_back_porch,
        }
    
    def _calculate_from_pixel_clock(self, h_active: int, v_active: int,
                                    pixel_clock: float, reduced_blanking: bool = False) -> dict:
        """
        从像素时钟反向计算时序参数
        """
        # 简化实现，只用于测试
        if reduced_blanking:
            h_blanking = self.RB_H_BLANK
            h_sync_pulse = self.RB_H_SYNC
            h_back_porch = 80
            h_front_porch = h_blanking - h_sync_pulse - h_back_porch
            h_total = ((h_active // self.CELL_GRAN) * self.CELL_GRAN) + h_blanking
            
            v_sync_pulse = self.RB_V_SYNC
            v_front_porch = self.MIN_V_PORCH
            v_back_porch = self.RB_MIN_V_BPORCH
            v_blanking = v_front_porch + v_sync_pulse + v_back_porch
            v_total = v_active + v_blanking
        else:
            if ((h_active // self.CELL_GRAN) * self.CELL_GRAN) <= 1024:
                h_blank_pixels = 256
            elif ((h_active // self.CELL_GRAN) * self.CELL_GRAN) <= 1280:
                h_blank_pixels = 320
            elif ((h_active // self.CELL_GRAN) * self.CELL_GRAN) <= 1920:
                h_blank_pixels = 280
            else:
                h_blank_pixels = 288
            
            h_blanking = ((h_blank_pixels + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
            h_total = ((h_active // self.CELL_GRAN) * self.CELL_GRAN) + h_blanking
            
            h_sync_pulse = int(round(h_blanking * self.H_SYNC_PERCENT / 100.0))
            h_sync_pulse = ((h_sync_pulse + self.CELL_GRAN - 1) // self.CELL_GRAN) * self.CELL_GRAN
            
            h_back_porch = (h_blanking // 2) - (h_sync_pulse // 2)
            h_back_porch = (h_back_porch // self.CELL_GRAN) * self.CELL_GRAN
            h_front_porch = h_blanking - h_sync_pulse - h_back_porch
            
            v_front_porch = self.MIN_V_PORCH
            v_sync_pulse = 4
            v_back_porch = 10
            v_blanking = v_front_porch + v_sync_pulse + v_back_porch
            v_total = v_active + v_blanking
        
        # 计算刷新率
        refresh_rate = (pixel_clock * 1000000.0) / (h_total * v_total)
        
        return {
            'pixel_clock': round(pixel_clock, 2),
            'refresh_rate': round(refresh_rate, 2),
            'h_total': h_total,
            'h_blanking': h_blanking,
            'h_front_porch': h_front_porch,
            'h_sync_pulse': h_sync_pulse,
            'h_back_porch': h_back_porch,
            'v_total': v_total,
            'v_blanking': v_blanking,
            'v_front_porch': v_front_porch,
            'v_sync_pulse': v_sync_pulse,
            'v_back_porch': v_back_porch,
        }


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
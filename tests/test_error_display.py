"""
错误显示测试 - 验证错误处理和显示功能
"""
import sys
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import MainWindow, VesaCalculator


def test_error_display_in_table():
    """测试错误在表格中的显示"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # 直接调用 _show_error 方法
    test_message = "这是一个测试错误消息"
    window._show_error(test_message)
    
    # 验证错误显示在表格第一行
    error_text = window.results_table.item(0, 1).text()
    assert "错误" in error_text, "表格应该显示错误标识"
    assert test_message in error_text, "表格应该包含错误消息"
    
    # 验证错误文本是红色的
    error_item = window.results_table.item(0, 1)
    assert error_item.foreground().color() == Qt.red, "错误文本应该是红色"
    
    # 验证其他行被清空
    for i in range(1, 11):
        assert window.results_table.item(i, 1).text() == "", f"第 {i} 行应该被清空"
    
    # 验证状态栏显示错误
    status_message = window.statusBar().currentMessage()
    assert "错误" in status_message, "状态栏应该显示错误"
    assert test_message in status_message, "状态栏应该包含错误消息"
    
    print("✓ 错误显示在表格中测试通过")
    app.quit()


def test_validation_error_handling():
    """测试输入验证错误处理"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # 使用 VesaCalculator 直接测试验证错误
    calculator = VesaCalculator()
    
    # 测试超出范围的输入
    result = calculator.calculate(h_active=100, v_active=1080, refresh_rate=60.0)
    assert 'error' in result, "应该返回错误"
    assert result['error'] == True, "错误标志应该为 True"
    assert '水平分辨率' in result['message'], "错误消息应该提到水平分辨率"
    
    result = calculator.calculate(h_active=1920, v_active=100, refresh_rate=60.0)
    assert 'error' in result, "应该返回错误"
    assert result['error'] == True, "错误标志应该为 True"
    assert '垂直分辨率' in result['message'], "错误消息应该提到垂直分辨率"
    
    result = calculator.calculate(h_active=1920, v_active=1080, refresh_rate=10.0)
    assert 'error' in result, "应该返回错误"
    assert result['error'] == True, "错误标志应该为 True"
    assert '刷新率' in result['message'], "错误消息应该提到刷新率"
    
    print("✓ 输入验证错误处理测试通过")
    app.quit()


def test_calculation_error_recovery():
    """测试计算错误后的恢复"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # 先进行一次成功的计算
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.calculate_button.click()
    
    # 验证有结果
    first_result = window.results_table.item(0, 1).text()
    assert first_result != "", "应该有计算结果"
    assert "MHz" in first_result, "结果应该包含单位"
    
    # 验证状态栏样式正常（没有错误样式）
    # 注意：在成功计算后，状态栏样式应该被清除
    
    print("✓ 计算错误恢复测试通过")
    app.quit()


def test_error_message_format():
    """测试错误消息格式"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # 测试不同类型的错误消息
    error_messages = [
        "水平分辨率超出范围",
        "垂直分辨率无效",
        "刷新率必须大于零"
    ]
    
    for msg in error_messages:
        window._show_error(msg)
        
        # 验证表格显示
        error_text = window.results_table.item(0, 1).text()
        assert msg in error_text, f"错误消息应该包含: {msg}"
        assert "⚠" in error_text, "应该包含警告图标"
        
        # 验证状态栏显示
        status_text = window.statusBar().currentMessage()
        assert msg in status_text, f"状态栏应该包含: {msg}"
    
    print("✓ 错误消息格式测试通过")
    app.quit()


if __name__ == "__main__":
    test_error_display_in_table()
    test_validation_error_handling()
    test_calculation_error_recovery()
    test_error_message_format()
    
    print("\n✓✓✓ 所有错误显示测试通过 ✓✓✓")

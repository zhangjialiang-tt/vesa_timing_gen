"""
事件处理测试 - 验证信号槽连接和事件处理方法
"""
import sys
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import MainWindow


def test_calculate_button(app):
    """测试计算按钮功能"""
    window = MainWindow()
    
    # 设置输入参数
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.reduced_blanking_checkbox.setChecked(False)
    
    # 点击计算按钮
    window.calculate_button.click()
    
    # 验证结果表格已填充
    pixel_clock_text = window.results_table.item(0, 1).text()
    assert pixel_clock_text != "", "像素时钟应该有值"
    assert "MHz" in pixel_clock_text, "像素时钟应该包含单位 MHz"
    
    print("✓ 计算按钮测试通过")


def test_preset_selection(app):
    """测试预设选择功能"""
    window = MainWindow()
    
    # 选择预设 1920x1080@60Hz (索引 2)
    window.preset_combobox.setCurrentIndex(2)
    
    # 验证输入框已填充
    assert window.h_active_spinbox.value() == 1920
    assert window.v_active_spinbox.value() == 1080
    assert window.refresh_rate_spinbox.value() == 60.0
    
    # 验证自动触发了计算
    pixel_clock_text = window.results_table.item(0, 1).text()
    assert pixel_clock_text != "", "预设选择后应该自动计算"
    
    print("✓ 预设选择测试通过")


def test_input_changed_realtime(app):
    """测试输入变化实时计算"""
    window = MainWindow()
    
    # 清空结果（通过设置无效值然后恢复）
    window.h_active_spinbox.setValue(1280)
    window.v_active_spinbox.setValue(720)
    window.refresh_rate_spinbox.setValue(60.0)
    
    # 验证实时计算已触发
    pixel_clock_text = window.results_table.item(0, 1).text()
    assert pixel_clock_text != "", "输入变化应该触发实时计算"
    
    # 记录当前像素时钟值
    old_value = pixel_clock_text
    
    # 修改输入
    window.h_active_spinbox.setValue(1920)
    
    # 验证结果已更新
    new_value = window.results_table.item(0, 1).text()
    assert new_value != old_value, "输入变化应该更新计算结果"
    
    print("✓ 实时计算测试通过")


def test_error_handling(app):
    """测试错误处理"""
    window = MainWindow()
    
    # 设置有效输入先计算一次
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.calculate_button.click()
    
    # 验证有结果
    assert window.results_table.item(0, 1).text() != ""
    
    # 注意：SpinBox 会自动限制范围，所以我们无法直接测试超出范围的情况
    # 但我们可以验证范围限制是否正确设置
    assert window.h_active_spinbox.minimum() == 640
    assert window.h_active_spinbox.maximum() == 7680
    
    print("✓ 错误处理测试通过")


def test_copy_results(app):
    """测试复制结果功能"""
    window = MainWindow()
    
    # 先计算
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.calculate_button.click()
    
    # 点击复制按钮
    window.copy_button.click()
    
    # 验证剪贴板内容
    clipboard = QApplication.clipboard()
    clipboard_text = clipboard.text()
    
    assert clipboard_text != "", "剪贴板应该有内容"
    assert "像素时钟:" in clipboard_text, "剪贴板应该包含参数名称"
    assert "MHz" in clipboard_text, "剪贴板应该包含单位"
    
    # 验证格式：每行一个参数
    lines = clipboard_text.split("\n")
    assert len(lines) == 11, "应该有 11 行结果"
    
    print("✓ 复制结果测试通过")


def test_copy_empty_results(app):
    """测试复制空结果"""
    window = MainWindow()
    
    # 不计算，直接点击复制
    window.copy_button.click()
    
    # 验证状态栏显示提示
    status_message = window.statusBar().currentMessage()
    assert "没有可复制的内容" in status_message
    
    print("✓ 复制空结果测试通过")


def test_all_presets(app):
    """测试所有预设"""
    window = MainWindow()
    
    presets = [
        (1, 1280, 720, 60.0),
        (2, 1920, 1080, 60.0),
        (3, 2560, 1440, 60.0),
        (4, 3840, 2160, 60.0),
        (5, 1920, 1200, 60.0),
    ]
    
    for index, h_active, v_active, refresh_rate in presets:
        window.preset_combobox.setCurrentIndex(index)
        
        assert window.h_active_spinbox.value() == h_active
        assert window.v_active_spinbox.value() == v_active
        assert window.refresh_rate_spinbox.value() == refresh_rate
        
        # 验证计算结果存在
        assert window.results_table.item(0, 1).text() != ""
    
    print("✓ 所有预设测试通过")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    test_calculate_button(app)
    test_preset_selection(app)
    test_input_changed_realtime(app)
    test_error_handling(app)
    test_copy_results(app)
    test_copy_empty_results(app)
    test_all_presets(app)
    
    print("\n✓✓✓ 所有事件处理测试通过 ✓✓✓")
    app.quit()

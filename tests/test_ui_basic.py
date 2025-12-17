"""
基本 UI 测试 - 验证 MainWindow 可以正确创建
"""
import sys
import os
from PyQt5.QtWidgets import QApplication

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vesa_timing_calculator import MainWindow


def test_mainwindow_creation():
    """测试 MainWindow 可以成功创建"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # 验证窗口标题
    assert window.windowTitle() == "VESA 视频时序计算器"
    
    # 验证输入控件存在
    assert hasattr(window, 'h_active_spinbox')
    assert hasattr(window, 'v_active_spinbox')
    assert hasattr(window, 'refresh_rate_spinbox')
    assert hasattr(window, 'reduced_blanking_checkbox')
    assert hasattr(window, 'preset_combobox')
    assert hasattr(window, 'calculate_button')
    
    # 验证输出控件存在
    assert hasattr(window, 'results_table')
    assert hasattr(window, 'copy_button')
    
    # 验证输入控件的默认值
    assert window.h_active_spinbox.value() == 1920
    assert window.v_active_spinbox.value() == 1080
    assert window.refresh_rate_spinbox.value() == 60.0
    
    # 验证输入控件的范围
    assert window.h_active_spinbox.minimum() == 640
    assert window.h_active_spinbox.maximum() == 7680
    assert window.v_active_spinbox.minimum() == 480
    assert window.v_active_spinbox.maximum() == 4320
    assert window.refresh_rate_spinbox.minimum() == 24.0
    assert window.refresh_rate_spinbox.maximum() == 240.0
    
    # 验证预设列表包含所有必需的预设
    preset_items = [window.preset_combobox.itemText(i) 
                   for i in range(window.preset_combobox.count())]
    assert "1280x720@60Hz" in preset_items
    assert "1920x1080@60Hz" in preset_items
    assert "2560x1440@60Hz" in preset_items
    assert "3840x2160@60Hz" in preset_items
    assert "1920x1200@60Hz" in preset_items
    
    # 验证结果表格有 11 行 2 列
    assert window.results_table.rowCount() == 11
    assert window.results_table.columnCount() == 2
    
    print("✓ 所有 UI 基本测试通过")
    
    app.quit()


if __name__ == "__main__":
    test_mainwindow_creation()

"""
需求验证测试 - 验证任务 6 的所有需求
"""
import sys
from PyQt5.QtWidgets import QApplication
from vesa_timing_calculator import MainWindow


def verify_requirement_3_1_and_3_2():
    """
    验证需求 3.1 和 3.2:
    - 3.1: 用户修改任何输入参数时自动重新计算
    - 3.2: 用户点击"计算"按钮时立即执行计算
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    
    print("验证需求 3.1 和 3.2...")
    
    # 测试需求 3.2: 点击计算按钮
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.calculate_button.click()
    
    result_1 = window.results_table.item(0, 1).text()
    assert result_1 != "", "需求 3.2: 点击计算按钮应该执行计算"
    print("  ✓ 需求 3.2: 点击计算按钮立即执行计算")
    
    # 测试需求 3.1: 修改输入参数自动计算
    old_result = result_1
    window.h_active_spinbox.setValue(1280)  # 修改输入
    
    new_result = window.results_table.item(0, 1).text()
    assert new_result != old_result, "需求 3.1: 修改输入应该自动重新计算"
    print("  ✓ 需求 3.1: 修改输入参数自动重新计算")
    
    app.quit()


def verify_requirement_4_2_and_4_3():
    """
    验证需求 4.2 和 4.3:
    - 4.2: 选择预设时自动填充对应参数
    - 4.3: 预设被选择并填充后自动触发计算
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    
    print("验证需求 4.2 和 4.3...")
    
    # 测试需求 4.2: 选择预设自动填充参数
    window.preset_combobox.setCurrentIndex(2)  # 1920x1080@60Hz
    
    assert window.h_active_spinbox.value() == 1920, "需求 4.2: 预设应该填充水平分辨率"
    assert window.v_active_spinbox.value() == 1080, "需求 4.2: 预设应该填充垂直分辨率"
    assert window.refresh_rate_spinbox.value() == 60.0, "需求 4.2: 预设应该填充刷新率"
    print("  ✓ 需求 4.2: 选择预设自动填充对应参数")
    
    # 测试需求 4.3: 预设选择后自动触发计算
    result = window.results_table.item(0, 1).text()
    assert result != "", "需求 4.3: 预设选择后应该自动触发计算"
    print("  ✓ 需求 4.3: 预设选择后自动触发计算")
    
    app.quit()


def verify_signal_connections():
    """验证所有信号槽连接"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    print("验证信号槽连接...")
    
    # 验证方法存在
    assert hasattr(window, '_on_calculate'), "应该有 _on_calculate 方法"
    assert hasattr(window, '_on_input_changed'), "应该有 _on_input_changed 方法"
    assert hasattr(window, '_on_preset_selected'), "应该有 _on_preset_selected 方法"
    assert hasattr(window, '_connect_signals'), "应该有 _connect_signals 方法"
    print("  ✓ 所有事件处理方法已实现")
    
    # 验证信号连接（通过触发信号并检查结果）
    # 计算按钮
    window.calculate_button.click()
    assert window.results_table.item(0, 1).text() != "", "计算按钮信号应该连接"
    print("  ✓ 计算按钮信号已连接")
    
    # 输入控件变化
    old_value = window.results_table.item(0, 1).text()
    window.h_active_spinbox.setValue(1280)
    new_value = window.results_table.item(0, 1).text()
    assert old_value != new_value, "输入控件信号应该连接"
    print("  ✓ 输入控件变化信号已连接")
    
    # 预设选择
    window.preset_combobox.setCurrentIndex(3)  # 2560x1440@60Hz
    assert window.h_active_spinbox.value() == 2560, "预设选择信号应该连接"
    print("  ✓ 预设选择信号已连接")
    
    # 复制按钮
    window.copy_button.click()
    clipboard = QApplication.clipboard()
    assert clipboard.text() != "", "复制按钮信号应该连接"
    print("  ✓ 复制按钮信号已连接")
    
    app.quit()


def verify_vesa_calculator_integration():
    """验证 VesaCalculator 业务逻辑集成"""
    app = QApplication(sys.argv)
    window = MainWindow()
    
    print("验证 VesaCalculator 集成...")
    
    # 验证计算器实例存在
    assert hasattr(window, 'calculator'), "应该有 calculator 实例"
    print("  ✓ VesaCalculator 实例已创建")
    
    # 验证计算器被正确调用
    window.h_active_spinbox.setValue(1920)
    window.v_active_spinbox.setValue(1080)
    window.refresh_rate_spinbox.setValue(60.0)
    window.reduced_blanking_checkbox.setChecked(False)
    window.calculate_button.click()
    
    # 检查结果是否合理
    pixel_clock = window.results_table.item(0, 1).text()
    assert "MHz" in pixel_clock, "应该显示像素时钟单位"
    
    h_total = window.results_table.item(1, 1).text()
    assert "pixels" in h_total, "应该显示水平总像素单位"
    
    v_total = window.results_table.item(6, 1).text()
    assert "lines" in v_total, "应该显示垂直总行数单位"
    
    print("  ✓ VesaCalculator 正确调用并返回结果")
    
    # 测试 Reduced Blanking 模式
    window.reduced_blanking_checkbox.setChecked(True)
    window.calculate_button.click()
    
    rb_pixel_clock = window.results_table.item(0, 1).text()
    assert rb_pixel_clock != pixel_clock, "RB 模式应该产生不同的结果"
    print("  ✓ Reduced Blanking 模式正确切换")
    
    app.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("任务 6 需求验证测试")
    print("=" * 60)
    print()
    
    verify_requirement_3_1_and_3_2()
    print()
    
    verify_requirement_4_2_and_4_3()
    print()
    
    verify_signal_connections()
    print()
    
    verify_vesa_calculator_integration()
    print()
    
    print("=" * 60)
    print("✓✓✓ 所有需求验证通过 ✓✓✓")
    print("=" * 60)

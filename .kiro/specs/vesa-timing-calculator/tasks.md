# 实施计划

- [x] 1. 创建项目结构和数据模型





  - 创建主应用文件 `vesa_timing_calculator.py`
  - 实现 `TimingParameters` 数据类，包含所有输入和输出字段
  - 实现输入验证方法 `validate_input()`
  - 实现数据序列化方法 `to_dict()`
  - _需求: 1.1, 1.2, 1.3, 1.4, 7.1, 7.2_

- [ ]* 1.1 为 TimingParameters 编写属性测试
  - **Property 1: 输入参数存储一致性**
  - **验证需求: Requirements 1.1**

- [x] 2. 实现 VesaCalculator 核心计算类





  - 创建 `VesaCalculator` 类，独立于 UI
  - 定义 CVT 算法常量（标准模式和 RB 模式）
  - 实现主计算方法 `calculate(h_active, v_active, refresh_rate, reduced_blanking)` 返回字典
  - _需求: 2.1, 7.1, 7.3_

- [x] 2.1 实现标准 CVT 算法


  - 实现 `_calculate_standard_cvt()` 私有方法
  - 计算纵横比和像素时钟因子
  - 计算水平时序参数（h_total, h_blanking, h_front_porch, h_sync_pulse, h_back_porch）
  - 计算垂直时序参数（v_total, v_blanking, v_front_porch, v_sync_pulse, v_back_porch）
  - 计算像素时钟频率
  - 添加详细的算法注释，解释 VESA CVT 标准公式
  - _需求: 2.1, 2.2, 2.3, 2.5, 7.4_

- [ ]* 2.2 为标准 CVT 算法编写单元测试
  - 使用 VESA 标准参考值测试 1920x1080@60Hz
  - 测试边界值：640x480@24Hz
  - 测试边界值：7680x4320@240Hz
  - _需求: 2.1, 2.5_

- [ ]* 2.3 为标准 CVT 编写属性测试
  - **Property 2: 水平时序参数数学一致性**
  - **Property 3: 垂直时序参数数学一致性**
  - **验证需求: Requirements 2.2, 2.3**

- [x] 2.4 实现 CVT-RB 算法

  - 实现 `_calculate_reduced_blanking()` 私有方法
  - 使用 CVT-RB 固定常量（RB_H_BLANK, RB_V_BLANK 等）
  - 计算所有时序参数
  - 添加算法注释
  - _需求: 2.4, 7.4_

- [ ]* 2.5 为 CVT-RB 算法编写单元测试
  - 使用 VESA 标准参考值测试 1920x1080@60Hz RB 模式
  - _需求: 2.4_

- [ ]* 2.6 为 CVT-RB 编写属性测试
  - **Property 4: CVT-RB 模式消隐时间减少**
  - **验证需求: Requirements 2.4**

- [ ]* 2.7 为计算输出编写属性测试
  - **Property 6: 输出完整性**
  - **Property 10: VesaCalculator 接口契约**
  - **验证需求: Requirements 3.3, 7.3**

- [x] 3. 实现错误处理和验证





  - 在 `VesaCalculator.calculate()` 中添加输入参数验证
  - 对无效输入（<= 0 或超出范围）返回错误状态和消息
  - 添加异常捕获，处理计算过程中的数学错误
  - 实现精度控制，确保浮点数输出至少两位小数
  - _需求: 3.4, 8.1, 8.2, 8.3, 2.6_

- [ ]* 3.1 为错误处理编写属性测试
  - **Property 7: 无效输入错误处理**
  - **Property 5: 输出精度保证**
  - **验证需求: Requirements 3.4, 8.1, 2.6**

- [x] 4. 检查点 - 确保所有测试通过




  - 确保所有测试通过，如有问题请询问用户

- [x] 5. 创建 MainWindow UI 类





  - 创建 `MainWindow` 类，继承自 `QMainWindow`
  - 设置窗口标题、大小和基本属性
  - 创建主布局（水平布局 QHBoxLayout）
  - _需求: 6.1, 7.2_

- [x] 5.1 实现输入面板


  - 实现 `_create_input_panel()` 方法，返回 QGroupBox
  - 设置 GroupBox 标题为"输入参数"
  - 添加水平分辨率 QSpinBox（范围 640-7680，默认 1920）
  - 添加垂直分辨率 QSpinBox（范围 480-4320，默认 1080）
  - 添加刷新率 QDoubleSpinBox（范围 24-240，默认 60.0）
  - 添加 "Reduced Blanking" QCheckBox
  - 添加预设下拉菜单 QComboBox，包含至少 5 个常见分辨率
  - 添加"计算"按钮
  - 使用 QFormLayout 组织输入控件
  - _需求: 1.2, 1.3, 1.4, 1.5, 4.1, 4.4, 6.2_

- [ ]* 5.2 为输入面板编写单元测试
  - 测试 QGroupBox 标题为"输入参数"
  - 测试预设列表包含所有必需的 5 个预设
  - _需求: 6.2, 4.1, 4.4_

- [x] 5.3 实现输出面板

  - 实现 `_create_output_panel()` 方法，返回 QGroupBox
  - 设置 GroupBox 标题为"计算结果"
  - 创建 QTableWidget，设置为 2 列（参数名称，数值+单位）
  - 设置表格为 11 行（对应 11 个输出参数）
  - 添加"复制所有结果"按钮
  - 添加状态栏用于显示消息
  - _需求: 6.3, 6.4_

- [ ]* 5.4 为输出面板编写单元测试
  - 测试 QGroupBox 标题为"计算结果"
  - 测试 QTableWidget 列数为 2
  - _需求: 6.3, 6.4_

- [x] 6. 实现事件处理和业务逻辑连接









  - 实现 `_on_calculate()` 方法：获取输入，调用 VesaCalculator，更新结果表格
  - 实现 `_on_input_changed()` 方法：连接到所有输入控件的信号，实现实时计算
  - 实现 `_on_preset_selected(index)` 方法：根据预设填充输入框并触发计算
  - 连接所有信号槽（按钮点击、输入变化、预设选择）
  - _需求: 3.1, 3.2, 4.2, 4.3_

- [ ]* 6.1 为预设功能编写属性测试
  - **Property 8: 预设参数映射正确性**
  - **验证需求: Requirements 4.2**

- [x] 7. 实现结果显示和复制功能





  - 实现 `_update_results_table(results)` 方法：将计算结果填充到表格
  - 格式化数值，确保浮点数至少两位小数
  - 为每个参数添加适当的单位（MHz, pixels, lines）
  - 实现 `_copy_results()` 方法：格式化结果为文本并复制到剪贴板
  - 复制格式：每行一个参数，格式为"参数名称: 数值 单位"
  - 复制成功后在状态栏显示确认消息
  - _需求: 2.6, 5.1, 5.2, 5.3_

- [ ]* 7.1 为复制功能编写属性测试
  - **Property 9: 复制结果格式正确性**
  - **验证需求: Requirements 5.1, 5.2**

- [x] 7.2 实现空结果复制处理


  - 在 `_copy_results()` 中检查是否有计算结果
  - 如果没有结果，显示提示消息"没有可复制的内容"
  - _需求: 5.4_

- [ ]* 7.3 为空结果复制编写单元测试
  - 测试没有结果时复制操作的行为
  - _需求: 5.4_

- [x] 8. 实现 UI 错误显示





  - 实现 `_show_error(message)` 方法：在输出区域或状态栏显示错误
  - 使用红色文本或警告样式突出显示错误
  - 在 `_on_calculate()` 中集成错误处理，显示验证错误
  - 在计算异常时显示友好的错误消息
  - _需求: 3.4, 8.1, 8.3, 8.4_

- [x] 9. 添加应用程序入口点和主函数





  - 创建 `if __name__ == "__main__":` 入口
  - 初始化 QApplication
  - 创建并显示 MainWindow
  - 设置应用程序图标和样式（可选）
  - 启动事件循环
  - _需求: 所有需求_

- [ ] 10. 最终检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请询问用户

- [ ]* 11. 代码质量检查和文档完善
  - 运行 `pylint` 或 `flake8` 检查 PEP 8 合规性
  - 确保所有关键函数和类都有文档字符串
  - 验证 CVT 算法部分有详细注释
  - 添加模块级文档字符串，说明应用程序用途
  - _需求: 7.4, 7.5_

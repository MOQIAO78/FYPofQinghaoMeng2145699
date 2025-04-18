import pytest
import pandas as pd
from unittest.mock import MagicMock
from ShinyTB import server

# 模拟输入数据
input_data = {
    "population": 1000,
    "init_infected": 10,
    "init_clinical": 5,
    "infection_rate": 0.1,
    "sim_days": 365
}

# 模拟模拟结果
simulation_result = {
    "data": pd.DataFrame({
        "Day": [1, 2, 3],
        "Susceptible": [990, 980, 970],
        "Infected": [10, 20, 30],
        "Clinical": [5, 10, 15],
        "Recovered": [0, 0, 0],
        "Death": [0, 0, 0]
    }),
    "fig": MagicMock(),
    "params": {
        "population": 1000,
        "init_infected": 10,
        "init_clinical": 5,
        "infection_rate": 0.1,
        "sim_days": 365
    }
}

# 修改所有测试用例的实例化方式
from ShinyTB import app  # 替换原有server导入

# 测试 run_sim 函数
def test_run_sim():
    # 替换原有实例创建代码
    test_app = app
    
    # 模拟输入事件
    test_app.input.simulate = MagicMock()
    
    # 调用 run_sim 函数
    test_app.run_sim()  # 调整方法调用路径
    
    # 断言输入事件被触发
    app.input.simulate.assert_called_once()

# 修改其他测试用例的实例化方式（同样适用于test_sim_plot、test_sim_table、test_download_pdf）
def test_sim_plot():
    test_app = app  # 直接使用导入的app实例
    test_app.simulation_result = simulation_result
    fig = test_app.sim_plot()  # 调整方法调用路径

    # 断言返回的是模拟结果中的图
    assert fig == simulation_result["fig"]
    # 新增图形属性验证
    assert fig.axes[0].xaxis.label.get_text() == 'Day'
    assert len(fig.axes[0].lines) == 5  # 验证5条趋势线

# 测试 sim_table 函数
def test_sim_table():
    # 创建服务器实例
    app = server.App()

    # 模拟模拟结果
    app.simulation_result = simulation_result

    # 调用 sim_table 函数
    table = app.server.sim_table()

    # 断言返回的是模拟结果中的数据表
    assert table.equals(simulation_result["data"])

# 测试 download_pdf 函数
def test_download_pdf():
    # 创建服务器实例
    app = server.App()

    # 模拟模拟结果
    app.simulation_result = simulation_result

    # 调用 download_pdf 函数
    pdf_data = app.server.download_pdf()

    # 断言返回的是 PDF 数据
    assert isinstance(pdf_data, bytes)
    # 新增文件头验证
    assert pdf_data.startswith(b'%PDF-1.')

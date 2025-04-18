import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, reactive
simulation_result = reactive.Value(None)
from unittest.mock import MagicMock
from shiny.test import TestApp

# 测试正常情况
# 在测试函数前添加模拟对象
def test_run_sim_normal():
    # 创建测试用 App 上下文
    app = TestApp()
    with app.test_scope():
        # 模拟 input 对象
        global input
        input = MagicMock()
        input.population = lambda: 1000
        input.init_infected = lambda: 10
        input.init_clinical = lambda: 5
        input.infection_rate = lambda: 0.1
        input.sim_days = lambda: 30

        run_sim()

        # 获取结果时也需要在响应式上下文中
        result = simulation_result.get()
    assert result is not None
    assert isinstance(result["data"], pd.DataFrame)
    assert isinstance(result["fig"], plt.Figure)
    
    # 验证参数范围
    params = result["params"]
    assert 0.001 <= params["s (Recovered to Susceptible)"] <= 0.005
    assert 0.05 <= params["c (Infected to Clinical)"] <= 0.15
    assert 0.1 <= params["r1 (Infected to Recovered)"] <= 0.3
    
    # 验证数据完整性
    data = result["data"]
    assert len(data) >= 1
    assert data["Death"].iloc[-1] >= 0

def run_sim():
        print("Run Simulation Pushed", flush=True)
        # 获取用户输入参数
        pop = input.population()
        init_inf = input.init_infected()
        init_cli = input.init_clinical()
        inf_rate = input.infection_rate()
        sim_days = input.sim_days()
        # 运行模拟
        data, fig, params = run_simulation(pop, init_inf, init_cli, inf_rate, sim_days)
        print(data)
        print(fig)
        print(
            f"Simulation completed with parameters: {params}"
        )
        # 保存模拟结果
        simulation_result.set({"data": data, "fig": fig, "params": params})

def run_simulation(population, init_infected, init_clinical, infection_rate, sim_days):
    print("Running simulation...", flush=True)
    """
    模拟 TB 传播模型。
    
    参数:
    - population: 总人口数 (int)
    - init_infected: 初始感染状态人数 (int)
    - init_clinical: 初始临床状态人数 (int)
    - infection_rate: 易感转感染的转换率 (float)
    - sim_days: 模拟天数 (int)
    
    返回:
    - data: 每 31 天（月）聚合的状态人数数据，类型为 Pandas DataFrame。
    - fig: 展示状态变化的堆叠区域图（Matplotlib 图形）。
    - params: 包含随机生成模型参数（s、c、r1、r2、d）和用户输入参数的字典。
    
    注：随机参数基于 TB 传播研究中的合理分布生成。
    """
    # 随机生成模型参数（均匀分布）：
    s = np.random.uniform(0.001, 0.005)  # 痊愈转易感
    c = np.random.uniform(0.05, 0.15)      # 感染转临床
    r1 = np.random.uniform(0.1, 0.3)       # 感染转痊愈
    r2 = np.random.uniform(0.05, 0.2)      # 临床转痊愈
    d = np.random.uniform(0.01, 0.05)      # 临床转死亡
    
    # 初始状态
    S = population - (init_infected + init_clinical)  # 易感
    I = init_infected                                # 感染
    C = init_clinical                                # 临床
    R = 0                                            # 痊愈
    D = 0                                            # 死亡
    
    # 用于记录每 31 天的数据
    days_recorded = []
    S_list, I_list, C_list, R_list, D_list = [], [], [], [], []
    
    # 模拟循环：每天更新状态
    for day in range(1, sim_days + 1):
        # 计算有效感染比率
        effective_infection_ratio = ((I + C) * S) / population
        
        # 状态转换
        new_infections = S * infection_rate * effective_infection_ratio
        new_clinical = I * c
        new_recovered_from_infection = I * r1
        new_recovered_from_clinical = C * r2
        new_deaths = C * d
        new_susceptible = R * s
        
        # 更新各状态人数
        S_next = S - new_infections + new_susceptible
        I_next = I + new_infections - new_clinical - new_recovered_from_infection
        C_next = C + new_clinical - new_recovered_from_clinical - new_deaths
        R_next = R + new_recovered_from_infection + new_recovered_from_clinical - new_susceptible
        D_next = D + new_deaths
        
        # 保证人数不为负
        S = max(S_next, 0)
        I = max(I_next, 0)
        C = max(C_next, 0)
        R = max(R_next, 0)
        D = max(D_next, 0)
        
        # 每 31 天或最后一天记录数据
        if (day % 31 == 0) or (day == sim_days):
            days_recorded.append(day)
            S_list.append(S)
            I_list.append(I)
            C_list.append(C)
            R_list.append(R)
            D_list.append(D)
    
    # 将数据聚合成 DataFrame
    data = pd.DataFrame({
        "Day": days_recorded,
        "Susceptible": S_list,
        "Infected": I_list,
        "Clinical": C_list,
        "Recovered": R_list,
        "Death": D_list
    })
    
    # 绘制堆叠区域图展示状态动态
    fig, ax = plt.subplots()
    ax.stackplot(days_recorded, S_list, I_list, C_list, R_list, D_list,
                 labels=["Susceptible", "Infected", "Clinical", "Recovered", "Death"])
    ax.set_xlabel("Day")
    ax.set_ylabel("Population")
    ax.legend(loc="upper left")
    ax.set_title("TB Transmission Simulation Over Time")
    
    
    # 打包所有参数
    params = {
        "s (Recovered to Susceptible)": s,
        "i (Susceptible to Infection)": infection_rate,
        "c (Infected to Clinical)": c,
        "r1 (Infected to Recovered)": r1,
        "r2 (Clinical to Recovered)": r2,
        "d (Clinical to Death)": d
    }
    return data, fig, params


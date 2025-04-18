import pytest
from sim import run_simulation

# 测试正常情况
def test_run_simulation_normal():
    population = 1000
    init_infected = 10
    init_clinical = 5
    infection_rate = 0.02
    sim_days = 365

    data, fig, params = run_simulation(population, init_infected, init_clinical, infection_rate, sim_days)

    # 调试输出
    print("\n=== 数据结构 ===")
    print(f"数据类型: {type(data)}")
    print(f"数据维度: {data.shape}")
    print("前5行数据:\n", data.head(2 if data.shape[0] >=2 else 1))
    
    print("\n=== 图形对象 ===")
    print(f"图形类型: {type(fig)}")
    
    print("\n=== 参数详情 ===")
    for k, v in params.items():
        print(f"{k}: {v:.4f}")

    assert data.shape[0] > 0
    assert fig is not None
    assert params["s (Recovered to Susceptible)"] > 0
    assert params["i (Susceptible to Infection)"] == infection_rate
    assert params["c (Infected to Clinical)"] > 0
    assert params["r1 (Infected to Recovered)"] > 0
    assert params["r2 (Clinical to Recovered)"] > 0
    assert params["d (Clinical to Death)"] > 0




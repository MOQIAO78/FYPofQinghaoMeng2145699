import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_simulation(population, init_infected, init_clinical,init_recovered,init_death,basic_repro, sim_days):
    print("Running simulation...", flush=True)
    """
    参数:
    - population: 总人口数 (int)
    - init_infected: 初始感染状态人数 (int)
    - init_clinical: 初始临床状态人数 (int)
    - infection_rate: 易感转感染的转换率 (float)
    - sim_days: 模拟天数 (int)
    常假设感染事件为泊松过程（Poisson process），每个易感者被感染概率随感染人数而变，以指数分布描述【Ma et al., 2018】。通常模型设定的基本再生数R₀约为1至4，因此每名感染者年感染人数约为1–10。
    返回:
    - data: 每 31 天（月）聚合的状态人数数据，类型为 Pandas DataFrame。
    - fig: 展示状态变化的堆叠区域图（Matplotlib 图形）。
    - params: 包含随机生成模型参数（s、c、r1、r2、d）和用户输入参数的字典。
    
    随机参数基于 TB 传播研究中的合理分布生成，以“年率”生成，转换为每日率时除以365。
    """
    # 参数验证
    if population <= 0:
        raise ValueError("Population must be positive")
    if (init_infected + init_clinical) > population:
        raise ValueError("Initial cases exceed total population")
    
    # 定义辅助函数：用于生成截断的指数分布样本
    def sample_truncated_exponential(low, high, mean):
        # np.random.exponential 的参数为 scale=mean
        while True:
            candidate = np.random.exponential(scale=mean)
            if low <= candidate <= high:
                return candidate

    # 定义辅助函数：用于生成截断的 Gamma 分布样本
    def sample_truncated_gamma(low, high, shape, scale):
        while True:
            candidate = np.random.gamma(shape, scale)
            if low <= candidate <= high:
                return candidate
            
    # 初始状态
    S = population - (init_infected + init_clinical + init_recovered + init_death)  # 易感
    I = init_infected                                # 感染
    C = init_clinical                                # 临床
    R = init_recovered                               # 痊愈
    D = init_death                                  # 死亡
    
    # 用于记录每 31 天的数据
    results = {
        "Days": [],
        "Susceptible": [],
        "Infected": [],
        "Clinical": [],
        "Recovered": [],
        "Death": []
    }
   

    # 模拟循环：每天更新状态
    for day in range(1, sim_days + 1):
        N=S+I+C+R+D
        # 计算有效感染比率
        effective_infection_ratio =  C / N
        # 生成随机参数  
        # 选择 mean = 0.1 (中间值)，范围 0.05–0.15
        s_annual = sample_truncated_exponential(0.05, 0.15, mean=0.1)
        s = s_annual / 365

        # 按照文献，快速进展概率约为 0.69
        # 慢速进展：采用 Gamma 分布，形状参数 shape=2，scale设为0.01 均值约为0.02
        c_annual = sample_truncated_gamma(0.01, 0.05, shape=2, scale=0.01)
        c = c_annual / 365

        #mean = 0.2, 范围 0.1–0.3
        r1_annual = sample_truncated_exponential(0.1, 0.3, mean=0.2)
        r1 = r1_annual / 365

        #mean = 1.1, 范围 0.2–2.0
        r2_annual = sample_truncated_exponential(0.2, 1.5, mean=1)
        r2 = r2_annual / 365

        #mean = 0.125, 范围 0.1–0.15
        d_annual = sample_truncated_exponential(0.05, 0.1, mean=0.1)
        d = d_annual / 365

        # 根据 R0 公式反推 i
        i_annual =  basic_repro * (c_annual + r1_annual) * (r2_annual + d_annual) / c_annual *0.1
        i = i_annual / 365  # 转换为日率

        # 更新状态转换
        new_infections = S * i * effective_infection_ratio
        new_clinical = I * c
        new_recovered_from_infection = I * r1
        new_recovered_from_clinical = C * r2
        new_deaths = C * d
        new_susceptible = R * s
        if day >= 2:
            new_infections = NS * i * effective_infection_ratio
            new_clinical = NI * c
            new_recovered_from_infection = NI * r1
            new_recovered_from_clinical = NC * r2
            new_deaths = NC * d
            new_susceptible = NR * s
            
        # 各状态更新人数
        S_next = new_susceptible - new_infections
        I_next = new_infections - new_clinical - new_recovered_from_infection
        C_next = new_clinical - new_recovered_from_clinical - new_deaths
        R_next = new_recovered_from_infection + new_recovered_from_clinical - new_susceptible
        D_next = new_deaths

        # 状态人数更新
        NI = I + I_next
        NS = S + S_next
        NC = C + C_next
        NR = R + R_next
        ND = D + D_next
        if day >= 2:
            NI = NI + I_next
            NS = NS + S_next
            NC = NC + C_next
            NR = NR + R_next
            ND = ND + D_next
            
        
        # 每 31 天或最后一天记录数据
        if  (day % 31 == 0) or(day == sim_days):
            results["Days"].append(day)
            results["Susceptible"].append(np.round(NS))
            results["Infected"].append(np.round(NI))
            results["Clinical"].append(np.round(NC))
            results["Recovered"].append(np.round(NR))
            results["Death"].append(np.round(ND))


            
    
    # 将数据聚合成 DataFrame
    data = pd.DataFrame(results)
    
    # 绘制堆叠区域图展示状态动态
    fig, ax = plt.subplots()
    ax.stackplot(
            results["Days"],
            results["Susceptible"],
            results["Infected"],
            results["Clinical"],
            results["Recovered"],
            results["Death"],
                 labels=["Susceptible", "Infected", "Clinical", "Recovered", "Death"])
    ax.set_xlabel("Days")
    ax.set_ylabel("Population")
    ax.legend(loc="upper left")
    ax.set_title("TB Transmission Simulation")
    
    
    # 打包所有参数
    params = {
        "Basic Reproduction number (R0)": basic_repro,
        "s (Recovered to Susceptible) annual": s_annual,
        "s (Recovered to Susceptible) daily": s,
        "i (Susceptible to Infection) annual": i_annual, 
        "i (Susceptible to Infection) daily": i, 
        "c (Infected to Clinical) annual": c_annual,
        "c (Infected to Clinical) daily": c,
        "r1 (Infected to Recovered) annual": r1_annual,
        "r1 (Infected to Recovered) daily": r1,
        "r2 (Clinical to Recovered) annual": r2_annual,
        "r2 (Clinical to Recovered) daily": r2,
        "d (Clinical to Death) annual": d_annual,
        "d (Clinical to Death) daily": d,
    }
    return data, fig, params
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from shiny import App, reactive, render, ui

from sim import run_simulation
from report import  generate_pdf_report

# 定义 Shiny Tool的 UI
app_ui = ui.page_navbar( 
    ui.nav_panel(
        "Introduction",
        ui.tags.h3("Project Background"),
        ui.tags.p("""
                Tuberculosis (TB) remains a significant public health challenge globally, with complex transmission dynamics that require advanced modeling to understand and mitigate effectively. This research proposal outlines the development of a simulation software aimed at accurately modeling TB transmission, providing a valuable tool for public health researchers and policymakers.
                """),
        ui.tags.hr(),
        ui.tags.h3("Overview of the TB Simulation Tool"),
        ui.tags.ul(
            ui.tags.p(
            "This tool simulates the transmission dynamics of Tuberculosis (TB) using a compartmental model "
            "that divides the population into five states: "),
            ui.tags.li("Susceptible: Individuals who are susceptible to TB infection."),
            ui.tags.li("Infected: Individuals who are infected with TB, but not contagious."),
            ui.tags.li("Clinical: Individuals who have developed symptoms of TB, whcih are capable of transmitting the bacteria to others."),
            ui.tags.li("Recovered: Individuals who have recovered from TB."),
            ui.tags.li("Death: Individuals who have died related with TB."),
            ui.tags.p("The simulation is performed on a daily basis, and the results are aggregated monthly. "
            "Users can adjust simulation parameters and export a detailed PDF report of the results."),
        ),
        ui.tags.hr(),
        ui.tags.h3("Basic Reproduction Number (R₀)"),
        ui.tags.ul(
            ui.tags.p("""
                    The basic reproduction number, denoted as R₀ (pronounced "R nought" or "R zero"), is a key epidemiological metric that indicates the average number of secondary infections produced by a single infected individual in a fully susceptible population. It helps determine the potential for a disease to spread within a community:
                    Tuberculosis (TB) remains a significant public health challenge globally, with complex transmission dynamics that require advanced modeling to understand and mitigate effectively. This research proposal outlines the development of a simulation software aimed at accurately modeling TB transmission, providing a valuable tool for public health researchers and policymakers.
                    """),
            ui.tags.li("If R₀ > 1, the infection is likely to spread exponentially, potentially leading to an epidemic."),
            ui.tags.li("If R₀ = 1, the disease may persist endemically within the population."),
            ui.tags.li("If R₀ < 1, the infection will likely decline and eventually die out."),
            ui.tags.p("""
                    It's important to note that R₀ is not a fixed value for a given pathogen; it can vary based on factors such as environmental conditions, population density, social behavior, and public health interventions.
                    """),
        ),
        ui.tags.hr(),
        ui.tags.h3("Status Tranformation & Parameters Diagram"),
        ui.output_image('image'),
        ui.tags.hr(),
        ui.tags.h3("Contact Me"),
        ui.tags.p("""If you have any questions during TB Simulating, please don't hesitate to get in touch with me."""),
        ui.tags.p("Email: Qinghao.Meng21@student.xjtlu.edu.cn"),
    ),

    ui.nav_panel(
        "Simulation",
        ui.tags.h5('Enter your parameters then run a simulation ', ui.HTML("&#128075;")),
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_numeric("population", "Total Population", value=1000, min=1),
                ui.input_numeric("init_infected", "Initial Infected", value=10, min=0),
                ui.input_numeric("init_clinical", "Initial Clinical", value=5, min=0),
                ui.input_numeric("init_recovered", "Initial Recovered", value=0, min=0),
                ui.input_numeric("init_death", "Initial Death", value=0, min=0),
                ui.input_numeric("basic_repro", "Basic reproduction number (R₀)", value=1.5, min=0, step=0.01),
                ui.input_numeric("sim_days", "Simulation Days", value=365, min=1, max=365),
                ui.input_action_button("simulate", "Simulation")
            ),
            ui.output_plot("sim_plot")
        ),
    ),

    ui.nav_panel(
        "Data Table",
        ui.tags.h5('Here is the monthly statistics in your simulation ', ui.HTML("&#128075;")),
        ui.output_data_frame("sim_table"),
        ),
        

    ui.nav_panel(
    "Report",
    ui.tags.h5('Here is a preview of Simulation Report, you can export the results ', ui.HTML("&#128075;")),
    ui.tags.span("Exporting results may error due to browser or network reasons, please see the preview below", style="color: #666; font-size: 0.9em;"),
    ui.layout_sidebar(
        ui.sidebar(
                ui.input_text("add","Please enter the address of the browser running this page if cannot export report",placeholder="Optional"),
                ui.tags.span("Make sure the path points to the browser executable (e.g., chrome.exe/msedge.exe)", style="color: #666; font-size: 0.9em;"),
                ui.download_button("download_pdf", "Export PDF Report")
            ),
        ui.output_ui("report_preview")
    ),
    ),

    ui.nav_panel(
        "About",
        ui.output_image('logo',inline=True),
        ui.tags.h4('Supervisor: Dr. Tenglong Li', style="text-align: center; margin: 20px 0;"),
        ui.tags.h5('Qinghao Meng, Bsc Biomedical Statistics', style="text-align: center; margin: 20px 0;"),
        ui.tags.hr(),
        ui.layout_columns(  
        ui.card(  
            ui.card_header("XJTLU Wisdom Lake Academy of Pharmacy", href="https://www.xjtlu.edu.cn/en/study/departments/academy-of-pharmacy", target="_blank"),
            ui.tags.p("""Suzhou will be the site of a large biopharmaceutical ecosystem, featuring leading global pharmaceutical companies, premier healthcare providers, and world-class academic forums. The goal is to build, within 10 years, a Pharma Valley of China – a globally recognised, influential and best-in-class industry landmark in China. It is under this strategic background that Xi’an Jiaotong-Liverpool University and Suzhou Industrial Park government co-founded the XJTLU Wisdom Lake Academy of Pharmacy on 11 November 2020. In addition to the university-industry partnership, the Academy of Pharmacy added the notion of society to create a society-university-industry ecosystem, as an innovative and practice-based exploration of the national strategy. The University is able to take advantage of its multi-disciplinary expertise and global connectivity in building an academically rigorous Academy of Pharmacy that is uniquely positioned to train high-quality, internationally minded talents. Consequently, the Academy was proposed as part of the plan to execute this strategy. Recognised as the catalyst and enabler for building a first-rate and sustainable society-university-industry ecosystem, the Academy has reached full agreement with other parties in the ecosystem, and endeavours to help transform Suzhou into a world-class biopharmaceutical and healthcare hub by aligning its strategic positioning with the goal of the Pharma Valley of China."""),    
        ),
        ui.card(ui.card_header('Final Year Project: Interactive TB Transmission Simulation Tool'),
                ui.tags.p("I developed a Shiny-based interactive TB transmission simulation tool to help researchers and public health policy makers better understand and predict TB transmission dynamics for more effective control strategies through learning from Shiny development, systematic literature review, and evaluation and calibration of model parameters using Real World data."),
                ),
        ),
    ),
    title="TB Transmission Simulation",  
    id="page",
)


# 定义 Shiny 应用的 Server

def server(input, output, session):
    print("Server function loaded.", flush=True)
    r=0.1
    # 新增会话初始化逻辑
    simulation_result = reactive.Value(None)  # 将响应式变量移至会话作用域内
    session.on_ended(lambda: simulation_result.set(None))  # 会话结束时自动清理
    
    
    @reactive.effect
    def _():
        m = ui.modal(  ui.markdown(
            """
                Welcome to Qinghao Meng's final year project! \n
                This project is about the simulation of TB transmission. \n
                Here are five pages within this Shiny APP \n
                1. Introduction & Overview \n 
                2. Simulation & Dynamic figure \n 
                3. Monthly Data Table \n
                4. Report & PDF export \n
                5. About & References \n
                """),
            title=ui.h3("Qinghao Meng's Final Year Project"),  
            easy_close=True,
            footer=None,  
        )  
        ui.modal_show(m)  
    
    @output
    @render.image
    def image():
        img_path = "status.png" 
        return {"src": img_path, "width": "50%", "style": "display: block; padding: 0;"}
    
    @render.image 
    def logo():
        img_path = "wlap.png"  
        return {"src": img_path, "width": "280px", "style": "display: block; margin: 0 auto 10px auto; padding: 0;"}

    # 当用户点击“Run Simulation”按钮时运行模拟
    @reactive.Effect
    @reactive.event(input.simulate)
    def run_sim():
        print("Run Simulation Pushed", flush=True)
        simulation_result.set(None)
        # 获取用户输入参数
        pop = input.population()
        init_inf = input.init_infected()
        init_cli = input.init_clinical()
        init_rec = input.init_recovered()
        init_death = input.init_death()
        basic_repro = input.basic_repro()
        sim_days = input.sim_days()
        # 运行模拟
        data, fig, params = run_simulation(pop, init_inf, init_cli,init_rec,init_death, basic_repro, sim_days)
        # 保存模拟结果
        simulation_result.set({"data": data, "fig": fig, "params": params})

    
    # 绘制模拟结果图（堆叠区域图）
    @output
    @render.plot
    def sim_plot():
        print("Rendering plot...", flush=True)
        
        # Get the simulation result
        result = simulation_result.get()

        if result is None:
            fig, ax = plt.subplots()
            ax.axis('off')
            ax.text(0.5, 0.5, "No simulation data available, Please run a simulation.",
                    ha="center", va="center", fontsize=15)
            return fig
        
        return result["fig"]
    
    # 显示每月数据表
    @output
    @render.data_frame
    def sim_table():
        print("Rendering table...", flush=True)
        result = simulation_result.get()
        if result is None:
            return pd.DataFrame(columns=["Day", "Susceptible", "Infected", "Clinical", "Recovered", "Death"])
        return result["data"]
    
    # PDF 导出：点击下载按钮时生成 PDF 报告
    @render.download(
        filename=lambda: f"TB_Simulation_Report_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    )
    async def download_pdf(): 
        result = simulation_result.get()
        browser_path = input.add().strip()
        if result is None:
            return
        
        pdf_bytes = await generate_pdf_report({
            "params": result["params"],
            "fig": result["fig"],
            "data": result["data"]
        },browser_path=browser_path)
        
        yield pdf_bytes

    # 在服务器逻辑添加新的输出（约第255行）
    @output
    @render.ui
    def report_preview():
        result = simulation_result.get()
        if result is None:
            return ui.tags.div("No simulation data available, Please run a simulation.", style="color: #666; text-align: center; padding: 100px;")

        # 复用report模块生成HTML内容
        from report import generate_html_template
        report_html = generate_html_template({
            "params": result["params"],
            "fig": result["fig"],
            "data": result["data"]
        })
        
        # 移除PDF专用样式，添加响应式样式
        responsive_html = report_html.replace(
            '<style>', 
            '''<style>
                @media screen and (max-width: 768px) {
                    .plot-img { max-width: 95% !important; }
                    .param-table, .data-table { font-size: 14px; }
                }
            '''
        )
        
        return ui.HTML(responsive_html)

    

# 创建并运行 Shiny 
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
import io
import base64
import numpy as np
from datetime import datetime
from playwright.async_api import async_playwright  # 异步API

async def generate_pdf_report(simulation_data, browser_path):
    print("Report Generating...", flush=True)
    
    # 生成HTML内容
    html_content = generate_html_template(simulation_data)
    
    async with async_playwright() as p:
        # 创建浏览器启动配置
        launch_options = {}
        if browser_path:
            # 使用关键字参数传递路径
            launch_options["executable_path"] = browser_path.replace("\\", "/")
        browser = await p.chromium.launch(**launch_options)
        
        try:
            # 自动安装缺失的浏览器组件
            browser = await p.chromium.launch(**launch_options)
        except Exception as e:
            # 当自定义路径失败时尝试使用默认浏览器
            if browser_path:
                print(f"使用自定义浏览器失败，正在尝试默认浏览器: {str(e)}", flush=True)
                browser = await p.chromium.launch()
            else:
                raise

        page = await browser.new_page()
        await page.set_content(html_content)
        pdf_bytes = await page.pdf(format="A4")
        await browser.close()
    
    return pdf_bytes

def generate_html_template(simulation_data):
    """生成报告HTML模板"""
    # 转换图表为Base64
    plot_base64 = fig_to_base64(simulation_data["fig"])
    
    # 生成数据表格
    data_table = simulation_data["data"].to_html(
        index=False,
        classes="data-table",
        float_format=lambda x: f"{x:.2f}"
    )

    param_rows = "".join(
        f"<tr><td>{key}</td><td>{_format_value(value)}</td></tr>"
        for key, value in simulation_data["params"].items()
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>TB Transmission Simulation Report</title>
        <style>
            .report-header {{ 
                border-bottom: 2px solid #3498db;
                margin-bottom: 25px;
                padding-bottom: 15px;
                text-align: center;
            }}
            .report-title {{
                font-size: 24px;
                color: #2c3e50;
                margin: 0;
                text-align: center;
            }}
            .report-date {{
                color: #7f8c8d;
                font-size: 14px;
                text-align: center;
            }}
            .param-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            .param-table td, .param-table th {{
                padding: 8px;
                border: 1px solid #ddd;
                text-align: center;
            }}
            .plot-section {{
                margin: 30px 0;
                text-align: left;
            }}
            .plot-img {{
                max-width: 80%;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                height: auto;
            }}
            .data-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            .data-table th {{
                background-color: #f8f9fa;
                padding: 12px;
            }}
            .data-table td {{
                padding: 10px;
                border-top: 1px solid #dee2e6;
            }}
        </style>
    </head>
    <body>
        <div class="report-header">
            <h1 class="report-title">TB Transmission Simulation Report</h1>
            <div class="report-date">DATE:{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>

        <p>This report presents the simulation of TB transmission dynamics over the simulated period. <br></p>
        <p>The model uses randomly generated parameters based on estimates from TB transmission studies, which introduces realistic variability into the simulation.</p>
        <table class="param-table">
            <h2>Parameters</h2>
            <tr><th>Parameters</th><th>Value</th></tr>
            {param_rows}
        </table>

        <p>The stacked area chart displays the evolution of different states (Susceptible, Infected, Clinical, Recovered, Death) over time.</p>
        <div class="plot-section">
            <h2>Transmission Dynamics</h2>
            <img class="plot-img" src="data:image/png;base64,{plot_base64}">
        </div>

        <p>The results are aggregated monthly (every 31 days), providing insights into the progression of TB within the population.</p>
        <h2>Simulation Data</h2>
        {data_table}
    </body>
    </html>
    """
def _format_value(value):
    """统一格式化参数值"""
    if isinstance(value, float):
        return f"{value:.4f}"
    elif isinstance(value, (int, np.integer)):
        return f"{value:,}"
    elif isinstance(value, str):
        return value
    else:
        return str(value)
    
def fig_to_base64(fig):
    """将matplotlib图表转换为Base64字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    return base64.b64encode(buf.getvalue()).decode("utf-8")
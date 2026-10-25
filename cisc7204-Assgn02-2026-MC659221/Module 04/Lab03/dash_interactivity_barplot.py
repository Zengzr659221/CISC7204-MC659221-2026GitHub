# 1/ 导入所需库
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# 读取数据集
df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)


# 初始化 Dash 应用
app = Dash(__name__)

# 2/ 定义布局：标题 + 输入组件 + 输出图表
app.layout = html.Div(
    children=[
        # 标题：字体大小 40
        html.H1(
            'Total number of flights to the destination state split by reporting airline',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),

        # 第一个 division：输入组件（年份下拉框）
        html.Div(
            children=[
                html.H2('Enter a year:', style={'margin-right': '2em'}),  # 提示文字
                dcc.Input(
                    id='input-year',        # 唯一标识符，供回调使用
                    value=2010,             # 默认年份
                    type='number',          # 输入类型为数字
                    style={'height': '50px', 'font-size': 35}  # 输入框高 50px，字体 35
                ),
            ],
            # 整个 division 的字体大小设为 40
            style={'font-size': 40}
        ),

        # 第二个 division：输出组件（柱状图）
        html.Div(
            children=[
                dcc.Graph(id='bar-plot')  # 图表 id，供回调使用
            ]
        ),
    ]
)

# 3/ 回调装饰器：把输入组件和输出组件绑定起来
#    - Output: id='bar-plot' 的 figure 属性
#    - Input : id='input-year' 的 value 属性
@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)

# 4/ 回调函数：根据选择的年份，生成柱状图
def update_graph(entered_year):
    # 根据年份筛选数据
    df_yr = df[df['Year'] == int(entered_year)]

    # 按目的地州和报告航空公司分组，统计航班总数
    # （as_index=False 让分组键保留为普通列，方便后续画图）
    df_grp = df_yr.groupby(['DestState', 'Reporting_Airline'], as_index=False)['Flights'].sum()

    # 用 Plotly Express 画柱状图
    fig = px.bar(
        df_grp,
        x='DestState',                  # x 轴：目的地州
        y='Flights',                    # y 轴：航班总数
        color='Reporting_Airline',      # 按航空公司分色
        title='Total number of flights to the destination state split by reporting airline'
    )

    # 设置图表标题字体大小（可选，让图更清晰）
    fig.update_layout(
        title_font_size=25,
        xaxis_title='Destination State',
        yaxis_title='Number of Flights'
    )

    return fig

# 5/ 运行应用
if __name__ == '__main__':
    app.run()

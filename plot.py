import matplotlib.pyplot as plt
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('data/event.csv')

colors = ['#ffffff'] * len(df)
for i in range(len(df)):
    if df.iloc[i].type == 'main':
        colors[i] = '#8fbc8f'
    elif df.iloc[i].type == 'act_ss':
        colors[i] = '#b0c4de'
    elif df.iloc[i].type == 'act_om':
        colors[i] = '#bc8f8f'

data = [go.Bar(
    x=[i/10000 for i in df.charnum],
    y=[str(i) for i in df.time],
    marker_color=colors,
    customdata=np.transpose([df.sname]), # 用于显示文字的自定义数据
    orientation='h' # 水平
)]
fig = go.Figure(data=data)
fig.update_traces(texttemplate="%{customdata[0]}<br>%{x:.1f}万") # 显示文字模板
fig.update_traces(textposition="auto", textangle=0) # 文字位置
fig.update_traces(textfont_color="black", textfont_size=24, textfont_family='Microsoft YaHei') # 字体相关
fig.update_layout(yaxis=dict(tickfont_size=16), xaxis=dict(ticksuffix='万', tickfont_size=16)) # 轴相关
fig.update_layout(autosize=True, height=(len(df)-4)*60) # 设置图片大小
fig.update_yaxes(autorange="reversed") # 设置y轴反转
fig.show()

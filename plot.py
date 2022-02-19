import matplotlib.pyplot as plt
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import io
import copy


def set_color(df):
    colors = ['#ffffff'] * len(df)
    for i in range(len(df)):
        if df.iloc[i].type == 'main':
            colors[i] = '#8fbc8f'
        elif df.iloc[i].type == 'act_ss':
            colors[i] = '#b0c4de'
        elif df.iloc[i].type == 'act_om':
            colors[i] = '#bc8f8f'
    return colors

# 水平柱状图，用于汇总表示
def plot_h(df):
    colors = set_color(df)
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

    return fig

# 垂直柱状图，用于分类表示
def plot_v(df):
    colors = set_color(df)
    data = [go.Bar(
        x=df.sname,
        y=[i/10000 for i in df.charnum],
        marker_color = colors,
        orientation='v' # 垂直
    )]
    fig = go.Figure(data=data)
    fig.update_traces(texttemplate="%{x}<br>%{y:.1f}万") # 显示文字模板
    fig.update_traces(textposition="inside", textangle=0) # 文字位置
    fig.update_traces(textfont_color="black", textfont_size=16, textfont_family='Microsoft YaHei') # 字体相关
    fig.update_layout(xaxis=dict(showticklabels=False), yaxis=dict(ticksuffix='万', tickfont_size=16)) # 轴相关
    fig.update_layout(autosize=True, width=(len(df)*120)) # 设置图片大小
    fig.show()


df = pd.read_csv('data/event.csv')

fig = plot_h(df) # 全部活动

df_ss = df.query("type == 'act_ss'")
for i in range(len(df_ss)): # 增加换行
    act = df_ss.iloc[i].sname
    if len(act) > 5:
        df_ss.iat[i, 1] = f'{act[:4]}<br>{act[4:]}'

df_om = df.query("type == 'act_om'")
for i in range(len(df_om)): # 增加换行
    act = df_om.iloc[i].sname
    if len(act) > 5:
        df_om.iat[i, 1] = f'{act[:4]}<br>{act[4:]}'

df_main = df.query("type == 'main'")
for i in range(len(df_main)): # 增加换行，表示章节
    act = df_main.iloc[i].sname
    df_main.iat[i, 1] = f'EP{int(act[0]):02}<br>{act[2:]}'

fig_main = plot_v(df_main) # main
fig_ss = plot_v(df_ss) # sidestory
fig_om = plot_v(df_om) # omnibus

# 保存图片
# _im = fig.to_image(format="png", engine="kaleido", height=(len(df)-4)*100, width=2680, scale=2)
# _im = Image.open(io.BytesIO(_im))
# _im.save('./data/1.png')

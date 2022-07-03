import plotly.graph_objects as go
import numpy as np
# 可视化相关


def _set_color(df):
    # 设置柱状图颜色
    colors = ['#ffffff'] * len(df)
    for i in range(len(df)):
        if df.iloc[i].type == 'main':
            colors[i] = '#8fbc8f'
        elif df.iloc[i].type == 'act_ss':
            colors[i] = '#b0c4de'
        elif df.iloc[i].type == 'act_om':
            colors[i] = '#bc8f8f'
    return colors


def extract_type(df, type):
    # 过滤相应类型的活动，并调整显示的活动名
    ''' args
    df: 目标dataframe
    type: 需要过滤的活动类型(支持act_ss, act_om, main)

    return
    df_part(type: dataframe): 处理后的dataframe
    '''
    q = f"type == '{type}'"
    df_part = df.query(q)
    if type == 'act_ss' or type == 'act_om':
        for i in range(len(df_part)): # 增加换行
            act = df_part.iloc[i].sname
            if len(act) > 5:
                df_part.iat[i, 1] = f'{act[:4]}<br>{act[4:]}'
    elif type == 'main':
        for i in range(len(df_part)): # 增加换行，表示章节
            act = df_part.iloc[i].sname
            df_part.iat[i, 1] = f'EP{int(act[0:2]):02}<br>{act[3:]}'
    else:
        print(f'不支持的剧情类型: {type}')
    return df_part


def plot_h(df):
    # 水平柱状图，用于汇总表示
    ''' args
    df: 目标dataframe

    return
    fig(type: Figure): 生成的柱状图
    '''
    colors = _set_color(df)
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


def plot_v(df):
    # 垂直柱状图，用于分类表示
    ''' args
    df: 目标dataframe

    return
    fig(type: Figure): 生成的柱状图
    '''
    colors = _set_color(df)
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
    return fig

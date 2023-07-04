import plotly.graph_objects as go
import numpy as np
import pandas as pd
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
        elif df.iloc[i].type == 'pred':
            colors[i] = '#ff6666'
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


def plot_h(df, show=True):
    # 水平柱状图，用于汇总表示
    ''' args
    df: 目标dataframe
    show: 是否在浏览器中显示生成图片

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
    fig.update_layout(autosize=True, height=(len(df)-4)*60, width=2000) # 设置图片大小
    fig.update_yaxes(autorange="reversed") # 设置y轴反转
    if show:
        fig.show()
    return fig


def plot_v(df, show=True):
    # 垂直柱状图，用于分类表示
    ''' args
    df: 目标dataframe
    show: 是否在浏览器中显示生成图片

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
    fig.update_layout(autosize=True, width=(len(df)*120), height=1200) # 设置图片大小
    if show:
        fig.show()
    return fig


def _solve_df_for_table(df, focus_act):
    # 处理在表格中显示的数据
    df_main = df[["sname", "charnum", 'time', 'type']]
    df_main.sort_values(by='charnum', ascending=False, inplace=True)
    df_main.reset_index(drop=True, inplace=True)
    df_main.drop(index=df_main[df_main['charnum']==0].index, inplace=True)
    actnum = len(df_main)

    for i in range(len(df_main)):
        if df_main.iloc[i].type == 'main':
            act = df_main.iloc[i].sname
            df_main.iat[i, 0] = f'EP{int(act[0:2]):02}_{act[3:]}'

    df_print = df_main.drop(columns='type', inplace=False)
    text = list(map(lambda x: f'{x/10000:.02f}万', df_print['charnum'].values))
    df_print['charnum'] = text
    df_print = df_print.set_axis(['活动', '字数', '时间'], axis='columns')
    df_print.insert(0, '@x叉X叉x', list(range(1, len(df_print)+1)))

    # n<=5 [1, 10]
    # 6<=n<=15 [1, n+5]
    # n>=16 [1, 5]∪[n-5, n+5]
    focus_item = df_print[df_print['活动']==focus_act]
    assert len(focus_item) == 1, (f'不存在的活动名: {focus_act}')
    fidx = focus_item['@x叉X叉x'].values[0]
    df_print.loc[fidx-1] = df_print.loc[fidx-1].map(lambda x: f'<b>{x}</b>')
    add_print = pd.DataFrame([['...','...','...','...']], columns=df_print.columns)
    if fidx <= 5:
        df_main = df_main[0:10]
        add_main = pd.DataFrame([['...','...','...',df_main.tail(1).type.values[0]]], columns=df_main.columns)
        df_main = pd.concat([df_main, add_main])
        df_print = df_print[0:10]
        df_print = pd.concat([df_print, add_print])
    elif fidx <= 15:
        df_main = df_main[0:fidx+5]
        add_main = pd.DataFrame([['...','...','...',df_main.tail(1).type.values[0]]], columns=df_main.columns)
        df_main = pd.concat([df_main, add_main])
        df_print = df_print[0:fidx+5]
        df_print = pd.concat([df_print, add_print])
    else:
        add_main = pd.DataFrame([['...','...','...',df_main.loc[5].type]], columns=df_main.columns)
        df_main = pd.concat([df_main[0:5], add_main, df_main[fidx-6:fidx+5]])
        if fidx < actnum-5:
            add_main = pd.DataFrame([['...','...','...',df_main.tail(1).type.values[0]]], columns=df_main.columns)
            df_main = pd.concat([df_main, add_main])
            df_print = pd.concat([df_print[0:5], add_print, df_print[fidx-6:fidx+5], add_print])
        else:
            df_print = pd.concat([df_print[0:5], add_print, df_print[fidx-6:fidx+5]])
    return df_main, df_print


def plot_table(df, focus_act, show=True):
    # 数据表格
    ''' args
    df: 目标dataframe
    focus_act: 当期活动名
    show: 是否在浏览器中显示生成图片

    return
    fig(type: Figure): 生成的表格
    '''
    df_main, df_print = _solve_df_for_table(df, focus_act)
    colors = _set_color(df_main)
    data = [go.Table(
        columnwidth=[10, 20, 10, 10],
        header=dict(
            values=df_print.columns,
            align='center',
            fill_color='grey',
            font=dict(color='white', size=24, family='Microsoft YaHei'),
            height=40
        ),
        cells=dict(
            values=np.array(df_print.values).T,
            align='center',
            fill_color=[colors*4],
            font=dict(color='black', size=24, family='Microsoft YaHei'),
            height=40
        )
    )]

    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, height=((len(df_print)))*40+400, width=1000)
    if show:
        fig.show()
    return fig
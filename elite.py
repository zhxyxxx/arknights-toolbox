import json
import pandas as pd
import numpy as np
import csv
import plotly.graph_objects as go
import datetime
import math

import utils.visualize

def make_df(df, star, anni, color_dict):
    new_df = df.query(f"star == '{star}'")
    new_df = new_df[['char', 'cost', 'time']]
    new_df.sort_values('cost', inplace=True, ascending=False)
    new_df['cost'] = new_df['cost'].map(lambda x: f'{x:.01f}')
    new_df.reset_index(inplace=True, drop=True)
    new_df['id'] = new_df.index.values + 1

    color = [color_dict[star][0]] * len(new_df)
    for i in range(len(new_df)):
        impl_time = new_df.iloc[i].time
        dt = datetime.datetime.strptime(impl_time, '%Y-%m-%d')
        date = datetime.date(dt.year, dt.month, dt.day)
        if anni*10 % 10 == 0: # 周年
            start = datetime.date(int(2019+anni-1), 11, 2)
            end = datetime.date(int(2019+anni), 5, 1)
        else: # 半周年
            start = datetime.date(int(2019+anni-0.5), 5, 2)
            end = datetime.date(int(2019+anni-0.5), 11, 1)
        if not (date < start or date > end):
            color[i] = color_dict[star][1]

    new_df = new_df[['id', 'char', 'cost']]
    return new_df, color


def make_full_df(df_full, star):
    new_df = df_full.query(f"star == {star}")
    new_df = new_df.drop(columns=['star', 'time'])
    new_df.sort_values('cost', inplace=True, ascending=False)
    new_df['cost'] = new_df['cost'].map(lambda x: f'{x:.01f}')
    new_df.reset_index(inplace=True, drop=True)
    return new_df


def plot_final_table(df, colors):
    if len(df) % 4 != 0:
        mod = 4 - len(df) % 4
        df_append = pd.DataFrame([['', '', ''] for _ in range(mod)], index=list(range(len(df), len(df)+mod)), columns=df.columns)
        df = pd.concat([df, df_append])
        colors.extend(['#ffffff' for _ in range(mod)])
    row = math.ceil(len(df) / 4)
    np_df = np.array(df.values)
    for i in range(0, len(df), row):
        row_color = np.repeat(np.array(colors[i:i+row]), 3).reshape(-1, 3)
        row_color[:, 0] = np.vectorize(lambda x: '#fffaf0' if x != '#ffffff' else '#ffffff')(row_color[:, 0])
        row_color[:, 2] = np.vectorize(lambda x: '#dcdcdc' if x != '#ffffff' else '#ffffff')(row_color[:, 2])
        if i == 0:
            df_result = np_df[i:i+row].T
            color_result = row_color
        else:
            df_result = np.append(df_result, np_df[i:i+row].T, axis=0)
            color_result = np.append(color_result, row_color, axis=1)
    color_result = color_result.T

    data = [go.Table(
        columnwidth=[2, 6, 4] * 4,
        header=dict(fill_color='#ffffff'),
        cells=dict(
            values=df_result,
            align='center',
            fill_color=color_result,
            font=dict(color='black', size=24, family='Microsoft YaHei'),
            height=40
        )
    )]

    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, height=(math.ceil(len(df)/4))*40+400, width=1500)
    return fig


def plot_full_table(df, color):
    data = [go.Table(
        columnwidth=[5, 5, 2, 5, 2, 5, 2, 5, 2, 5],
        header=dict(
            values=['', '精英一', '', '', '', '精英二', '', '', '', ''],
            align='left',
            line_color=['white', '#afeeee', '#afeeee', '#afeeee', '#afeeee', '#98fb98', '#98fb98', '#98fb98', '#98fb98', 'white'],
            fill_color=['white', '#afeeee', '#afeeee', '#afeeee', '#afeeee', '#98fb98', '#98fb98', '#98fb98', '#98fb98', 'white'],
            font=dict(color='black', size=24, family='Microsoft YaHei'),
            height=40
        ),
        cells=dict(
            values=df.T,
            align='center',
            fill_color=[color, '#e6e6fa', '#f0f8ff', '#e6e6fa', '#f0f8ff', '#e6e6fa', '#f0f8ff', '#e6e6fa', '#f0f8ff', '#dcdcdc'],
            font=dict(color='black', size=24, family='Microsoft YaHei'),
            height=40
        )
    )]

    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, height=(math.ceil(len(df)))*40+400, width=1500)
    return fig


color_dict = {6: ['#f5c193', '#ff8c00'],
              5: ['#f0e68c', '#ffd700'],
              4: ['#d8bfd8', '#ee82ee']}

with open('./resource/item_value_table.json', encoding='utf-8') as f:
    jdic = json.load(f)

item_dic = {}
for item in jdic:
    item_dic[item['name']] = item['apValue']

char_dic = {}
with open("./data/elite_data/elite_data.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'char':
            continue
        cost = item_dic[row[2]] * int(row[3]) + item_dic[row[4]] * int(row[5]) + item_dic[row[6]] * int(row[7]) + item_dic[row[8]] * int(row[9])
        char_dic[row[0]] = {'star': row[1], 'cost': cost, 'time':row[10]}

df = pd.DataFrame(char_dic).T
df['char'] = df.index.values
df.reset_index(inplace=True, drop=True)

df_full = pd.read_csv("./data/elite_data/elite_data.csv")
df_full = df_full.assign(cost=df['cost'])

df_6, color_6 = make_df(df, 6, 5.5, color_dict)
df_5, color_5 = make_df(df, 5, 5.5, color_dict)
df_4, color_4 = make_df(df, 4, 5, color_dict)
fig_table_6 = plot_final_table(df_6, color_6)
fig_table_6.write_image('./data/elite_data/table_6.png', engine="kaleido")
fig_table_5 = plot_final_table(df_5, color_5)
fig_table_5.write_image('./data/elite_data/table_5.png', engine="kaleido")
fig_table_4 = plot_final_table(df_4, color_4)
fig_table_4.write_image('./data/elite_data/table_4.png', engine="kaleido")
utils.visualize.crop_img('./data/elite_data/table_6.png')
utils.visualize.crop_img('./data/elite_data/table_5.png')
utils.visualize.crop_img('./data/elite_data/table_4.png')

df_full_6 = make_full_df(df_full, 6)
df_full_5 = make_full_df(df_full, 5)
df_full_4 = make_full_df(df_full, 4)
fig_table_6 = plot_full_table(df_full_6, color_dict[6][0])
fig_table_6.write_image('./data/elite_data/table_6_full.png', engine="kaleido")
fig_table_5 = plot_full_table(df_full_5, color_dict[5][0])
fig_table_5.write_image('./data/elite_data/table_5_full.png', engine="kaleido")
fig_table_4 = plot_full_table(df_full_4, color_dict[4][0])
fig_table_4.write_image('./data/elite_data/table_4_full.png', engine="kaleido")
utils.visualize.crop_img('./data/elite_data/table_6_full.png')
utils.visualize.crop_img('./data/elite_data/table_5_full.png')
utils.visualize.crop_img('./data/elite_data/table_4_full.png')

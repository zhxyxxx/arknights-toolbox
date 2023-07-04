from utils import visualize
import pandas as pd

actname = '空想花庭'
acttype = 'act_ss'
show = False

df = pd.read_csv('data/event.csv')
# df = pd.read_csv('data/ja/event_jp.csv')

fig = visualize.plot_h(df, show) # 全部活动

df_part = visualize.extract_type(df, acttype)
fig_part = visualize.plot_v(df_part, show)

fig_table = visualize.plot_table(df, actname, show)

fig.write_image('full.png', engine='kaleido')
fig_part.write_image(f'{acttype}.png', engine='kaleido')
fig_table.write_image('table.png', engine='kaleido')


# df_ss = visualize.extract_type(df, 'act_ss')
# df_om = visualize.extract_type(df, 'act_om')
# df_main = visualize.extract_type(df, 'main')

# fig_main = visualize.plot_v(df_main, show) # main
# fig_ss = visualize.plot_v(df_ss, show) # sidestory
# fig_om = visualize.plot_v(df_om, show) # omnibus

# fig_main.write_image('main.png', engine="kaleido")
# fig_ss.write_image('act_ss.png', engine="kaleido")
# fig_om.write_image('act_om.png', engine="kaleido")

from utils import visualize
import pandas as pd

df = pd.read_csv('data/event.csv')

fig = visualize.plot_h(df) # 全部活动

df_ss = visualize.extract_type(df, 'act_ss')
df_om = visualize.extract_type(df, 'act_om')
df_main = visualize.extract_type(df, 'main')

fig_main = visualize.plot_v(df_main) # main
fig_ss = visualize.plot_v(df_ss) # sidestory
fig_om = visualize.plot_v(df_om) # omnibus

# 保存图片
# import io
# from PIL import Image
# _im = fig.to_image(format="png", engine="kaleido", height=(len(df)-4)*100, width=2680, scale=2)
# _im = Image.open(io.BytesIO(_im))
# _im.save('./data/1.png')

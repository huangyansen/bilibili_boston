# 生成情感分析饼状图 
# 先输出排序，再将结果填入饼状图中
import pandas as pd
from itertools import groupby
from pyecharts import options as opts
from pyecharts.charts import Pie
#from pyecharts.faker import Faker

data = pd.read_excel(r"F:\\bili\\out\\bili_b.xlsx")
print(data.情感评分.values)

# 以10为间隔，自动分组并统计各组个数
subs,counts = [],[]
for k, g in groupby(sorted(data.情感评分.values), key=lambda x: x//10):
    #print('{}-{}: {}'.format(k*10, (k+1)*10-1, len(list(g))))
    subs.append(str(k*10) +'~'+ str((k+1)*10-1))
    counts.append(len(list(g)))

#data.情感评分.value_counts().sort_index(ascending=False) #得到大致分布

c2 = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(subs, counts)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="情感评分分布"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("F:\\bili\\out\\bzt.html")
)




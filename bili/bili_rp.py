# 生成热评网页
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

data = pd.read_excel(r"F:\\bili\\out\\bili_b.xlsx")
df1 = data.sort_values(by="点赞",ascending=False).head(20)

c1 = ( #c1 动态柱状图
    Bar()
    .add_xaxis(df1["评论"].tolist())
    .add_yaxis("点赞数", df1["点赞"].tolist(), color=Faker.rand_color())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="评论热度Top20"),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
    )
    #.render_notebook()
    .render("F:\\bili\\out\\rp.html")
)
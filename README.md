# bilibili_boston
基于哔哩哔哩平台，课程评价数据的情感分析


运行说明 :
    0. bili_txt.py为测试文件
    
    一: 生成源数据文件
        1. 运行bili_snow.py 生成带有用户名、评论、情感评分和点赞数的表格文件,存在out下的bili_s.xlsx  (5000条评论3分钟左右)
        1. 同上，或者运行用Boston情感分析工具做的xlsx，存在out下的bili_b.xlsx (5000条评论10分钟左右)
    
    二: 分析数据，可视化
        2. 再运行bili_rp.py 生成热评网页文件，存在out下的rp.html

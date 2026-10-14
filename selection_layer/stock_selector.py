import pandas as pd
from sqlalchemy import create_engine

import sys
import os

# 添加项目根目录
sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from strategy_layer.short_strategy import short_score


# 数据库路径

engine = create_engine(
    "sqlite:///C:/Users/14820/Desktop/量化分析/database/stock.db"
)


# 获取所有股票表名

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    engine
)


results = []


# 遍历股票

for table in tables["name"]:

    # 跳过实时行情表
    if table == "stock_price":
        continue

    try:

        data = pd.read_sql(
            table,
            engine
        )


        # 数据太少跳过
        if len(data) < 10:
            continue


        score = short_score(data)


        results.append(
            {
                "股票": table,
                "评分": score
            }
        )


    except Exception as e:
        print("错误:", table, e)



# 转成DataFrame

result_df = pd.DataFrame(results)


# 排序

result_df = result_df.sort_values(
    by="评分",
    ascending=False
)


print("===== 短线候选股票 =====")

print(
    result_df.head(20)
)
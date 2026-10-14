import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import time


# 数据库

engine = create_engine(
    "sqlite:///C:/Users/14820/Desktop/量化分析/database/stock.db"
)


# 获取股票列表

stocks = pd.read_sql(
    "stock_price",
    engine
)

print("股票数量:", len(stocks))


print("股票数量:", len(stocks))


success = 0


for index, row in stocks.iterrows():

    code = row["代码"]

    try:

        print(
            f"正在下载 {index+1}/{len(stocks)} : {code}"
        )


        # 获取历史K线

        data = ak.stock_zh_a_daily(
            symbol=code,
            adjust="qfq"
        )


        if len(data) < 100:
            continue


        # 保存表名

        table_name = "kline_" + code


        data.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )


        success += 1


        # 防止请求过快

        time.sleep(0.2)


    except Exception as e:

        print(
            code,
            "失败"
        )

        continue



print("================")
print("完成")
print("成功保存:", success)
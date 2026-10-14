import pandas as pd
from sqlalchemy import create_engine
import sys
import os


# =========================
# 添加项目路径
# =========================

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)


from strategy_layer.short_strategy import short_score



# =========================
# 数据库
# =========================

engine = create_engine(
    "sqlite:///C:/Users/14820/Desktop/量化分析/database/stock.db"
)



# =========================
# 参数
# =========================

initial_money = 10000

money = initial_money

hold_days = 5

min_score = 80



trades = []



# =========================
# 获取股票列表
# =========================

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    engine
)


stock_tables = list(
    tables["name"]
)


print(
    "股票数量:",
    len(stock_tables)
)



count = 0



# =========================
# 开始扫描
# =========================

example=stock_tables[:20]

for stock in example:


    count += 1


    print(
        f"正在回测 {count}/{len(example)} : {stock}"
    )


    try:


        data = pd.read_sql(
            stock,
            engine
        )


        if len(data) < 100:
            continue



        # 日期排序

        if "date" in data.columns:

            data["date"] = pd.to_datetime(
                data["date"]
            )

            data = data.sort_values(
                "date"
            )


        data = data.reset_index(
            drop=True
        )



        i = 30


        while i < len(data)-hold_days:



            # 只使用过去数据
            history = data.iloc[:i]


            score = short_score(
                history
            )


            if score >= min_score:


                buy_price = data.iloc[i]["close"]

                sell_price = data.iloc[
                    i + hold_days
                ]["close"]



                profit = (
                    sell_price /
                    buy_price
                    - 1
                )


                money *= (
                    1 + profit
                )


                trades.append(
                    {

                    "股票":stock,

                    "日期":
                    data.iloc[i]["date"]
                    if "date" in data.columns
                    else i,


                    "评分":
                    score,


                    "收益":
                    round(
                        profit*100,
                        2
                    )

                    }
                )


                i += hold_days


            else:

                i += 1



    except Exception as e:

        continue




# =========================
# 输出
# =========================


print("====================")

print(
    "回测完成"
)


print(
    "初始资金:",
    initial_money
)


print(
    "最终资金:",
    round(
        money,
        2
    )
)


print(
    "累计收益:",
    round(
        (money/initial_money-1)*100,
        2
    ),
    "%"
)


print(
    "交易次数:",
    len(trades)
)



if len(trades)>0:


    win = len(
        [
            t for t in trades
            if t["收益"] > 0
        ]
    )


    print(
        "胜率:",
        round(
            win /
            len(trades)
            *100,
            2
        ),
        "%"
    )



    print(
        "最近10笔交易:"
    )


    for t in trades[-10:]:

        print(t)


else:

    print(
        "没有交易"
    )
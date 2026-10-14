import pandas as pd
from sqlalchemy import create_engine
import sys
import os


# 添加项目根目录

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
# 回测参数
# =========================

stock = "kline_sz300866"

hold_days = 5

initial_money = 10000



# =========================
# 读取数据
# =========================

data = pd.read_sql(
    stock,
    engine
)



# 时间排序

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



# =========================
# 开始回测
# =========================

money = initial_money

trades = []



i = 30


while i < len(data)-hold_days:


    history = data.iloc[:i]


    score = short_score(
        history
    )


    # 买入条件

    if score >= 80:


        buy_price = data.iloc[i]["close"]


        sell_price = data.iloc[
            i + hold_days
        ]["close"]


        profit = (
            sell_price /
            buy_price
            - 1
        )


        money = money * (
            1 + profit
        )


        trades.append(
            {
                "买入日期": data.iloc[i]["date"]
                if "date" in data.columns else i,

                "买入价格": buy_price,

                "卖出价格": sell_price,

                "收益": round(
                    profit * 100,
                    2
                ),

                "评分": score
            }
        )


        i += hold_days


    else:

        i += 1



# =========================
# 输出结果
# =========================


print("===================")

print(
    "股票:",
    stock
)


print(
    "初始资金:",
    initial_money
)


print(
    "最终资金:",
    round(money,2)
)


print(
    "累计收益:",
    round(
        (money / initial_money - 1)*100,
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
            x for x in trades
            if x["收益"] > 0
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
        "最近交易:"
    )


    for t in trades[-10:]:

        print(t)

else:

    print(
        "没有符合条件的交易"
    )
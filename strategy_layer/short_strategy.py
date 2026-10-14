import pandas as pd
import numpy as np


def short_score(data):

    score = 0


    # =========================
    # 基础数据检查
    # =========================

    if len(data) < 30:
        return 0


    close = data["close"]
    volume = data["volume"]

    today = data.iloc[-1]


    # 防止空值
    if pd.isna(today["close"]):
        return 0


    # =========================
    # 1. 五日涨幅
    # =========================

    pct_5 = (
        today["close"] /
        data.iloc[-6]["close"]
        - 1
    )


    # 健康上涨
    if 0.03 <= pct_5 <= 0.12:
        score += 15

    # 强势上涨
    elif 0.12 < pct_5 <= 0.20:
        score += 10

    # 涨太多，避免追高
    elif pct_5 > 0.20:
        score -= 10



    # =========================
    # 2. 均线趋势
    # =========================


    ma5 = close.tail(5).mean()
    ma10 = close.tail(10).mean()
    ma20 = close.tail(20).mean()



    # 多头排列
    if ma5 > ma10 > ma20:
        score += 15



    # 当前价格距离20日线

    bias = (
        today["close"] /
        ma20
        - 1
    )


    # 健康上涨
    if 0 < bias < 0.10:
        score += 10


    # 偏离太远
    elif bias > 0.20:
        score -= 10




    # =========================
    # 3. 回踩买点
    # =========================


    high_10 = close.tail(10).max()


    if high_10 != 0:

        drawdown = (
            today["close"] /
            high_10
            - 1
        )


        # 上涨后的正常回踩
        if -0.08 < drawdown < -0.02:
            score += 10


        # 跌太多
        elif drawdown < -0.15:
            score -= 10




    # =========================
    # 4. 成交量
    # =========================


    vol20 = volume.tail(20).mean()


    if vol20 != 0:

        vol_ratio = (
            today["volume"] /
            vol20
        )


        # 温和放量
        if 1.3 <= vol_ratio <= 2.5:
            score += 20


        # 巨量风险
        elif vol_ratio > 4:
            score -= 15




    # =========================
    # 5. K线强度
    # =========================


    high = today["high"]
    low = today["low"]
    close_price = today["close"]


    if high != low:


        strength = (
            close_price - low
        ) / (
            high - low
        )


        # 收盘靠近最高
        if strength > 0.75:
            score += 15


        elif strength < 0.25:
            score -= 5




    # =========================
    # 6. RSI
    # =========================


    delta = close.diff()


    gain = delta.where(
        delta > 0,
        0
    )


    loss = -delta.where(
        delta < 0,
        0
    )


    avg_gain = gain.tail(14).mean()

    avg_loss = loss.tail(14).mean()



    if avg_loss != 0:


        rs = (
            avg_gain /
            avg_loss
        )


        rsi = (
            100 -
            100 /
            (1 + rs)
        )


        # 正常强势区
        if 45 < rsi < 70:
            score += 10


        # 超买
        elif rsi > 80:
            score -= 10




    # =========================
    # 最终限制
    # =========================


    score = int(score)


    if score < 0:
        score = 0


    if score > 90:
        score = 90


    return score
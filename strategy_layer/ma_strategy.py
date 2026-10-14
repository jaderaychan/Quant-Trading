import pandas as pd
from sqlalchemy import create_engine

# 连接数据库
engine = create_engine("sqlite:///stock.db")

# 读取K线数据
data = pd.read_sql("kline_300368", engine)

# 按日期排序
data = data.sort_values("date")

# 计算20日均线
data["MA20"] = data["close"].rolling(20).mean()

#计算20日均量
data["VOL20"] = data["volume"].rolling(20).mean()

# 判断趋势
data["signal"] = (
    (data["close"] > data["MA20"]) &
    (data["volume"] > data["VOL20"])
)

print(data.tail(10))
import akshare as ak
from sqlalchemy import create_engine

# 创建数据库连接
engine = create_engine("sqlite:///stock.db")

# 获取一只股票历史K线
data = ak.stock_zh_a_daily(
    symbol="sz300368",
    adjust="qfq"
)

print(data.head())

# 保存到数据库
data.to_sql(
    "kline_300368",
    engine,
    if_exists="replace",
    index=False
)

print("K线保存完成")
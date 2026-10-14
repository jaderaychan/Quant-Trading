import os

os.environ["NO_PROXY"] = "*"

import akshare as ak
from sqlalchemy import create_engine

import akshare as ak
from sqlalchemy import create_engine

# 创建数据库
engine = create_engine("sqlite:///stock.db")

# 获取行情
data = ak.stock_zh_a_spot()

# 保存到数据库
data.to_sql("stock_price", engine, if_exists="replace", index=False)

print("行情保存完成")
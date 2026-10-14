import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///stock.db")

data = pd.read_sql("stock_price", engine)

print(data.head())
print("股票数量:", len(data))
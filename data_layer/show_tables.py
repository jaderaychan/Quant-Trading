from sqlalchemy import create_engine
import pandas as pd


engine = create_engine(
    "sqlite:///C:/Users/14820/Desktop/量化分析/database/stock.db"
)


tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    engine
)


print(tables)
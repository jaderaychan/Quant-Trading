import akshare as ak
import time

print("正在获取A股数据...")

start = time.time()

data = ak.stock_zh_a_spot_em()
data.to_csv("stock_data.csv", index=False)

end = time.time()

print("获取完成，用时：", round(end-start,2), "秒")

print(data.head())
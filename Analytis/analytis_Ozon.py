import requests
import pandas as pd

# 分析报告-分析数据
# Ozon API 信息
client_id = "494570"
api_key = "e9df976b-2636-41cc-8348-12bd786c22d4"
ozon_api_url = "https://api-seller.ozon.ru/v1/analytics/data"

# 配置 Ozon API 请求头
ozon_headers = {
    "Client-Id": client_id,
    "Api-Key": api_key,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

data = {
    "date_from": "2025-04-30",
    "date_to": "2025-05-06",
    "metrics": [
        "revenue"
    ],
    "dimension": [
        "sku",
        "day"
    ],
    "filters": [],
    "sort": [
        {
            "key": "revenue",
            "order": "DESC"
        }
    ],
    "limit": 1000,
    "offset": 0
}

response = requests.post(ozon_api_url, headers=ozon_headers, json=data)
response.raise_for_status()
result = response.json()
print(result)
print(result['result']['data'])
objs = result['result']['data']
each_times = []
each_revs = []
for obj in objs:
    # each_time = result['result']['data'][0]['dimensions'][1]['id']
    # print(obj)
    each_time = obj['dimensions'][1]['id']
    each_times.append(each_time)
    print('销售时间：', each_time)
    each_rev = obj['metrics'][0]
    each_revs.append(each_rev)
    print('销售额：', each_rev)
print(each_times)
print(each_revs)

# 创建 DataFrame
data = {
    '日期': each_times,
    '销售额': each_revs
}
df = pd.DataFrame(data)
print(df)

# 保存为 Excel 文件
try:
    df.to_excel('Ozon卖家销售额.xlsx', index=True)
    print("Ozon卖家销售额.xlsx")
except Exception as e:
    print(f"保存文件时出现错误: {e}")


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
        "ordered_units"
    ],
    "dimension": [
        "sku",
        "day"
    ],
    "filters": [],
    "sort": [
        {
            "key": "ordered_units",
            "order":"DESC"
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
each_amts = []
for obj in objs:
    each_time = obj['dimensions'][1]['id']
    each_times.append(each_time)
    print('销售时间：', each_time)
    each_rev = obj['metrics'][0]
    each_amts.append(each_rev)
    print('销售数量：', each_amts)
print(each_times)
print(each_amts)

# 创建 DataFrame
data = {
    '日期': each_times,
    '销售数量': each_amts
}
df_01 = pd.DataFrame(data)
print(df_01)

data_list = {
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
            "order":"DESC"
        }
    ],
    "limit": 1000,
    "offset": 0
}

response = requests.post(ozon_api_url, headers=ozon_headers, json=data_list)
response.raise_for_status()
result = response.json()
print(result)
print(result['result']['data'])
objs = result['result']['data']
each_times = []
each_revs = []
for obj in objs:
    print(obj)
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
df_02 = pd.DataFrame(data)
print(df_02)

# 合并两个 DataFrame
merged_df = pd.merge(df_01, df_02, on='日期', how='outer')
print("合并表格", merged_df)

# 将销量、销售额进行合并加总
# 按日期分组并求和
grouped_df = merged_df.groupby('日期').sum().reset_index()
print(grouped_df)
print("按日期分组求和", grouped_df)

# 保存合并且加总后的数据到 Excel 文件
try:
    grouped_df.to_excel('Ozon销售额分析2版.xlsx', index=False)
    print("合并且加总后的数据已成功保存到 'Ozon销售额分析2版.xlsx'")
except Exception as e:
    print(f"保存文件时出现错误: {e}")
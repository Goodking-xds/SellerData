import json
import requests
import pandas as pd

# Ozon表格与飞书自动化的结合
app_id = "cli_a88b77b97959100b"
app_secret = "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme"
name = "Ozon和WB电商运营API数据"

# 1、获取机器人的access_token
def get_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    req = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    request_content = json.dumps(req)
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    response = requests.request("POST", url, headers=headers, data=request_content)
    print(response.text)
    token = response.json()["tenant_access_token"]
    print("token的值：", token)
    return token

tenant_access_token = get_access_token("cli_a88b77b97959100b","cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme")

# # 2、创建一个多维表格 Ozon销售额数据（飞书自动化版）
def create_table(tenant_access_token):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    req = {
        "name":"Ozon销售额数据（飞书自动化版）",
        "folder_token":"PZayf4IUqlGyiKd4fH7cZKbRnIb"
    }
    request_content = json.dumps(req)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization":"Bearer u-eTAXffhP9c0aILYKjz7au5h0gH2wl0EpqW0040u800mE".format(access_token)
    }
    response = requests.request("POST", url, headers=headers, data=request_content)
    print(response.text)

create_table(teaccess_token)

# 3、新增一个数据表
def create_data_table(tenant_access_token):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/UdzVbOLiCajoWosh4T8cAYEanfe/tables"
    headers = {
        "Authorization": "Bearer u-eTAXffhP9c0aILYKjz7au5h0gH2wl0EpqW0040u800mE".format(tenant_access_token),
        "Content-Type": "application/json; charset=utf-8"
    }
    req = {
        "table": {
            "name": "Ozon销售额",
            "default_view_name": "默认的表格视图",
            "fields": [
                {
                    "field_name": "日期",
                    "type": 5
                },
                {
                    "field_name": "销售数量",
                    "type": 2
                },
                {
                    "field_name": "销售额",
                    "type": 2
                }]
        }
    }
    payload = json.dumps(req)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("新增数据表：", response.text)

create_data_table(tenant_access_token)

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

# 4、新增多条记录
def create_record(tenant_access_token, app_token, table_id):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"

    headers = {
            "Content-Type": "application/json;",
            "Authorization": "Bearer u-e6olx6_19168xexoi4F9gH5k5Qy0l00VOy00lhqy2BOU".format(tenant_access_token)
        }

    records = {
        "records": [
        {
            "fields": {
                "日期": 1745942400000,
                "销售额": 861327,
                "销售数量":171
            }
        },
        {
            "fields": {
                "日期": 1746028800000,
                "销售额": 32984,
                "销售数量":56
            }
        },
        {
            "fields": {
                "日期": 1746115200000,
                "销售额": 771064,
                "销售数量": 224
            }
        },
        {
            "fields": {
                "日期": 1746201600000,
                "销售额": 77440,
                "销售数量": 110
            }
        },
        {
            "fields": {
                "日期": 1746288000000,
                "销售额": 33573,
                "销售数量": 57
            }
        },
        {
            "fields": {
                "日期": 1746374400000,
                "销售额": 34776,
                "销售数量": 46
            }
        },
        {
            "fields": {
                "日期": 1746460800000,
                "销售额": 60,
                "销售数量": 45360
            }
        }
    ]}
    # 遍历数组元素，为每个元素组合创建一条记录
    print(records)
    response = requests.request("POST", url, headers=headers, json=records)
    print("新增数据表：", response.text)
    return response

create_record(tenant_access_token,"UdzVbOLiCajoWosh4T8cAYEanfe", "tblE46mBICKjeXWW")

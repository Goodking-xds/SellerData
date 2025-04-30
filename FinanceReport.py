import requests
import pandas as pd

# 关于卖家交易清单
# Ozon API 信息
client_id = "494570"
api_key = "e9df976b-2636-41cc-8348-12bd786c22d4"
ozon_api_url = "https://api-seller.ozon.ru/v3/finance/transaction/list"

# 配置 Ozon API 请求头
ozon_headers = {
    "Client-Id": client_id,
    "Api-Key": api_key,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

data = {
    "filter":{
        "date": {
            "from": "2025-04-01T00:00:00.000Z",
            "to": "2025-04-29T00:00:00.000Z"
        },
    },
    "page":1,
    "page_size":1000
}

response = requests.post(ozon_api_url, headers=ozon_headers, json=data)
response.raise_for_status()
result = response.json()
# 解析JSON数据
# 提取operations信息
operations = result["result"]['operations']

for operation in operations:
    operation_id = operation['operation_id']
    operation_type = operation['operation_type']
    operation_date = operation['operation_date']
    operations_date = operation['operation_date']
    operation_type_name = operation['operation_type_name']
    delivery_charge = operation['delivery_charge']
    return_delivery_charge = operation['return_delivery_charge']
    accruals_for_sale = operation['accruals_for_sale']
    sale_commission = operation['sale_commission']
    amount = operation['amount']
    type = operation['type']
    print("操作ID：",operation_id)
    print("操作类型：",operation_type)
    print("操作类型名称",operation_type_name)
    print("操作类型日期",operation_date)
    print("运费：",delivery_charge)
    print("退货和取消订单费用适用于2021年2月1日之前有效的费率，以及超大商品的费用：",return_delivery_charge)
    print("退货和取消订单费用适用于2021年2月1日之前有效的费率，以及超大商品的费用：",return_delivery_charge)
    print("考虑到买家折扣的商品成本：",accruals_for_sale)
    print("销售提成或销售提成返还：",sale_commission)
    print("交易总额:",amount)
    print("收费类型：",type)

# 用于存储每行数据的列表
data_list = []

for operation in operations:
    operation_id = operation['operation_id']
    operation_type = operation['operation_type']
    operation_date = operation['operation_date']
    operation_type_name = operation['operation_type_name']
    delivery_charge = operation['delivery_charge']
    return_delivery_charge = operation['return_delivery_charge']
    accruals_for_sale = operation['accruals_for_sale']
    sale_commission = operation['sale_commission']
    amount = operation['amount']
    type_ = operation['type']

    # 将每个操作的数据作为一个字典添加到列表中
    row = {
        "操作ID": operation_id,
        "操作类型": operation_type,
        "操作类型名称": operation_type_name,
        "操作类型日期": operation_date,
        "运费": delivery_charge,
        "退货和取消订单费用适用于2021年2月1日之前有效的费率，以及超大商品的费用": return_delivery_charge,
        "考虑到买家折扣的商品成本": accruals_for_sale,
        "销售提成或销售提成返还": sale_commission,
        "交易总额": amount,
        "收费类型": type_
    }
    data_list.append(row)

# 将列表转换为 DataFrame
df = pd.DataFrame(data_list)

# 将 DataFrame 保存到 Excel 文件
df.to_excel('operations.xlsx', index=False)

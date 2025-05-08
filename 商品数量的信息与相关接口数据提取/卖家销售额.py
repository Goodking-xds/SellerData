import requests

# 关于卖家交易清单
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
        "date_from": "2024-04-30",
        "date_to": "2025-04-30",
        "metrics": [
            "hits_view_search"
        ],
        "dimension": [
            "sku",
            "day"
        ],
        "filters": [],
        "sort": [
            {
                "key": "ordered_items_reserved_price",
                "order": "DESC"
            }
        ],
        "limit": 1000,
        "offset": 0
    }

response = requests.post(ozon_api_url, headers=ozon_headers, json=data)
response.raise_for_status()
result = response.json()
# print(result['result']['data'])
infos = result['result']['data']
print(infos)


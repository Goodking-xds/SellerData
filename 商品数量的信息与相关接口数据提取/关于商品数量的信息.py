import requests

# 关于商品数量的信息
# Ozon API 信息
client_id = "494570"
api_key = "e9df976b-2636-41cc-8348-12bd786c22d4"
ozon_api_url = "https://api-seller.ozon.ru/v4/product/info/stocks"

# 配置 Ozon API 请求头
ozon_headers = {
    "Client-Id": client_id,
    "Api-Key": api_key,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json"
}

data = {
        "filter": {
            "visibility": "ALL",
        },
        "limit": 10
    }

response = requests.post(ozon_api_url, headers=ozon_headers, json=data)
response.raise_for_status()
result = response.json()
print(result)
print(result['items'][0])
# print(result['items'][0]['product_id'])

skus = []
product_ids = []
offer_ids = []
for item in result['items']:
    for stock in item['stocks']:
        print('product_id:', item['product_id'])
        product_ids.append(item['product_id'])
        print('offer_id:', item['offer_id'])
        offer_ids.append(item['offer_id'])
        print('sku:', stock["sku"])
        skus.append(stock["sku"])
print("skus:",skus)
print("product_ids:",product_ids)
print("offer_ids:",offer_ids)


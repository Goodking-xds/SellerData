# 获取订单数量
import requests

# WB API 地址，这里假设的创建订单备注接口地址
url = "https://statistics-api.wildberries.ru/api/v1/supplier/incomes"
# 从 WB 平台获取到的认证 Token，需替换为真实有效的值
token = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MDY0ODg2MywiaWQiOiIwMTk2NDMwMS0wYTEyLTc4YTktOTk3ZS01NWRlZTdmZDU0MzAiLCJpaWQiOjQ3MjkwMTcxLCJvaWQiOjIwNDc3MiwicyI6NzkzNCwic2lkIjoiYzM5OWYxNGEtNDM2MS00YjdlLTkwZmMtMzc3N2E4ZDdjODExIiwidCI6ZmFsc2UsInVpZCI6NDcyOTAxNzF9.d_R6r9g3Xy1O5nrHZ62QTU3hYRsuR6MkjqFpp6gdG9dVNNqvo4saTkxo4ix4ProlVSr2pMsdDs7dO1JMYjmvcg"

# 构建请求头，包含认证信息和常见的请求头字段
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

params = {
    "dateFrom": "2025-04-01"
}
# 发送 POST 请求创建订单备注
response = requests.get(url, headers=headers, params=params)

# 检查响应状态码
if response.status_code == 200:
    objs = response.json()
    # print(objs)
for obj in objs:
    print(obj)
    # print('销售时间：',obj['date'])
    # print('销售额(总价)：',obj['totalPrice'])
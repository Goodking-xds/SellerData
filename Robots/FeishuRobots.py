# 搭建一个飞书机器人，给机器人发消息后，自动从 ozon 拉取数据同步到多维表格，完成后机器人给用户推消息告知的功能。
import requests
import pandas as pd
import json

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

app_id = "cli_a88b77b97959100b"
app_secret = "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme"

# # Ozon表格与飞书自动化的结合
# name = "Ozon和WB电商运营API数据"

lark.APP_ID = "cli_a88b77b97959100b"
lark.APP_SECRET = "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme"

# 注册接收消息事件，处理接收到的消息。
# Register event handler to handle received messages.
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    res_content = ""
    if data.event.message.message_type == "text":
        res_content = json.loads(data.event.message.content)["text"]
    else:
        res_content = "解析消息失败，请发送文本消息\nparse message failed, please send text message"
    content = json.dumps(
        {
            "text": f'正在获取您需要的信息...'
        }
    )
    if data.event.message.chat_type == "p2p":
        request = (
            CreateMessageRequest.builder()
            .receive_id_type("chat_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(data.event.message.chat_id)
                .msg_type("text")
                .content(content)
                .build()
            )
            .build()
        )
        # 使用发送OpenAPI发送消息
        # Use send OpenAPI to send messages
        # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        response = client.im.v1.chat.create(request)
        if not response.success():
            raise Exception(
                f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )
    else:
        request: ReplyMessageRequest = (
            ReplyMessageRequest.builder()
            .message_id(data.event.message.message_id)
            .request_body(
                ReplyMessageRequestBody.builder()
                .content(content)
                .msg_type("text")
                .build()
            )
            .build()
        )
        # 使用回复OpenAPI回复消息
        # Use send OpenAPI to send messages
        # https://open.larkoffice.com/document/server-docs/im-v1/message/reply
        response: ReplyMessageResponse = client.im.v1.message.reply(request)
        if not response.success():
            raise Exception(
                f"client.im.v1.message.reply failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}"
            )
# 注册事件回调
# Register event handler.
event_handler = (
    lark.EventDispatcherHandler.builder("", "")
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)
# 创建 LarkClient 对象，用于请求OpenAPI, 并创建 LarkWSClient 对象，用于使用长连接接收事件。
# Create LarkClient object for requesting OpenAPI, and create LarkWSClient object for receiving events using long connection.
client = lark.Client.builder().app_id(lark.APP_ID).app_secret(lark.APP_SECRET).build()
wsClient = lark.ws.Client(
    lark.APP_ID,
    lark.APP_SECRET,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)
def main():
    #  启动长连接，并注册事件处理器。
    #  Start long connection and register event handler.
    wsClient.start()

main()

# 机器人发送消息
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main_final():
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("open_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id("ou_5ef243dc5f9f04a7dbd0d115c057662d")
            .msg_type("text")
            .content("{\"text\":\"我可以获取Ozon的销售额\"}")
            .build()) \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

main_final()

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


get_access_token(app_id, app_secret)
tenant_access_token = get_access_token("cli_a88b77b97959100b", "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme")


# # 2、创建一个多维表格 Ozon销售额数据（飞书自动化版）
# def create_table(tenant_access_token):
#     url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
#     req = {
#         "name": "Ozon销售额数据（飞书自动化版）",
#         "folder_token": "PZayf4IUqlGyiKd4fH7cZKbRnIb"
#     }
#     request_content = json.dumps(req)
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization": f"Bearer {tenant_access_token}"
#     }
#     response = requests.request("POST", url, headers=headers, data=request_content)
#     print(response.text)
#
#
# create_table(tenant_access_token)


# 3、新增一个数据表
# def create_data_table(tenant_access_token):
#     url = "https://open.feishu.cn/open-apis/bitable/v1/apps/UdzVbOLiCajoWosh4T8cAYEanfe/tables"
#     headers = {
#         "Authorization": f"Bearer {tenant_access_token}",
#         "Content-Type": "application/json; charset=utf-8"
#     }
#     req = {
#         "table": {
#             "name": "Ozon销售额",
#             "default_view_name": "默认的表格视图",
#             "fields": [
#                 {
#                     "field_name": "日期",
#                     "type": 5
#                 },
#                 {
#                     "field_name": "销售数量",
#                     "type": 2
#                 },
#                 {
#                     "field_name": "销售额",
#                     "type": 2
#                 }]
#         }
#     }
#     payload = json.dumps(req)
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print("新增数据表：", response.text)


# create_data_table(tenant_access_token)

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
            "order": "DESC"
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
        "Authorization": f"Bearer {tenant_access_token}"
    }

    records = {
        "records": [
            {
                "fields": {
                    "日期": 1745942400000,
                    "销售额": 861327,
                    "销售数量": 171
                }
            },
            {
                "fields": {
                    "日期": 1746028800000,
                    "销售额": 32984,
                    "销售数量": 56
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
    response = requests.request("POST", url, headers=headers, json=records)
    print("新增数据表记录成功：", response.text)
    return response


create_record(tenant_access_token, "UdzVbOLiCajoWosh4T8cAYEanfe", "tblE46mBICKjeXWW")


# 机器人自动发送信息
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main_final():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id("ou_5ef243dc5f9f04a7dbd0d115c057662d")
                      .msg_type("text")
                      .content("{\"text\":\"Ozon的销售额获取完毕\"}")
                      .build()) \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
main_final()

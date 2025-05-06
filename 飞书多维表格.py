import json
import requests
import openpyxl
# Ozon和WB电商运营API数据Demo测试
app_id = "cli_a88b77b97959100b"
app_secret = "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme"

# 获取机器人的access_token
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

access_token = get_access_token("cli_a88b77b97959100b","cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme")

#获取文件夹元数据 #已废弃
# def create_folder_meta(access_token):
#     url = "https://open.feishu.cn/open-apis/drive/explorer/v2/folder/:PZayf4IUqlGyiKd4fH7cZKbRnIb/meta"
#     req = {
#         "name":"Ozon交易清单与飞书自动化平台",
#         "folder_token":"PZayf4IUqlGyiKd4fH7cZKbRnIb"
#     }
#     request_content = json.dumps(req)
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization":"Bearer t-g10451c7SIITGXCC3S24ZFZPM3JRPZ2PC7OBTXQO".format(access_token)
#     }
#     response = requests.request("POST", url, headers=headers, data=request_content)
#     print(response.text)

# def create_folder(access_token): # 新建文件夹 必须在子文件创建
#     url = "https://open.feishu.cn/open-apis/drive/v1/files/create_folder"
#     req = {
#         "name":"自动化表格",
#         "folder_token":"PZayf4IUqlGyiKd4fH7cZKbRnIb"
#     }
#     request_content = json.dumps(req)
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization":"Bearer t-g10451c7SIITGXCC3S24ZFZPM3JRPZ2PC7OBTXQO".format(access_token)
#     }
#     response = requests.request("POST", url, headers=headers, data=request_content)
#     print(response.text)
# create_folder(access_token)

#创建多维表格 需要文件夹的token 保持鉴权未过期
# def create_table(access_token):
#     url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
#     req = {
#         "name":"Ozon交易清单与飞书自动化平台",
#         "folder_token":"PZayf4IUqlGyiKd4fH7cZKbRnIb"
#     }
#     request_content = json.dumps(req)
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization":"Bearer u-dIpV5_hKZfZUbm1rVsxlqK4gl8gB10EjM0G0hgo0217q".format(access_token)
#     }
#     response = requests.request("POST", url, headers=headers, data=request_content)
#     print(response.text)
#
# create_table(access_token)
#
# def create_table_tab(access_token):
#     url = "https://open.feishu.cn/open-apis/bitable/v1/apps/H7dubhQ4NaB0vDsVoaTcMk6rnpg/tables/table=tblmsLyx4uELVhkE&view=vew1C2SVbF/fields"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization":"Bearer u-fDrOPoYpJ3ObRz0RaPpCArhg7b3x10GrpW0040mw0DGQ".format(access_token)
#     }
#     payload = {
#         "field_name": "操作过程",
#         "type": 1
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print(response.text)
#
# create_table_tab(access_token)
#
# def read_excel(file_path):
#     wb = openpyxl.load_workbook("交易清单汇总记录.xlsx")
#     sheet = wb.active  # 默认读取第一个工作表
#     data = []
#     # 读取表头（第一行）
#     headers = [cell.value for cell in sheet[1]]
#     # 读取数据行（从第二行开始）
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         data.append(dict(zip(headers, row)))
#     return data
# data = read_excel("交易清单汇总记录.xlsx")
# print(data)

# # 新建数据表
# # 新增一个数据表
# def create_data_table(access_token):
#     url = "https://open.feishu.cn/open-apis/bitable/v1/apps/C9HdbVUZiadQCxsRNYpcV7qfnqf/tables"
#     headers = {
#         "Authorization": "Bearer u-dIpV5_hKZfZUbm1rVsxlqK4gl8gB10EjM0G0hgo0217q".format(access_token),
#         "Content-Type": "application/json; charset=utf-8"
#     }
#     req = {
#         "table": {
#             "name": "Ozon平台API自动化",
#             "default_view_name": "默认的表格视图",
#             "fields": [
#                 {
#                     "field_name": "操作ID",
#                     "type": 2
#                 },
#                 {
#                     "field_name": "操作类型",
#                     "type": 1
#                 },
#                 {
#                     "field_name": "操作类型名称",
#                     "type": 2
#                 },
#                 {
#                     "field_name": "操作类型日期",
#                     "type": 5
#                 },
#                 {
#                     "field_name": "运费",
#                     "type": 2
#                 },
#                 {
#                     "field_name": "退货和取消订单费用适用于2021年2月1日之前有效的费率，以及超大商品的费用",
#                     "type" :2
#                 },
#                 {
#                     "field_name":"考虑到买家折扣的商品成本",
#                     "type": 2
#                 },
#                 {
#                     "field_name": "销售提成或销售提成返还",
#                     "type": 2
#                 },
#                 {
#                     "field_name":"交易总额",
#                     "type": 2
#                 },
#                 {
#                     "field_name":"收费类型",
#                     "type": 1
#                 }
#             ]
#         }
#     }
#     payload = json.dumps(req)
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print("新增数据表：", response.text)
#
# create_data_table(access_token)

# 新增多条记录
def create_data_table(access_token):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/C9HdbVUZiadQCxsRNYpcV7qfnqf/tables/table=tblIPMRMlxQCEI8n&view=vew3h5q9pG/records/batch_create"
    headers = {
        "Authorization": "Bearer u-dIpV5_hKZfZUbm1rVsxlqK4gl8gB10EjM0G0hgo0217q".format(access_token),
        "Content-Type": "application/json; charset=utf-8"
    }
    req = {}
    payload = json.dumps(req)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("新增数据表：", response.text)

create_data_table(access_token)
import json
import requests

# Ozon和WB电商运营API数据Demo测试
app_id = "cli_a88b77b97959100b"
app_secret = "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme"
name = "Ozon和WB电商运营API数据"


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
    print("响应数据:", response.text)
    token = response.json()["tenant_access_token"]
    print("token的值：", token)
    return token


access_token = get_access_token("cli_a88b77b97959100b", "cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme")


# 新增一个数据表
def create_data_table(access_token):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps/U5PpboZGTaCUa1s4sl0clCLAn0I/tables"
    headers = {
        "Authorization": "Bearer u-cFpChy7dZbLbTVNAE8UXmqh4jkU1008PUW20h5222KGC".format(access_token),
        "Content-Type": "application/json; charset=utf-8"
    }
    req = {
        "table": {
            "name": "WB数据表",
            "default_view_name": "默认的表格视图",
            "fields": [
                {
                    "field_name": "索引字段",
                    "type": 1
                },
                {
                    "field_name": "单选",
                    "type": 3,
                    "ui_type": "SingleSelect",
                    "property": {
                        "options": [
                            {
                                "name": "Enabled",
                                "color": 0
                            },
                            {
                                "name": "Disabled",
                                "color": 1
                            },
                            {
                                "name": "Draft",
                                "color": 2
                            }
                        ]
                    }
                }
            ]
        }
    }
    payload = json.dumps(req)
    response = requests.request("POST", url, headers=headers, data=payload)
    print("新增数据表：", response.text)

create_data_table(access_token)

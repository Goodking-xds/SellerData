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
    print(response.text)
    token = response.json()["tenant_access_token"]
    print("token的值：", token)
    return token

access_token = get_access_token("cli_a88b77b97959100b","cW23FFCTA7BS5DuiqvZNlfWXbJGn4Zme")

#获取我的空间的元数据
def get_folder_token(access_token):
    url = "	https://open.feishu.cn/open-apis/drive/explorer/v2/root_folder/meta"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization":"Bearer u-ctsk2Uu59e9oCbzakYYpdw5lj8M1000PXo00hgs82EOo".format(access_token)
    }
    response = requests.request("GET", url, headers=headers)
    res = response.json()
    return res

res_folder = get_folder_token(access_token)
print("res_folder:", res_folder)

def create_table(access_token):
    url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    req = {
        "name":"电商平台多维数据",
        "folder_token":"nodcnWS89VvwSrdKz8Mv6rsgvqd"
    }
    request_content = json.dumps(req)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization":"Bearer u-eWXz.SW4V9FqP71Tqi8f9fhkk0ix000rNU001k2E0c_S".format(access_token)
    }
    response = requests.request("POST", url, headers=headers, data=request_content)
    print(response.text)

create_table(access_token)

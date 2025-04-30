import requests

# 关于卖家交易清单
# Ozon API 信息
client_id = "494570"
api_key = "e9df976b-2636-41cc-8348-12bd786c22d4"
ozon_api_url = "https://seller.ozon.ru/api/premium/summary/company/494570"

# 配置 Ozon API 请求头
ozon_headers = {
    "Client-Id": client_id,
    "Api-Key": api_key,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json,, text/plain, */*",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Accept-Language":"zh-Hans",
    "Cookie":"__Secure-ab-group=70; __Secure-ext_xcid=cab1c9aecc7461f52ec57e21c7dcf57a; __Secure-user-id=201937788; bacntid=5481250; sc_company_id=494570; x-o3-language=zh-Hans; xcid=4c83c104c6f371677021c4082904cc4b; rfuid=LTE5NTAyNjU0NzAsMTI0LjA0MzQ3NTI3NTE2MDc0LDE5MDczMzM5MzQsLTEsLTYyNjAyMDU4OCxXM3NpYm1GdFpTSTZJbEJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFsSUZCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxcGRXMGdVRVJHSUZacFpYZGxjaUlzSW1SbGMyTnlhWEIwYVc5dUlqb2lVRzl5ZEdGaWJHVWdSRzlqZFcxbGJuUWdSbTl5YldGMElpd2liV2x0WlZSNWNHVnpJanBiZXlKMGVYQmxJam9pWVhCd2JHbGpZWFJwYjI0dmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmU3g3SW5SNWNHVWlPaUowWlhoMEwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjFkZlN4N0ltNWhiV1VpT2lKTmFXTnliM052Wm5RZ1JXUm5aU0JRUkVZZ1ZtbGxkMlZ5SWl3aVpHVnpZM0pwY0hScGIyNGlPaUpRYjNKMFlXSnNaU0JFYjJOMWJXVnVkQ0JHYjNKdFlYUWlMQ0p0YVcxbFZIbHdaWE1pT2x0N0luUjVjR1VpT2lKaGNIQnNhV05oZEdsdmJpOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5TEhzaWRIbHdaU0k2SW5SbGVIUXZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklsZGxZa3RwZENCaWRXbHNkQzFwYmlCUVJFWWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SjZhQzFEVGlKZCwwLDEsMCwyNCwyMzc0MTU5MzAsOCwyMjcxMjY1MjAsMCwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdWMmx1TXpJZ05TNHdJQ2hYYVc1a2IzZHpJRTVVSURFd0xqQTdJRmRwYmpZME95QjROalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE16VXVNQzR3TGpBZ1UyRm1ZWEpwTHpVek55NHpOaUJGWkdjdk1UTTFMakF1TUM0d0lESXdNRE13TVRBM0lFMXZlbWxzYkdFPSxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LC0xMTgzNDEwNzIsMSwxLC0xLDE2OTk5NTQ4ODcsMTY5OTk1NDg4NywyMDc0NDcwMzk2LDEy; __Secure-ETC=d77195a247610c793ec89829216365f6; abt_data=7.JkAOzmOoOrBvJ1HXN_ZYy7d_xgWfiqUWuuYZodiDR5flA7Ic2nPm732k1TDJNWqgOzKnARzFY6U88hWl5lNdej9rtXcJo6YKRevcR2-26FIWp9FuBa1wZS3FNmHUtbiHupUJedj_OrGPdBk9MKsbNxMDesQhUiPjbvR2Ftarhv5ul5OyrG-2NTZkiIzYabVCklkgecCZaVGF9KHumYEvf0yBHwKS4Zf0NsjrrSY2WxzucJBcw05d1eyZiwK4f9yjB0RECjPJXey3GV40opcRG8KCvwWuBoOj7OJZOMBhJw1ZRsOkDNuBP_eF_fNx08glD5RnRnTqxg91nunqJyKVN4Wgro4yi_198sHwCMxWA8wZjN_eEtEpCflTP4BjbTpf3auA-3x9RgO8VbR8DLhczWN4wOajf9mOPpzxJi5NPsFQDZHgdeR4gCOIaBU4tmjkG2SKSmAi6MvyQfK8ugJF2z7irLKa389-yEeEo9FW-vzxWVo11EY9onv4e7mZyDl-h4xFgJlqlWgerhzW5Zdi; __Secure-access-token=7.201937788.W8c9OlCSRDaJ87zh3bPwKQ.70.AYOs6ExdEZ3plZE1jeBn8Hsl5SqoCgtNDuMLlrpLig_Nk8-I1oIn0_FpgpGCm0j6nr-ZNItlr193juoSCaMAr2M.20250416015412.20250430082325.404n2G1lP71iDHmK41xoodrxkcdqYmqI6wMf1YVrXEA.1aafb3b5e4ff7f0e0; __Secure-refresh-token=7.201937788.W8c9OlCSRDaJ87zh3bPwKQ.70.AYOs6ExdEZ3plZE1jeBn8Hsl5SqoCgtNDuMLlrpLig_Nk8-I1oIn0_FpgpGCm0j6nr-ZNItlr193juoSCaMAr2M.20250416015412.20250430082325.rZfPi1itw-9LrF3jwLyxUjeaVbarXVEA4mhw2jXAfhI.1b5fd3d61eec51309",
    "Priority": "u=1, i",
    "Referer": "https://seller.ozon.ru",
    "Sec-Ch-Ua": "'Microsoft Edge';v='135', 'Not-A.Brand';v='8', 'Chromium';v='135'",
    "Sec-Ch-Ua-mobile": "?0",
    "Sec-Ch-Ua-platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Sites": "same-origin",
    "X-O3-App-Name": "seller-ui",
    "X-O3-Company-Id": "494570",
    "X-O3-Language": "zh-Hans",
    "X-O3-Page-Type": "finances-other"
}

data = {
    "company_id":454970,
    "poll_type": "NPS"
    }

response = requests.get(ozon_api_url,headers=ozon_headers,params=data)
print(response)
response.raise_for_status()
result = response.json()
print(result)








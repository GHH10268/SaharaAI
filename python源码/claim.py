import time,asyncio
from os import access

import requests,json,os
import uuid
import random
import string
from eth_account import Account
from eth_account.messages import encode_defunct

class Gobi_Bear:
    def __init__(self,login_info):
        self.mistakelist_flush=[]
        self.mistakelist_claim=[]
        self.login_info=login_info#list
        print(f"一共{len(self.login_info)}个号。")
        self.start()
        print(f"mistakelist_flush:{self.mistakelist_flush}")
        print(f"mistakelist_claim:{self.mistakelist_claim}")
    def start(self):
        asyncio.run(self.task_flush())
        print("全部刷新完成！！！！！")
        asyncio.run(self.task_claim())
        print("全部领取完成！！！！！")
    async def task_flush(self):
        tasks=[self.flush("1004",login_info) for login_info in self.login_info]
        await asyncio.gather(*tasks)

    async def task_claim(self):
        tasks=[self.claim("1004",login_info) for login_info in self.login_info]
        await asyncio.gather(*tasks)

    async def flush(self,taskid,login_info):
        try:
            url = 'https://legends.saharalabs.ai/api/v1/task/flush'
            data = {"taskID": taskid}
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
                "authorization": 'Bearer ' + login_info["accessToken"],
                "content-length": "17",
                "content-type": "application/json",
                "origin": "https://legends.saharalabs.ai",
                "priority": "u=1, i",
                "referer": "https://legends.saharalabs.ai",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            }
            result = requests.post(url, data=json.dumps(data), headers=headers)
            print(result)
        except Exception as e:
            address=login_info["username"]
            print (f"❌地址：{address} flush失败: {e}")
            self.mistakelist_flush.append(address)
        # time.sleep(1)

    async def claim(self,taskid,login_info):
        try:
            address = login_info["username"]
            accessToken=login_info["accessToken"]
            url='https://legends.saharalabs.ai/api/v1/task/claim'
            data={"taskID":taskid}
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
                "authorization": 'Bearer '+login_info["accessToken"],
                "content-length": "17",
                "content-type": "application/json",
                "origin":"https://legends.saharalabs.ai",
                "priority": "u=1, i",
                "referer":"https://legends.saharalabs.ai",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            }
            # print(self.login_info["accessToken"])
            result=requests.post(url,data=json.dumps(data),headers=headers)
            # print(result.text)
            result=result.json()
            # print(result)

            if 'message' in result:
                if 'has been claimed' in result["message"]:
                    print("任务{}:已经领取过了~".format(taskid))
                else:
                    print("等60s后再次刷新~")
                    time.sleep(60)
                    print(result)
                    # self.flush("1004",login_info)
                    # self.claim("1004",login_info)
            else:
                earn=result[0]["amount"]
                print(f"✅地址：{address} claim成功,Earn:{earn}积分~")
                # print(result)
        except Exception as e:
            address = login_info["username"]
            print (f"❌地址：{address} claim失败: {e}")
            self.mistakelist_claim.append(address)

class Sahara_Login:
    def __new__(cls):
        instance = super().__new__(cls)

        instance.mistakelist_wallet=[]
        instance.mistakelist_chanllge=[]
        instance.chanllges = []
        instance.login_info = []
        instance.accounts = []
        instance.read_eth_accounts()
        instance.start()
        return instance.login_info

    def start(self):
        print(self.accounts)
        asyncio.run(self.task_chanllge())
        asyncio.run(self.task_wallet())
        print(f"mistakelist_chanllge:{self.mistakelist_chanllge}")
        print(f"mistakelist_wallet:{self.mistakelist_wallet}")

    async def task_chanllge(self):
        # account0 = self.accounts[0]
        tasks=[self.chanllge(account) for account in self.accounts]
        await asyncio.gather(*tasks)

    async def task_wallet(self):
        tasks=[self.wallet(self.sign_wallet_data(chanllge["account"],chanllge["challenge"])) for chanllge in self.chanllges]
        await asyncio.gather(*tasks)

    def read_eth_accounts(self,filename="accounts.txt"):
        accounts = []
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"文件 {filename} 不存在。")
            # return accounts
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()  # 去除换行符
                if not line:
                    continue  # 跳过空行
                try:
                    address, key, uid = line.split("@")  # 按 "@" 分割
                    accounts.append({"address": address, "key": key, "uuid": uid})
                except ValueError:
                    print(f"警告：跳过格式错误的行 -> {line}")

        self.accounts=accounts

    async def chanllge(self,account):
        try:
            address=account["address"]
            url='https://legends.saharalabs.ai/api/v1/user/challenge'
            data={
                "address":address
            }
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
                "content-length": "17",
                "content-type": "application/json",
                "cookie": "hubspotutk=69b3a4d8407fd4c20f8b62edfd2e7d09; _ga=GA1.1.430869306.1737550036; _ga_8JY051HV2D=GS1.1.1737649311.2.0.1737649311.0.0.0; __hstc=35783295.69b3a4d8407fd4c20f8b62edfd2e7d09.1737344239375.1737549817620.1738932020134.3; __hssrc=1; _ga_Q55XJSKGWT=GS1.1.1738932020.1.1.1738932020.0.0.0",
                "origin": "https://legends.saharalabs.ai",
                "priority": "u=1, i",
                "referer": "https://legends.saharalabs.ai/?code=KQ3U0K",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            }
            result=requests.post(url,data=json.dumps(data),headers=headers).json()
            if "challenge" in result:
                challenge=result["challenge"]
                self.chanllges.append({"account":account,"challenge":challenge})
            else:
                print("chanllge出错！！！")
                challenge = None

            return challenge
        except Exception as e:
            address=account["address"]
            print(f"❌地址：{address} chanllge失败: {e}")
            self.mistakelist_chanllge.append(address)


    async def wallet(self,data):
        try:
            url='https://legends.saharalabs.ai/api/v1/login/wallet'
            headers = {

                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
               "content-length": "17",
                "content-type": "application/json",
                "cookie": "hubspotutk=69b3a4d8407fd4c20f8b62edfd2e7d09; _ga=GA1.1.430869306.1737550036; _ga_8JY051HV2D=GS1.1.1737649311.2.0.1737649311.0.0.0; __hstc=35783295.69b3a4d8407fd4c20f8b62edfd2e7d09.1737344239375.1737549817620.1738932020134.3; __hssrc=1; _ga_Q55XJSKGWT=GS1.1.1738932020.1.1.1738932020.0.0.0",
                "origin": "https://legends.saharalabs.ai",
                "priority": "u=1, i",
                "referer": "https://legends.saharalabs.ai/?code=KQ3U0K",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            }
            login_info = requests.post(url, data=json.dumps(data), headers=headers).json()
            print(login_info)
            if "accessToken" in login_info:
                accessToken=login_info["accessToken"]
            else:
                print("获取accessToken出错！！！")
                accessToken=None
            self.login_info.append(login_info)

        except Exception as e:
            address=data["address"]
            print(f"❌地址：{address} wallet失败: {e}")
            self.mistakelist_wallet.append(address)


    def sign_wallet_data(self,account,chanllge):

        # 生成一个以太坊钱包
        # wallet = Account.create()
        # address = wallet.address
        # 原始消息，注意这里的换行符
        address=account["address"]
        private_key=account["key"]
        walletUUID=account["uuid"]
        message = "Sign in to Sahara!\nChallenge:{}".format(chanllge)

        # 1. 进行 EIP-191 规范的消息编码
        message_hash = encode_defunct(text=message)

        # 2. 进行签名
        signed_message = Account.sign_message(message_hash, private_key)

        # 输出签名结果
        data={"address": address,
         "sig": '0x'+signed_message.signature.hex(),
         "walletUUID": walletUUID,
        "walletName": "OKX Wallet"}

        return data

if __name__ == '__main__':
    login_info=Sahara_Login()
    print(login_info)
    GB=Gobi_Bear(login_info)
    input("Press Enter to exit...")

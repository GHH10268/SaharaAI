import time,os,web3,requests,json,asyncio
from web3 import Web3
from eth_account import Account

class Super_Testnet01:
    def __init__(self):
        self.mistakelist=[]
        self.accounts=[]
        self.start()

    def start(self):
        self.accounts=self.read_eth_accounts()
        asyncio.run(self.giveaway())#启动小号转账给随机生成的地址
        print("[][][][]---转账已经完成！---[][][][]")

    async def giveaway(self):
        value=0.0000001
        to_address_list=[]
        for i in range(len(self.accounts)):
            account = Account.create()  # 生成以太坊账户
            address = account.address  # 以太坊地址
            to_address_list.append(address)
        w3=self.w3()
        # tasks = [self.transfer(w3,Web3.to_checksum_address(from_address["address"]),from_address["key"],Web3.to_checksum_address(to_address),value) for from_address in self.accounts[:100]]
        tasks = [
            self.transfer(
                w3,
                Web3.to_checksum_address(from_address["address"]),
                from_address["key"],
                Web3.to_checksum_address(to_address),
                value
            )
            for from_address, to_address in zip(self.accounts, to_address_list)
        ]
        await asyncio.gather(*tasks)

    def get_recent_addresses(self,block_number, limit=100):
        url='https://testnet-explorer.saharalabs.ai/api/v2/transactions?block_number={}&index=19&items_count={}&filter=validated'.format(block_number,limit)
        result=requests.get(url).json()
        print(result)

    def w3(self):
        # 连接到 Sahara Labs 的测试网
        rpc_url = "https://testnet.saharalabs.ai"
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        # 确保连接成功
        if not w3.is_connected():
            raise Exception("无法连接到 Sahara Labs 测试网")
        return w3

    async def transfer(self,w3,from_address,private_key,to_address,value):
        try:
            # 获取 nonce
            nonce = w3.eth.get_transaction_count(from_address)

            # 构造交易
            tx = {
                "nonce": nonce,
                "to": to_address,
                "value": Web3.to_wei(value, "ether"),  # 0x9184e72a000 = 0.01 Sahara
                "gas": 21000,  # 0x5208
                "gasPrice": w3.eth.gas_price,  # 也可以手动设置
                "chainId": w3.eth.chain_id,
            }

            # 使用私钥签名交易
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)

            # 发送交易
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            # 获取交易哈希
            print(f"交易已发送，哈希值: {tx_hash.hex()}")
            # 等待交易确认（可选）
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"✅交易成功，区块号: {receipt['blockNumber']}")
            return tx_hash.hex()
        except Exception as e:

            print(f"❌地址：from_address：{from_address} ，from_address{to_address}。发送失败: {e}")
            self.mistakelist.append({"from_address":from_address,"to_address":to_address})

    def read_eth_accounts(self,filename="accounts.txt"):
        accounts = []
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"文件 {filename} 不存在。")
            return accounts
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
        return accounts
if __name__ == '__main__':
    Super_Testnet01=Super_Testnet01()
    input("Press Enter to exit...")

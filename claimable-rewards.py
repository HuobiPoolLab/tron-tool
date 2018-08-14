# -*- coding: utf-8 -*-

# 使用说明:
# 操作系统: ubuntu 16.04
# python版本: Python 3.5.2
# 功能: 填写账户地址和私钥,可以收取波场超级节点的出块奖励. 根据波场规则, 每24小时收取一次. 可以在crontab定时执行.
# 地址转换工具: https://github.com/tronprotocol/tron-demo/blob/master/TronConvertTool.zip    可以将地址由Base58转为HexString.
# 依赖包:  pip3　install requests
#　需要配置地址　私钥　网址


import sys, getopt
import requests
import json


def main(argv):
    #账户地址, 需要转成 hex string
    # example: 41e9d79cc47518930bc322d9bf7cddd260a0260a8d
    owner_address = ''
    #私钥
    private_key = ''
    #网址
    # example: http://127.0.0.1:8090
    base_url = ''

    prompt_info = 'claimable-rewards.py --owner-address <your address> --private-key <your private key> --base-url <FullNode url>'

    try:
        opts, args = getopt.getopt(argv,"h",["owner-address=","private-key=","base-url="])
    except getopt.GetoptError:
        print(prompt_info)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(prompt_info)
            sys.exit()
        elif opt in ("--owner-address"):
            owner_address = arg
        elif opt in ("--private-key"):
            private_key = arg
        elif opt in ("--base-url"):
            base_url = arg

    print('账户地址：', owner_address)
    print('私钥：', private_key)
    print('网址：', base_url)

    #生成事务
    withdrawbalance_payload = {'owner_address': owner_address}
    withdrawbalance_url = base_url + '/wallet/withdrawbalance'
    withdrawbalance_response = requests.post(withdrawbalance_url, data=json.dumps(withdrawbalance_payload)).json()
    print(withdrawbalance_response)
    withdrawbalance_error = withdrawbalance_response.get('Error', '')

    if(withdrawbalance_error):
        print("距离上次收取不足24小时")
        sys.exit()

    #给事务签名
    gettransactionsign_payload = {'transaction': withdrawbalance_response, 'privateKey': private_key}
    gettransactionsign_url = base_url + '/wallet/gettransactionsign'
    gettransactionsign_response = requests.post(gettransactionsign_url, data=json.dumps(gettransactionsign_payload)).json()
    print(gettransactionsign_response)

    #TODO:
    #出错处理

    #广播事务
    broadcasttransaction_payload = gettransactionsign_response
    broadcasttransaction_url = base_url + '/wallet/broadcasttransaction'
    broadcasttransaction_response = requests.post(broadcasttransaction_url, data=json.dumps(broadcasttransaction_payload)).json()
    print(broadcasttransaction_response)
    broadcasttransaction_code = broadcasttransaction_response.get('code', '')
    broadcasttransaction_result = broadcasttransaction_response.get('result', False)

    if((broadcasttransaction_code == "DUP_TRANSACTION_ERROR")
            or (broadcasttransaction_code == "TRANSACTION_EXPIRATION_ERROR")):
        print("事务过期或事务已提交. 广播事务失败")
        sys.exit()

    if(broadcasttransaction_result):
        print("收取奖励成功")
    else:
        print("收取奖励失败, 请查明原因并重试")


if __name__ == "__main__":
    main(sys.argv[1:])

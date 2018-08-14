# -*- coding: utf-8 -*-

# 使用说明:
# 操作系统: ubuntu 16.04
# python版本: Python 3.5.2
# 功能: 填写转出账户地址(付款账户地址)  转入账户地址(收款账户地址) 和 转出账户(付款账户)私钥,可以给指定账户转账. 可以在crontab定时执行.
# 地址转换工具: https://github.com/tronprotocol/tron-demo/blob/master/TronConvertTool.zip    可以将地址由Base58转为HexString.
# 依赖包:  pip3　install requests
#　需要配置  转出账户地址　转入账户地址  私钥　网址

import sys, getopt
import requests
import json


def main(argv):
    # 账户地址, 需要转成 hex string
    # example: 41e9d79cc47518930bc322d9bf7cddd260a0260a8d
    # 转出账户(付款账户)地址
    from_address = ''
    # 转入账户(收款账户)地址
    to_address = ''
    # 转出账户(付款账户)私钥
    private_key = ''
    # 网址
    # example: http://127.0.0.1:8090
    base_url = ''

    prompt_info = 'easy-transfer.py --from-address <drawee address> --to-address <payee address> --private-key <drawee private key> --base-url <FullNode url>'

    try:
        opts, args = getopt.getopt(argv,"h",["from-address=","to-address=","private-key=","base-url="])
    except getopt.GetoptError:
        print(prompt_info)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(prompt_info)
            sys.exit()
        elif opt in ("--from-address"):
            from_address = arg
        elif opt in ("--to-address"):
            to_address = arg
        elif opt in ("--private-key"):
            private_key = arg
        elif opt in ("--base-url"):
            base_url = arg

    print('转出账户(付款账户)地址：', from_address)
    print('转入账户(收款账户)地址：', to_address)
    print('私钥：', private_key)
    print('网址：', base_url)

    # 获取转出账户余额
    getaccount_payload = {'address': from_address}
    getaccount_url = base_url + '/wallet/getaccount'
    getaccount_response = requests.post(getaccount_url, data=json.dumps(getaccount_payload)).json()
    print(getaccount_response)
    getaccount_balance = getaccount_response.get('balance', 0)

    if (getaccount_balance <= 0):
        print("账户余额不足．无法转账")
        sys.exit()

    print("转账金额：　", getaccount_balance)

    # 转账
    easytransferbyprivate_payload = {'privateKey': private_key, 'toAddress': to_address, 'amount': getaccount_balance}
    easytransferbyprivate_url = base_url + '/wallet/easytransferbyprivate'
    easytransferbyprivate_response = requests.post(easytransferbyprivate_url,
                                                   data=json.dumps(easytransferbyprivate_payload)).json()
    easytransferbyprivate_result = easytransferbyprivate_response.get('result', {}).get('result', False)
    print(easytransferbyprivate_response)

    if (easytransferbyprivate_result):
        print("转账成功")
    else:
        print("转账失败．　请查明原因并重试．")


if __name__ == "__main__":
    main(sys.argv[1:])

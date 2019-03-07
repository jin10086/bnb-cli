from subprocess import Popen, PIPE, STDOUT
import subprocess
import random, string, json
from multiprocessing import Pool
import time


def runPool(f, accounts):
    with Pool() as pool:
        pool.map(f, accounts)


def genrateRandomN(k=5):
    return "".join(random.choices(string.ascii_lowercase, k=k))


def _createkey(password):
    cmd = ["bnbcli", "keys", "new", genrateRandomN(), "--default"]
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    createBNBKey = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(createBNBKey)


def createkey(password, x):
    "生成x 个 key,password是签名时候用的"
    for i in range(x):
        _createkey(password)


def runcleos(cmd):
    a = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return a.stdout


def getkeylist():
    d = runcleos("bnbcli keys list -o json".split())
    return json.loads(d)


def getaccounts():
    d = getkeylist()
    return [i["address"] for i in d]


def getpub_keys():
    d = getkeylist()
    return [i["pub_key"] for i in d]


def getNameWithAddress():
    ret = {}
    d = getkeylist()
    for i in d:
        ret[i["address"]] = i["name"]
    return ret


def getBalance():
    "获取有余额的账号."
    accounts = getaccounts()
    ret = []
    for account in accounts:
        cmd = (
            f"bnbcli account {account} --trust-node --node=data-seed-pre-2-s1.binance.org:80 -o json".split()
        )
        c = runcleos(cmd)

        # return
        # {
        #     "type": "bnbchain/Account",
        #     "value": {
        #         "base": {
        #             "address": "tbnb1r8tp2d6ecx33q3xctvqlsgfly5pgmtu4a469q7",
        #             "coins": [{"denom": "BNB", "amount": "20000000000"}],
        #             "public_key": null,
        #             "account_number": "3049",
        #             "sequence": "0",
        #         },
        #         "name": "",
        #         "frozen": null,
        #         "locked": null,
        #     },
        # }
        if b"ERROR" in c:
            print(account)

        else:
            ret.append(json.loads(c))
    return ret


def transferToken(f, to, amount, password, memo="testtransfer"):
    "给别人转账,f需要是本地的用户名,不是address"
    cmd = (
        f"bnbcli send --from {f} --to={to} --amount={amount}:BNB --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --json --memo {memo}"
    ).split()
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    transferToken = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(transferToken)


def issueToken(issuer, password):
    cmd = (
        f'bnbcli token issue --token-name "hello-world" --total-supply 100000000000000000 --symbol HWD --mintable --from {issuer} --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node'.split()
    )
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    issuetoken = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(issuetoken)


def createProposal(name, baseAssetSymbol, password):
    t = int(time.time()) + 60 * 60 * 4
    cmd = [
        "bnbcli",
        "gov",
        "submit-list-proposal",
        "--from",
        name,
        "--deposit",
        "10000000000:BNB",
        "--base-asset-symbol",
        baseAssetSymbol,
        "--quote-asset-symbol",
        "BNB",
        "--init-price",
        "100000000",
        "--title",
        f"list {baseAssetSymbol}/BNB",
        "--description",
        f"list {baseAssetSymbol}/BNB",
        "--expire-time",
        t,
        "--chain-id=Binance-Chain-Nile",
        "--node=data-seed-pre-2-s1.binance.org:80",
    ]
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    e = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(e)


def depositProposal(name, proposalid, amount, password):
    cmd = (
        f"bnbcli gov deposit --deposit {amount*100000000}:BNB --from {name} --proposal-id {proposalid} --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --json".split()
    )
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    e = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(e)


def maker(f, symbol, side, price, qty, password="Yijia7dengyu8"):
    cmd = (
        f"bnbcli dex order --symbol {symbol} --side {side} --price {int(price*100000)*1000} --qty {int(qty*1000)*100000} --tif gte --from {f} --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80 --trust-node"
    ).split()
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    marketmaking = p.communicate(input=bytes(password + "\n", "utf-8"))[0]
    print(marketmaking)


def summaryBNB(name, password):
    transferToken(
        name, "tbnb1c7sg5wwqsvxd52tlmmhyj3dxvc6njl5vvdterk", 19999875000, password
    )


if __name__ == "__main__":
    password = "Yijia7dengyu8"
    # issueToken("testkey", password)
    createProposal("testkey", "HWD-27B", password)
    # createkey(password, 100)
    # NameWithAddress = getNameWithAddress()
    # password = ""
    # for i in getBalance():
    #     if i:
    #         address = i["value"]["base"]["address"]
    #         bnbAmount = 0
    #         if i["value"]["base"]["coins"]:
    #             for coin in i["value"]["base"]["coins"]:
    #                 if coin["denom"] == "BNB":
    #                     bnbAmount = coin["amount"]
    #             if bnbAmount == "20000000000":
    #                 summaryBNB(NameWithAddress[address], password)

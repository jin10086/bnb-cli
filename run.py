from ut import (
    getkeylist,
    getNameWithAddress,
    transferToken,
    getaccounts,
    createProposal,
    issueToken,
)
from addaddress import getbnb


if __name__ == "__main__":
    password = "Yijia7dengyu8"
    name = "abcdefghijklmnopqrst"
    NameWithAddress = getNameWithAddress()
    a = []
    d = getkeylist()
    for i in d:
        if i["name"] in name:
            a.append(i["address"])

    # 先批量获取 bnb
    getbnb(a)

    # 代币汇总
    for address in a:
        transferToken(
            NameWithAddress[address],
            "tbnb1yc3al3wvs4efu2yrw4a3d8r5yevc9uzsd5rmh2",
            19999875000,
            password,
        )

    issueToken("testkey", password)
    # 查看asset name
    # "bnbcli account tbnb1779vy8x6m70mya5p703jdgsuh3lffegdq3lapy --chain-id=Binance-Chain-Nile --node=data-seed-pre-2-s1.binance.org:80"

    # 提案
    # createProposal("testkey", "", password)

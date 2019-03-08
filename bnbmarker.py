from ut import *
import random
import requests
import json
import time
import logging
import os

symbol = "PRA.B-31A_BNB"
# symbol = "HWD-0A2_BNB"
# symbol = "BIN-986_BNB"
account = "testkey"

s = requests.Session()


def loggingSetting(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("{}.log".format(name))
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


log = loggingSetting("bnbMarker")


def buyOtherToken():
    maker(account, "ANN-457_BNB", 1, 1, 100)
    maker(account, "BNN-411_BNB", 1, 1, 100)
    maker(account, "CNN-210_BNB", 1, 1, 100)
    maker(account, "UKT-710_BNB", 1, 1, 100)
    maker(account, "E0C-EF8_BNB", 1, 1, 100)
    maker(account, "FLC-FB2_BNB", 1, 1, 100)
    maker(account, "SLC-6D1_BNB", 1, 1, 100)
    maker(account, "NMSL-19D_BNB", 1, 1, 100)
    maker(account, "NARN-278_BNB", 1, 1, 100)
    maker(account, "OEN-FD1_BNB", 1, 1, 100)


def init():
    """初始化挂单90~99"""
    for i in range(10):
        maker(account, symbol, 1, 90 + i + random.random(), 0.1 + random.random())
    maker(account, symbol, 1, 100, 0.1)  # 初始化价格100-买
    maker(account, symbol, 2, 100, 0.1)  # 初始化价格100-卖

    """初始化挂卖单110~120"""
    for i in range(10):
        maker(account, symbol, 2, 120 - i - random.random(), 0.1 + random.random())


def run():
    log.info("开始刷单.")
    targetPrice = 4.9  # 设定初始价格
    log.info(f"初始价格为{targetPrice}")
    while True:
        side = int(2 * random.random()) + 1  # 随机买卖方向
        r = s.get(
            "https://testnet-dex.binance.org/api/v1/depth?symbol=" + symbol
        )  # 获取TOKEN挂单
        p = r.json()
        if targetPrice >= 10:  # 大于1200则一定下跌
            side = 2
            targetPrice = 14.9
        if targetPrice < 5:
            side = 1
            targetPrice = 4.9
        log.info(f"刷单方向为{side}")
        if side == 1:
            targetPrice += 10
            qty = 0
            for i, j in p["asks"]:
                if float(i) < targetPrice:
                    qty += float(j)  # 集合所有低于目标价的深度

            log.info(f"下单价格为 {targetPrice}")
            if qty < 0.001:  # 如果可吃单量小于0.001，自己下一单对敲
                log.info(f"可吃单为{qty},自己下单")
                t = maker(account, symbol, 2, targetPrice, 0.001)
                log.info(t)
            log.info("刷单>>>")
            t = maker(account, symbol, 1, targetPrice, 0.001)  # 否则直接吃单
            log.info(t)

        elif side == 2:
            targetPrice -= 10
            qty = 0
            for i, j in p["bids"]:
                if float(i) > targetPrice:
                    qty += float(j)
            log.info(f"下单价格为 {targetPrice}")
            if qty < 0.001:
                log.info(f"可吃单为{qty},自己下单")
                t = maker(account, symbol, 1, targetPrice, 0.001)
                log.info(t)
            log.info("刷单>>>")
            t = maker(account, symbol, 2, targetPrice, 0.001)
            log.info(t)
        log.info("等待180s后开启下一次刷单")
        log.info("-" * 60)
        time.sleep(180)  # 三分钟交易一次


def main():
    log.info("AutoRes is starting")

    run()
    executable = sys.executable
    args = sys.argv[:]
    print(args)
    args.insert(0, sys.executable)
    time.sleep(1)
    log.info("Respawning")
    os.execvp(executable, args)


if __name__ == "__main__":
    main()

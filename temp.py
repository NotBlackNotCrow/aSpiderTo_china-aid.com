import numpy as np
import matplotlib.pyplot as plt

# 定义股票参数
vh = 200  # 上行市场股票价格
vl = 100  # 下行市场股票价格

# 定义交易者比例
mu = 0.1  # 知情交易者比例
gamma = 0.13  # 环境担忧型知情交易者比例

# 假设市场上行的初始概率
theta = 0.5

# 定义价格和成交量变量
asks_B = np.zeros(13)
bids_B = np.zeros(13)
transactions_B = np.zeros(13)
transaction_prices_B = []

# 进行13次交易
for i in range(13):
    # 市场随机上行
    is_market_up = np.random.rand() < 0.5

    # 随机决定交易者类型
    trader_type = np.random.rand()

    # B股票的报价和交易
    ask = (1+mu)*theta/(1-mu*(1-2*theta))*vh + (1-(1+mu)*theta/(1-mu*(1-2*theta)))*vl
    bid = (1-mu)*theta/(1+mu*(1-2*theta))*vh + (1-(1-mu)*theta/(1+mu*(1-2*theta)))*vl
    asks_B[i] = ask
    bids_B[i] = bid

    # 交易
    if trader_type < mu:
        # 知情交易者
        if is_market_up:
            # 买入
            transactions_B[i] += 1
            transaction_prices_B.append(ask)
            # 调整预期
            theta = (ask - vl) / (vh - vl)
        else:
            # 卖出
            transactions_B[i] -= 1
            transaction_prices_B.append(bid)
            # 调整预期
            theta = (bid - vl) / (vh - vl)
    elif trader_type < mu + gamma:
        # 环境担忧型知情交易者，只卖出B股票
        # 卖出
        transactions_B[i] -= 1
        transaction_prices_B.append(bid)
        # 调整预期
        theta = (bid - vl) / (vh - vl)
    else:
        # 非知情交易者
        if np.random.rand() < 0.5:
            # 买入
            transactions_B[i] += 1
            transaction_prices_B.append(ask)
            # 调整预期
            theta = (ask - vl) / (vh - vl)
        else:
            # 卖出
            transactions_B[i] -= 1
            transaction_prices_B.append(bid)
            # 调整预期
            theta = (bid - vl) / (vh - vl)

# 绘制报价和成交价格的图表
plt.figure(figsize=(10, 6))
plt.plot(range(1, 14), asks_B, marker='o', linestyle='-', color='r', label='Ask Prices')
plt.plot(range(1, 14), bids_B, marker='o', linestyle='-', color='g', label='Bid Prices')
plt.plot(range(1, 14), transaction_prices_B, marker='o', linestyle='None', color='b', label='Transaction Prices')

plt.title('B Stock Prices over 13 Transactions')
plt.xlabel('Transaction Number')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

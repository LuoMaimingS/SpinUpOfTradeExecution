import numpy as np
from excutes import *


def load(sym, split="train"):
    file_name = sym + ".npz"
    raw_data = np.load(file_name)
    data = raw_data['data']
    if split == "train":
        data = data[:2400]
    elif split == "eval":
        data = data[2400:]
    else:
        raise NotImplementedError
    print(data.shape)
    return data


def main():
    data = load('000012')
    sl1 = execute(5000, 8, 4, 4, data)
    sl2 = execute(5000, 2, 4, 4, data)
    sl3 = execute(10000, 8, 4, 4, data)
    sl4 = execute(10000, 2, 4, 4, data)
    print(sl1, sl2, sl3, sl4)


def execute(V, H,
            T, I,
            data,
            strategy='S&L'):
    """
    :param V: 要交易的股票数量（股）
    :param H: 完成交易的时间（分钟）
    :param T: 交易分成几段
    :param I: 股票分成几份
    :param data:
    :param strategy:
    :return:
    """
    if strategy == "S&L":
        cost = executeSL(V, H, T, I, data)
        return cost
    else:
        raise NotImplementedError


if __name__ == '__main__':
    main()

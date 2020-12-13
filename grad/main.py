import numpy as np
from excutes import *
from envs import ExeEnv


def load(sym):
    file_name = sym + ".npz"
    raw_data = np.load(file_name)
    data = raw_data['data']
    print(data.shape)
    return data


def excuteSLInEnv(V, H,
                  data,
                  dire=1):
    env = ExeEnv(V, H, 1, 1, data, dire, mode="train")
    env.reset()
    r1, count1, cost1 = 0, 0, 0
    for i in range(env.data.shape[0]):
        ob, rwd, don, info = env.step(0.0, debug=False)
        assert don
        if don:
            count1 += 1
            r1 += rwd
            cost1 += info["cost"] * 10000
            env.reset()

    env.mode = "eval"
    env.first_reset = False
    env.reset()
    r2, count2, cost2 = 0, 0, 0
    for i in range(env.data.shape[0]):
        ob, rwd, don, info = env.step(0.0, debug=False)
        assert don
        if don:
            count2 += 1
            r2 += rwd
            cost2 += info["cost"] * 10000
            env.reset()

    return r1 / count1, cost1 / count1, r2 / count2, cost2 / count2


def main():
    data = load('000012')
    sl11, c11, sl12, c12 = excuteSLInEnv(50000, 8, data)
    sl21, c21, sl22, c22 = excuteSLInEnv(50000, 2, data)
    sl31, c31, sl32, c32 = excuteSLInEnv(100000, 8, data)
    sl41, c41, sl42, c42 = excuteSLInEnv(100000, 2, data)
    print("50K 8min: MeanReward: {:.2f} {:.2f} MeanCost: {:.2f} {:.2f}".format(sl11, c11, sl12, c12 ))
    print("50K 2min: MeanReward: {:.2f} {:.2f} MeanCost: {:.2f} {:.2f}".format(sl21, c21, sl22, c22))
    print("100K 8min: MeanReward: {:.2f} {:.2f} MeanCost: {:.2f} {:.2f}".format(sl31, c31, sl32, c32))
    print("100K 2min: MeanReward: {:.2f} {:.2f} MeanCost: {:.2f} {:.2f}".format(sl41, c41, sl42, c42))


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


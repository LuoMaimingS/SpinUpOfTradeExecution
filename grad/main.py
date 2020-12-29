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
    debugFlag = False
    T = 1
    env = ExeEnv(V, H, T, T, data, dire, mode="train")
    r1, count1, cost1 = 0, 0, 0
    for i in range(env.data.shape[0]):
        rwd = 0
        for _ in range(T):
            _, temp_r, don, info = env.step(0.00, debug=debugFlag)
            rwd += temp_r
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
        rwd = 0
        for _ in range(T):
            _, temp_r, don, info = env.step(0.00, debug=debugFlag)
            rwd += temp_r
        assert don
        if don:
            count2 += 1
            r2 += rwd
            cost2 += info["cost"] * 10000
            env.reset()

    return r1 / count1, cost1 / count1, r2 / count2, cost2 / count2


def main():
    data = load('000012')
    rtrain_58, ctrain_58, rtest_58, ctest_58 = excuteSLInEnv(50000, 8, data)
    rtrain_54, ctrain_54, rtest_54, ctest_54 = excuteSLInEnv(50000, 4, data)
    rtrain_52, ctrain_52, rtest_52, ctest_52 = excuteSLInEnv(50000, 2, data)
    
    rtrain_18, ctrain_18, rtest_18, ctest_18 = excuteSLInEnv(100000, 8, data)
    rtrain_14, ctrain_14, rtest_14, ctest_14 = excuteSLInEnv(100000, 4, data)
    rtrain_12, ctrain_12, rtest_12, ctest_12 = excuteSLInEnv(100000, 2, data)
    
    print("50K 8min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_58, ctrain_58, rtest_58, ctest_58))
    print("50K 4min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_54, ctrain_54, rtest_54, ctest_54))
    print("50K 2min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_52, ctrain_52, rtest_52, ctest_52))

    print("100K 8min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_18, ctrain_18, rtest_18, ctest_18))
    print("100K 4min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_14, ctrain_14, rtest_14, ctest_14))
    print("100K 2min: Training Set: {:.2f} {:.2f} Test Set: {:.2f} {:.2f}".format(rtrain_12, ctrain_12, rtest_12, ctest_12))

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


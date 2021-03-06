import gym
import numpy as np


class ExeEnv(gym.Env):
    def __init__(self, V, H, T, I, data, dire=1, mode="train"):
        self.V = V
        self.H = H
        self.T = T
        self.I = I
        self.raw_data = data
        self.mode = mode
        if mode == "train":
            self.data = data[:2400]
        else:
            assert mode == "eval"
            self.data = data[2400:]
        self.dire = dire
        self.N = self.data.shape[0]
        length = H * 20
        self.interval = int(length / T)

        self.first_reset = True

        self.observation_space = gym.spaces.Box(low=0, high=10, shape=(4,))
        self.action_space = gym.spaces.Box(-0.05, 0.05, (1,))

        self.p = -1

        self.t = 0
        self.offset = 0
        self.rest_vol = 0
        self.base_cost = 0.
        self.total_cost = 0.
        self.opt_price = 0.
        self.prev_reward = 0.

    def reset(self, rolling=True, debug=False):
        if self.mode == "eval" and self.N == 2400:
            self.data = self.raw_data[2400:]
            self.N = self.data.shape[0]
            self.first_reset = True
        if self.first_reset:
            print("First Reset Executing Environment, {} trajectories, interval: {}.".format(self.N, self.interval))
            self.first_reset = False
            self.p = 0
        else:
            self.p = (self.p + 1) % self.N if rolling else self.p

        self.t = 0
        self.offset = 0
        self.rest_vol = self.V
        self.base_cost = 0.
        self.total_cost = 0.

        cur_lob = self.data[self.p][self.offset]
        a = cur_lob[10]
        if cur_lob[8] != 0: a = cur_lob[8]
        b = cur_lob[8]
        if cur_lob[10] != 0: b = cur_lob[10]
        # self.opt_price = (self.data[self.p][self.offset][8] + self.data[self.p][self.offset][10]) / 2
        self.opt_price = (a + b) / 2
        self.prev_reward = 0.
        if debug: print(self.data.shape, self.N, self.p)
        return np.array((self.T, self.I, min((cur_lob[8] - cur_lob[10]) * 100, 10), 0))

    def step(self, action, debug=False):
        # assert isinstance(action, gym.spaces.Box)
        traj_data = self.data[self.p]

        if self.dire == 1:
            limit_p = traj_data[self.offset][10] + action

            for i in range(0, self.interval // 2, 2):
                if self.rest_vol == 0: break
                temp_off = self.offset + i

                for j in [8, 6, 4, 2, 0]:
                    if self.rest_vol == 0: break

                    tmp_vol = self.rest_vol
                    if traj_data[temp_off][j] <= limit_p:
                        if self.rest_vol > traj_data[temp_off][j + 1]:
                            self.rest_vol -= traj_data[temp_off][j + 1]
                            tmp_vol = traj_data[temp_off][j + 1]
                        else:
                            self.rest_vol = 0
                        self.total_cost += traj_data[temp_off][j] * tmp_vol
                        if debug: print(self.t, temp_off, "买 ", traj_data[temp_off][j], tmp_vol, self.total_cost, "剩余 ", self.rest_vol)
                    else:
                        break

        else:
            assert self.dire == 0
            limit_p = traj_data[self.offset][8] - action

            for i in range(0, self.interval // 2, 2):
                if self.rest_vol == 0: break
                temp_off = self.offset + i

                for j in [10, 12, 14, 16, 18]:
                    if self.rest_vol == 0: break

                    tmp_vol = self.rest_vol
                    if traj_data[temp_off][j] >= limit_p:
                        if self.rest_vol > traj_data[temp_off][j + 1]:
                            self.rest_vol -= traj_data[temp_off][j + 1]
                            tmp_vol = traj_data[temp_off][j + 1]
                        else:
                            self.rest_vol = 0
                        self.total_cost += traj_data[temp_off][j] * tmp_vol
                        if debug: print(self.t, temp_off, "卖 ", traj_data[temp_off][j], tmp_vol, self.total_cost, "剩余 ", self.rest_vol)
                    else:
                        break

        self.offset += self.interval
        if self.offset >= traj_data.shape[0]: self.offset = traj_data.shape[0] - 1
        self.t += 1

        if self.t == self.T:
            if self.rest_vol > 0:
                if self.dire == 1:
                    limit_p = 100000
                    for j in [8, 6, 4, 2, 0]:
                        if self.rest_vol == 0:
                            break

                        tmp_vol = self.rest_vol
                        if traj_data[self.offset][j] <= limit_p:
                            if self.rest_vol > traj_data[self.offset][j + 1]:
                                self.rest_vol -= traj_data[self.offset][j + 1]
                                tmp_vol = traj_data[self.offset][j + 1]
                            else:
                                self.rest_vol = 0
                            self.total_cost += traj_data[self.offset][j] * tmp_vol
                            if debug: print(self.t, self.offset, "强制买 ", traj_data[self.offset][j], tmp_vol, self.total_cost, "剩余 ", self.rest_vol)
                        else:
                            break
                    if self.rest_vol > 0 and traj_data[self.offset][0] > 0:
                        self.total_cost += (traj_data[self.offset][0] + 0.01) * self.rest_vol
                        if debug: print(self.t, self.offset, "虚拟强制买 ", traj_data[self.offset][0] + 0.01, self.rest_vol, self.total_cost)
                        self.rest_vol = 0
                elif self.dire == 0:
                    limit_p = 0
                    for j in [10, 12, 14, 16, 18]:
                        if self.rest_vol == 0:
                            break

                        tmp_vol = self.rest_vol
                        if traj_data[self.offset][j] >= limit_p:
                            if self.rest_vol > traj_data[self.offset][j + 1]:
                                self.rest_vol -= traj_data[self.offset][j + 1]
                                tmp_vol = traj_data[self.offset][j + 1]
                            else:
                                self.rest_vol = 0
                            self.total_cost += traj_data[self.offset][j] * tmp_vol
                            if debug: print(self.t, self.offset, "强制卖 ", traj_data[self.offset][j], tmp_vol, self.total_cost, "剩余 ", self.rest_vol)
                        else:
                            break
                    if self.rest_vol > 0 and traj_data[self.offset][18] > 0:
                        self.total_cost += (traj_data[self.offset][18] - 0.01) * self.rest_vol
                        if debug: print(self.t, self.offset, "虚拟强制卖 ", traj_data[self.offset][18] - 0.01, self.rest_vol, self.total_cost)
                        self.rest_vol = 0

        traded_vol = self.V - self.rest_vol
        baseline_cost = self.opt_price * traded_vol
        cur_ret = 0
        cost_ratio = 0.
        if baseline_cost != 0:
            if self.dire == 1:
                cur_ret = baseline_cost - self.total_cost
            else:
                cur_ret = self.total_cost - baseline_cost
            cost_ratio = -cur_ret / baseline_cost
        step_reward = cur_ret - self.prev_reward
        self.prev_reward = cur_ret

        i = int(np.ceil(self.rest_vol / self.V * self.I))
        done = (self.t == self.T)
        if debug and done: print("交易了{} 股, 总花费：{:.2f}，基准：{:.2f}\n".format(traded_vol, self.total_cost, baseline_cost))
        if self.dire == 1:
            delta_opt = traj_data[self.offset][8] - self.opt_price
        else:
            delta_opt = self.opt_price - traj_data[self.offset][10]
        return (self.T - self.t, i, min((traj_data[self.offset][8] - traj_data[self.offset][10]) * 100, 10),
                min(delta_opt * 100, 10)), step_reward, done, {'cost': cost_ratio}

    def seed(self, seed=None):
        pass


if __name__ == '__main__':
    raw_data = np.load('000012.npz')
    # data = raw_data['data'][:2400]
    data = raw_data['data']
    """
    selected = [2107]
    for t in selected:
        print('-----', t, '-----')
        for i in range(160):
            for j in range(20):
                print(data[t][i][j], end=' ')
            print("")
    """
    env = ExeEnv(50000, 8, 4, 4, data)
    """
    ob = env.reset()
    print(ob)
    r = 0
    c = 0
    ep_r = 0
    ct = 0
    for i in range(40):
        for _ in range(4):
            ob, rwd, don, info = env.step(0.0)
            print(ob)
            r += rwd
            ep_r += rwd
            if don:
                c += 1
                ct += info['cost']
                env.reset()
                ep_r = 0
    print(c, r / c, ct / c)
    """




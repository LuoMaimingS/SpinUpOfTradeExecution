import gym
import numpy as np


class ExeEnv(gym.Env):
    def __init__(self, V, H, T, I, data, dire=1):
        self.V = V
        self.H = H
        self.T = T
        self.I = I
        self.data = data
        self.dire = dire
        self.N = data.shape[0]
        length = H * 20
        self.interval = int(length / T)
        print(self.interval)
        print("Initializing Executing Environment, {} trajectories.".format(self.N))

        self.observation_space = gym.spaces.Box(low=0, high=T, shape=(2,))
        self.action_space = gym.spaces.Box(-0.05, 0.05, (1,))

        self.p = -1

        self.t = 0
        self.offset = 0
        self.rest_vol = 0
        self.base_cost = 0.
        self.total_cost = 0.
        self.opt_price = 0.
        self.prev_reward = 0.

    def reset(self, rolling=True):
        self.p = self.p + 1 if rolling else self.p
        if self.p >= self.N: self.p = 0

        self.t = 0
        self.offset = 0
        self.rest_vol = self.V
        self.base_cost = 0.
        self.total_cost = 0.

        a = self.data[self.p][self.offset][10]
        if self.data[self.p][self.offset][8] != 0: a = self.data[self.p][self.offset][8]
        b = self.data[self.p][self.offset][8]
        if self.data[self.p][self.offset][10] != 0: b = self.data[self.p][self.offset][10]
        # self.opt_price = (self.data[self.p][self.offset][8] + self.data[self.p][self.offset][10]) / 2
        self.opt_price = (a + b) / 2
        self.prev_reward = 0.
        return np.array((self.t, self.I))

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
                        if debug: print("买 ", traj_data[temp_off][j], tmp_vol, self.total_cost)
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
                        if debug: print("卖 ", traj_data[temp_off][j], tmp_vol, self.total_cost)
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
                            if debug: print("买 ", traj_data[self.offset][j], tmp_vol, self.total_cost)
                        else:
                            break
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
                            if debug: print("卖 ", traj_data[self.offset][j], tmp_vol, self.total_cost)
                        else:
                            break

        traded_vol = self.V - self.rest_vol
        baseline_cost = self.opt_price * traded_vol
        if debug: print('baseline cost: ', baseline_cost)
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

        i = int(np.ceil(self.rest_vol / self.V) * self.I)
        done = (self.t == self.T)
        return (self.T - self.t, i), step_reward, done, {'cost': cost_ratio}

    def seed(self, seed=None):
        pass


if __name__ == '__main__':
    raw_data = np.load('000012.npz')
    data = raw_data['data'][:2400]
    """
    selected = [2107]
    for t in selected:
        print('-----', t, '-----')
        for i in range(160):
            for j in range(20):
                print(data[t][i][j], end=' ')
            print("")
    """
    env = ExeEnv(10000, 2, 4, 4, data)
    ob = env.reset()
    a = env.action_space.sample()
    r = 0
    c = 0
    ep_r = 0
    ct = 0
    for i in range(2400):
        for _ in range(4):
            ob, rwd, don, info = env.step(0.0)
            r += rwd
            ep_r += rwd
            if don:
                c += 1
                ct += info['cost']
                env.reset()
                if np.abs(ep_r) > 200: print(i)
                ep_r = 0
    print(r / c, ct / c)








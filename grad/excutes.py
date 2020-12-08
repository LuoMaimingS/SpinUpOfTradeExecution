import numpy as np
import math


def executeSL(V, H,
              T, I,
              data,
              dire=1,
              stat_len=-1):

    if stat_len == -1: stat_len = data.shape[0]
    costs = []

    for t in range(stat_len):
        traj_data = data[t]
        assert traj_data.shape[1] == 20
        mid_price = (traj_data[0][8] + traj_data[0][10]) / 2
        length = H * 20
        offset = 0

        total_cost = 0.0
        rest_vol = V
        for i in range(0, length // 2, 2):
            if dire == 1:
                limit_p = mid_price
                # print(tmp_vol, limit_p)
                for j in [8, 6, 4, 2, 0]:
                    if rest_vol == 0:
                        break

                    tmp_vol = rest_vol
                    if traj_data[offset][j] <= limit_p:
                        if rest_vol > traj_data[offset][j + 1]:
                            rest_vol -= traj_data[offset][j + 1]
                            tmp_vol = traj_data[offset][j + 1]
                        else:
                            rest_vol = 0
                        total_cost += traj_data[offset][j] * tmp_vol
                    else:
                        break
            elif dire == 0:
                limit_p = mid_price
                # print(tmp_vol, limit_p)
                for j in [10, 12, 14, 16, 18]:
                    if rest_vol == 0:
                        break

                    tmp_vol = rest_vol
                    if traj_data[offset][j] >= limit_p:
                        if rest_vol > traj_data[offset][j + 1]:
                            rest_vol -= traj_data[offset][j + 1]
                            tmp_vol = traj_data[offset][j + 1]
                        else:
                            rest_vol = 0
                        total_cost += traj_data[offset][j] * tmp_vol
                    else:
                        break

            offset += 2

        if offset >= traj_data.shape[0]: offset = traj_data.shape[0] - 1
        if rest_vol > 0:
            if dire == 1:
                limit_p = 100000
                for j in [8, 6, 4, 2, 0]:
                    if rest_vol == 0:
                        break

                    tmp_vol = rest_vol
                    if traj_data[offset][j] <= limit_p:
                        if rest_vol > traj_data[offset][j + 1]:
                            rest_vol -= traj_data[offset][j + 1]
                            tmp_vol = traj_data[offset][j + 1]
                        else:
                            rest_vol = 0
                        total_cost += traj_data[offset][j] * tmp_vol
                    else:
                        break
            elif dire == 0:
                limit_p = 0
                for j in [10, 12, 14, 16, 18]:
                    if rest_vol == 0:
                        break

                    tmp_vol = rest_vol
                    if traj_data[offset][j] >= limit_p:
                        if rest_vol > traj_data[offset][j + 1]:
                            rest_vol -= traj_data[offset][j + 1]
                            tmp_vol = traj_data[offset][j + 1]
                        else:
                            rest_vol = 0
                        total_cost += traj_data[offset][j] * tmp_vol
                    else:
                        break

        traded_vol = V - rest_vol
        baseline_cost = mid_price * traded_vol
        if baseline_cost != 0:
            if dire == 1:
                cur_cost = (total_cost - baseline_cost) / baseline_cost
            else:
                cur_cost = (baseline_cost - total_cost) / baseline_cost
            costs.append(cur_cost)

    avg_cost = np.mean(costs)
    return np.round(avg_cost * 10000, 2)



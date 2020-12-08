import h5py
import numpy as np
import tqdm


def load(sym):
    symbol = sym + ".XSHE"
    default_path = 'D:\\0\Virtual-Stock\\data\\tick_data\\'
    default_path = default_path + symbol + ".h5"
    tb = h5py.File(default_path, 'r')

    data = tb[symbol]
    # ['a1', 'a1_v', 'a2', 'a2_v', 'a3', 'a3_v', 'a4', 'a4_v', 'a5', 'a5_v',
    # 'b1', 'b1_v', 'b2', 'b2_v', 'b3', 'b3_v', 'b4', 'b4_v', 'b5', 'b5_v',
    # 'datetime', 'high', 'last', 'low', 'volume' 'amount']

    n = len(data['last'])

    saved = np.zeros((4000, 160, 20))
    temp_mat = np.zeros((160, 20))

    a1 = data['a1']
    a1v = data['a1_v']
    a2 = data['a2']
    a2v = data['a2_v']
    a3 = data['a3']
    a3v = data['a3_v']
    a4 = data['a4']
    a4v = data['a4_v']
    a5 = data['a5']
    a5v = data['a5_v']

    b1 = data['b1']
    b1v = data['b1_v']
    b2 = data['b2']
    b2v = data['b2_v']
    b3 = data['b3']
    b3v = data['b3_v']
    b4 = data['b4']
    b4v = data['b4_v']
    b5 = data['b5']
    b5v = data['b5_v']

    rec = 0
    count = 0
    for i in tqdm.tqdm(range(n)):
        dt = data['datetime'][i]
        clock = int(dt % 1e9 // 100000)
        if clock < 945 or clock > 1445:
            temp_mat = np.zeros((160, 20))
            count = 0
            continue
        temp_mat[count] = [a5[i], a5v[i], a4[i], a4v[i], a3[i], a3v[i], a2[i], a2v[i], a1[i], a1v[i],
                           b1[i], b1v[i], b2[i], b2v[i], b3[i], b3v[i], b4[i], b4v[i], b5[i], b5v[i]]
        count += 1
        if count == 160:
            count = 0
            saved[rec] = temp_mat
            rec += 1

        # saved[i] = [i, a5[i], a5v[i], a4[i], a4v[i], a3[i], a3v[i], a2[i], a2v[i], a1[i], a1v[i],
        #             b1[i], b1v[i], b2[i], b2v[i], b3[i], b3v[i], b4[i], b4v[i], b5[i], b5v[i],
        #             data['datetime'][i]]

    print(rec)
    saved = saved[:rec]
    print(saved.shape)
    save_file = sym
    np.savez(save_file, data=saved)


def main():
    load('000025')


if __name__ == '__main__':
    main()

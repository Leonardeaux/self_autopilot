import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_track_plot(track_name: str):
    track_path = f'racetrack-database-master/tracks/{track_name}.csv'
    df = pd.read_csv(track_path)

    df = df.drop(['w_tr_right_m', 'w_tr_left_m'], axis=1)

    track_path2 = f'racetrack-database-master/racelines/{track_name}.csv'
    df2 = pd.read_csv(track_path2)

    lap_path = f'lap/first.csv'
    df3 = pd.read_csv(lap_path)

    df_np = df.to_numpy()
    df_np2 = df2.to_numpy()
    df_np3 = df3.to_numpy()

    df_np = np.append(df_np, [df_np[0]], axis=0)
    df_np2 = np.append(df_np2, [df_np2[0]], axis=0)

    xs, ys = zip(*df_np)
    x, y = zip(*df_np2)
    x_, y_ = zip(*df_np3)

    # fig, axs = plt.subplots(2)
    plt.figure()
    plt.plot(xs, ys, 'tab:orange', label='track')
    plt.plot(x, y, 'tab:green', label='raceline')
    plt.plot(x_, y_, 'tab:red', label='lapline')
    plt.legend(loc="upper right")
    plt.show()


get_track_plot('Melbourne')
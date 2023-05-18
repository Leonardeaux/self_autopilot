import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_track_plot(track_name: str) -> None:
    """Get the layout of a formula 1 circuit"""
    track_path = f'racetrack-database-master/tracks/{track_name}.csv'
    df = pd.read_csv(track_path)

    df = df.drop(['w_tr_right_m', 'w_tr_left_m'], axis=1)

    df_np = df.to_numpy()

    df_np = np.append(df_np, [df_np[0]], axis=0)

    xs, ys = zip(*df_np)

    # fig, axs = plt.subplots(2)
    plt.figure()
    plt.plot(xs, ys, 'tab:orange', label='track')
    plt.legend(loc="upper right")
    plt.show()
from pathlib import Path
import csv
import numpy as np
from mindpong.model.player import PlayerName


def get_available_games():
    p = Path("History/")
    if not p.is_dir():
        raise FileNotFoundError("The directory History does not exist")
    return [x.parts[1] for x in Path("History/").iterdir() if x.is_dir()]


def read_player_signal(game_name: str, player_name: str):
    file_path = Path('History/%s/%s' %
                     (game_name, player_name)).with_suffix('.csv')
    signals = [[] for _ in range(7)]
    last_not_nan_val = [0] * 7
    headers = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(list(reader)):
            if i is not 0:
                for j in range(0, len(row)):
                    data = row[j]
                    if data == 'nan':
                        signals[j].append(last_not_nan_val[j])
                    else:
                        last_not_nan_val[j] = data
                        signals[j].append(data)
            else:
                headers = row[0:-1]
        signals = [np.array(signal).astype(np.float) for signal in signals]
    return {headers[i]: signals[i] for i in range(len(headers))}

from lib import elo

import os

def ranking(times = 3, output_index = [1, 5, 9, 13, 17, 20]):
    """

    :return:
    """
    ranking_system = elo.RankingSystem()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    ranking_data_folder = os.path.join(current_dir, 'data/ranking')
    filenames = [f for f in os.listdir(ranking_data_folder) if os.path.isfile(os.path.join(ranking_data_folder, f))]
    for round in range(times):
        ranking_system.set_round(round + 1)
        for filename in filenames:
            file_path = os.path.join(ranking_data_folder, filename)
            with open(file_path, 'r') as input:
                input.readline()
                line = input.readline()
                while line:
                    segs = line.split(',')
                    segs = [seg.strip() for seg in segs]
                    [id1, id2, result] = segs
                    result = float(result)

                    ranking_system.add_comparison(id1, id2, result)
                    line = input.readline()

    ranking_system.output_result(output_index)


if __name__ == '__main__':
    ranking(20, [1, 5, 9, 13, 17, 20])
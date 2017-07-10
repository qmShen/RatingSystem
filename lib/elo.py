import json

class EloRank:
    def __init__(self, k = 32):
        self.k = k

    def setKFactor(self, k):
        self.k = k

    def getKFactor(self):
        return self.k

    def getExpected(self, a, b):
        return 1 / (1 + 10 ** ((b - a) / 400))

    def updateRatingWithExpected(self, expected, actual, current):
        return current + self.k * (actual - expected)

    def updateRating(self, play_a, play_b, sign):
        # sign == 1
        r = 1 if sign == 1 else 0 if sign == 0 else 0.5
        # print("Input : ", play_a, play_b)
        expected_a = self.getExpected(play_a, play_b)
        expected_b = self.getExpected(play_b, play_a)

        result_a = self.updateRatingWithExpected(expected_a, r, play_a)
        result_b = self.updateRatingWithExpected(expected_b, (1 - r), play_b)
        return result_a, result_b


class RankingSystem:

    def __init__(self):
        self.id_2_rating = {}
        self.init_rating = 1000
        self.rating_system = EloRank()
        self.current_round = 1
        pass

    def add_comparison(self, id1, id2, result):
        """

        :param id1:  first item
        :param id2:  second item
        :param result: comparison result, 0 id1 is better,  1 equal, 2 id2 is better
        :return:
        """
        r = 1 if result == 0 else 0 if result == 2 else 0.5 if result == 1 else "Illegal"


        if r == "Illegal":
            print('Illegal comparison', result, r)
            return None

        if id1 not in self.id_2_rating:
            self.id_2_rating[id1] = {}

        if self.current_round not in self.id_2_rating[id1]:
            if self.current_round == 1:
                self.id_2_rating[id1][self.current_round] = self.init_rating
            else:
                self.id_2_rating[id1][self.current_round] = self.id_2_rating[id1][self.current_round - 1]


        if id2 not in self.id_2_rating:
            self.id_2_rating[id2] = {}
        if self.current_round not in self.id_2_rating[id2]:
            if self.current_round == 1:
                self.id_2_rating[id2][self.current_round] = self.init_rating
            else:
                self.id_2_rating[id2][self.current_round] = self.id_2_rating[id2][self.current_round - 1]

        rating1, rating2 = self.id_2_rating[id1][self.current_round], self.id_2_rating[id2][self.current_round]
        update1, update2 = self.rating_system.updateRating(rating1, rating2, r)

        self.id_2_rating[id1][self.current_round] = update1
        self.id_2_rating[id2][self.current_round] = update2


    def output_result(self, rounds = [1], sort_index = 1):
        rating_list = []
        for id in self.id_2_rating:
            rating_list.append({'id': id, 'rating': self.id_2_rating[id]})

        results = sorted(rating_list, key= lambda x:x['rating'][self.current_round], reverse = True)

        with open('result.csv', 'w') as output:
            head = ",".join(["id"] + ["round_" + str(round) for round in rounds])
            output.write(head+'\n')
            for rating_dict in results:
                output_string = str(rating_dict['id'])
                _rd = rating_dict['rating']
                for index in rounds:

                    if index not in _rd:
                        continue
                    output_string += (',' + str(_rd[index]))

                output_string += "\n"

                output.write(output_string)

    def set_round(self, round):
        self.current_round = round

if __name__ == "__main__":
    elo = EloRank()
    play_a = 1613

    update_a, update_b = elo.updateRating(play_a, 1613, 0)

    print(update_a, update_b)

    update_a, update_b = elo.updateRating(1613, play_a, 1)

    print(update_a, update_b)

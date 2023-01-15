import math


class Elo:
    def __init__(self, ratings=None, denom=1.0):
        if not ratings:
            ratings = {}
        self.__ratings = ratings
        self.__denom = denom

    # expected score of player 1
    def expected_score(self, player1, player2):
        r1 = self.__ratings[player1]
        r2 = self.__ratings[player2]
        return 1/(1 + math.e**((r2 - r1)/self.__denom))

    def add_match(self, player1, player2, result, k=0.1, default_rating=0):
        if player1 not in self.__ratings:
            self.__ratings[player1] = default_rating
        if player2 not in self.__ratings:
            self.__ratings[player2] = default_rating

        e1 = self.expected_score(player1, player2)
        e2 = 1 - e1
        self.__ratings[player1] = self.__new_rating(
                self.__ratings[player1], result, e1, k)
        self.__ratings[player2] = self.__new_rating(
                self.__ratings[player2], 1 - result, e2, k)

    def add_matches(self, matches: list, k=0.1, default_rating=0):
        for m in matches:
            player1, player2, result = m
            self.add_match(player1, player2, result, k, default_rating)

    def ratings(self):
        return self.__ratings
 
    def rating(self, player):
        return self.__ratings[player]

    def items(self):
        return list(self.__ratings.keys())

    def rankings(self):
        players = sorted(self.__ratings)
        players_sorted = sorted(players, key=self.__ratings.get, reverse=True)
        return {u: r for r, u in enumerate(players_sorted)}

    def ranking(self, player):
        return self.rankings()[player]

    def __new_rating(
            self,
            current_rating: float,
            real_score: float,
            expected_score: float,
            k: int):
        return current_rating + k*(real_score - expected_score)

from enum import Enum

class Answer(Enum):
    left = "left"
    right = "right"
    equal = "equal"

class Player(Enum):
    player_a = "playerA"
    player_b = "playerB"

class Result(Enum):
    win = 1
    lose = 0
    tie = 0.5

def expected_score(ra, rb):
    return 1/(1 + 10**((ra - rb)/400))

def update_rating(r: float, real_score: float,
        expected_score:float, k_value: int):
    return r + k_value*(real_score - expected_score)

def make_match(task: dict, answer: dict):
    """ make a single elo match for a task and its corresponding answer """
    elo_match = {}
    elo_match[Player.player_a] = task["tweet1"]
    elo_match[Player.player_b] = task["tweet2"]

    if answer["answer"][0]["selection"] == Answer.left.value:
        elo_match["SA"] = Result.win.value
        elo_match["SB"] = Result.lose.value

    elif answer["answer"][0]["selection"] == Answer.right.value:
        elo_match["SA"] = Result.lose.value
        elo_match["SB"] = Result.win.value

    elif answer["answer"][0]["selection"] == Answer.equal.value:
        elo_match["SA"] = Result.tie.value
        elo_match["SB"] = Result.tie.value

    else:
        print(answer)
        print(elo_match)
        raise RuntimeError("bad match")

    return elo_match

def elo(match: dict, ratings, k):
    updated_ratings = ratings#.copy()
    tweet_id_a = match[Player.player_a]
    tweet_id_b = match[Player.player_b]
    ea = expected_score(updated_ratings[tweet_id_b],
            updated_ratings[tweet_id_a])
    eb = expected_score(updated_ratings[tweet_id_a],
            updated_ratings[tweet_id_b])
    updated_ratings[tweet_id_a] = update_rating(
            updated_ratings[tweet_id_a], match["SA"], ea, k)
    updated_ratings[tweet_id_b] = update_rating(
            updated_ratings[tweet_id_b], match["SB"], eb, k)

    return updated_ratings

def ratings_distance(rating1, rating2):
    if set(rating1) != set(rating2):
        raise RuntimeError("conversations are different!")
    size = len(rating1)
    return sum([(rating1[tid] - rating2[tid])**2 for tid in rating1])/size

def rankings_distance(rating1, rating2):
    if set(rating1) != set(rating2):
        raise RuntimeError("conversations are different!")
    root_tweet_ids = sorted(set(rating1))
    size = len(rating1)

    rankings1 = get_ranking(rating1)
    rankings2 = get_ranking(rating2)
    return sum((rankings2[u] - rankings1[u])**2 for u in root_tweet_ids)/size

def get_ranking(rating):
    root_tweet_ids = sorted(set(rating))
    convs_sorted = sorted(root_tweet_ids, key=rating.get, reverse=True)
    return {u: r for r, u in enumerate(convs_sorted)}

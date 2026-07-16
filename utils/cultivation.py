RANKS = [
    ("Disciple", 0),
    ("Inner Gate Disciple", 1500),
    ("Core Disciple", 5000),
    ("Elder", 12000),
    ("Grand Elder", 25000),
    ("Sect Master", 50000),
]

def get_current_rank(xp):
    current_rank = RANKS[0][0]

    for rank_name, required_xp in RANKS:
        if xp >= required_xp:
            current_rank = rank_name
        else:
            break

    return current_rank


def get_next_rank(xp):

    for rank_name, required_xp in RANKS:
        if xp < required_xp:
            xp_remaining = required_xp - xp
            return rank_name, xp_remaining

    return "Maximum Rank", 0
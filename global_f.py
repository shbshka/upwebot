import random
from files import cards
from cards import score_assigner, start_cards, study_again


# ----- Глобальные функции -----
def randomizer(item):
    key = [str(x) for x in range(len(item))]
    random.shuffle(key)
    return key


async def reset():
    score = 0
    qs = []
    cards_pool = []
    n = -1
    bad = []
    try_again = []
    good = []
    awesome = []

# modify to make every card separate
def set_card(score, bad, try_again, good, awesome):
    card = list(cards.values())
    for item in card:
        scores = score_assigner(item, score, bad, try_again, good, awesome)
        face_pool, back_pool = start_cards(scores)
        bad_score, try_again_score, good_score, awesome_score = study_again(scores, cards)
    return scores, face_pool, back_pool, card
from files import cards


def score_assigner(card, score, bad, try_again, good, awesome):
    scores = {"bad": bad, "try again": try_again, "good": good, "awesome": awesome}
    # retrieve score for a card and assign it to a deck
    if score == 0 and card not in bad:
        bad.append(card)
        try:
            try_again.remove(card)
        except ValueError:
            pass
        try:
            good.remove(card)
        except ValueError:
            pass
        try:
            awesome.remove(card)
        except ValueError:
            pass
    elif score == 1 and card not in try_again:
        try_again.append(card)
        try:
            bad.remove(card)
        except ValueError:
            pass
        try:
            good.remove(card)
        except ValueError:
            pass
        try:
            awesome.remove(card)
        except ValueError:
            pass
    elif score == 2 and card not in good:
        good.append(card)
        try:
            bad.remove(card)
        except ValueError:
            pass
        try:
            try_again.remove(card)
        except ValueError:
            pass
        try:
            awesome.remove(card)
        except ValueError:
            pass
    elif score == 3 and card not in awesome:
        try:
            bad.remove(card)
        except ValueError:
            pass
        try:
            try_again.remove(card)
        except ValueError:
            pass
        try:
            good.remove(card)
        except ValueError:
            pass
        awesome.append(card)
    print(scores)
    return scores


def study_again(scores, anki_cards):
    # keys for a dictionary of cards
    bad_score = 0
    try_again_score = 0
    good_score = 0
    awesome_score = 0
    # for item in a dictionary
    for card in anki_cards.keys():
        # for item in a dictionary of lists
        for key in scores:
            # for item in keys of every card
            if key in scores["bad"]:
                bad_score += 1
            if key in scores["try again"]:
                try_again_score += 1
            if key in scores["good"]:
                good_score += 1
            if key in scores["awesome"]:
                awesome_score += 1

    return bad_score, try_again_score, good_score, awesome_score


def start_cards(scores):
    inner_face_pool = []
    inner_back_pool = []

    for key in ("bad", "try again", "good", "awesome"):
        for d in scores[key]:
            inner_face_pool.append(d["face"])
            inner_back_pool.append(d["back"])

    return inner_face_pool, inner_back_pool




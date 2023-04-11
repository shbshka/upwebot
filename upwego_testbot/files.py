import json

# ----- Файлы для работы -----
with open("./jsons/vocabulary.json", "r") as f_voc:
    vocabulary = json.load(f_voc)
with open("./jsons/schedule.json", "rb") as f_sch:
    schedule = json.load(f_sch)
with open("./jsons/grammar.json", "r") as f_gram:
    grammar = json.load(f_gram)
with open("./jsons/cs.json", "r") as f_cs:
    cs = json.load(f_cs)
with open("./jsons/cards.json", "r", encoding="utf-8") as f_cards:
    cards = json.load(f_cards)
with open("./jsons/registred_users.json", "r", encoding="utf-8") as f_registred_users:
    registred_users = json.load(f_registred_users)

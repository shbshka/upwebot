import json

# ----- Файлы для работы -----
with open("./vocabulary.json", "r") as f_voc:
    vocabulary = json.load(f_voc)
with open("schedule.json", "rb") as f_sch:
    schedule = json.load(f_sch)
with open("./grammar.json", "r") as f_gram:
    grammar = json.load(f_gram)
with open("./cs.json", "r") as f_cs:
    cs = json.load(f_cs)
with open("./cards.json", "r", encoding="utf-8") as f_cards:
    cards = json.load(f_cards)

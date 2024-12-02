import os


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "statics")
EQUIPMENTS_PATH = os.path.join(STATIC_PATH, "equipments.json")
HEROES_PATH = os.path.join(STATIC_PATH, "heroes.json")
AUGMENTS_PATH = os.path.join(STATIC_PATH, "hex.json")
EVOLUTIONS_PATH = os.path.join(STATIC_PATH, "goop.json")
IMAGE_PATH = os.path.join(STATIC_PATH, "images")


"""
Some game settings
"""
# the interval after each operation, note: the smaller the value, the faster the operation, but with a higher risk
INTERVAL = 0.3

# the special items in candidates
SPECIAL_CANDIDATES = {
    "基础装备锻造器",
    "成装锻造器",
    "神器锻造器",
    "辅助装备锻造器",
    "金蛋"
}

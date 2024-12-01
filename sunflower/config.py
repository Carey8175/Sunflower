import os


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "statics")
EQUIPMENTS_PATH = os.path.join(STATIC_PATH, "equipments.json")
HEROES_PATH = os.path.join(STATIC_PATH, "heroes.json")
AUGMENTS_PATH = os.path.join(STATIC_PATH, "hex.json")
EVOLUTIONS_PATH = os.path.join(STATIC_PATH, "goop.json")
IMAGE_PATH = os.path.join(STATIC_PATH, "images")

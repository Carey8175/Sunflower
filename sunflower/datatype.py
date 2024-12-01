from sunflower.adb import BoundingBox, OcrResult
from enum import auto, StrEnum
from dataclasses import dataclass


class GameState(StrEnum):
    """
    An enum representing the current state of the game.
    """
    # in the main menu
    MAIN_MENU = auto()
    # the mode choose menu
    MODE_CHOOSE_MENU = auto()
    # in the game room
    ROOM = auto()
    # in the game
    IN_GAME = auto()


class SpecificArea:
    """
    A class representing a specific area on the screen.
    """
    # main menu ---------------------------------------------------------------
    NAME = BoundingBox(700, 15, 210, 30)

    # IN GAME -----------------------------------------------------------------
    PERIOD = BoundingBox(320, 0, 60, 30)
    COIN = BoundingBox(490, 550, 60, 30)
    LEVEL = BoundingBox(70, 550, 60, 30)
    EVOLVE = BoundingBox(240, 600, 250, 30)

    # PLAYERS = BoundingBox(850, 50, 150, 440)
    PLAYERS: list[BoundingBox] = [
        BoundingBox(850, 55 + i*53, 120, 55) for i in range(8)
    ]

    AUGMENTS: list[BoundingBox] = [
        BoundingBox(200, 280, 80, 25),       # augment 1 button
        BoundingBox(460, 280, 80, 25),       # augment 2 button
        BoundingBox(730, 280, 80, 25),       # augment 3 button
    ]

    BOARD: list[list[BoundingBox]] = [
        [BoundingBox(290 + i*65, 265, 50, 25) for i in range(7)],
        [BoundingBox(310 + i*65, 310, 50, 25) for i in range(7)],
        [BoundingBox(270 + i*70, 355, 50, 25) for i in range(7)],
        [BoundingBox(295 + i*77, 405, 50, 25) for i in range(7)],
    ]

    CANDIDATES: list[BoundingBox] = [
        BoundingBox(205 + i * 72, 490, 40, 40) for i in range(9)
    ]

    CHESS_PRICE: BoundingBox = BoundingBox(850, 100, 50, 20)
    CHESS_NAME: BoundingBox = BoundingBox(830, 75, 120, 25)
    CIRCLE_PLACE = BoundingBox(510, 425, 10, 10)
    CHESS_STAR = BoundingBox(860, 40, 70, 30)

    CHESS_EQUIPMENTS: list[BoundingBox] = [
        BoundingBox(790 + i*80, 410, 50, 50) for i in range(3)
    ]


class SpecificButton:
    """
    A class representing a specific button area on the screen which can be clicked.
    """
    # main menu ---------------------------------------------------------------
    PROFILE = BoundingBox(5, 630, 70, 70)      # profile button, down left corner
    START_MAIN = BoundingBox(880, 560, 150, 150)       # start button, down right corner

    # mode choose menu --------------------------------------------------------
    START_MODE = BoundingBox(820, 640, 195, 70)       # start button, down right corner

    # room --------------------------------------------------------------------
    START_ROOM = START_MODE      # start button, down right corner
    ACCEPT_COMBAT = BoundingBox(440, 460, 140, 50)       # accept combat button, down right corner
    RETURN_BOARD = START_MODE      # return board button, down right corner,

    # in game -----------------------------------------------------------------
    BUY_XP = BoundingBox(80, 600, 130, 50)       # buy xp button
    ROLL = BoundingBox(80, 655, 130, 50)       # roll button
    CHOOSE_HP = BoundingBox(950, 480, 50, 50)       # choose hp button
    CHESS_SELL = BoundingBox(830, 480, 120, 30)       # chess sell button

    ROLL_AUGMENTS: list[BoundingBox] = [
        BoundingBox(207, 468, 90, 30),       # roll augment 1 button
        BoundingBox(475, 468, 90, 30),       # roll augment 2 button
        BoundingBox(740, 468, 90, 30),       # roll augment 3 button
    ]

    STORE_HERO: list[BoundingBox] = [
        BoundingBox(220, 680, 80, 40),       # store hero 1 button
        BoundingBox(365, 680, 80, 40),       # store hero 2 button
        BoundingBox(510, 680, 80, 40),       # store hero 3 button
        BoundingBox(665, 680, 80, 40),       # store hero 4 button
        BoundingBox(805, 680, 80, 40),       # store hero 5 button
    ]

    CHOOSE_EQUIPMENT = BoundingBox(10, 160, 50, 100)       # choose equipment button
    EQUIPMENT: list[BoundingBox] = [
        BoundingBox(65, 55, 60, 60),       # equipment 1 button
        BoundingBox(65, 117, 60, 60),       # equipment 2 button
        BoundingBox(65, 179, 60, 60),       # equipment 3 button
        BoundingBox(65, 241, 60, 60),       # equipment 4 button
        BoundingBox(65, 303, 60, 60),       # equipment 5 button
        BoundingBox(140, 55, 60, 60),       # equipment 6 button
        BoundingBox(140, 117, 60, 60),       # equipment 7 button
        BoundingBox(140, 179, 60, 60),       # equipment 8 button
        BoundingBox(140, 241, 60, 60),       # equipment 9 button
        BoundingBox(140, 303, 60, 60),       # equipment 10 button
    ]

    EVOLVE = BoundingBox(780, 600, 110, 50)
    EVOLVE_ROLL = BoundingBox(780, 655, 110, 50)

    EXIT_NOW = BoundingBox(320, 610, 150, 50)  # exit now button, down right corner

    # result menu -------------------------------------------------------------
    NEXT_STEP = BoundingBox(810, 660, 120, 50)   # next step button, down right corner


@dataclass
class BasicGameInfo:
    coin: int
    level: int
    period: tuple
    store: list[str]


@dataclass
class Chess:
    name: str
    star: int
    location: tuple
    is_candidate: bool
    equipments: list[str | None]

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
        BoundingBox(850, 50, 150, 60),       # player 1
        BoundingBox(850, 103, 150, 60),       # player 2
        BoundingBox(850, 156, 150, 60),       # player 3
        BoundingBox(850, 209, 150, 60),       # player 4
        BoundingBox(850, 262, 150, 60),       # player 5
        BoundingBox(850, 315, 150, 60),       # player 6
        BoundingBox(850, 368, 150, 60),       # player 7
        BoundingBox(850, 421, 150, 60),       # player 8
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

    EVOLVE = BoundingBox(700, 580, 150, 100)
    # EVOLVE_ROLL = BoundingBox(70, 600, 60, 30)

    EXIT_NOW = BoundingBox(430, 600, 170, 70)  # exit now button, down right corner

    # result menu
    NEXT_STEP = BoundingBox(810, 660, 120, 50)   # next step button, down right corner


@dataclass
class BasicGameInfo:
    coin: int
    level: int
    period: tuple
    store: list[str]
import asyncio

from sunflower.adb import AdbOCR
from sunflower.config import INTERVAL
from sunflower.datatype import SpecificButton, SpecificArea


class MainMenu:
    @staticmethod
    async def start_game(app: AdbOCR):
        await app.click(*SpecificButton.START_MAIN.get_middle_coordinate())

    @staticmethod
    async def setting(app: AdbOCR):
        await app.click(*SpecificButton.SETTING_MAIN.get_middle_coordinate())


class ModeChooseMenu:
    @staticmethod
    async def start_game(app: AdbOCR):
        await app.click(*SpecificButton.START_MODE.get_middle_coordinate())


class RoomMenu:
    @staticmethod
    async def start_game(app: AdbOCR):
        await app.click(*SpecificButton.START_ROOM.get_middle_coordinate())

    async def accept_combat(app: AdbOCR):
        await app.click(*SpecificButton.ACCEPT_COMBAT.get_middle_coordinate())


class InGame:
    @staticmethod
    async def setting(app: AdbOCR):
        await app.go_back()

    @staticmethod
    async def exit_game(app: AdbOCR):
        pass

    @staticmethod
    async def buy_xp(app: AdbOCR):
        await app.click(*SpecificButton.BUY_XP.get_middle_coordinate())

    @staticmethod
    async def roll(app: AdbOCR):
        await app.click(*SpecificButton.ROLL.get_middle_coordinate())

    @staticmethod
    async def sell_chess(app: AdbOCR, location: tuple):
        if len(location) == 2:
            await app.click(*SpecificArea.BOARD[location[0]][location[1]].get_middle_coordinate())
        else:
            await app.click(*SpecificArea.CANDIDATES[location[0]].get_middle_coordinate())

        await asyncio.sleep(INTERVAL)
        await app.click(*SpecificButton.CHESS_SELL.get_middle_coordinate())

    @staticmethod
    async def move_chess(app: AdbOCR, location: tuple, target: tuple):
        if len(location) == 2:
            location = SpecificArea.BOARD[location[0]][location[1]].get_middle_coordinate()
        else:
            location = SpecificArea.CANDIDATES[location[0]].get_middle_coordinate()

        if len(target) == 2:
            target = SpecificArea.BOARD[target[0]][target[1]].get_middle_coordinate()
        else:
            target = SpecificArea.CANDIDATES[target[0]].get_middle_coordinate()

        await app.swipe(*location, *target, duration=400)

    @staticmethod
    async def roll_augment(app: AdbOCR, index: int):
        await app.click(*SpecificButton.ROLL_AUGMENTS[index].get_middle_coordinate())

    @staticmethod
    async def choose_augment(app: AdbOCR, index: int):
        await app.click(*SpecificArea.AUGMENTS[index].get_middle_coordinate())

    @staticmethod
    async def buy_chess(app: AdbOCR, index: int):
        await app.click(*SpecificButton.STORE_HERO[index].get_middle_coordinate())


class ResultMenu:
    @staticmethod
    async def next_step(app: AdbOCR):
        await app.click(*SpecificButton.NEXT_STEP.get_middle_coordinate())


class SunflowerControl:
    MainMenu = MainMenu
    ModeChooseMenu = ModeChooseMenu
    RoomMenu = RoomMenu
    InGame = InGame
    ResultMenu = ResultMenu
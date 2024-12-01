import asyncio
from numpy import ndarray
from loguru import logger
from sunflower.adb import AdbOCR, BoundingBox
from sunflower.utils import SunflowerUtils
from sunflower.datatype import GameState, SpecificArea, SpecificButton, BasicGameInfo


class SunflowerCatcher(AdbOCR):
    def __init__(self):
        super().__init__()

    async def get_user_name(self, game_state: GameState) -> str | None:
        """
        Get the user name from the device by ocr.
        :return:
        """
        if game_state != GameState.MAIN_MENU:
            logger.warning("The game state is not main menu. Cannot get user name.")
            return None

        # click profile button
        await self.click(*SpecificButton.PROFILE.get_middle_coordinate())
        await asyncio.sleep(1)

        # ocr the name
        name = await self.get_screen_text(SpecificArea.NAME)
        if not name:
            logger.warning("The user name is not found.")
            return None

        # return main menu
        await self.go_back()

        return name[0].text

    async def get_screen_box(self, area: BoundingBox) -> ndarray | None:
        """
        Get the screen of the device.
        :return:
        """
        screen = await self.get_screen()
        if area:
            screen = screen[area.y:area.y + area.height, area.x:area.x + area.width]

        return screen

    async def get_coin(self, game_state: GameState) -> int | None:
        """
        Get the coin from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get coin.")
            return None

        # ocr the coin
        coin = await self.get_screen_text(SpecificArea.COIN)
        if not coin:
            logger.warning("The coin is not found.")
            return None

        return int(coin[0].text)

    async def get_level(self, game_state: GameState) -> int | None:
        """
        Get the level from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get level.")
            return None

        # ocr the level
        level = await self.get_screen_text(SpecificArea.LEVEL)
        if not level:
            logger.warning("The level is not found.")
            return None

        level = level[0].text.replace('级', '')

        return int(level)

    async def get_period(self, game_state: GameState) -> tuple | None:
        """
        Get the period from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get period.")
            return None

        # ocr the period
        period = await self.get_screen_text(SpecificArea.PERIOD)
        if not period:
            logger.warning("The period is not found.")
            return None

        period = list(period[0].text)
        if len(period) == 2 and period[0].isnumeric() and period[1].isnumeric():
            return int(period[0]), int(period[1])
        elif len(period) == 3 and period[0].isnumeric() and period[2].isnumeric():
            return int(period[0]), int(period[2])

        logger.warning("The period is not found.")
        return None

    async def get_hp(self, game_state: GameState, user_name: str) -> dict | None:
        """
        Get the hp from the device by ocr.
        :return: {player_name: hp} maybe the hp info's length is not 8, but you could ignore the other players' hp.
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get hp.")
            return None

        # click hp button
        await self.click(*SpecificButton.CHOOSE_HP.get_middle_coordinate())
        await asyncio.sleep(0.5)

        # ocr the hp
        hp = {}
        for i in range(8):
            ocr_results = await self.get_screen_text(SpecificArea.PLAYERS[i])
            if not ocr_results:
                continue

            if len(ocr_results) == 1 and ocr_results[0].text.isnumeric():
                hp[user_name] = int(ocr_results[0].text)

            elif len(ocr_results) == 2 and ocr_results[1].text.isnumeric():
                hp[ocr_results[0].text] = int(ocr_results[1].text)

        return hp if hp else None

    async def get_equipment(self, game_state: GameState) -> list[str] | None:
        """
        Get the equipment from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get equipment.")
            return None

        # click choose equipment button
        await self.click(*SpecificButton.CHOOSE_EQUIPMENT.get_middle_coordinate())
        await asyncio.sleep(0.5)

        # click each equipment and ocr the results
        equipments = []
        for i in range(10):
            await self.click(*SpecificButton.EQUIPMENT[i].get_middle_coordinate())
            await asyncio.sleep(0.5)

            if equipment := await self.get_equipment_name(game_state):
                equipments.append(equipment)

            else:
                break

        return equipments if equipments else None

    async def get_equipment_name(self, game_state: GameState) -> str | None:
        """
        Get the equipment from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get equipment.")
            return None

        ocr_results = await self.get_screen_text(BoundingBox(0, 0, 514, 360))
        # save the real equipment results
        equipment_results = [r for r in ocr_results if r.text in SunflowerUtils.get_equipments()]

        if equipment_results:
            # the max y coordinate of the equipment is the real one
            top_equipment = min(equipment_results, key=lambda x: x.y)
            return top_equipment.text

        else:
            return None

    async def get_store(self, game_state: GameState) -> list[str] | None:
        """
        Get the store from the device by ocr.
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get store.")
            return None

        # get the ocr result
        heroes = []
        for i in range(5):
            ocr_results = await self.get_screen_text(SpecificButton.STORE_HERO[i])
            heroes.append(SunflowerUtils.is_hero(ocr_results))

        return heroes

    async def get_basic_game_info(self, game_state: GameState) -> BasicGameInfo | None:
        """
        Get the basic game information from the device by ocr.
        - coin
        - level
        - period
        - store
        - hp (to do
        :param game_state:
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get basic game information.")
            return None

        coin = await self.get_coin(game_state)
        level = await self.get_level(game_state)
        period = await self.get_period(game_state)
        store = await self.get_store(game_state)
        # hp = await self.get_hp(game_state)

        return BasicGameInfo(coin, level, period=period, store=store)

    async def get_augments(self, game_state: GameState) -> list[str] | None:
        """
        Get the augments from the device by ocr.
        :param game_state:
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get augments.")
            return None

        augments = []
        for i in range(3):
            ocr_results = await self.get_screen_text(SpecificArea.AUGMENTS[i])
            if not ocr_results:
                augments.append(None)

            augments.append(SunflowerUtils.is_augments(ocr_results))

        return augments if augments else None

    async def get_evolution(self, game_state: GameState) -> list[str] | None:
        """
        Get the evolution from the device by ocr.
        :param game_state:
        :return:
        """
        if game_state != GameState.IN_GAME:
            logger.warning("The game state is not in game. Cannot get evolution.")
            return None

        ocr_results = await self.get_screen_text(SpecificArea.EVOLVE)
        evolution = SunflowerUtils.is_evolution(ocr_results)

        return evolution


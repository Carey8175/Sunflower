import asyncio
from loguru import logger

from sunflower.config import *
from sunflower.sunflower_catcher import SunflowerCatcher
from sunflower.sunflower_control import SunflowerControl


class Sunflower:
    def __init__(self):
        self.sc = SunflowerCatcher()

    async def init_emulator(self):
        """
        Initialize the emulator
        """
        # emulator settings
        await self.sc.load(ADB_PORT, host=ADB_HOST)

        screen_resolution, screen_density = await asyncio.gather(
            self.sc.get_screen_size(),
            self.sc.get_screen_density()
        )

        logger.debug(f"Screen resolution: {screen_resolution}, Screen density: {screen_density}")

        if screen_resolution != SCREEN_RESOLUTION:
            await self.sc.set_screen_size(*SCREEN_RESOLUTION[0])
            logger.info(f"Set screen resolution to {SCREEN_RESOLUTION}")
        if screen_density != SCREEN_DPI:
            await self.sc.set_screen_density(SCREEN_DPI)
            logger.info(f"Set screen density to {SCREEN_DPI}")

        logger.info("Emulator initialized")

    async def init_game(self):
        pass

    async def wrapper_loop(self):
        asyncio.run(self.main())

    async def main(self):
        """
        Main function for Sunflower
         - recognize the game state
         - make decision
        """

    async def start(self):
        """
        Start Sunflower
        """
        await self.init_emulator()
        await self.init_game()
        await self.wrapper_loop()
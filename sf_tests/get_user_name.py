from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
import cv2
from sunflower.datatype import SpecificArea, SpecificButton, GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(16416)
    # screen = await sc.get_screen_box(SpecificArea.NAME_AREA)
    user_name = await sc.get_user_name(GameState.MAIN_MENU)
    print(user_name)


if __name__ == '__main__':
    asyncio.run(main())

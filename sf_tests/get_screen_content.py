from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
import cv2
from sunflower.datatype import SpecificArea, SpecificButton


async def main():
    sc = SunflowerCatcher()
    await sc.load(16416)
    screen = await sc.get_screen_box(SpecificButton.EVOLVE)
    # screen = await sc.get_screen_box(SpecificButton.ACCEPT_COMBAT)
    # print(vars(SpecificButton.START))
    cv2.imwrite("screen.png", screen)


if __name__ == '__main__':
    asyncio.run(main())

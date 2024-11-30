from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
import cv2
from sunflower.datatype import SpecificArea, SpecificButton
from sunflower.utils import SunflowerUtils


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)
    screen = await sc.get_screen()
    SunflowerUtils.locate_bounding_box(screen)


if __name__ == '__main__':
    asyncio.run(main())

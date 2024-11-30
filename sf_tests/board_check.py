from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
import cv2
from sunflower.datatype import SpecificArea, SpecificButton


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)

    for i in range(7):
        await sc.click(*SpecificArea.BOARD[3][i].get_middle_coordinate())

        await asyncio.sleep(0.5)
        print(await sc.get_screen_text(SpecificArea.CHESS_NAME))
        await sc.click(*SpecificButton.CHESS_SELL.get_middle_coordinate())
        await asyncio.sleep(0.5)

if __name__ == '__main__':
    asyncio.run(main())

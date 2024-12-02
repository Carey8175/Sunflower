import asyncio

from sunflower.sunflower_control import SunflowerControl
from sunflower.sunflower_catcher import SunflowerCatcher


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)

    for i in range(7):
        SunflowerControl.InGame.move_chess(sc, (1, 0), (1, i))
        await asyncio.sleep(0.5)
        SunflowerControl.InGame.move_chess(sc, (1, i), (1, 0))

if __name__ == '__main__':
    asyncio.run(main())
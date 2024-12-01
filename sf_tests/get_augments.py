from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)
    augs = await sc.get_augments(GameState.IN_GAME)
    print(augs)


if __name__ == '__main__':
    asyncio.run(main())
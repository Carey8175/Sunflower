from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(16384)
    augs = await sc.get_game_state()
    print(augs)


if __name__ == '__main__':
    asyncio.run(main())
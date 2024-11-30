from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(16416)
    equipments = await sc.get_hp(GameState.IN_GAME, user_name='12313')
    print(equipments)


if __name__ == '__main__':
    asyncio.run(main())
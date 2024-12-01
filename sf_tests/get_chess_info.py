from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)
    equipments = await sc.get_chess_info(GameState.IN_GAME, location=(3, 0), check_equipment=True)
    print(equipments)


if __name__ == '__main__':
    asyncio.run(main())
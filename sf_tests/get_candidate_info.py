import time

from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(5555)
    time1 = time.time()
    equipments = await sc.get_candidate_info(GameState.IN_GAME, order=1, check_equipment=True)
    print(equipments)
    print(time.time() - time1)


if __name__ == '__main__':
    asyncio.run(main())
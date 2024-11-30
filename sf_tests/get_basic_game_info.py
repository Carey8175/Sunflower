from sunflower.sunflower_catcher import SunflowerCatcher
import asyncio
from sunflower.datatype import GameState


async def main():
    sc = SunflowerCatcher()
    await sc.load(16416)
    # screen = await sc.get_screen_box(SpecificArea.NAME_AREA)
    game_info = await sc.get_basic_game_info(game_state=GameState.IN_GAME)

    print(game_info)


if __name__ == '__main__':
    asyncio.run(main())
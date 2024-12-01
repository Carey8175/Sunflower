import json
import cv2
import numpy

from sunflower.config import *


class SunflowerUtils:
    @staticmethod
    def get_equipments(file_path: str = EQUIPMENTS_PATH) -> set:
        """
        Get the equipment from the json file.
        :param file_path:
        :return:
        """
        data = json.load(open(file_path, encoding='utf-8'))['data']

        return {data[k]['name'] for k in data.keys()}

    @staticmethod
    def is_equipment(ocr_text_set: set) -> str | None:
        """
        After ocr, check if the text has equipment.
        :param ocr_text_set: the ocr text set of current screen
        :return: the name of the equipment
        """
        shared = SunflowerUtils.get_equipments() & ocr_text_set

        return None if not shared else list(shared)[0]

    @staticmethod
    def text_similarity(text1: str, text2: str) -> float:
        """
        Calculate the similarity of two texts.
        :param text1:
        :param text2:
        :return:
        """
        t1 = set(text1)
        t2 = set(text2)

        return round(len(t1 & t2) / len(t1 | t2), 2)

    @staticmethod
    def get_heroes(file_path: str = HEROES_PATH) -> set:
        """
        Get the heroes from the json file.
        :param file_path:
        :return:
        """
        data = json.load(open(file_path, encoding='utf-8'))['data']

        return {data[k]['name'] for k in data.keys()}

    @staticmethod
    def is_hero(ocr_results: list) -> str | None:
        if ocr_results is None:
            return None

        ocr_name = ''.join([ocr_result.text for ocr_result in ocr_results])
        if ocr_name in SunflowerUtils.get_heroes():
            return ocr_name

        # if the ocr name is not in the heroes, return the most similar hero
        return max([(SunflowerUtils.text_similarity(ocr_name, hero), hero) for hero in SunflowerUtils.get_heroes()])[1]

    @staticmethod
    def locate_bounding_box(image: numpy.ndarray) -> None:
        """
        it's a method to get a location of a bounding box rapidly
        which can be to find the specific area or button of the screen rapidly
        :param image:
        :return:
        """
        # 创建一个窗口
        cv2.namedWindow('Image Window')

        # 全局变量来保存图像的副本，用于绘制
        global img_click
        img_click = image.copy()

        def onMouseClick(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # plot the circle
                cv2.circle(img_click, (x, y), 5, (0, 255, 0), -1)
                # plot the text
                cv2.putText(img_click, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                cv2.imshow('Image Window', img_click)

        cv2.setMouseCallback('Image Window', onMouseClick)

        cv2.imshow('Image Window', img_click)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def get_augments() -> set:
        """
        Get the augments from the json file.
        :return:
        """
        data = json.load(open(AUGMENTS_PATH, encoding='utf-8'))['data']

        return {data[k]['name'] for k in data.keys()}

    @staticmethod
    def is_augments(ocr_results: list) -> str | None:
        """
        After ocr, check if the text has augments.
        :param ocr_results: the ocr results of current screen
        :return: the name of the augments
        """
        if not ocr_results:
            return None

        augment_name = ''.join([ocr_result.text for ocr_result in ocr_results])
        if augment_name in SunflowerUtils.get_augments():
            return augment_name

        return max([(SunflowerUtils.text_similarity(augment_name, augment), augment) for augment in SunflowerUtils.get_augments()])[1]

    @staticmethod
    def get_evolutions() -> set:
        """
        Get the evolutions from the json file.
        :return:
        """
        data = json.load(open(EVOLUTIONS_PATH, encoding='utf-8'))['data']

        return {data[k]['title'] for k in data.keys()}

    @staticmethod
    def is_evolution(ocr_results: list) -> str | None:
        """
        After ocr, check if the text has evolutions.
        :param ocr_results: the ocr results of current screen
        :return: the name of the evolutions
        """
        evolution_name = ''.join([ocr_result.text for ocr_result in ocr_results])
        if evolution_name in SunflowerUtils.get_evolutions():
            return evolution_name

        return max([(SunflowerUtils.text_similarity(evolution_name, evolution), evolution) for evolution in SunflowerUtils.get_evolutions()])[1]

    @staticmethod
    async def count_template_matches(template, image, threshold=0.8):
        """
        count the number of template matches in an image
        """
        template_height, template_width = template.shape[:2]

        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

        locations = numpy.where(result >= threshold)
        locations = list(zip(*locations[::-1]))  # 将位置转换为(x, y)格式

        matches = []
        for loc in locations:
            match = True
            for match_loc in matches:
                if abs(loc[0] - match_loc[0]) < template_width and abs(loc[1] - match_loc[1]) < template_height:
                    match = False
                    break
            if match:
                matches.append(loc)

        return len(matches)

    @staticmethod
    async def get_chess_star(image, threshold=0.8):
        """
        get the chess star from the image
        """
        template = cv2.imread(os.path.join(IMAGE_PATH, 'chess_star.jpg'), cv2.IMREAD_GRAYSCALE)
        return await SunflowerUtils.count_template_matches(template, image, threshold)


if __name__ == '__main__':
    # print(SunflowerUtils.get_augments())
    print(SunflowerUtils.get_evolutions())

import json
import cv2
import numpy

from sunflower.config import HEROES_PATH, EQUIPMENTS_PATH


class SunflowerUtils:
    @staticmethod
    def get_equipments(file_path: str = EQUIPMENTS_PATH) -> set:
        """
        Get the equipment from the json file.
        :param file_path:
        :return:
        """
        data = json.load(open(file_path))['data']

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
        data = json.load(open(file_path))['data']

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


if __name__ == '__main__':
    print(SunflowerUtils.get_heroes())
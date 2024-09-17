import cv2
import cvzone
import numpy as np


class Collision:
    def __init__(self, img: cv2.typing.MatLike = None, width=0, height=0, x=0, y=0, is_bat=False) -> None:
        self.x = x
        self.y = y
        self.is_img = img is not None
        if self.is_img:
            self.source_image = img
            self.width = img.shape[1]
            self.height = img.shape[0]
        else:
            self.width = width
            self.height = height
            self.source_image = self.empty_image(width, height)
        self.bounding_box = {
            "left": self.x,
            "right": self.x + self.width,
            "top": self.y,
            "bottom": self.y + self.height
        }
        self.is_bat = is_bat

    def empty_image(self, width, height):
        white_image = np.ones((self.height, self.width, 4), dtype=np.uint8)  * 255 # 255, beyaz rengi temsil eder
        white_image[..., 3] = 120  # Alpha kanalı tamamen saydam
        return white_image


    def draw(self, img: cv2.typing.MatLike, x, y, bound_x=None, bound_y=None):
        self.x = x
        self.y = y

        # referansı korumak için
        if self.is_img:
            x = x-self.width//2 if bound_x == None else bound_x
            y = y-self.height//2 if bound_y == None else bound_y

        self.bounding_box["left"] = x
        self.bounding_box["right"] = x + self.width
        self.bounding_box["top"] = y
        self.bounding_box["bottom"] = y + self.height
        #cv2.circle(img, (x, y), 9, (0, 100, 100), cv2.FILLED)
        cvzone.overlayPNG(img, self.source_image, (x, y))
        return img

    def __str__(self) -> str:
        return f"Collision at {self.bounding_box}"

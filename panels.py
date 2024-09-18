import cv2
import cvzone
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Panels:

    def __init__(self):
        pass

    def draw_exit1(self, img: cv2.typing.MatLike, img_exit: cv2.typing.MatLike, pos_x, pos_y, restart_def, resume_def, now, text) -> cv2.typing.MatLike:
        # 720, 1280 - 360, 640
        menu_w, menu_h = img_exit.shape[1], img_exit.shape[0]
        target_w, target_h = img.shape[1], img.shape[0]
        menu_x, menu_y = (target_w - menu_w) // 2, (target_h - menu_h) // 2
        bt_y1, bt_y2 = menu_y + menu_h*(5/8), menu_y + menu_h*(6/8)
        bt_x1, bt_x2, bt_x3, bt_x4 = menu_x + menu_w * \
            (2/10), menu_x + menu_w*(4.5/10), menu_x + \
            menu_w*(6/10), menu_x + menu_w*(8.5/10)
        cvzone.overlayPNG(img, img_exit, (menu_x, menu_y))
        cv2.putText(img, text, (menu_x + 20, menu_y + 50),
                    cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (255, 255, 255), 1)

        if bt_x1 < pos_x < bt_x2 and bt_y1 < pos_y < bt_y2:
            print("Tekrar Başla")
            restart_def()
            now()
        elif bt_x3 < pos_x < bt_x4 and bt_y1 < pos_y < bt_y2:
            print("Devam Et")
            resume_def()
        return img

    def draw_exit(self, img: cv2.typing.MatLike, img_exit: cv2.typing.MatLike, pos_x, pos_y, restart_def, resume_def, now, text) -> cv2.typing.MatLike:
        # 720, 1280 - 360, 640
        menu_w, menu_h = img_exit.shape[1], img_exit.shape[0]
        target_w, target_h = img.shape[1], img.shape[0]
        menu_x, menu_y = (target_w - menu_w) // 2, (target_h - menu_h) // 2
        bt_y1, bt_y2 = menu_y + menu_h * (5 / 8), menu_y + menu_h * (6 / 8)
        bt_x1, bt_x2, bt_x3, bt_x4 = menu_x + menu_w * (2 / 10), menu_x + menu_w * (
            4.5 / 10), menu_x + menu_w * (6 / 10), menu_x + menu_w * (8.5 / 10)

        # PNG'yi üst üste bindir
        cvzone.overlayPNG(img, img_exit, (menu_x, menu_y))
        cv2.circle(img, (pos_x, pos_y), 9, (255, 255, 255), cv2.FILLED)
        img = self.utf8_text(img, text, menu_x + 20, menu_y + 50, (0,0,0))

        # Buton etkileşimleri
        if bt_x1 < pos_x < bt_x2 and bt_y1 < pos_y < bt_y2:
            print("Tekrar Başla")
            restart_def()
            now()
        elif bt_x3 < pos_x < bt_x4 and bt_y1 < pos_y < bt_y2:
            print("Devam Et")
            resume_def()

        return img

    def utf8_text(self, img: cv2.typing.MatLike, text, x, y, color) -> cv2.typing.MatLike:
        pil_image = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype("arial.ttf", 32)
        draw.text((x, y), text, font=font, fill=color)
        img = np.array(pil_image)
        return img

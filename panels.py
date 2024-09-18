import cv2
import cvzone
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class Panels:
    def __init__(self):
        pass

    def draw_panel(self, img: cv2.typing.MatLike, img_exit: cv2.typing.MatLike, pos_x, pos_y, restart_def, resume_def, now, text, time_left) -> cv2.typing.MatLike:
        """
        Menüyü ve butonları çizen fonksiyon. Butonlara basıldığında ilgili fonksiyonlar çağrılır.
        """
        # Menü ve hedef ekran boyutlarını al
        menu_w, menu_h = img_exit.shape[1], img_exit.shape[0]
        target_w, target_h = img.shape[1], img.shape[0]

        # Menü konumunu hesapla
        menu_x, menu_y = (target_w - menu_w) // 2, (target_h - menu_h) // 2

        # Butonların dikey ve yatay sınırlarını belirle
        bt_y1, bt_y2 = menu_y + menu_h * (5 / 8), menu_y + menu_h * (6 / 8)
        bt_x1, bt_x2 = menu_x + menu_w * (2 / 10), menu_x + menu_w * (4.5 / 10)
        bt_x3, bt_x4 = menu_x + menu_w * (6 / 10), menu_x + menu_w * (8.5 / 10)

        # PNG menüsünü görüntünün üzerine bindir
        img = cvzone.overlayPNG(img, img_exit, (menu_x, menu_y))

        # Fare tıklama işaretçisi
        cv2.circle(img, (pos_x, pos_y), 9, (255, 255, 255), cv2.FILLED)

        # Metni yaz
        img = self.utf8_text(img, text, menu_x + 20, menu_y + 50, (0, 0, 0))

        # Buton etkileşimleri
        if bt_x1 < pos_x < bt_x2 and bt_y1 < pos_y < bt_y2:
            print("Tekrar Başla")
            restart_def()
            now()
        elif bt_x3 < pos_x < bt_x4 and bt_y1 < pos_y < bt_y2:
            print(f"Devam Et {time_left}")
            if time_left <= 0:
                restart_def()
                now()
            else:
                resume_def()

        return img

    def utf8_text(self, img: cv2.typing.MatLike, text, x, y, color) -> cv2.typing.MatLike:
        """
        OpenCV görüntüsüne UTF-8 uyumlu metin çizmek için Pillow kullanılır.
        """
        # OpenCV görüntüsünü PIL formatına dönüştür
        pil_image = Image.fromarray(img)

        # Pillow ile metin çizimi
        draw = ImageDraw.Draw(pil_image)
        try:
            # Arial fontunu yüklemeye çalış, hata alırsan varsayılan fontu kullan
            font = ImageFont.truetype("arial.ttf", 32)
        except IOError:
            font = ImageFont.load_default()

        # Metni çiz
        draw.text((x, y), text, font=font, fill=color)

        # PIL görüntüsünü tekrar OpenCV formatına dönüştür
        img = np.array(pil_image)
        return img

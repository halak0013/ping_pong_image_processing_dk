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
        white_image[..., 3] = 0  # Alpha kanalı tamamen saydam
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
    
    @staticmethod
    def get_sign(num):
        return 1 if num > 0 else -1

    @staticmethod
    def collision_detection(obj, bounding_box, img: cv2.typing.MatLike) -> tuple[bool, int, int, int, int]:
        obs_top = bounding_box["top"]
        obs_bottom = bounding_box["bottom"]
        obs_right = bounding_box["right"]
        obs_left = bounding_box["left"]
        x, y, radius, dx, dy = obj

        def check_collision(x, y):
            return obs_left <= x <= obs_right and obs_top <= y <= obs_bottom

        offset = 10
        collision_detected = False

        # Sağ kontrol
        for r in range(abs(dx)):
            r += 1
            val = x + radius + r * Collision.get_sign(dx)
            if check_collision(val, y):
                cv2.circle(img, (val, y), 3, (0, 255, 0), cv2.FILLED)
                dx *= -1
                x += Collision.get_sign(dx) * offset
                y += Collision.get_sign(dy) * offset
                collision_detected = True
                print(f"Ball: {x}, {y} speed: {dx}, {dy} - Sağ çarpışma")
                break

        # Sol kontrol
        if not collision_detected:
            for l in range(abs(dx)):
                l += 1
                val = x + l * Collision.get_sign(dx)
                if check_collision(val, y):
                    cv2.circle(img, (val, y), 3, (0, 255, 0), cv2.FILLED)
                    dx *= -1
                    x += Collision.get_sign(dx) * offset
                    y += Collision.get_sign(dy) * offset
                    collision_detected = True
                    print(f"Ball: {x}, {y} speed: {dx}, {dy} - Sol çarpışma")
                    break

        # Yukarı kontrol
        if not collision_detected:
            for t in range(abs(dy)):
                t += 1
                val = y - 10 + t * Collision.get_sign(dy)
                if check_collision(x, val):
                    cv2.circle(img, (x, val), 3, (0, 255, 0), cv2.FILLED)
                    dy *= -1
                    x += Collision.get_sign(dx) * offset
                    y += Collision.get_sign(dy) * offset
                    collision_detected = True
                    print(f"Ball: {x}, {y} speed: {dx}, {dy} - Üst çarpışma")
                    break

        # Aşağı kontrol
        if not collision_detected:
            for b in range(abs(dy)):
                b += 1
                val = y + radius + b * Collision.get_sign(dy)
                if check_collision(x, val):
                    cv2.circle(img, (x, val), 3, (0, 255, 0), cv2.FILLED)
                    dy *= -1
                    x += Collision.get_sign(dx) * offset
                    y += Collision.get_sign(dy) * offset
                    collision_detected = True
                    print(f"Ball: {x}, {y} speed: {dx}, {dy} - Alt çarpışma")
                    break

        return collision_detected, x, y, dx, dy

    def __str__(self) -> str:
        return f"Collision at {self.bounding_box}"

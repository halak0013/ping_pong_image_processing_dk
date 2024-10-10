# Bismillahirrahmanirrahim

import random
import cv2
import cvzone.HandTrackingModule as htm
from dk_connection import ImageReceiver, SocketServer
import Collision
import Ball
import panels
import time


class PingPong:
    def __init__(self, target_width=1920, target_height=1080, detection_confidence=0.40, max_hands=2, source="camera") -> None:
        self.target_width = target_width
        self.target_height = target_height
        self.detection_confidence = detection_confidence
        self.max_hands = max_hands
        self.source = source

        if source == "camera":
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, self.target_width)
            self.cap.set(4, self.target_height)
        else:
            self.sock_server = SocketServer()
            self.image_receiver = ImageReceiver(self.sock_server)

        self.img_background = self.resize_img(cv2.imread(
            "resources/background.png"), self.target_width, self.target_height)
        self.img_ball = self.resize_img(cv2.imread(
            "resources/ball.png", cv2.IMREAD_UNCHANGED), 40, 40)
        self.img_left_bat = self.resize_img(cv2.imread(
            "resources/left_bat.png", cv2.IMREAD_UNCHANGED), 24, 150)
        self.img_right_bat = self.resize_img(cv2.imread(
            "resources/right_bat.png", cv2.IMREAD_UNCHANGED), 24, 150)
        self.img_menu = self.resize_img(cv2.imread(
            "resources/menu.png", cv2.IMREAD_UNCHANGED), 640, 360)
        self.img_obstacle = self.resize_img(cv2.imread(
            "resources/engel.png", cv2.IMREAD_UNCHANGED), 75, 75)
        
        self.o1_x = random.randint(100, self.target_width-100)
        self.o1_y = random.randint(100, self.target_height-100)
        self.o2_x = random.randint(100, self.target_width-100)
        self.o2_y = random.randint(100, self.target_height-100)

        self.detector = htm.HandDetector(
            maxHands=self.max_hands, detectionCon=self.detection_confidence)

        bl, bu = 50, 60
        self.boundaries = {
            "left": bl,
            "right": self.target_width - bl,
            "top": bu,
            "bottom": self.target_height - bu*2
        }

        self.scores = {"left": 0, "right": 0}

        self.hx, self.hy = 0, 0

        self.bats = {"left_bat": Collision.Collision(self.img_left_bat, is_bat=True),
                     "right_bat": Collision.Collision(self.img_right_bat, is_bat=True), }

        self.objects = {
            "up": Collision.Collision(width=self.target_width, height=bu, x=0, y=0),
            "down": Collision.Collision(width=self.target_width, height=bu, x=0, y=self.target_height-bu),
            "left": Collision.Collision(width=bl, height=self.target_height, x=0, y=0),
            "right": Collision.Collision(width=bl, height=self.target_height, x=self.target_width-bl, y=0),
            "obstacle1": Collision.Collision(self.img_obstacle, x=-10, y=-10),
            "obstacle2": Collision.Collision(self.img_obstacle, x=-10, y=-10),
        }
        # Referansları içeren liste
        self.collisions = [{key: val.bounding_box}
                           for key, val in self.objects.items()]
        self.collisions.extend(
            [{key: val.bounding_box} for key, val in self.bats.items()])
        self.ball = Ball.Ball(self.img_ball, (self.target_width//2,
                                              self.target_height//2), self.scores)
        self.panel = panels.Panels()

        self.game_time = 120
        self.obs_time = 15
        self.now = time.time()
        self.hand_free_time = 0
        self.is_hand_free = False

    def resize_img(self, img: cv2.typing.MatLike, width, height):
        return cv2.resize(img, (width, height))

    def get_img(self):
        img = None
        success = None
        if self.source == "sock":
            img = self.image_receiver.get_image()
            success = img is not None
        else:
            success, img = self.cap.read()
        return success, img

    def draw_hand_pose(self, img: cv2.typing.MatLike, hands: list):
        if hands:
            self.hand_free_time = 0
            for hand in hands:
                x, y, w, h = hand["bbox"]
                x2, y2 = x+w//2, y+h//2  # hand center
                self.hx, self.hy = x2, y2
                # TODO: renk tespiti ile raket de yapılabilir
                if hand["type"] == "Right" and x2 > self.target_width//2:
                    img = self.bats["right_bat"].draw(
                        img=img, x=x2, y=y2, bound_x=self.boundaries["right"] - 20)
                    img = cv2.circle(img, (x2, y2), 9, (255, 0, 0), cv2.FILLED)
                elif hand["type"] == "Left" and x2 < self.target_width//2:
                    img = self.bats["left_bat"].draw(
                        img=img, x=x2, y=y2, bound_x=self.boundaries["left"] + 20)
                    img = cv2.circle(img, (x2, y2), 9, (0, 0, 255), cv2.FILLED)
        else:
            self.hand_free_time += 1
        return img

    def draw_score(self, img: cv2.typing.MatLike):
        space = 100
        text = f"Oyuncu 2: {self.scores['left']}"
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        font_scale = 1
        font_color = (100, 100, 255)
        thickness = 1
        # Yazının boyutunu hesapla
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, thickness)

        # Yazıyı yerleştirmek için dinamik bir konum belirle
        x = (self.target_width // 2) - (text_width)
        # Y ekseninde biraz boşluk bırak
        y = (text_height + baseline) + self.boundaries["top"]

        cv2.putText(img, text, (x, y), font, font_scale, font_color, thickness)

        cv2.putText(img, f"Oyuncu 1: {self.scores['right']}", (self.target_width//2 + space, y),
                    font, font_scale, (255, 100, 100), thickness)
        return img

    def reset(self):
        self.now = time.time()
        self.hand_free_time = 0
        self.scores["left"] = 0
        self.scores["right"] = 0
        self.is_hand_free = False
    def resume(self):
        #self.now = time.time()
        self.hand_free_time = 0
        self.is_hand_free = False
        self.ball.resume()

    def draw_time(self, img: cv2.typing.MatLike) -> cv2.typing.MatLike:
        time_left = self.game_time - (time.time() - self.now)
        if self.hand_free_time > 100:
            self.is_hand_free = True
        if time_left <= 0 or self.is_hand_free:
            self.ball.pause()
            img = self.panel.draw_panel(img, self.img_menu, self.hx, self.hy,
                                       self.ball.restart, self.resume, self.reset,
                                       "Tekrar Başlamak İçin Butona Elinizi getirin", time_left)
        if time_left <= 0:
            time_left = 0
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        font_scale = 1
        font_color = (0, 255, 0)
        thickness = 1
        text = f"Zaman: {int(time_left)}"
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, thickness)
        x = (self.target_width // 2) - (text_width // 2)
        y = (text_height + baseline) + self.boundaries["top"] + 100
        cv2.putText(img, text, (x, y), font, font_scale, font_color, thickness)

        return img

    def draw_obstacle(self):
        if (time.time() - self.now) % self.obs_time < 2:
            self.o1_x = random.randint(100, self.target_width-100)
            self.o1_y = random.randint(100, self.target_height-100)
            self.o2_x = random.randint(100, self.target_width-100)
            self.o2_y = random.randint(100, self.target_height-100)
        self.objects["obstacle1"].x=self.o1_x
        self.objects["obstacle1"].y=self.o1_y
        self.objects["obstacle2"].x=self.o2_x
        self.objects["obstacle2"].y=self.o2_y

    def draw_components(self, img: cv2.typing.MatLike, hands: list):
        img = cv2.addWeighted(
            img, alpha=0.3, src2=self.img_background, beta=0.9, gamma=0)

        img = self.draw_hand_pose(img, hands)
        for obj in self.objects.values():
            img = obj.draw(img, obj.x, obj.y)
            
        n = time.time() - self.now
        if n > 5:
            self.ball.move(img, self.collisions)
        else:
            img = self.panel.utf8_text(img, f"Başlamak lütfen için elinizi getiriniz: {int(5 - n)}", 
                                       self.target_width//4, self.target_height//2, (0,255,100))
        self.draw_obstacle()
        img = self.draw_score(img)
        img = self.draw_time(img)
        return img

    def run(self):
        print("running")
        while True:
            success, img = self.get_img()
            if not success:
                print("Failed to read from camera")
                break
            img: cv2.typing.MatLike = cv2.flip(img, 1)
            img = cv2.resize(img, (self.target_width, self.target_height))
            hands, img = self.detector.findHands(img, flipType=False)

            img = self.draw_components(img, hands)

            cv2.imshow("Dk Ping Pong", img)
            if cv2.waitKey(5) & 0xFF == 27:  # ord('q')
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = PingPong(source="camera") # source="sock" , "camera"
    app.run()

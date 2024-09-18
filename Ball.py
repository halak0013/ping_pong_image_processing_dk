import cv2
import cvzone
import pygame
import numpy as np
# https://happycoding.io/tutorials/processing/collision-detection#collision-detection-between-many-objects


class Ball:
    def __init__(self, ball, init_pos, scores) -> None:
        self.x = init_pos[0]
        self.y = init_pos[1]
        self.speed = 2
        self.max_speed = 6
        self.dx = self.speed
        self.dy = self.speed
        self.img_ball = ball
        print(ball.shape)
        self.radius = ball.shape[0]

        self.init_pos = init_pos
        self.sing_x = 1
        self.sing_y = 1

        self.scores = scores

        pygame.mixer.init()

        self.shot_sound = pygame.mixer.Sound("resources/shot.wav")
        self.fail_sound = pygame.mixer.Sound("resources/fail.wav")

    def restart(self):
        self.x = self.init_pos[0]
        self.y = self.init_pos[1]
        self.dx = self.speed * self.sing_x
        self.dy = self.speed * self.sing_y
        
    def resume(self):
        self.dx = self.speed * self.sing_x
        self.dy = self.speed * self.sing_y

    def pause(self):
        self.dx = 0
        self.dy = 0

    def collision_detection(self, bounding_box) -> bool:
        top = bounding_box["top"]
        bottom = bounding_box["bottom"]
        right = bounding_box["right"]
        left = bounding_box["left"]

        print(f"Ball: {self.x}, {self.y} speed: {self.dx}, {self.dy}")
        #bouncing - > self
        #rectangle -> top, right

        # Sağ ve sol çarpışma kontrolü
        if self.x + self.radius + self.dx > left and self.x < right:
            if self.y + self.radius + self.dy > top and self.y + self.dy < bottom:
                # X ekseninde çarpışma durumu
                self.dx *= -1
                self.x += self.dx
                print("sağ, sol")
                return True

        # Üst ve alt çarpışma kontrolü
        if self.x + self.radius > left and self.x < right:
            if self.y + self.radius + self.dy > top and self.y + self.dy < bottom:
            # Y ekseninde çarpışma durumu
                self.dy *= -1
                self.y += self.dy
                print("üst, alt")
                return True

        # Sağ ve sol çarpışma kontrolü
        #if self.x + self.radius + self.dx > left and self.x + self.dx < right:
        #    if self.y + self.radius > top and self.y < bottom:
        #        # X ekseninde çarpışma durumu
        #        self.dx *= -1
        #        self.x += self.dx
        #        print("sağ, sol")
        #        return True
            
        

        return False
    
    def get_sign(self, num):
        return 1 if num > 0 else -1
    
    def collision_detection2(self, bounding_box, img: cv2.typing.MatLike) -> bool:
            
        obs_top = bounding_box["top"]
        obs_bottom = bounding_box["bottom"]
        obs_right = bounding_box["right"]
        obs_left = bounding_box["left"]

        def chech_all_collision(x, y):
            return x >= obs_left and x <= obs_right and y >= obs_top and y <= obs_bottom
        #sağ kortol
        
        for r in range(abs(self.dx) + 1):
            val = self.x + self.radius + r * self.get_sign(self.dx)
            if val >= obs_left and chech_all_collision(val, self.y):
                cv2.circle(img, (val, self.y), 3, (0,255,0),cv2.FILLED)
                self.dx *= -1
                self.x += self.get_sign(self.dx) * 30
                self.y += self.get_sign(self.dy) * 30
                print(f"Ball: {self.x}, {self.y} speed: {self.dx}, {self.dy}")
                print("sağ")
                return True
        
        #sol kontrol
        for l in range(abs(self.dx) + 1):
            val = self.x + l * self.get_sign(self.dx)
            if val <= obs_right and chech_all_collision(val, self.y):
                cv2.circle(img, (val, self.y), 3, (0,255,0),cv2.FILLED)
                self.dx *= -1
                self.x += self.get_sign(self.dx) * 30
                self.y += self.get_sign(self.dy) * 30
                print(f"Ball: {self.x}, {self.y} speed: {self.dx}, {self.dy}")
                print("sol")
                return True
        
        #yukarı kontrol
        for t in range(abs(self.dy) + 1):
            val = self.y + t * self.get_sign(self.dy)
            if val <= obs_bottom and chech_all_collision(self.x, val):
                cv2.circle(img, (self.x, val), 3, (0,255,0),cv2.FILLED)
                self.dy *= -1
                self.x += self.get_sign(self.dx) * 30
                self.y += self.get_sign(self.dy) * 30
                print(f"Ball: {self.x}, {self.y} speed: {self.dx}, {self.dy}")
                print("üst")
                return True
        
        #aşağı kontrol
        for b in range(abs(self.dy)+1):
            val = self.y + self.radius + b * self.get_sign(self.dy)
            if val >= obs_top and chech_all_collision(self.x, val):
                cv2.circle(img, (self.x ,val), 3, (0,255,0),cv2.FILLED)
                self.dy *= -1
                self.x += self.get_sign(self.dx) * 30
                self.y += self.get_sign(self.dy) * 30
                print(f"Ball: {self.x}, {self.y} speed: {self.dx}, {self.dy}")
                print("alt")
                return True
        
        return False



    def increase_speed(self):
        self.sing_x = 1 if self.dx > 0 else -1  # Hareket yönünü belirle
        self.sing_y = 1 if self.dy > 0 else -1  # Hareket yönünü belirle
        if abs(self.dx) < self.max_speed:
            self.dx += 1 * self.sing_x
            self.dy += 1 * self.sing_y

    def move(self, img: cv2.typing.MatLike, collisions: list[dict[str, dict[str, int]]]):
        # for i in range(abs(self.dx)):
        # TODO: Keep all collsion on np matris
        for c in collisions:
            if not self.collision_detection2(next(iter(c.values())), img):
                self.x +=  self.dx # self.get_sign(self.dx) *
                self.y +=  self.dy # self.get_sign(self.dy) *
                cvzone.overlayPNG(img, self.img_ball, (self.x, self.y))
                cv2.putText(img, str(abs(self.dx)), (self.init_pos[0], 150),
                            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 200, 0), 1)
            else:
                print(f"Collision {self.get_sign(self.dy) * self.dy}")
                key = next(iter(c.keys()))
                if key == "right":
                    self.scores["right"] -= 2
                    self.scores["left"] += 1
                    self.fail_sound.play()
                    self.restart()
                elif key == "left":
                    self.scores["left"] -= 2
                    self.scores["right"] += 1
                    self.fail_sound.play()
                    self.restart()
                elif key == "right_bat":
                    self.scores["right"] += 2
                    self.increase_speed()
                    self.shot_sound.play()
                elif key == "left_bat":
                    self.scores["left"] += 2
                    self.increase_speed()
                    self.shot_sound.play()
                return

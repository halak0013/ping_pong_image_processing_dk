import cv2
import cvzone
import pygame
from Collision import Collision
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
    

    def get_info(self):
        return self.x, self.y, self.radius, self.dx, self.dy




    def increase_speed(self):
        self.sing_x = 1 if self.dx > 0 else -1  # Hareket yönünü belirle
        self.sing_y = 1 if self.dy > 0 else -1  # Hareket yönünü belirle
        if abs(self.dx) < self.max_speed:
            self.dx += 1 * self.sing_x
            self.dy += 1 * self.sing_y

    def move(self, img: cv2.typing.MatLike, collisions: list[dict[str, dict[str, int]]]):
        for i in range(abs(self.dx)):
            # TODO: Keep all collsion on np matris
            for c in collisions:
                collision_detected, self.x, self.y, self.dx, self.dy = Collision.collision_detection(self.get_info(), next(iter(c.values())), img)
                if not collision_detected:
                    self.x += Collision.get_sign(self.dx) #self.dx
                    self.y += Collision.get_sign(self.dy) #self.dy
                    cvzone.overlayPNG(img, self.img_ball, (self.x, self.y))
                    cv2.putText(img, str(abs(self.dx)), (self.init_pos[0], 150),
                                cv2.FONT_HERSHEY_COMPLEX, 2, (0, 200, 0), 1)
                else:
                    print(f"Collision {Collision.get_sign(self.dy) * self.dy}")
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
                        # self.scores["right"] += 2
                        self.increase_speed()
                        self.shot_sound.play()
                    elif key == "left_bat":
                        # self.scores["left"] += 2
                        self.increase_speed()
                        self.shot_sound.play()
                    return

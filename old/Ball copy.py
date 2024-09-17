import cv2
import cvzone

# https://happycoding.io/tutorials/processing/collision-detection#collision-detection-between-many-objects


class Ball:
    def __init__(self, ball, init_pos, scores) -> None:
        self.x = init_pos[0]
        self.y = init_pos[1]
        self.dx = 7
        self.dy = 7
        self.img_ball = ball
        print(ball.shape)
        self.radius = ball.shape[0] // 2

        self.init_pos = init_pos
        self.sing_x = 1
        self.sing_y = 1

        self.scores = scores

    def restart(self):
        self.x = self.init_pos[0]
        self.y = self.init_pos[1]
        self.dx = 7 * self.sing_x
        self.dy = 7 * self.sing_y

    def collision_detection(self, bounding_box) -> bool:
        top = bounding_box["top"]
        bottom = bounding_box["bottom"]
        right = bounding_box["right"]
        left = bounding_box["left"]

        # Sağ ve sol çarpışma kontrolü
        if self.x + self.radius + self.dx > left and self.x + self.radius + self.dx < right:
            if self.y + self.radius > top and self.y + self.radius < bottom:
                # X ekseninde çarpışma durumu
                self.dx *= -1
                return True

        # Üst ve alt çarpışma kontrolü
        if self.y + self.radius + self.dy > top and self.y + self.radius + self.dy < bottom:
            if self.x + self.radius > left and self.x + self.radius < right:
                # Y ekseninde çarpışma durumu
                self.dy *= -1
                return True

        return False

    def move(self, img: cv2.typing.MatLike, collisions: list[dict[str, dict[str, int]]]):
        self.sing_x = 1 if self.dx > 0 else -1  # Hareket yönünü belirle
        self.sing_y = 1 if self.dy > 0 else -1  # Hareket yönünü belirle
        cv2.putText(img, str(f"{self.x}, {self.y}"), (self.init_pos[0], 200),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 200, 0), 1)

        for i in range(abs(self.dx)):
            # TODO: Keep all collsion on np matris
            for c in collisions:
                if not self.collision_detection(next(iter(c.values()))):
                    self.x += self.sing_x
                    self.y += self.sing_y
                    cvzone.overlayPNG(img, self.img_ball, (self.x, self.y))
                    cv2.putText(img, str(abs(self.dx)), (self.init_pos[0], 150),
                                cv2.FONT_HERSHEY_COMPLEX, 2, (0, 200, 0), 1)
                else:
                    key = next(iter(c.keys()))
                    if key == "right":
                        self.scores["right"] -= 2
                        self.scores["left"] += 1
                        self.restart()
                    elif key == "left":
                        self.scores["left"] -= 2
                        self.scores["right"] += 1
                        self.restart()
                    elif key == "right_bat":
                        self.scores["right"] += 2
                        self.dx -= 1 * self.sing_x
                        self.dy -= 1 * self.sing_y
                    elif key == "left_bat":
                        self.scores["left"] += 2
                        self.dx -= 1 * self.sing_x
                        self.dy -= 1 * self.sing_y
                    return

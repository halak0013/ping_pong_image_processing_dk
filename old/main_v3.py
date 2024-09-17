import cv2
import cvzone
import numpy as np
import pygame
import time

from cvzone.HandTrackingModule import HandDetector

width, height = 1280, 720
cap = cv2.VideoCapture(0)

cap.set(3, width)
cap.set(4, height)

img_background = cv2.imread("resources/background.png")
img_background = cv2.resize(img_background, (width, height))
img_ball = cv2.imread("resources/ball.png", cv2.IMREAD_UNCHANGED)
img_ball = cv2.resize(img_ball, (40, 40))
img_left_bat = cv2.imread("resources/left_bat.png", cv2.IMREAD_UNCHANGED)
img_left_bat = cv2.resize(img_left_bat, (24, 150))
img_right_bat = cv2.imread("resources/right_bat.png", cv2.IMREAD_UNCHANGED)
img_right_bat = cv2.resize(img_right_bat, (24, 150))

pygame.mixer.init()
sound = pygame.mixer.Sound("resources/shot.wav")
fail = pygame.mixer.Sound("resources/fail.wav")

detector = HandDetector(staticMode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5)

ballPos = [width // 2, height // 2]
speedX = 30
speedY = 30

left_boundary = 50
right_boundary = width - left_boundary

up_boundary = 50
bottom_boundary = height - up_boundary * 2

left_score = 0
right_score = 0

max_speed = 70

obstacles = [
    {'center_x': left_boundary + 60, 'center_y': height // 2, 'width': 24, 'height': 150},
    {'center_x': right_boundary - 60, 'center_y': height // 2, 'width': 24, 'height': 150},
]

step_counter = 0

def draw_ball(img):
    global ballPos, speedY, right_score, left_score, step_counter
    step_counter += 1

    if ballPos[1] > bottom_boundary or ballPos[1] < up_boundary:
        speedY = -speedY
    ballPos[0] += speedX
    ballPos[1] += speedY

    if ballPos[0] < 0:
        left_score -= 2
        ballPos = [width // 2, height // 2]
        fail.play()
    elif ballPos[0] > width - 10:
        right_score -= 2
        ballPos = [width // 2, height // 2]
        fail.play()

    # Her 5 adımda bir engellerle çarpışmayı kontrol et
    if step_counter % 5 == 0:
        for obstacle in obstacles:
            collision_detection(ballPos[0], ballPos[1], img_ball.shape[1], img_ball.shape[0], obstacle)

    return cvzone.overlayPNG(img, img_ball, ballPos)

def collision_detection(ball_center_x, ball_center_y, ball_width, ball_height, obstacle):
    global speedX, speedY

    ball_left = ball_center_x - (ball_width / 2)
    ball_right = ball_center_x + (ball_width / 2)
    ball_top = ball_center_y - (ball_height / 2)
    ball_bottom = ball_center_y + (ball_height / 2)

    obstacle_left = obstacle['center_x'] - (obstacle['width'] / 2)
    obstacle_right = obstacle['center_x'] + (obstacle['width'] / 2)
    obstacle_top = obstacle['center_y'] - (obstacle['height'] / 2)
    obstacle_bottom = obstacle['center_y'] + (obstacle['height'] / 2)

    if (ball_right >= obstacle_left and ball_left <= obstacle_right and
            ball_bottom >= obstacle_top and ball_top <= obstacle_bottom):
        overlap_left = ball_right - obstacle_left
        overlap_right = obstacle_right - ball_left
        overlap_top = ball_bottom - obstacle_top
        overlap_bottom = obstacle_bottom - ball_top

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_left or min_overlap == overlap_right:
            speedX = -speedX
        if min_overlap == overlap_top or min_overlap == overlap_bottom:
            speedY = -speedY
        return True

while True:
    succes, img = cap.read()
    img = cv2.flip(img, 1)

    try:
        hands, img = detector.findHands(img, draw=True, flipType=False)
    except:
        continue

    if not succes:
        break

    img = cv2.addWeighted(img, alpha=0.2, src2=img_background, beta=0.8, gamma=0)

    if hands:
        for hand in hands:
            x, y, h, w = hand["bbox"]
            y1 = y - 150 // 2
            y1 = np.clip(y1, up_boundary - 10, bottom_boundary + 10)

            if hand["type"] == "Left":
                obstacles[0]['center_y'] = y1

            if hand["type"] == "Right":
                obstacles[1]['center_y'] = y1

    img = draw_ball(img)

    # Engelleri çizin
    img = cvzone.overlayPNG(img, img_left_bat, (int(obstacles[0]['center_x'] - obstacles[0]['width'] / 2), int(obstacles[0]['center_y'] - obstacles[0]['height'] / 2)))
    img = cvzone.overlayPNG(img, img_right_bat, (int(obstacles[1]['center_x'] - obstacles[1]['width'] / 2), int(obstacles[1]['center_y'] - obstacles[1]['height'] / 2)))

    cv2.putText(img, str(left_score), (width // 2 - 100, height // 4), cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 255, 255), 3)
    cv2.putText(img, str(right_score), (width // 2 + 50, height // 4), cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 255, 255), 3)

    cv2.imshow("Deneyap", img)
    if cv2.waitKey(5) & 0xFF == 27:
        break
    elif cv2.waitKey(5) & 0xFF == ord('a'):
        ballPos = [100, 100]

cap.release()
cv2.destroyAllWindows()

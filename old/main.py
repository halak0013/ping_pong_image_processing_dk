import cv2
import cvzone
import numpy as np
import pygame
import time

from cvzone.HandTrackingModule import HandDetector
from dk_connection import get_img

width, height = 1280, 720
#width, height = 800, 600
cap = cv2.VideoCapture(0)

print(width)
cap.set(3, width)
cap.set(4, height)

img_background = cv2.imread("resources/background.png")
img_background = cv2.resize(
    img_background, (width, height))  # Boyutları düzelt
img_ball = cv2.imread("resources/ball.png", cv2.IMREAD_UNCHANGED)
img_ball = cv2.resize(img_ball, (40, 40))
img_left_bat = cv2.imread("resources/left_bat.png", cv2.IMREAD_UNCHANGED)
img_left_bat = cv2.resize(img_left_bat, (24, 150))
img_right_bat = cv2.imread("resources/right_bat.png", cv2.IMREAD_UNCHANGED)
img_right_bat = cv2.resize(img_right_bat, (24, 150))


pygame.mixer.init()

sound = pygame.mixer.Sound("resources/shot.wav")
fail = pygame.mixer.Sound("resources/fail.wav")



# el tespit edici
detector = HandDetector(staticMode=False, maxHands=2,
                        detectionCon=0.5, minTrackCon=0.5)

ballPos = [width//2, height//2]
speedX = 30
speedY = 30

left_boundary = 50
right_boundary = width - left_boundary


up_boundary = 50
bottom_boundary = height - up_boundary * 2


left_score = 0
right_score = 0

max_speed=80


def draw_ball(img):
    global ballPos
    global speedY
    global right_score
    global left_score
    if ballPos[1] > bottom_boundary or ballPos[1] < up_boundary:
        speedY = -speedY
    ballPos[0] += speedX
    ballPos[1] += speedY
    cv2.putText(img, "ball"+str(ballPos), org=(100, 200), fontFace=cv2.FONT_HERSHEY_PLAIN,
                fontScale=2, color=(255, 255, 255), thickness=3)
    if ballPos[0] < 0:
        right_score += 1
        ballPos = [width//2, height//2]
        fail.play()
    elif ballPos[0] > width - 10:
        left_score += 1
        ballPos = [width//2, height//2]
        fail.play()

    return cvzone.overlayPNG(img, img_ball, ballPos)




while True:
    succes, img = cap.read()
    #succes, img = get_img()
    img = cv2.flip(img, 1)
    print(img.shape)

    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    try:
        hands, img = detector.findHands(img, draw=True, flipType=False)
    except:
        continue

    if not succes:
        break  # Eğer görüntü alınamazsa döngüden çık



    # img_background'ı img ile aynı boyuta getirdik
    img = cv2.addWeighted(
        img, alpha=0.2, src2=img_background, beta=0.8, gamma=0)

    if hands:
        for hand in hands:
            x, y, h, w = hand["bbox"]
            h1, w1, _ = img_left_bat.shape
            y1 = y - h1//2
            y1 = np.clip(y1, up_boundary-10, bottom_boundary+10)

            if hand["type"] == "Left":
                img = cvzone.overlayPNG(img, img_left_bat, (left_boundary, y1))
                cv2.putText(img, "left"+str(y1), org=(100, 100), fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=2, color=(255, 255, 255), thickness=3)
                if left_boundary < ballPos[0] < left_boundary + w1 * 2 and y1 < ballPos[1] < y1 + h1 + 20:
                    sound.play()
                    if abs(speedX) < max_speed:
                        speedX -= 5
                        speedY -= 5
                    speedX = -speedX
                    ballPos[0] += 30

            if hand["type"] == "Right":
                img = cvzone.overlayPNG(img, img_right_bat, (width-100, y1))
                cv2.putText(img, "right"+str(y1), org=(100, 150), fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=2, color=(255, 255, 255), thickness=3)
                if right_boundary-100 < ballPos[0] < right_boundary + w1 and y1 < ballPos[1] < y1 + h1:
                    sound.play()
                    if abs(speedX) < max_speed:
                        speedX += 5
                        speedY += 5
                    speedX = -speedX
                    ballPos[0] -= 30

            cv2.putText(img, "speed"+str(speedX), org=(100, 250), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=(255, 255, 255), thickness=3)

    cv2.putText(img, str(left_score), (width//2-100, height//4),
                cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 255, 255), 3)
    cv2.putText(img, str(right_score), (width//2+50, height//4),
                cv2.FONT_HERSHEY_TRIPLEX, 3, (255, 255, 255), 3)

    img = draw_ball(img)

    cv2.imshow("Deneyap", img)
    if cv2.waitKey(5) & 0xFF == 27:
        print("çık")
        break
    elif cv2.waitKey(5) & 0xFF == ord('a'):
        print("aa")
        ballPos = [100, 100]


cap.release()
cv2.destroyAllWindows()

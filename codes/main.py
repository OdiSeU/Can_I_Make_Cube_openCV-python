import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('../Images/ex_view_hand.png')
# 이미지의 외곽 검출
img1_canny = cv2.Canny(img1, 100, 200)

# 면과 경계를 구분하기 위한 팽창 연산
k = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
img1_dlt = cv2.dilate(img1_canny, k)

# 꼭지점 검출
cont, _ = cv2.findContours(img1_dlt, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

cube = []
# i = 0
for cnt in cont:
    # contour 근사를 이용해 필요없는 꼭지점 수 줄이기
    eps = 0.03 * cv2.arcLength(cnt, True)
    poly = cv2.approxPolyDP(cnt, eps, True)
    # 꼭지점이 4개인 배열만 cube 에 추가
    if len(poly) == 4:
        cube.append(poly)
        # cv2.drawContours(img1, [cube[i]], -1, (0,0,255), 1)
        # i = i + 1

i = 0
for cnt in cube:
    i = i + 1
    j = 0
    for p in cnt:
        j = j + 1
        print(i, j, p[0][0], p[0][1])
        cv2.circle(img1, (p[0][0], p[0][1]), 2, (255, 0, 0), -1)

imgs = {'1': img1[:, :, ::-1], '2': img1_dlt}

for i, (k, v) in enumerate(imgs.items()):
    plt.subplot(1, 2, i + 1)
    plt.title(k)
    plt.imshow(v, cmap='gray')
    plt.xticks([])
    plt.yticks([])
plt.show()

cv2.imshow('img', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

import codes.cube as cb
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

#두 점 사이의 각도 구하기
def getAngle(pt1, pt2):
    dx = pt1[0] - pt2[0]
    dy = pt1[1] - pt2[1]
    rad = math.atan2(dx, dy)
    return (rad * 180) / math.pi

def autoRotExView(img_org):
    # 이미지의 외곽 검출
    img_canny = cv2.Canny(img_org, 100, 200)
    # 면과 경계를 구분하기 위한 팽창 연산
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    img_dlt = cv2.dilate(img_canny, k)

    rows, cols = img_dlt.shape[0:2]
    # 평균 기울기 구하기
    _, avgDeg = scanExView(img_dlt)
    # 회전 행렬 생성 (전개도가 회전하면서 이미지 밖으로 나가는 것을 막기위해 scale 변환)
    matRot = cv2.getRotationMatrix2D((cols/2, rows/2), -avgDeg, 0.7)
    # 회전 변환
    img_org = cv2.warpAffine(img_org, matRot, (cols, rows))
    img_dlt = cv2.warpAffine(img_dlt, matRot, (cols, rows))

    return img_org, img_dlt

# 꼭지점 검출과 평균 기울기 반환
def scanExView(img):
    rects = []
    degs = []
    cont, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in cont:
        # contour 근사를 이용해 필요없는 꼭지점 수 줄이기
        eps = 0.03 * cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, eps, True)
        # 꼭지점이 4개이고 일정 크기 이상의 사각형만 cube 에 추가
        if len(poly) == 4 and cv2.contourArea(cnt) > 1000:
            rects.append(poly)
            # 변의 기울기 계산
            degs.append(getAngle(poly[2][0], poly[1][0]))
            degs.append(getAngle(poly[3][0], poly[0][0]))

    return rects, np.mean(degs)

# 전개도를 행렬로 변환
def getExViewMatrix(img):
    # 전개도 각 면 검출
    rects, _ = scanExView(img)

    viewMat = np.zeros((8, 8))
    minX = minY = np.inf
    centers = []
    for rect in rects:
        # 무게중심 좌표 구하기
        mmt = cv2.moments(rect)
        cx = int(mmt['m10'] / mmt['m00'])
        cy = int(mmt['m01'] / mmt['m00'])
        centers.append([cx, cy])
        for p in rect:
            if minX > p[0][0]:
                minX = p[0][0]
            if minY > p[0][1]:
                minY = p[0][1]

    # 무게중심 간의 거리 구하기
    minDist = np.inf
    for center in centers:
        dist = math.dist(centers[0], center)
        if dist != 0 and dist < minDist:
            minDist = dist
    # 행렬로 변환..
    for center in centers:
        row, col = int((center[1] - minY) / minDist), int((center[0] - minX) / minDist)
        if row > len(viewMat) or col > len(viewMat[0]):
            print("행렬 초과..!")
            break
        viewMat[row][col] = 1

    return viewMat, rects

img1 = cv2.imread('../Images/ex_view_hand.jpg')
# 이미지 기울기 보정
img_horz, img_dlt = autoRotExView(img1)
# 전개도를 행렬로 변환
viewMat, rects = getExViewMatrix(img_dlt)
print(viewMat)

# 검출한 사각형 그리기
cv2.drawContours(img_horz, rects, -1, (0, 0, 255), 2)
# 정육면체 전개도인지 검사
cube = cb.Cube(viewMat)
if cube.isCube():
    print("정육면체 전개도입니다아ㅏㅏㅏ!!!!!!!")
else:
    print("정육면체 전개도가 아닙니다ㅏㅏㅏㅏㅏ!!!!")

imgs = {'Original': img1[:, :, ::-1], 'Rotate&Scale': img_horz[:,:,::-1], 'Dilate': img_dlt}

for i, (k, v) in enumerate(imgs.items()):
    plt.subplot(1, 3, i + 1)
    plt.title(k)
    plt.imshow(v, cmap='gray')
    plt.xticks([])
    plt.yticks([])
plt.show()

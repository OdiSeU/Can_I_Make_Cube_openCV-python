import numpy as np

class Rect:
    def __init__(self, idx):
        self.idx = idx

class Cube:
    #한 변의 길이
    def __init__(self, matrix):
        self.r = self.c = -1
        self.mat = []
        self.check = []
        self.staus = [
            # U, L, D, R
            [5, 3, 2, 4], # 1
            [1, 3, 6, 4], # 2
            [5, 6, 2, 4], # 3
            [5, 1, 2, 6], # 4
            [6, 3, 1, 4], # 5
            [2, 3, 5, 4]  # 6
        ]
        for i in range(0, len(matrix)):
            self.mat.append([])
            for j in range(0, len(matrix)):
                if matrix[i][j] == 1:
                    if self.r == -1 or self.c == -1:
                        self.r, self.c = i, j
                    self.check.append(False)
                    self.mat[i].append(Rect(-1))
                else:
                    self.mat[i].append(Rect(0))

    def isCube(self):
        if len(self.check) != 6:
            print("면의 개수", len(self.check))
            return False
        self.checkMatrix(self.r, self.c, 1)
        ans = True

        for ck in self.check:
            if ck == False:
                print("정육면체의 전개도가 아님!")
                ans = False
                break
        return ans

    def checkMatrix(self, r, c, now):
        if self.check[now - 1]:
            return False
        self.mat[r][c].idx = now
        self.check[now - 1] = True
        idx1 = -1
        idx2 = 0
        adj = [0, 0, 0, 0]
        vx = [0, -1, 0, 1]
        vy = [-1, 0, 1, 0]

        for i in range(0, 4):
            if 0 <= r + vy[i] < len(self.mat):
                if 0 <= c + vx[i] < len(self.mat[0]):
                    adj[i] = self.mat[r + vy[i]][c + vx[i]]
                    if adj[i].idx > 0:
                        idx1 = i
        if idx1 != -1:
            for i in range(0, 3):
                if adj[idx1].idx == self.staus[now - 1][idx2]:
                    break
                else:
                    idx2 = (idx2 + 1) % 4
        else:
            idx1 = 0

        for i in range(0, 4):
            if adj[idx1] != 0 and adj[idx1].idx == -1:
                self.checkMatrix(r + vy[idx1], c + vx[idx1], self.staus[now - 1][idx2])
            idx1 = (idx1 + 1) % 4
            idx2 = (idx2 + 1) % 4
# 给一个m×n的矩阵,如果某个位置元素为0,则把该元素对应的行与列所有元素全部变成0

def zero(matrix):
    row = len(matrix)
    columns = len(matrix[0])
    m, n = [0] * row, [0] * columns

    for i in range(row):
        for j in range(columns):
            if matrix[i][j] == 0:
                # 先纪录0出现的位置
                m[i] = 1
                n[j] = 1

    for k in range(row):
        for q in range(columns):
            if m[k] == 1 or n[q] == 1:
                matrix[k][q] = 0


if __name__ == '__main__':
    import numpy as np

    matrix = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    print(np.array(matrix), end='\n\n')
    zero(matrix)
    print(np.array(matrix))

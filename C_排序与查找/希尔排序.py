# 希尔排序:是插入排序的一种更高效的改进版本.但希尔排序是非稳定排序算法
# 希尔排序的基本思想是:先将整个待排序的记录序列分割成为若干子序列分别进行直接插入排序,待整个序列中的记录"基本有序"时,再对全体记录进行依次直接插入排序
def shellSort(lst):
    n = len(lst)
    gap = n // 2
    while gap > 0:
        for k in range(gap, n):
            cur = lst[k]
            j = k
            while j > gap - 1 and lst[j - gap] > cur:
                lst[j] = lst[j - gap]
                j -= gap
            lst[j] = cur
        gap = gap // 2

    return lst


'''
上述代码解析:
1. gap=12
    * 12和0,13和1,14和2,15和3,......,23和11进行插入排序
2. gap=6
    * 6和0,7和1,8和2,......,12和6和0,......,23和17和11进行插入排序
3. gap=3
    * 3和0,4和1,5和2,......,6和3和0,......,12和9和6和3和0,......,23和20和17和14和11和8和5和2进行插入排序
2. gap=1
    * 此时即为全部数据的插入排序
'''
if __name__ == '__main__':
    disorder_lst = [1, 34, 51, 6, 9, 3, 0, -2, 5, 88, 342, -55, 999, 7, 21, 512, 66, 8342, 134, 551, 43, 31, 85, 66]
    print(disorder_lst)
    print(shellSort(disorder_lst))

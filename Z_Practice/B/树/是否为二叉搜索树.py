from utity import binary_tree_by_list


pre = -float("inf")  # 负无穷大


def isValidBST(root):
    """验证是否为二叉搜索树(中序遍历)"""
    global pre  # 全局变量

    if root is None:
        return True
    
    if not isValidBST(root.left) or root.val <= pre:
        return False
    
    pre = root.val  #  更新pre的值
    
    return isValidBST(root.right)


if __name__ == '__main__':
    tree0 = binary_tree_by_list([2, 1, 3])
    print(isValidBST(tree0))  # print->True

    tree1 = binary_tree_by_list([5, 1, 4, None, None, 3, 6])
    print(isValidBST(tree1))  # print->False

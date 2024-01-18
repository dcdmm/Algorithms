class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def binary_tree_by_list(data):
    """从列表创建二叉树"""
    root = TreeNode(data[0])
    root_list = [root]
    i = 1
    while i < len(data):
        current = root_list.pop(0)
        if data[i] is not None:
            current.left = TreeNode(data[i])
            root_list.append(current.left)

        i += 1

        if i < len(data) and data[i] is not None:
            current.right = TreeNode(data[i])
            root_list.append(current.right)
        i += 1
    return root


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

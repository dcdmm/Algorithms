class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def binary_tree_by_list(data):
    """从列表(层序遍历得到)创建二叉树"""
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

if __name__ == '__main__':
    # 根节点:1
    # 第二层:2  2
    # 第三层:3  5
    # 第四层:4  4
    list0 = [1, 2, 2, 3, None, None, 5, 4, None, None, 4]

    tree0 = binary_tree_by_list(list0)
    
    print(tree0.val)
    print(tree0.left.val)  # print->2
    print(tree0.right.val)  # print->2
    print(tree0.left.left.left.val)  # print->4
    print(tree0.right.right.right.val)  # print->4

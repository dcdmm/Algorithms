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

if __name__ == '__main__':
    list0 = [3, 9, 20, None, None, 15, 7]
    tree0 = binary_tree_by_list(list0)
    
    print(tree0.val)
    print(tree0.left.val)
    print(tree0.right.val)
    print(tree0.right.left.val)
    print(tree0.right.right.val)
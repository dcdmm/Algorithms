class Node:
    def __init__(self, element, pointer):
        self._element = element
        self._pointer = pointer


def delete_node(node):
    """单向链表删除node节点"""
    del_node = node._pointer
    node._element = node._pointer._element
    node._pointer = node._pointer._pointer
    del del_node


if __name__ == '__main__':
    node0 = Node(0, None)
    node1 = Node(1, node0)
    node2 = Node(2, node1)
    node3 = Node(3, node2)

    print(node3._pointer._element)  # print->2  

    delete_node(node2)
    
    print(node3._pointer._element)  # print->0
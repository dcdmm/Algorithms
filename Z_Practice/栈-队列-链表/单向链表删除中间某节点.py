def delete_node(node):
    """单向链表删除node节点"""
    del_node = node._pointer
    node._element = node._pointer._element
    node._pointer = node._pointer._pointer
    del del_node
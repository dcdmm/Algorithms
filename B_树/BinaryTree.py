from Tree import Tree


class BinaryTree(Tree):
    """Abstract base class representing a binary tree structure."""

    # --------------------- additional abstract methods ---------------------
    def left(self, p):
        """Return a Position representing p's left child.

        Return None if p does not have a left child.
        """
        raise NotImplementedError("must be implemented by subclass")

    def right(self, p):
        """Return a Position representing p's right child.

        Return None if p does not have a right child.
        """
        raise NotImplementedError("must be implemented by subclass")

    # ---------- concrete methods implemented in this class ----------
    def siblings(self, p):
        """Return a Position representing p s sibling (or None if no sibling)."""
        parent = self.parent(p)
        if parent is None:  # p must be root
            return None  # root has no sibling
        else:
            # 把位置p的兄弟节点定义为p双亲节点的"另一个"孩子节点
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of Positions representing p s children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)


# 二叉树
class LinkedBinaryTree(BinaryTree):
    """
    Linked representation of a binary tree structure.

    二叉树链式存储结构实现方式性能:
    len: O(1)
    is_empty: O(1)
    root: O(1)
    parent: O(1)
    left: O(1)
    right: O(1)
    sibling: O(1)
    children: O(1)
    num_children: O(1)
    is_root: O(1)
    is_leaf: O(1)
    depth(p): O(d_p + 1)  # 其中d_p指的是树T中p节点的深度(最坏情况下为O(n),其中n是树中节点的总个数)
    height: O(n) # 其中n是树中节点的总个数
    _add_root: O(1)
    _add_left: O(1)
    _add_right: O(1)
    _replace: O(1)
    _delete: O(1)
    _attach: O(1)
    """

    class _Node:  # Lightweight, nonpublic class for storing a node.
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent  # 该节点的父节点(可以双向遍历)
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Positon type')
        if p._container is not self:
            raise ValueError("p does not belong to the container")
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    # -------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # -------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p s parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:  # left child exists
            count += 1
        if node._right is not None:  # risht child exists
            count += 1
        return count

    def _add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None: raise ValueError("Root exists")
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        """
        Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None: raise ValueError("Left child exists")
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """
        Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None: raise ValueError("Right child exists")
        self._size += 1
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        """
        Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError("p has two children")  # 不支持删除拥有2个孩子的节点
        child = node._left if node._left else node._right
        if child is not None:  # 拥有一个孩子
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')  # 如果p不是叶子节点,则抛出错误
        if not type(self) is type(t1) is type(t2): raise ValueError('Tree must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None  # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None  # set t1 instance to empty
            t2._size = 0

    def preorder(self):  # 先序遍历
        """Generate a preorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):  # start recursion
                yield p

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p  # visit p before its subtrees
        for c in self.children(p):
            for other in self._subtree_preorder(c):  # do preorder of c's subtree
                yield other  # yielding each to our caller

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):  # 后序遍历
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p  # visit p after its subtrees

    def inorder(self):  # 中序遍历
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:  # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other

        yield p  # visit p between its subtrees

        if self.right(p) is not None:  # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

if __name__ == '__main__':
    lbt = LinkedBinaryTree()  # 初始化

    """
    二叉树lbt结构如下:
            r
        rl      rr
    rll 
        rllr
    rllrl   rllrr
                    rllrrr
                            rllrrrr
                       rllrrrrl
                                rllrrrrll  
    """
    r = lbt._add_root(0)
    rl = lbt._add_left(r, 10)
    rr = lbt._add_right(r, 20)
    rll = lbt._add_left(rl, 30)
    rllr = lbt._add_right(rll, 40)
    rllrl = lbt._add_left(rllr, 50)
    rllrr = lbt._add_right(rllr, 60)
    rllrrr = lbt._add_right(rllrr, 70)
    rllrrrr = lbt._add_right(rllrrr, 80)
    rllrrrrl = lbt._add_left(rllrrrr, 90)
    rllrrrrll = lbt._add_left(rllrrrrl, 90)

    # print(lbt.siblings(rl)._node._element)  # r1的兄弟节点的值为20
    # print(lbt.left(rllrrrr)._node._element)  # rllrrrr的左节点的值为90
    # for c in lbt.children(rllr):  # rllr的左节点的值为50,右节点的值为60
    #     print(c._node._element)
    # print(lbt.num_children(r))  # r有2个孩子
    # print(lbt.depth(rllrrr))  # rllrrr的深度为5
    # print(lbt.height(r))  # r的高度为8

    for i in lbt.preorder():  # 先序遍历
        print(i._node._element)

    print()

    for j in lbt.postorder():  # 后序遍历
        print(j._node._element)

    print()

    for k in lbt.inorder():  # 中序遍历
        print(k._node._element)

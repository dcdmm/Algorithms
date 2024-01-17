from collections.abc import MutableMapping  # 抽象基类

from BinaryTree import LinkedBinaryTree


class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic Item class."""

    # ------------------------------- nested Item class -------------------------------
    class _Item:
        """Lightweight composite to store key-value pairs as map items."""
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class TreeMap(LinkedBinaryTree, MapBase):
    """
    Sorted map implementation using a binary search tree.
    """

    # ---------------------------- override Position class ----------------------------
    class Position(LinkedBinaryTree.Position):
        def key(self):
            """Return key of map's key-value pair."""
            return self.element()._key

        def value(self):
            """Return value of map's key-value pair"""
            return self.element()._value

    # ------------------------------- nonpublic utilities -------------------------------
    # 从根节点开始每一次下降一层.因此,节点的数量被限定为h+1,其中h是二叉树的高度,换句话说,因为每一个节点的搜索时间为O(1),则总的搜索运行时间为O(h)
    def _subtree_search(self, p, k):
        """Return Position of p's subtree having key k, or last node searched."""
        if k == p.key():  # found match
            return p
        elif k < p.key():  # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:  # search right subtree
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p  # unsucessful search

    def _subtree_first_positon(self, p):
        """Return Position of first item in subtree rooted at p."""
        walk = p
        while self.left(walk) is not None:  # keep walking left
            walk = self.left(walk)
        return walk

    def _subtree_last_positon(self, p):
        """Return Position of last item in subtree rooted at p."""
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):  # 时间复杂度:O(h),其中h为树的高度
        """返回一个包含最小键的节点,如果树为空,则返回None"""
        return self._subtree_first_positon(self.root()) if len(self) > 0 else None

    def last(self):  # 时间复杂度:O(h),其中h为树的高度
        """返回一个包含最大键的节点,如果树为空,则返回None"""
        return self._subtree_last_positon(self.root()) if len(self) > 0 else None

    def before(self, p):  # 时间复杂度:O(h),其中h为树的高度
        """
        返回比节点p的键小的所有节点中键最大的节点(即中序遍历中在p之前最后一个被访问的节点)

        二叉树特性(假设节点p存储了一个键值对(k,v)):
        * 存储在p的左子树的键都小于k
        * 存储在p的右子树的键都大于k
        """
        self._validate(p)  # inherited from LinedBinary Tree
        if self.left(p):
            return self._subtree_last_positon(self.left(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)  # 节点p的父节点
            while above is not None and walk == self.left(above):  # 父节点不为None且p为父节点的左节点
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):  # 时间复杂度:O(h),其中h为树的高度
        """
        返回比节点p的键大的所有节点中键最小的节点(即中序遍历中在p之后第一个被访问的节点)
        """
        self._validate(p)
        if self.right(p):
            return self._subtree_first_positon(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_min(self):  # 时间复杂度:O(h),其中h为树的高度
        """Return (key,value) pair with minimum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_max(self):  # 时间复杂度:O(h),其中h为树的高度
        """Return (key,value) pair with maximum key (or None if empty)."""
        if self.is_empty():
            return None
        else:
            p = self.last()
            return (p.key(), p.value())

    def __getitem__(self, k):  # 时间复杂度:O(h),其中h为树的高度
        """Return value associated with key k (raise KeyError if not found)."""
        if self.is_empty():
            raise KeyError("Key Error: " + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            if k != p.key():  # 没有找到
                raise KeyError("Key Error: " + repr(k))
            return p.value

    def __setitem__(self, k, v):  # 时间复杂度:O(h),其中h为树的高度
        """Assign value v to key k, overwriting existing value if present."""
        if self.is_empty():
            self._add_root(self._Item(k, v))
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v  # replace existing item’s value
                return
            else:
                # 新的节点可以插到树的下一层
                item = self._Item(k, v)
                if p.key() < k:
                    self._add_right(p, item)  # inherited from LinkedBinaryTree
                else:
                    self._add_left(p, item)

    def delete(self, p):  # 时间复杂度:O(h),其中h为树的高度
        """Remove the item at given Position."""
        self._validate(p)  # inherited from LinkedBinaryTree
        if self.left(p) and self.right(p):  # p has two children
            replacement = self._subtree_last_positon(self.left(p))  # 比节点p的键小的所有节点中键最大的节点r(肯定没有2个子节点,不然其右子节点的键肯定比p大)
            self._replace(p, replacement.element())  # 使用t节点的值替换p节点原有的值
            p = replacement  # 删除r节点(r节点最多子只有1个子节点)
        # now p has at most one child
        self._delete(p)  # inherited from LinkedBinaryTree

    def __delitem__(self, k):  # 时间复杂度:O(h),其中h为树的高度
        """Remove item associated with key k (raise KeyError if not found)."""
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)
                return
        raise KeyError("Key Error: " + repr(k))

    def __iter__(self):  # 时间复杂度:O(n)
        """Generate an iteration of all keys in the map in order."""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)


if __name__ == '__main__':
    pass

class Tree:
    """Abstract base class representing a tree structure."""

    # ------------------------------- nested Position class -------------------------------
    class Position:
        """An abstraction representing the location of a single element."""

        def element(self):
            """Return the element stored at this Position."""
            raise NotImplementedError("must be implemented by subclass")

        def __eq__(self, other):
            """Return True if other Position represents the same location."""
            raise NotImplementedError("must be implemented by subclass")

        def __ne__(self, other):
            """Return True if other does not represent the same location."""
            raise NotImplementedError("must be implemented by subclass")

    # ---------- abstract methods that concrete subclass must support ----------
    def root(self):
        """Return Position representing the tree s root (or None if empty)."""
        raise NotImplementedError("must be implemented by subclass")

    def parent(self, p):
        """Return Position representing p s parent (or None if p is root)."""
        raise NotImplementedError("must be implemented by subclass")

    def num_children(self, p):
        """Return the number of children that Position p has."""
        raise NotImplementedError("must be implemented by subclass")

    def children(self, p):
        """Generate an iteration of Positions representing p s children."""
        raise NotImplementedError("must be implemented by subclass")

    def __len__(self):
        """Return the total number of elements in the tree."""
        raise NotImplementedError("must be implemented by subclass")

    # ---------- concrete methods implemented in this class ----------
    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        if self.is_root(p):  # 如果p是根节点,那么p的深度为0
            return 0
        else:
            return 1 + self.depth(self.parent(p))  # p的深度就是其父节点的深度+1

    def _height(self, p):
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0  # 如果p是一个叶子节点,那么它的高度为0
        else:
            return 1 + max(self._height(c) for c in self.children(p))  # p的高度就是它孩子节点中的最大高度+1

    def height(self, p=None):
        """Return the height of the subtree rooted at Position p.

        If p is None, return the height of the entire tree.
        """
        if p is None:
            p = self.root()
        return self._height(p)


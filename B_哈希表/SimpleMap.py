"""
This list-based map implementation is simple, but it is not particularly efficient.
Each of the fundamental methods, __getitem__, __setitem__, and __delitem__,
relies on a for loop to scan the underlying list of items in search of a matching key.
In a best-case scenario, such a match may be found near the beginning of the list, in
which case the loop terminates; in the worst case, the entire list will be examined.
Therefore, each of these methods runs in O(n) time on a map with n items
"""
from MapBase import MapBase


class SimpleMap(MapBase):
    """map的简单实现"""

    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __getitem__(self, k):  # 时间复杂度O(n)
        """Return value associated with key k (raise KeyError if not found)."""
        for item in self._table:  # 依赖for循环扫描列表中的元素
            if k == item._key:
                return item._value
        raise KeyError('Key Error:' + repr(k))

    def __setitem__(self, k, v):  # 时间复杂度O(n)
        """Assign value v to key k, overwriting existing value if present."""
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):  # 时间复杂度O(n)
        """Remove item associated with key k (raise KeyError if not found)."""
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError('Key Error:' + repr(k))

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __iter__(self):  # 时间复杂度O(1)
        """Generate iteration of the map s keys."""
        for item in self._table:
            yield item._key


if __name__ == '__main__':
    ut = SimpleMap()
    ut['a'] = 1
    ut['b'] = 2
    ut['c'] = 3
    ut['a'] = -1
    del ut['b']

    for (m, n) in ut.items():
        print(m, n)

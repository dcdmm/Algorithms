from abc import ABC
from random import randrange

from MapBase import MapBase
from SimpleMap import SimpleMap


class HashMapBase(MapBase, ABC):
    """Abstract base class for map using hash-table with MAD compression."""

    def __init__(self, cap=11, p=109345121):
        """Create an empty hash-table map."""
        self._table = cap * [None]
        self._n = 0  # 当前储存在哈希表中不同元素的个数
        self._prime = p  # MAD方法中的p
        self._scale = 1 + randrange(p - 1)  # MAD方法中的a
        self._shift = randrange(p)  # MAD方法中的b

    def _hash_function(self, k):
        # 依靠python内置哈希函数生成键的哈希码

        # len(self._table):MAD方法中的N
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)
        self._n -= 1

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v

    def _bucket_getitem(self, j, k):
        pass

    def _bucket_setitem(self, j, k, v):
        pass

    def _bucket_delitem(self, j, k):
        pass


# 分类链表实现的具体哈希map类
class ClainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution."""

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error:' + repr(k))
        return bucket[k]

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = SimpleMap()  # 每个桶A[j]存储自身的二级容器
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error:' + repr(k))
        del bucket[k]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for (k, v) in bucket.items():  # 遍历二级容器(调用SimpleMa __iter__方法)
                    yield k, v


# 含线性探测的开发寻址实现的具体哈希map类
class ProbeHashMap(HashMapBase):
    """Hash map implemented with linear probing for collision resolution."""
    _AVAIL = object()  # sentinal marks locations of previous deletions

    def _is_available(self, j):
        """Return True if index j is available in table."""
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        """
        Search for key k in bucket at index j.

        Return (success, index) tuple, described as follows:
        If match was found, success is True and index denotes its location.
        If no match found, success is False and index denotes first available slot.
        """
        firstAvail = None
        while True:
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self._table[j] is None:
                    return (False, firstAvail)  # search has failed
            elif k == self._table[j]._key:
                return (True, j)  # found a match
            j = (j + 1) % len(self._table)  # keep looking(cyclically)

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error:' + repr(k))
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._Item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError('Key Error:' + repr(k))
        self._table[s] = ProbeHashMap._AVAIL  # mark as vacated

    def __iter__(self):
        for i in range(len(self._table)):
            if not self._is_available(i):
                yield self._table[i]._key, self._table[i]._value


if __name__ == '__main__':
    chm = ClainHashMap()
    chm['a'] = 1
    chm['b'] = 2
    chm['c'] = 3
    chm['b'] = -2
    del chm['a']
    for i in chm:
        print(i)

    print('*' * 100)

    phm = ProbeHashMap()
    phm['a'] = 1
    phm['b'] = 2
    phm['c'] = 3
    phm['b'] = -2
    del phm['a']
    for j in phm:
        print(j)

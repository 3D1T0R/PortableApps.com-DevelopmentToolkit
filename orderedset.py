# Taken from http://code.activestate.com/recipes/576694/
# By Raymond Hettinger, MIT license

import collections

__all__ = ['OrderedSet']

KEY, PREV, NEXT = range(3)

def multi_property(fnfn): # This decorator is added by Chris Morgan
    def decorate(self, *args):
        result = self
        for i in args:
            result = fnfn(result)(i)
        return result
    return decorate

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev

    def __iter__(self):
        end = self.end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self.end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return collections.MutableSet.__eq__(self, other)

    def __del__(self):
        try:
            self.clear()                    # remove circular references
        except Exception:
            pass # TODO: fix this. Without wrapping this in a try block, I often get this:
        # Exception TypeError: TypeError('list indices must be integers, not NoneType',) in  ignored

    # Below this line are additions by Chris Morgan to get these methods back.
    difference = multi_property(lambda self: self.__sub__)
    difference_update = multi_property(lambda self: self.__isub__)
    intersection = multi_property(lambda self: self.__and__)
    intersection_update = multi_property(lambda self: self.__iand__)
    issubset = property(lambda self: self.__le__)
    issuperset = property(lambda self: self.__ge__)
    symmetric_difference = property(lambda self: self.__xor__)
    symmetric_difference_update = property(lambda self: self.__ixor__)
    union = multi_property(lambda self: self.__or__)


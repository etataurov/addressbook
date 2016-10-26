import weakref


class IndexNode:
    def __init__(self):
        self.tree = {}
        self.values = weakref.WeakSet()


class AttributeIndex:
    def __init__(self):
        self.start = IndexNode()
        self.keys = weakref.WeakValueDictionary()

    def add(self, attribute):
        node = self.start
        key = attribute.value
        self.keys[key] = attribute
        for letter in key:
            node = node.tree.setdefault(letter, IndexNode())
            node.values.add(attribute)

    def search(self, prefix):
        if prefix in self.keys:
            return [self.keys[prefix]]
        node = self.start
        for letter in prefix:
            node = node.tree.get(letter)
            if node is None:
                return []
        return list(node.values)

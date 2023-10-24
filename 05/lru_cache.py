class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class ListNode:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, node: Node):
        if not self.head and not self.tail:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def pop_tail(self):
        if self.tail:
            old_tail = self.tail
            self.tail = old_tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
            old_tail.prev = None
            return old_tail
        return None

    def move_to_head(self, node: Node):
        if self.head != node:
            if node.next:
                node.next.prev = node.prev
            if node.prev:
                node.prev.next = node.next
            if node == self.tail:
                self.tail = node.prev
            node.prev = None
            node.next = self.head
            if self.head:
                self.head.prev = node
            else:
                self.tail = node
            self.head = node


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.keys = {}
        self.values = ListNode()

    def get(self, key):
        if key in self.keys:
            node = self.keys[key]
            self.values.move_to_head(node)
            return node.value
        return None

    def set(self, key, value):
        if self.limit:
            if key not in self.keys and len(self.keys) >= self.limit:
                tail = self.values.pop_tail()
                if tail is not None:
                    del self.keys[tail.key]
            if key in self.keys:
                node = self.keys[key]
                node.value = value
            else:
                new_node = Node(key, value)
                self.values.add(new_node)
                self.keys[key] = new_node
            self.values.move_to_head(self.keys[key])

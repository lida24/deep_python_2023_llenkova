import logging
import sys
import argparse


def setup_logger(cmd_arguments):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_format = logging.Formatter(
        "======%(levelname)s - %(message)s"
    )
    stdout_handler.setFormatter(stdout_format)
    file_handler = logging.FileHandler("cache.log")
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        "====== %(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    blocked_level = logging.INFO
    custom_filter = CustomFilter(blocked_level)

    if cmd_arguments.s:
        logger.addHandler(stdout_handler)
    if cmd_arguments.f:
        logger.addFilter(custom_filter)
    return logging.getLogger(__name__)


class CustomFilter(logging.Filter):
    def __init__(self, block_level):
        super().__init__()
        self.block_level = block_level

    def filter(self, record):
        return record.levelno != self.block_level


class Node:
    def __init__(self, key, value):
        logger.debug("Initializing node with key=%s and value=%s", key, value)
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class ListNode:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, node: Node):
        logger.debug(
            "Adding node with key=%s and value=%s to the list", node.key, node.value
        )
        if not self.head and not self.tail:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def pop_tail(self):
        if self.tail:
            logger.debug(
                "Popped tail with key=%s and value=%s", self.tail.key, self.tail.value
            )
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
        logger.debug(
            "Moving node with key=%s and value=%s to the head of the list",
            node.key,
            node.value,
        )
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
        if limit <= 0:
            logger.error("Error creating LRUCache with parameter limit=%s", limit)
            raise ValueError("Limit must be a positive integer")
        self.limit = limit
        self.keys = {}
        self.values = ListNode()
        logger.info("New LRUCache created with limit=%s", limit)

    def get(self, key):
        if key in self.keys:
            logger.info("Getting existing key=%s", key)
            node = self.keys[key]
            self.values.move_to_head(node)
            return node.value
        logger.info("Trying to get non-existing key=%s", key)
        return None

    def set(self, key, value):
        if key not in self.keys and len(self.keys) >= self.limit:
            logger.info(
                "Setting new key=%s with value=%s when limit is reached", key, value
            )
            tail = self.values.pop_tail()
            if tail is not None:
                del self.keys[tail.key]
        if key in self.keys:
            logger.info("Setting existing key=%s with value=%s", key, value)
            node = self.keys[key]
            node.value = value
        else:
            logger.info("Setting new key=%s with value=%s", key, value)
            new_node = Node(key, value)
            self.values.add(new_node)
            self.keys[key] = new_node
        self.values.move_to_head(self.keys[key])


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-s", action="store_true")
    arg_parser.add_argument("-f", action="store_true")
    args = arg_parser.parse_args()
    logger = setup_logger(args)

    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")
    cache.get("k1")
    cache.get("k2")
    cache.set("k4", "val4")
    cache.get("k2")
    cache.get("k3")

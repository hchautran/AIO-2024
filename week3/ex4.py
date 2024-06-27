class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self._queue = []

    def is_empty(self):
        return len(self._queue) == 0

    def is_full(self):
        return len(self._queue) == self.capacity

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._queue.pop(0)

    def enqueue(self, value):
        if self.is_full():
            raise OverflowError("enqueue to full queue")
        self._queue.append(value)

    def front(self):
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._queue[0]

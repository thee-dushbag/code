import heapq as _heapq


class QueueError(Exception):
    ...


class QueueEmpty(QueueError):
    ...


class QueueFull(QueueError):
    ...


class Queue:
    def __init__(self, size: int | None = None, /) -> None:
        self._maxsize = 0 if size is None or size <= 0 else size
        self._store = []
        self._size = 0

    def full(self):
        if self._maxsize <= 0:
            return False
        return self._size >= self._maxsize

    def empty(self):
        return self._size <= 0

    def _putter(self):
        if self.full():
            raise QueueFull
        self._size += 1

    def _getter(self):
        if self.empty():
            raise QueueEmpty
        self._size -= 1

    def put(self, value):
        self._putter()
        self._put(value)

    def get(self):
        self._getter()
        return self._get()

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        return self

    def __next__(self):
        if self.empty():
            raise StopIteration
        return self.get()

    def extend(self, iterable):
        for value in iterable:
            self.put(value)

    def _put(self, value):
        self._store.append(value)

    def _get(self):
        return self._store.pop(0)


class LIFOQueue(Queue):
    def _get(self):
        return self._store.pop()


class PriorityQueue(Queue):
    def _get(self):
        return _heapq.heappop(self._store)

    def _put(self, value):
        _heapq.heappush(self._store, value)


class Deque(LIFOQueue):
    def putleft(self, value):
        self._putter()
        self._putleft(value)

    def getleft(self):
        self._getter()
        return self._getleft()

    def _getleft(self):
        return self._store.pop(0)

    def _putleft(self, value):
        self._store.insert(0, value)

    def extendleft(self, iterable):
        for value in iterable:
            self.putleft(value)

    def __next__(self):
        if self.empty():
            raise StopIteration
        return self.getleft()

    def __reversed__(self):
        while not self.empty():
            yield self.get()


def test_queue():
    data = [1, 2, 3, 4, 5]
    q = Queue()
    q.extend(data)
    for d in data:
        assert d == q.get()


def test_lifoqueue():
    data = [1, 2, 3, 4, 5]
    q = LIFOQueue()
    q.extend(data)
    data = reversed(data)
    for d in data:
        assert d == q.get()


def test_priority_queue():
    data = [1, 0.5, 1.5, 0.8, 0, 0.2, 2, 5, 0.3]
    q = PriorityQueue()
    q.extend(data)
    data.sort()
    for d in data:
        assert d == q.get()


def test_deque():
    data2 = [10, 20, 30]
    data3 = [110, 120, 130]
    q = Deque()
    q.put(50)
    q.extend(data2)
    q.extendleft(data3)
    data2.reverse()
    data3.reverse()
    for d in data2:
        assert d == q.get()
    for d in data3:
        assert d == q.getleft()
    assert 50 == q.get()


def test_errors():
    q = Queue(1)
    try:
        q.get()
    except QueueEmpty:
        ...
    else:
        raise Exception("Expected the queue to be empty.")

    q.put(1)

    try:
        q.put(2)
    except QueueFull:
        ...
    else:
        raise Exception("Expected queue to be full")


def test_iteration():
    data = [1, 0.5, 1.5, 0.8, 0, 0.2, 2, 5, 0.3]
    q = Queue()
    q.extend(data)
    assert data == list(q)
    q = LIFOQueue()
    q.extend(data)
    assert list(reversed(data)) == list(q)
    q = PriorityQueue()
    q.extend(data)
    assert sorted(data) == list(q)
    q = Deque()
    q.extendleft(data)
    assert data == list(reversed(q))

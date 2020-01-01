from bullet import Status

COUNTER = 0


class SequenceItem:
    """Элемент последовательности шариков"""

    def __init__(self, ball, next, past):
        self.next = next
        self.past = past
        self.value = ball
        global COUNTER
        self.count = COUNTER
        COUNTER += 1


class Sequence:
    """Последовательность шариков"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        """Содержит ли последовательность шарики"""
        return self.head is None

    def enqueue(self, ball):
        """Добавление элемента в конец последовательности (вызывается
        при добавлении шаров, которые должны быть изначально в уровне) """
        if self.is_empty():
            self.head = self.tail = SequenceItem(ball, None, None)
        else:
            item = SequenceItem(ball, self.tail, None)
            self.tail.past = item
            self.tail = item
        self.size += 1

    def add_ball(self, ball, next_ball):
        """
        Добавить шар в последовательность после 'next_ball'
        :type ball: Ball
        :type next_ball: SequenceItem
        """
        item = SequenceItem(ball, next_ball, next_ball.past)
        next_ball.past.next = item
        next_ball.past = item
        self._offset_next(item)
        self.size += 1

    def replace_head(self, ball):
        """Замена головы последовательности"""
        item = SequenceItem(ball, None, self.head)
        self.head.next = item
        self.head = item
        self.size += 1

    def replace_tail(self, ball):
        """Замена хвоста последовательности"""
        item = SequenceItem(ball, self.tail, None)
        self.tail.past = item
        self.tail = item
        self._offset_next(item)
        self.size += 1

    def _offset_next(self, tmp):
        while tmp is not None:
            if tmp.next is not None:
                tmp.value.position = tmp.next.value.position
                tmp.value.parameter = tmp.next.value.parameter
            tmp = tmp.next

    def delete_similar(self, ball, collision):
        """
        Удаляет шары одинакового с `ball` цвета
        @type ball: Ball
        @type collision: SequenceItem
        """
        start, end, length = self.get_delete_interval(ball, collision)
        #print('length', length)
        if length < 3:
            return False
        if end == self.head:
            if start == self.tail:
                self.size -= length
                self.head = self.tail = None
                return True
            self.head = start.past
            start = None
            self.head.next = None
            self.size -= length
            return True
        tmp1 = end.next
        tmp2 = start
        positions = []
        while tmp2 is not None:
            positions.append((tmp2.value.position, tmp2.value.parameter))
            tmp2 = tmp2.next
        i = 0
        while tmp1 is not None:
            tmp1.value.position = positions[i][0]
            tmp1.value.parameter = positions[i][1]
            tmp1 = tmp1.next
            i += 1
        tmp = start
        while tmp != end:
            tmp.value.status = Status.CAN_DELETE
            tmp = tmp.next
        if start == self.tail:
            self.tail = end.next
            self.tail.past = None
        else:
            start.past.next = end.next
        end.next.past = start.past
        self.size -= length
        #print('current size ', self.size)
        return True

    def get_delete_interval(self, ball, collision):
        """
        Определяет интервал, с одинаковым цветом шаров.
        @type ball: Ball
        @type collision: SequenceItem
        """
        start = None
        end = None
        length = 0
        tmp = ball
        if collision != self.tail and collision.past.value == ball:
            tmp = collision.past
        else:
            tmp = collision.next
        starter = tmp
        while tmp is not None and ball.color == tmp.value.color:
            start = tmp
            length += 1
            tmp = tmp.past

        tmp = starter
        while tmp is not None and ball.color == tmp.value.color:
            end = tmp
            length += 1
            tmp = tmp.next
        return start, end, length - 1

    def change_status(self, start, end):
        tmp = start
        while tmp != end:
            tmp.value.status = Status.CAN_DELETE
            tmp = tmp.next
        end.value.status = Status.CAN_DELETE

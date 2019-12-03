class SequenceItem:
    def __init__(self, ball, next, past):
        self.next = next
        self.past = past
        self.value = ball


class Sequence:
    tail: SequenceItem
    head: SequenceItem
    size: int

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def enqueue(self, ball):
        if self.is_empty():
            self.head = self.tail = SequenceItem(ball, None, None)
        else:
            item = SequenceItem(ball, self.tail, None)
            self.tail.past = item
            self.tail = item
        self.size += 1

    def add_ball(self, ball, next_ball):
        """
        :type ball: Ball
        :type next_ball: SequenceItem
        """
        item = SequenceItem(ball, next_ball, next_ball.past)
        next_ball.past.next = item
        next_ball.past = item

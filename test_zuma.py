import math
import os
import sys
import unittest

from Point import Point
from ball import Ball
from bullet import Bullet, Status
from colors import Colors
from frog import Frog
from game import Game
from levels import *
from player import *
from sequence import Sequence


class BallTest(unittest.TestCase):
    def test_change_position(self):
        ball = Ball(0, 0, Colors.red)
        ball.change_position(Point(1, 1), 5)
        self.assertEqual(5, ball.parameter)
        self.assertEqual(str(Point(1, 1)), str(ball.position))

    def test_collision(self):
        ball1 = Ball(0, 0, Colors.red)
        ball2 = Ball(10, 10, Colors.red)
        ball3 = Ball(40, 40, Colors.red)
        self.assertTrue(ball1.is_collision(ball2))
        self.assertFalse(ball1.is_collision(ball3))

    def test_distance(self):
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        self.assertEqual(0, p1.get_distance(p1))
        self.assertEqual(math.sqrt(2), p1.get_distance(p2))


class FrogTest(unittest.TestCase):
    def test_swap_balls(self):
        frog = Frog(Point(0, 0))
        b1 = frog.current_ball
        b2 = frog.next_ball
        frog.swap_balls()
        self.assertEqual(b1, frog.next_ball)
        self.assertEqual(b2, frog.current_ball)

    def test_get_next_ball(self):
        frog = Frog(Point(0, 0))
        b1 = frog.next_ball
        frog.get_next_ball()
        self.assertEqual(b1, frog.current_ball)

    def test_rotation(self):
        frog = Frog(Point(0, 0))
        frog.transform_angle(Point(0, -1))
        self.assertEqual(-180, frog.angle)
        frog.transform_angle(Point(-1, 1))
        self.assertEqual(45, frog.angle)


class BulletTest(unittest.TestCase):
    def test_update_position(self):
        ball = Ball(0, 0, Colors.red)
        bullet = Bullet(1, 1, ball)
        bullet.update_position()
        self.check_position(bullet)
        bullet.status = Status.CAN_DELETE
        bullet.update_position()
        self.check_position(bullet)

    def check_position(self, bullet):
        self.assertEqual(1, bullet.ball.position.x)
        self.assertEqual(1, bullet.ball.position.y)


class TableTest(unittest.TestCase):
    def test_player_inc(self):
        player = Player('')
        player.inc_scores(0)
        self.assertEqual(0, player.scores)
        player.inc_scores(3)
        self.assertEqual(300, player.scores)
        player.inc_scores(4)
        self.assertEqual(1100, player.scores)

    def fill_table(self):
        table = ResultTable('test_scores.txt')
        for i in range(0, 5):
            player = Player(str(i))
            player.inc_scores(i + 3)
            table.add_player(player)
        table.save_table()

    def test_table_size(self):
        self.fill_table()
        table = ResultTable('test_scores.txt')
        self.assertEqual(5, len(table.get_table()))

    def test_player_names(self):
        self.fill_table()
        table = ResultTable('test_scores.txt')
        self.assertEqual(['4', '3', '2', '1', '0'], [i.name for i in table.get_table()])

    def test_table_change_score(self):
        self.fill_table()
        table = ResultTable('test_scores.txt')
        p = Player('4')
        l = LevelTest1()
        l.update_balls_position()
        l.update_balls_position()
        l.update_balls_position()
        g = Game(Frog(Point(100, 200)), l, Player(''))
        g.bullets.append(Bullet(1, 1, Ball(4, 4, Colors.red)))
        g.update(Point(-1, 0))
        p.inc_scores(8)
        table.add_player(p)
        self.assertEqual(4800, table.get_table()[0].scores)


class SequenceTest(unittest.TestCase):
    def test_enqueue(self):
        sq = Sequence()
        self.assertTrue(sq.is_empty())
        b1 = Ball(0, 0, Colors.red)
        b2 = Ball(1, 1, Colors.blue)
        sq.enqueue(b1)
        sq.enqueue(b2)
        self.assertEqual([b1, b2], self.get_balls(sq))

    def test_add_ball(self):
        sq = Sequence()
        b1 = Ball(0, 0, Colors.red)
        b2 = Ball(1, 1, Colors.blue)
        b3 = Ball(2, 2, Colors.green)
        sq.enqueue(b1)
        sq.enqueue(b2)
        sq.add_ball(b3, sq.head)
        self.assertEqual([b1, b3, b2], self.get_balls(sq))

    def test_replace_head(self):
        sq = Sequence()
        b1 = Ball(0, 0, Colors.red)
        b2 = Ball(1, 1, Colors.blue)
        b3 = Ball(2, 2, Colors.green)
        sq.enqueue(b1)
        sq.enqueue(b2)
        sq.replace_head(b3)
        self.assertEqual([b3, b1, b2], self.get_balls(sq))

    def test_replace_tail(self):
        sq = Sequence()
        b1 = Ball(0, 0, Colors.red)
        b2 = Ball(1, 1, Colors.blue)
        b3 = Ball(2, 2, Colors.green)
        sq.enqueue(b1)
        sq.enqueue(b2)
        sq.replace_tail(b3)
        self.assertEqual([b1, b2, b3], self.get_balls(sq))

    def test_get_delete_interval(self):
        sq = Sequence()
        balls = [Ball(0, 0, Colors.red), Ball(2, 2, Colors.green),
                 Ball(3, 3, Colors.green), Ball(4, 4, Colors.green),
                 Ball(1, 1, Colors.blue)]
        for b in balls:
            sq.enqueue(b)
        ball = Ball(5, 5, Colors.green)
        sq.add_ball(ball, sq.head.past)
        result = sq.get_delete_interval(ball, sq.head.past)
        self.assertEqual((sq.tail.next, sq.head.past, 4), result)

    def test_delete_similar(self):
        sq = Sequence()
        balls = [Ball(0, 0, Colors.red), Ball(2, 2, Colors.green),
                 Ball(3, 3, Colors.green), Ball(4, 4, Colors.green),
                 Ball(1, 1, Colors.blue)]
        for b in balls:
            sq.enqueue(b)
        ball = Ball(5, 5, Colors.green)
        sq.add_ball(ball, sq.head.past)
        sq.delete_similar(ball, sq.head.past)
        self.assertEqual([balls[0], balls[4]], self.get_balls(sq))

    def get_balls(self, sq):
        tmp = sq.head
        result = []
        while tmp is not None:
            result.append(tmp.value)
            tmp = tmp.past
        return result


class LevelTest(unittest.TestCase):
    def test_get_path(self):
        level = LevelTest1()
        path = level.get_path()
        self.assertEqual(1000, len(path))

    def test_increase_coverage(self):
        levels = [Level1(),
                  Level2(),
                  Level3(),
                  Level4(),
                  Level0()]
        self.assertEqual(5, len(levels))

    def test_create_sequence(self):
        level = LevelTest1()
        level.update_balls_position()
        level.update_balls_position()
        level.update_balls_position()
        self.assertEqual(3, level.released_balls)
        ball = level.sequence.head.value
        level.offset_first_ball()
        self.assertEqual(ball.position, level.sequence.head.value.position)


if __name__ == '__main__':
    unittest.main()

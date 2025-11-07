from pygui.core.types import Point, Rect, Size


def test_point():
    p1 = Point(10, 20)
    p2 = Point(5, 10)

    assert p1.x == 10
    assert p1.y == 20

    p3 = p1 + p2
    assert p3.x == 15
    assert p3.y == 30

    p4 = p1 - p2
    assert p4.x == 5
    assert p4.y == 10


def test_rect():
    rect = Rect(10, 20, 100, 50)

    assert rect.x == 10
    assert rect.y == 20
    assert rect.width == 100
    assert rect.height == 50

    assert rect.left == 10
    assert rect.top == 20
    assert rect.right == 110
    assert rect.bottom == 70

    center = rect.center
    assert center.x == 60
    assert center.y == 45

    assert rect.contains(Point(50, 40))
    assert not rect.contains(Point(200, 200))


def test_size():
    size = Size(800, 600)
    assert size.width == 800
    assert size.height == 600

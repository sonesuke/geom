
from geom import *

def test_find_crossing_point_of_circle_and_arc():
    res = find_crossing_point_of_circle_and_arc(
            (10, 0), # center
            10,     # radius
            ["ARC", (0, 0), 10, (0, 360)]
            )
    assert round(res[0], 1) == 60.0
    assert round(res[1], 1) == 300.0


def test_generate_trajectory_arc():
    res = generate_trajectory_arc(
            ["ARC", (0, 0), 10, (0, 360)],
            (10, 0),
            1
            )
    print res
    assert True


def test_find_crossing_point_of_circle_and_line():
    res = find_crossing_point_of_circle_and_line(
            (0, 0), #center
            10,
            ["LINE", [(0, 0), (20, 0)]]
            )
    print res
    assert round(res[0][0], 1) == 10
    assert round(res[0][1], 1) == 0


def test_generate_trajectory_line():
    res = generate_trajectory_line(
            ["LINE", [(0, 0), (20, 0)]],
            (0, 0),
            1
            )
    print res
    assert True


def test_generate_trajectories():
    trajectories = [
            ["LINE", [(0, 0), (10, 0)]],
            ["ARC", (0, 0), 10, (0, 90)],
            ]
    res = generate_trajectories(
            trajectories,
            (0, 0),
            1
            )
    print res
    assert True


def test_offset_line():
    res = offset_line(
            ["LINE", [(0, 0), (10, 0)]],
            10
            )
    print res
    assert True


def test_offset_arc():
    res = offset_arc(
            ["ARC", (0, 0), 10, (0, 90)],
            10
            )
    print res
    assert True


def test_offset_trajectories():
    trajectories = [
            ["LINE", [(0, 0), (10, 0)]],
            ["ARC", (0, 0), 10, (0, 90)],
            ]
    res = offset_trajectories(
            trajectories,
            10
            )
    print res
    assert False

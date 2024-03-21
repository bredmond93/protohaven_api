"""Test behavior of linear solver for class scheduling"""
import datetime

from protohaven_api.class_automation.solver import Class, Instructor, solve


def d(i):
    """Returns a date based on an integer, for testing"""
    return datetime.datetime.now() + datetime.timedelta(days=i)


def test_solve():
    """Run an example set of classes and instructors through the solver"""
    long_ago = d(-1000)
    classes = [
        Class(*v)
        for v in [
            (1, "Embroidery", 1, 3, "textiles", long_ago, 0.7),
            (2, "Sewing Basics", 2, 3, "textiles", long_ago, 0.6),
            (3, "Basic Woodshop", 2, 3, "wood", long_ago, 0.5),
            (4, "Millwork", 1, 3, "wood", long_ago, 0.7),
            (5, "Basic Metals", 2, 3, "metal", long_ago, 0.8),
            (6, "Metal Workshop", 1, 3, "metal", long_ago, 0.4),
        ]
    ]

    people = [
        Instructor(*v)
        for v in [
            ("A", [1, 2], 6, [d(i) for i in [1, 7, 14, 21, 29]]),
            (
                "B",
                [3, 1, 4],
                4,
                [d(i) for i in [1, 4, 5, 8, 11, 14, 22, 25, 29]],
            ),
            ("C", [5, 6, 1], 2, [d(i) for i in [5, 7, 2, 1]]),
            ("D", [4, 2], 1, [d(i) for i in range(30)]),
        ]
    ]

    area_occupancy = {}

    solve(classes, people, area_occupancy)
    # (schedule, load, score) = solve(classes, people)

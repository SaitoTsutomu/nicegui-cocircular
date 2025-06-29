# flake8: noqa: S101
"""feature.pyのテスト"""

from fractions import Fraction

import pytest

from nicegui_cocircular import (
    CircularFeature,
    LineFeature,
    Point,
    get_circular_feature,
    get_line_feature,
)


@pytest.mark.parametrize(
    ("p0", "p1", "expected"),
    [
        ((0, 0), (1, 0), LineFeature(0, 1, 0)),  # y = 0
        ((0, 0), (0, 1), LineFeature(1, 0, 0)),  # x = 0
        ((0, 0), (1, 1), LineFeature(1, -1, 0)),  # x - y = 0
        ((1, 2), (3, 4), LineFeature(1, -1, 1)),  # x - y + 1 = 0
        ((0, 0), (2, 2), LineFeature(1, -1, 0)),  # gcd
        ((1, 1), (0, 0), LineFeature(1, -1, 0)),  # sign
    ],
)
def test_get_line_feature(p0: Point, p1: Point, expected: LineFeature) -> None:
    """get_line_featureのテスト"""
    assert get_line_feature(p0, p1) == expected


@pytest.mark.parametrize(
    ("p0", "p1", "p2", "expected"),
    [
        (
            (0, 0),
            (2, 0),
            (0, 2),
            CircularFeature(Fraction(1), Fraction(1), Fraction(2)),
        ),
        (
            (0, 0),
            (1, 1),
            (2, 0),
            CircularFeature(Fraction(1), Fraction(0), Fraction(1)),
        ),
    ],
)
def test_get_circular_feature(p0: Point, p1: Point, p2: Point, expected: CircularFeature) -> None:
    """get_circular_featureのテスト"""
    assert get_circular_feature(p0, p1, p2) == expected

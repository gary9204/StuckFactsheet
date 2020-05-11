"""
TODO
"""
import collections as COL
import enum

Placement = COL.namedtuple('Placement', ['anchor', 'place'])


class Places(enum.Enum):
    AFTER = enum.auto()
    BEFORE = enum.auto()
    CHILD = enum.auto()

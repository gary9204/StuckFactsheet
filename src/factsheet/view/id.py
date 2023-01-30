"""
Defines enumeration corresponding to identity fields: Name, Summary, and
Title.
"""
import enum


class FieldsId(enum.Flag):
    """Identifies search fields for :class:`.IdCore`.

    A search may combine fields using logical operators.

    .. data:: NAME

       Denotes name field.

    .. data:: TITLE

       Denotes title field.

    .. data:: SUMMARY

       Denotes summary field.

    .. data:: VOID

       Denotes no field.
    """
    VOID = 0
    NAME = enum.auto()
    SUMMARY = enum.auto()
    TITLE = enum.auto()

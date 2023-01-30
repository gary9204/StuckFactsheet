"""
Definition of types for storing Factsheet features.

A type for persistent storage of a feature should not depend on user
interface toolkit.  This module defines storage types that are toolkit-
independent.  Each storage type is defined with a Python type or type
alias rather that types from a toolkit type.

.. data:: StorePyMarkup

    User interface toolkit-independent type for storing markup text.
"""

StorePyMarkup = str

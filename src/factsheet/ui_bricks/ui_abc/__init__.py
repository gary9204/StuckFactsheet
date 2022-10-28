"""
Abstract interface for user interface toolkit features Factsheet uses.

Package :mod:`~.factsheet.ui_bricks` describes how Factsheet uses the
`abstract factory pattern`_ for features of a user interface toolkit.
This package defines the abstract interface for the pattern.

.. _`abstract factory pattern`:
    https://en.wikipedia.org/wiki/Abstract_factory_pattern

Module :mod:`.brick_abc` defines abstract component classes for toolkit
features that Factsheet used.  The component classes include model
facades for features along with corresponding control classes.

Module :mod:`.new_brick_abc` defines the abstract factory class for the
pattern.  Each additional module in the package defines an abstract
component factory class corresponding to a feature of a user interface
toolkit.
"""

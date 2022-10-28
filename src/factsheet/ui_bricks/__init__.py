"""
Classes, interfaces, and types to isolate user interface toolkit.

The Factsheet model uses features of a user interface toolkit.  Doing so
both reduces development effort and increases reliability.  However, the
choice of user interface toolkit may change over time (for example, GTK
3 to GTK 4) or between environments (for example, Linux to Windows).

This package implements the `abstract factory pattern`_ for toolkit
features. Package :mod:`~.factsheet.ui_bricks.ui_abc` provides an
abstract interface for user interface toolkit features that Factsheet
uses.

.. _`abstract factory pattern`:
    https://en.wikipedia.org/wiki/Abstract_factory_pattern

Package :mod:`~.factsheet.ui_bricks.ui_gtk3` implements the abstract
factory interface for GTK 3 toolkit.

Module :mod:`~.factsheet.ui_bricks.ui_factory` constructs a factory
object to produce components encapsulating toolkit features.  These
components include model facades for toolkit features along with
corresponding control objects and view facades.


.. admonition:: Maintain

    The `abstract factory pattern`_ pattern facilitates selecting from
    available factory implementations for user interface toolkits.
    Currently, module :mod:`~.factsheet.ui_bricks.ui_factory`
    instantiates a factory for GTK 3.  If future packages implement
    factories for other user interface toolkits, modify
    :mod:`~.factsheet.ui_bricks.ui_factory` to select the factory
    appropriate to the environment.

.. admonition:: Maintain

    The idea is to use simple components to build complex ones (a la
    Lego\ :sup:`TM` bricks).  Each abstract facade class represents a simple
    model or view component.  Each concrete subclass implements the
    facade based either on a component from the user interface toolkit
    or a Python object.  Implementation of the facades will differ for
    each toolkit.  However, the abstract facade classes and abstract
    factory classes accommodate switching toolkits transparently.
"""

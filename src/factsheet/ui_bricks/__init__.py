"""
Classes, interfaces, and types to isolate user interface toolkit.

The Factsheet model uses features of the user interface toolkit.  Doing
so both reduces development effort and increases reliability.  However,
the choice of user interface may change over time (for example, GTK 3 to
GTK 4) or between environments (for example, Linux to Windows).

This package provides an abstract interface for user interface toolkit
features that Factsheet uses.  The package implements the interface for
GTK 3.

Abstract factory classes facilitate selecting from available
implementations for user interface toolkits.

.. admonition:: Maintain

    The idea is to use simple components to build complex ones (a la
    Lego(TM) bricks).  Each abstract facade class represents a simple
    model or view component.  Each concrete subclass implements the
    facade based either on a component from the user interface toolkit
    or a Python object.  Implementation of the facades will differ for
    each toolkit.  However, the abstract facade classes and abstract
    factory classes accommodate switching toolkits transparently.
"""

"""
Classes, interfaces, and types to isolate user interface toolkit.

The Factsheet model uses features of the user interface toolkit.  Doing
so both reduces development effort and increases reliability.  However,
the choice of user interface may change over time (for example, GTK 3 to
GTK 4) or environment (for example, Linux to Windows).

This package provides an abstract interface for features that the
Factsheet model uses.  The package implements the interface for GTK 3.

Factory classes facilitate selecting from available implementations for
user interface toolkits.
"""

"""
Facade classes for GTK 3 user interface toolkit elements.

Each facade class specializes and simplifies the interface to a GTK 3
storage element or visual element.  The GTK 3 element may be a single
widget or a collection of related, interacting widgets.

.. admonition:: Maintain

    Element facade class methods isolate model and control classes from
    details of the GTK 3 toolkit.  At the same time, class properties
    provide view classes with direct access to GTK 3 widgets. A prefix
    of ``ui_`` identifies a method or property intended for use only
    with view classes.

.. admonition:: Plan

    The purpose of the element facade package is to facilitate support
    of user interface toolkits other than GTK 3.  In particular, the
    plan is for a future ``element_gtk4`` package as a drop-in
    alternative to support GTK 4.
"""

Conventions
===========


In general, Factsheet code follows `PEP 8 <PEP_8_>`_ style.

.. _PEP_8: https://www.python.org/dev/peps/pep-0008/


Names
-----

Names reflect usage with most important feature first. (A bit like nouns
and adjectives in Spanish.) ::

    outline_names = None    # An outline that contains names
    name_outline = 'Eric'   # Name of an outline

A prefix in a name identifies a column (C\_, c\_), index (I\_, i\_), 
(N\_, n\_) number, or function parameter (p\_). ::

    C_TITLE = 0     # Identifies title column
    i_topic_old = 2     # Index of old topic
    N_FACTS = 42    # Number of facts
    add(p_sheet)    # Sheet parameter of add function

A name of an Internal, helper method of a class begins with an
underscore. ::

    class Topic:

        def __init__(self):
            self._init_attributes()
            self._init_signals()
            ...

A model component class is named for its content.  Corresponding control
and view classes have the same name with a component prefix. ::

    class Sheet:    # Factsheet model
        ...
    class ControlSheet:    # Factsheet control
        ...
    class ViewSheet:    # Factsheet view
        ...

A view class name beginning with ``Display`` is for a static visual element.
``Editor`` identifies an editable visual element.  ``Chooser`` identifies a
visual element for selecting from a collection of options.  ``View``
identifies a compound or general visual element.


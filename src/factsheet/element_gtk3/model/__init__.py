"""
Facade classes for GTK 3 storage elements.

Each facade class specilizes a storage element for model classes to use.
See :mod:`.factsheet.element_gtk3`.

.. admonition:: Maintain

    GTK 3 implements a model-view design.  GTK 3 has well-developed
    mechanisms.  For example, GTK 3 implements signaling and data
    exchange between model and view classes.

    Element facade classes take advantage of GTK 3 mechanisms rather
    than duplicating them.  Storage elements in model facade classes
    interact with view elements in view facade classes using GTK 3
    mechanisms. However, each facade hides the elements and mechanisms
    from Factsheet model classes that use the facade.
"""

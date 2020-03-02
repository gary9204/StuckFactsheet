"""
Factsheet applicaton package.

:doc:`../guide/intro` describes the Factsheet application
:mod:`~factsheet.app`.  The description covers a factsheet document,
which is made up of facts grouped into topics.

Application Factsheet is based on a
`Model-View-Controller <Wikipedia_MVC_>`_ (MVC) design.  Package
`factsheet` partitions the source code into corresponding subpackages
:mod:`~factsheet.model`, :mod:`~factsheet.view`, and
:mod:`~factsheet.control`.  For each subpackage, there is a
corresponding unit test subpackage in the :mod:`factsheet_test` package.

The initial implementation of application Factsheet makes use ot the
`GTK widget toolkit <Wikipedia_GTK_>`_.  GTK also uses a MVC design.
In addition to the Factsheet view, the Factsheet model uses GTK
classes and mechanisms to avoid duplication.  However, Factsheet
encapsulates the GTK components used in the model.  Doing so isolates
model coupling with GTK.  Subpackage :mod:`~factsheet.abc_types`
specifies abstract classes and interfaces that the model uses.
Subpackage :mod:`~factsheet.adapt_gtk` defines implementations with GTK.

Subpackage :mod:`~factsheet.algebra` contains sample factsheet content.

.. data:: __version__

   Factsheet application version.

.. References

.. _Wikipedia_GTK:
   https://en.wikipedia.org/wiki/GTK

.. _Wikipedia_MVC:
   https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
"""

__version__ = '0.1.0'

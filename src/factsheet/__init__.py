"""
Package containing Factsheet applicaton code.

:doc:`../guide/intro` describes the Factsheet application
:mod:`app`.  The description covers a factsheet document,
which is made up of facts grouped into topics.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  Package `factsheet` partitions
the source code into corresponding subpackages :mod:`~factsheet.model`,
:mod:`~factsheet.view`, and :mod:`~factsheet.control` with supplemental
subpackages for content and supporting classes.  For each subpackage,
there is a corresponding unit test subpackage in the
:mod:`factsheet_test` package.

.. data:: __version__

   Factsheet application version.
"""

__version__ = '0.5.0'

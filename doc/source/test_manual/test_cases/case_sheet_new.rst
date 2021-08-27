Case Factsheet New
==================

**Purpose:** demonstrate Factsheet creation.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Click *Application* **new Factsheet icon** |document-new|
   (window title on left next to open buttons).

   a. *Expect:* Second window appears with name *Unnamed*.
   #. New window may cover first window.

#. **Step:** Edit factsheet name "Unnamed" to "Beta".

   a. *Expect:* "Beta" appears in field.
   #. *Expect:* No change in Alpha window name.

#. **Step:** Edit (|edit| icon on right) title in Beta window to
   "<i>Factsheet</i> Beta".

   a. *Expect:* Title changes to "\ *Factsheet* Beta" in Beta window.
   #. *Expect:* Title remains blank in Alpha window.

#. **Step:** Select *Factsheet* **menu** item **File ... > new** (|menu|
   icon on far right of *Factsheet* identity line).

   a. *Expect:* Third window appears with name *Unnamed*.
   #. New window may cover other windows.

#. **Step:** Edit factsheet name "Unnamed" to "Gamma".

   a. *Expect:* "Gamma" appears in field.
   #. *Expect:* No change in Alpha and Beta window names.

#. **Step:** In Alpha window, click window **close icon**
   |window-close| (window title far right).

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and Alpha window disappear.
   #. *Expect:* Beta and Gamma windows remain.

#. **Step:** In Gamma window, click window **close icon**
   |window-close|.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and Gamma window disappear.
   #. *Expect:* Beta windows remains.

#. **Step:** In window, click window **close icon** |window-close|.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button**

   a. *Expect:* Dialog and Beta window disappear.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


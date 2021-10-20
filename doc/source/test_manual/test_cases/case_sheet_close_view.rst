Case Factsheet Close Window
===========================

**Purpose:** demonstrate closing Factsheet windows with and without
changes to the factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps -- No Changes
-------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with same factsheet title as
      first window.
   #. New window may cover first window.

#. **Step:** In second window, select *Factsheet* **menu** |menu| item
   **Display ...  > Close window**.

   a. *Expect:* Second window disappears.
   #. *Expect:* First window is unchanged.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Window disappears and application closes.

Steps -- Unsaved Changes
------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in name field.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with factsheet name "Alpha".
   #. New window may cover first window.

#. **Step:** In second window, select *Factsheet* **menu** |menu| item
   **Display ...  > Close window**.

   a. *Expect:* Second window disappears.
   #. *Expect:* First window is unchanged.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).  

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears
   #. *Expect:* Window remains unchanged.

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ...  >
   Close window**.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* *Application* closes.

Steps -- Multiple Factsheet
---------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in name field.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window.** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with factsheet name "Alpha".
   #. *New window may cover first window.*
   #. Note position of *Alpha* windows.

#. **Step:** In second *Alpha* window, click *Factsheet* **new Factsheet
   icon** |document-new| (window title on left next to open buttons).

   a. *Expect:* Third window appears with factsheet name "Unnamed".
   #. *New window may cover Alpha windows.*

#. **Step:** In *Unnamed* window, select *Factsheet* **menu** |menu| item
   **Display ... > Open window.**

   a. *Expect:* Fourth window appears with factsheet name "Unnamed".
   #. *New window may cover Alpha windows.*
   #. Note positions of *Unnamed* windows.

#. **Step:** In first *Alpha* window, select *Factsheet* **menu** |menu|
   item **Display ... > Close window.**

   a. *Expect:* First *Alpha* window disappears.
   #. *Expect:* Second *Alpha* window remains.
   #. *Expect:* Both *Unnamed* windows remain.

#. **Step:** In second *Unnamed* window, select *Factsheet* **menu** |menu|
   item **Display ... > Close window.**

   a. *Expect:* Second *Unnamed* window disappears.
   #. *Expect:* First *Unnamed* window remains.
   #. *Expect:* *Alpha* window remains.

#. **Step:** In *Unnamed* window, click window **close icon**
   |window-close| (window title far right).

   a. *Expect:* *Unnamed* window disappears.
   #. *Expect:* *Alpha* window remains.

#. **Step:** In *Alpha* window, click window **close icon**
   |window-close|.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and *Alpha* window disappear.
   #. *Expect:* *Application* closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


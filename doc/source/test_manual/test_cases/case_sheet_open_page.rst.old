Case Factsheet Open Window
==========================

**Purpose:** demonstrate opening of Factsheet windows.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Type factsheet title "Alpha" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (right of *Factsheet* field).

   a. *Expect:* Second window appears with factsheet title ``Alpha``.
   #. New window may cover first window.

#. **Step:** Change title in second Alpha window to "Alpha Plus".

   a. *Expect:* Title changes to ``Alpha Plus`` in both windows.

#. **Step:** Click *Factsheet* **new Factsheet icon** (window title on
   left next to open buttons).

   a. *Expect:* Third window appears with blank factsheet title.
   #. New window may cover first or second window.

#. **Step:** Type *Factsheet* title "Beta" in third window.

   a. *Expect:* Title appears in third window.
   #. *Expect:* No change in either ``Alpha`` window.

#. **Step:** In ``Beta`` window, select *Factsheet* **menu** |menu|
   **Display ... > Open window**.

   a. *Expect:* Fourth window appears with factsheet title ``Beta``.
   #. New window may cover second sheet window.

#. **Step:** In second ``Beta`` window, change title to "Beta minus".

   a. *Expect:* Title changes in both ``Beta`` windows.
   #. *Expect:* Title is unchanged in both ``Alpha`` windows.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

Close each window as follows.

1. **Step:** In window, click window **close icon** |window-close|
   (window title far right).

   | Window closes or *Data Loss Warning* dialog appears.

#. **Step:** When dialog appears, click **Discard button**.

   | Dialog and window disappear.


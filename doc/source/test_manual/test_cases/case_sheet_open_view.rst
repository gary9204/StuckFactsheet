Case Factsheet Open Window
==========================

**Purpose:** demonstrate opening of windows for an existing Factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

Steps
-----
1. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with factsheet name "Alpha".
   #. New window may cover first window. Keep track of relative
      positions of windows.

#. **Step:** Edit (|edit| icon on right) title in second window to
   "<i>Factsheet</i> Alpha".

   a. *Expect:* Title changes to "\ *Factsheet* Alpha" in both windows.

#. **Step:** In second window, select *Factsheet* **menu** item
   **Display ... > Open window** (|menu| icon on identity line).

   a. *Expect:* Third window appears with factsheet name "Alpha" and
      factsheet title "\ *Factsheet* Alpha".
   #. New window may cover first or second window. Keep track of
      relative positions of windows.

#. **Step:** Click inside the *Factsheet Summary* frame away from the
   margins.

   a. *Expect:* A blinking text cursor (|) appears in the upper left
      corner of the frame.

#. **Step:** Edit the summary as follows: “Factsheet Alpha describes a
   Norwegian Blue parrot."

   a. *Expect:* The text appears as entered in all three windows.

#. **Step:** In second window, click window **close icon** |window-close|
   (window title far right).

   a. *Expect:* Second window closes.
   #. *Expect:* First and third windows are unchanged.

#. **Step:** In first window, add the following to the summary: “And
   it's a fine specimen too."

   a. *Expect:* The text appears as entered in first and third windows.

#. **Step:** In first window, click window **close icon**
   |window-close|.

   a. *Expect:* First window closes.
   #. *Expect:* Third windows is unchanged.

#. **Step:** In third window, click window **close icon**
   |window-close|.

   a. *Expect:* Third window closes.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

.. Note:: Update Teardown once close window is restored.

Close each window as follows.

1. **Step:** In window, click window **close icon** |window-close|
   (window title far right).

   | Window closes or *Data Loss Warning* dialog appears.

#. **Step:** When dialog appears, click **Discard button**.

   | Dialog and window disappear.


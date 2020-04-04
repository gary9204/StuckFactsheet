Case Factsheet Open Window
==========================

**Purpose:** demonstrate opening of Factsheet windows.

Setup
-----
None

Steps
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title in **Factsheet** field (e.g. First
   Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** Select Factsheet **menu > Display ... > Open window**
   (right of **Factsheet** field).

   a. *Expect:* Second window appears with same factsheet title as first
      window.  New window may cover first window.

#. **Step:** Change title in second window (e.g. Modified First
   Factsheet).

   a. *Expect:* Title changes in both windows.

#. **Step:** Click Factsheet **new Factsheet icon** (window title on
   left next to open buttons).

   a. *Expect:* Third window appears with blank factsheet title. New
      window may cover first or second window.

#. **Step:** Type factsheet title in third window (e.g. Second
   Factsheet).

   a. *Expect:* Title appears in new window.
   #. *Expect:* No change in first and second windows.

#. **Step:** In second sheet, select Factsheet **menu > Display ... >
   Open window**.

   a. *Expect:* Fourth window appears with same factsheet title as
      second sheet.  New window may cover second sheet window.

#. **Step:** Change title in new window (e.g. Modified Second
   Factsheet).

   a. *Expect:* Title changes in both second sheet windows.
   #. *Expect:* Title is unchanged in both first sheet windows.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

Close each window as follows.

1. **Step:** In window, click window **close icon** (window title far
   right).

   a. *Expect:* Window closes or Data Loss Warning dialog appears.

#. **Step:** When dialog appears, click **Discard button**

   a. *Expect:* Dialog and window disappear.


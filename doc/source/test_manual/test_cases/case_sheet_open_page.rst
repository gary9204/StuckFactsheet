Case Factsheet Open Window
==========================

**Purpose:** demonstrate opening of Factsheet windows.

Setup
-----
None

Steps
-----
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title in **Factsheet** field (e.g. First
      Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window**
      (right of **Factsheet** field).
   #. *Expect:* Second window appears with same factsheet title as first
      window.  New window may cover first window.

#. a. **Step:** Change title in second window (e.g. Modified First Sheet).
   #. *Expect:* Title changes in both windows.

#. a. **Step:** Click Factsheet **new Factsheet icon** (window title on
      left next to open buttons).
   #. *Expect:* Third window appears with blank factsheet title. New
      window may cover first or second window.

#. a. **Step:** Type factsheet title in third window (e.g. Second Sheet).
   #. *Expect:* Title appears in new window.  No change in first and
      second windows.

#. a. **Step:** In second sheet, select Factsheet **menu > Display ... >
      Open window**.
   #. *Expect:* Fourth window appears with same factsheet title as
      second sheet.  New window may cover second sheet window.

#. a. **Step:** Change title in new window (e.g. Modified Second Sheet).
   #. *Expect:* Title changes in both second sheet windows.  Title is
      unchanged in both first sheet windows.

Teardown
--------
Close each window as follows.

1. a. **Step:** In window, click window **close icon** (window title far
      right).
   #. *Expect:* Window closes or Data Loss Warning dialog appears.

#. a. **Step:** When dialog appears, click **Discard button**
   #. *Expect:* Dialog and window disappear.


Case Factsheet New
==================

**Purpose:** demonstrate Factsheet creation.

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

#. a. **Step:** Click Factsheet **new Factsheet icon** (window title on
      left next to open buttons).
   #. *Expect:* Second window appears with blank **Factsheet** field. New
      window may cover first window.

#. a. **Step:** Type title in **Factsheet** field of second window (e.g.
      Second Sheet).
   #. *Expect:* Title appears in new window.  No change in first
      window title.

#. a. **Step:** Select Factsheet **menu > File ... > New sheet.**
      (right of **Factsheet** field).
   #. *Expect:* Third window appears with blank **Factsheet** field.  New
      window may cover other windows.

#. a. **Step:** Type title in **Factsheet** field of third window (e.g.
      Third Sheet).
   #. *Expect:* Title appear in new window.  No change in first and
      second window titles.

#. a. **Step:** In first window, click window **close icon** (window
      title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and first window disappear. Second and third
      windows remain.

#. a. **Step:** In second window, click window **close icon**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button**
   #. *Expect:* Dialog and second window disappear. Third windows
      remains.

#. a. **Step:** In window, click window **close icon**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button**
   #. *Expect:* Dialog and window disappear. Application closes.

Teardown
--------
None


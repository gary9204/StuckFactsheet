Case Factsheet New
==================

**Purpose:** demonstrate Factsheet creation.

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

#. **Step:** Click Factsheet **new Factsheet icon** (window title on
   left next to open buttons).

   a. *Expect:* Second window appears with blank **Factsheet** field. New
      window may cover first window.

#. **Step:** Type title in **Factsheet** field of second window (e.g.
   Second Factsheet).

   a. *Expect:* Title appears in new window.
   #. *Expect:* No change in first window title.

#. **Step:** Select Factsheet **menu > File ... > New.**
   (right of **Factsheet** field).

   a. *Expect:* Third window appears with blank **Factsheet** field.  New
      window may cover other windows.

#. **Step:** Type title in **Factsheet** field of third window (e.g.
   Third Factsheet).

   a. *Expect:* Title appear in new window.
   #. *Expect:* No change in first and second window titles.

#. **Step:** In first window, click window **close icon** (window
   title far right).

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and first window disappear.
   #. *Expect:* Second and third windows remain.

#. **Step:** In second window, click window **close icon**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and second window disappear.
   #. *Expect:* Third windows remains.

#. **Step:** In window, click window **close icon**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button**

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


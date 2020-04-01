Case Factsheet Close Window
===========================

**Purpose:** demonstrate closing Factsheet windows with and without
changes to the factsheet.

Setup
-----
None

Steps -- No Changes
-------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window**
      (right of **Factsheet** field).
   #. *Expect:* Second window appears with same blank factsheet title as
      first window.  New window may cover first window.

#. a. **Step:** In second window, select Factsheet **menu > Display ...
      > Close window**.
   #. *Expect:* Second window disappears. First window is unchanged.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Window disappears and application closes.

Steps -- Unsaved Changes
------------------------
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

#. a. **Step:** In second window, select Factsheet **menu > Display ...
      > Close window**.
   #. *Expect:* Second window disappears. First window is unchanged.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears and window remains unchanged.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and window disappear. Application closes.

Steps -- Multiple Sheets
------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title in **Factsheet** field (e.g. First
      Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** Click Factsheet **new Factsheet icon** (window title on
      left next to open buttons).
   #. *Expect:* Second window appears with blank factsheet window.  New
      window may cover first window.

#. a. **Step:** In second window, type factsheet title in **Factsheet**
      field (e.g. Second Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** In second window, select Factsheet **menu > Display ...
      > Close window**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears and window remains unchanged.

#. a. **Step:** In second window, click window **close icon**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and second window disappear. First window remains
      unchanged.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button**
   #. *Expect:* Dialog and window disappear. Application closes

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


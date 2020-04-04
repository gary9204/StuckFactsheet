Case Factsheet Close Window
===========================

**Purpose:** demonstrate closing Factsheet windows with and without
changes to the factsheet.

Setup
-----
None

Steps -- No Changes
-------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > Display ... > Open window**
   (right of **Factsheet** field).

   a. *Expect:* Second window appears with same blank factsheet title as
      first window.  New window may cover first window.

#. **Step:** In second window, select Factsheet **menu > Display ...
   > Close window**.

   a. *Expect:* Second window disappears.
   #. *Expect:* First window is unchanged.

#. **Step:** Click window **close icon** (window title far right).

   a. *Expect:* Window disappears and application closes.

Steps -- Unsaved Changes
------------------------
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

#. **Step:** In second window, select Factsheet **menu > Display ...
   > Close window**.

   a. *Expect:* Second window disappears.
   #. *Expect:* First window is unchanged.

#. **Step:** Click window **close icon** (window title far right).

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears
   #. *Expect:* Window remains unchanged.

#. **Step:** Click window **close icon**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* Application closes.

Steps -- Multiple Factsheet
---------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title in **Factsheet** field (e.g. First
   Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** Click Factsheet **new Factsheet icon** (window title on
   left next to open buttons).

   a. *Expect:* Second window appears with blank factsheet window.  New
      window may cover first window.

#. **Step:** In second window, type factsheet title in **Factsheet**
   field (e.g. Second Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** In second window, select Factsheet **menu > Display ...
   > Close window**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Window remains unchanged.

#. **Step:** In second window, click window **close icon**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and second window disappear.
   #. *Expect:* First window remains unchanged.

#. **Step:** Click window **close icon**.

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


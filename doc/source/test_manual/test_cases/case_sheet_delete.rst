Case Factsheet Delete
=====================

**Purpose:** demonstrate Factsheet destruction.

Setup
-----
None

Steps -- Single Sheet and Single Window
---------------------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
      (right of **Factsheet** field).
   #. *Expect:* Window disappears. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title in **Factsheet** field (e.g. First
      Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears. Window remains.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and window disappear. Application closes.

Steps -- Single Sheet and Multiple Windows
------------------------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window.**
      (right of **Factsheet** field).
   #. *Expect:* Second window appears with blank Factsheet field. New
      window may cover first window.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
   #. *Expect:* Both windows disappear. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title in **Factsheet** field (e.g. First
      Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window.**
   #. *Expect:* Second window appears with same factsheet title as first
      window. New window may cover first window.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears. Both windows remain.

#. a. **Step:** Select Factsheet **menu > File ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and both windows disappear. Application closes.

Steps -- Multiple Sheets and Multiple Windows
---------------------------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window.**
      (right of **Factsheet** field).
   #. *Expect:* Second window appears with blank Factsheet field. New
      window may cover first window.

#. a. **Step:** Click Factsheet **new Factsheet icon** (window title on
      left next to open buttons).
   #. *Expect:* Third window appears with blank Factsheet field. New
      window may cover first window.

#. a. **Step:** In third window, select Factsheet **menu > Display ... >
      Open window.**
   #. *Expect:* Fourth window appears with blank Factsheet field. New
      window may cover first window.

#. a. **Step:** In first window, select Factsheet **menu > File ... >
      Close.**
   #. *Expect:* First and second windows disappear. Third and fourth
      windows remain.

#. a. **Step:** In (formerly) third window, select Factsheet **menu >
      File ... > Close.**
   #. *Expect:* Both remaining windows disappear. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title in **Factsheet** field (e.g. First
      Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window.**
   #. *Expect:* Second window appears with same factsheet title as first
      window. New window may cover first window.

#. a. **Step:** Select Factsheet **menu > File ... > New sheet.**
   #. *Expect:* Third window appears with blank Factsheet field. New
      window may cover other windows.

#. a. **Step:** In third window, type factsheet title in **Factsheet**
      field (e.g. Second Sheet).
   #. *Expect:* Title appears in field.

#. a. **Step:** In third window select Factsheet **menu > Display ... >
      Open window.**
   #. *Expect:* Fourth window appears with same factsheet title as
      third window. New window may cover other windows.

#. a. **Step:** In First Sheet window, select Factsheet **menu > File
      ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears. All windows remain.

#. a. **Step:** In First Sheet window, select Factsheet **menu > File
      ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and both First Sheet windows disappear. Both
      Second Sheet windows remain.

#. a. **Step:** In Second Sheet window, select Factsheet **menu > File
      ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button**.
   #. *Expect:* Dialog disappears. Both Second Sheet windows remain.

#. a. **Step:** In First Sheet window, select Factsheet **menu > File
      ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button**.
   #. *Expect:* Dialog and Second Sheet windows disappear. Application
      closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


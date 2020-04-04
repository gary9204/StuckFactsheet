Case Factsheet Delete
=====================

**Purpose:** demonstrate Factsheet destruction.

Setup
-----
None

Steps -- Single Sheet and Single Window
---------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > File ... > Close.**
   (right of **Factsheet** field).

   a. *Expect:* Window disappears.
   #. *Application closes.*

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title in **Factsheet** field (e.g. First
   Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** Select Factsheet **menu > File ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Window remains.

#. **Step:** Select Factsheet **menu > File ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and window disappear. Application closes.

Steps -- Single Sheet and Multiple Windows
------------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > Display ... > Open window.**
   (right of **Factsheet** field).

   a. *Expect:* Second window appears with blank Factsheet field.
   
      *New window may cover first window.*

#. **Step:** Select Factsheet **menu > File ... > Close.**

   a. *Expect:* Both windows disappear. Application closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title in **Factsheet** field (e.g. First
   Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** Select Factsheet **menu > Display ... > Open window.**

   a. *Expect:* Second window appears with same factsheet title as first
      window.
      
      *New window may cover first window.*

#. **Step:** Select Factsheet **menu > File ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Both windows remain.

#. **Step:** Select Factsheet **menu > File ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and both windows disappear.
   #. *Expect:* Application closes.

Steps -- Multiple Sheets and Multiple Windows
---------------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > Display ... > Open window.**
   (right of **Factsheet** field).

   a. *Expect:* Second window appears with blank Factsheet field.
      
      *New window may cover first window.*

#. **Step:** Click Factsheet **new Factsheet icon** (window title on
   left next to open buttons).

   a. *Expect:* Third window appears with blank Factsheet field.
   
      *New window may cover first window.*

#. **Step:** In third window, select Factsheet **menu > Display ... >
   Open window.**

   a. *Expect:* Fourth window appears with blank Factsheet field.
  
      *New window may cover first window.*

#. **Step:** In first window, select Factsheet **menu > File ... >
   Close.**

   a. *Expect:* First and second windows disappear.
   #. *Expect:* Third and fourth windows remain.

#. **Step:** In (formerly) third window, select Factsheet **menu >
   File ... > Close.**

   a. *Expect:* Both remaining windows disappear.
   #. *Expect:* Application closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title in **Factsheet** field (e.g. First
   Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** Select Factsheet **menu > Display ... > Open window.**

   a. *Expect:* Second window appears with same factsheet title as first
      window.
      
      *New window may cover first window.*

#. **Step:** Select Factsheet **menu > File ... > New sheet.**

   a. *Expect:* Third window appears with blank Factsheet field.
   
      *New window may cover other windows.*

#. **Step:** In third window, type factsheet title in **Factsheet**
   field (e.g. Second Factsheet).

   a. *Expect:* Title appears in field.

#. **Step:** In third window select Factsheet **menu > Display ... >
   Open window.**

   a. *Expect:* Fourth window appears with same factsheet title as
      third window.
     
      *New window may cover other windows.*

#. **Step:** In First Factsheet window, select Factsheet **menu > File
   ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:*  All windows remain.

#. **Step:** In First Factsheet window, select Factsheet **menu > File
   ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and both First Factsheet windows disappear.
   #. *Expect:* Both Second Factsheet windows remain.

#. **Step:** In Second Factsheet window, select Factsheet **menu > File
   ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* Both Second Factsheet windows remain.

#. **Step:** In First Factsheet window, select Factsheet **menu > File
   ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and Second Factsheet windows disappear.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


Case Factsheet Delete
=====================

**Purpose:** demonstrate closing Factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps -- Single Sheet and Single Window
---------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **File ... > Close.**
   (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Window disappears.
   #. *Application closes.*

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... >
   Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Window remains.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... >
   Close.** 
   
   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* *Application* closes.

Steps -- Single Sheet and Multiple Windows
------------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window.** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with factsheet name "Unnamed".
   #. *New window may cover first window.*

#. **Step:** In second window, select *Factsheet* **menu** |menu| item
   **File ... > Close.**

   a. *Expect:* Both windows disappear.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ... >
   Open window.**

   a. *Expect:* Second window appears with factsheet name "Alpha".
   #. *New window may cover first window.*

#. **Step:** In second *Alpha* window, select *Factsheet* **menu**
   |menu| item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Both windows remain.

#. **Step:** In first *Alpha* window, select *Factsheet* **menu** |menu|
   item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and both windows disappear.
   #. *Expect:* *Application* closes.

Steps -- Multiple Sheets and Multiple Windows
---------------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window.** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Second window appears with factsheet name "Unnamed".
   #. *New window may cover first window.*
   #. Note position of first and second windows.

#. **Step:** In second window, click *Factsheet* **new Factsheet icon**
   |document-new| (window title on left next to open buttons).

   a. *Expect:* Third window appears with factsheet name "Unnamed".
   #. *New window may cover first window.*

#. **Step:** In third window, select *Factsheet* **menu** |menu| item
   **Display ... > Open window.**

   a. *Expect:* Fourth window appears with factsheet name "Unnamed".
   #. *New window may cover first window.*
   #. Note positions of third and fourth windows.

#. **Step:** In first window, select *Factsheet* **menu** |menu| item
   **File ... > Close.**

   a. *Expect:* First and second windows disappear.
   #. *Expect:* Third and fourth windows remain.

#. **Step:** In (formerly) third window, select *Factsheet* **menu**
   |menu| item **File ... > Close.**

   a. *Expect:* Both remaining windows disappear.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ... >
   Open window.**

   a. *Expect:* Second window appears with factsheet name "Alpha"
   #. *New window may cover first window.*

#. **Step:** In second *Alpha* window, select *Factsheet* **menu**
   |menu| item **File ... > New**.

   a. *Expect:* Third window appears with factsheet name "Unnamed".
   #. *New window may cover first window.*

#. **Step:** In third window, edit |edit| factsheet name "Unnamed" to
   "Beta".

   a. *Expect:* "Beta" appears in field.

#. **Step:** In *Beta* window, select *Factsheet* **menu** |menu| item
   **Display ... > Open window.**

   a. *Expect:* Fourth window appears with factsheet name "Beta".
   #. *New window may cover first window.*

#. **Step:** In first *Alpha* window, select *Factsheet* **menu** |menu|
   item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:*  All windows remain.

#. **Step:** In first *Alpha* window, select *Factsheet* **menu** |menu|
   item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and both *Alpha* windows disappear.
   #. *Expect:* Both *Beta* windows remain.

#. **Step:** In second *Beta* window, select *Factsheet* **menu**
   |menu| item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* Both *Beta* windows remain.

#. **Step:** In second *Beta* window, select *Factsheet* **menu** |menu|
   item **File ... > Close.**

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and both *Beta* windows disappear.
   #. *Expect:* *Application* closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


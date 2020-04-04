Case Factsheet Save and Open
============================

**Purpose:** demonstrate Factsheet save to file and open from file.

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).

#. In the test data directory create a file ``test.txt`` containing a
   short text string (e.g., "The Spanish Inquisition."

#. In the test data directory create a file ``invalid.fsg`` containing a
   short test string (e.g., "No one expects the Spanish Inquisition."

Steps -- Save and Open
----------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title "sample" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "sample.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click Save button (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File ``sample.fsg`` appears with current timestamp. *Take
      note of file time and size.*

#. **Step:** Click window **close icon** (window title far right).

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Click Factsheet **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``sample.fsg`` and click **Open button** (dialog
   title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "sample" in **Factsheet**
      field. New window may cover first window.

#. **Step:** Edit factsheet title to "Sample Factsheet" in
   **Factsheet** field.

   a. *Expect:* Updated title appears in field.

#. **Step:** Select Factsheet **menu > File ... > Save**.
   (right of **Factsheet** field).

   a. *Expect:* Menu disappears.

#. **Step:** List test data directory contents.

   a. *Expect:* File ``sample.fsg`` appears with updated timestamp.

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > File ... > Open ...**.

   a. *Expect:* Open dialog appears.
   #. *Expect:* File **filter button** in lower right corner is labeled
      "Factsheet".

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Click **filter button**.

   a. *Expect:* List of file filters pops up: "Factsheet" and "Any".

#. **Step:** Click "Any" filter.

   a. *Expect:* Pop up collapses to "Any" on **filter button**.
   #. *Expect:* File list includes ``test.txt``.

#. **Step:** Click **filter button**.

   a. *Expect:* List of file filters pops up: "Factsheet" and "Any".

#. **Step:** Click "Factsheet" filter.

   a. *Expect:* Pop up collapses to "Factsheet" on **filter button**.
   #. *Expect:* File list only includes files with ``fsg`` extension.

#. **Step:** Select ``sample.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Sample Factsheet" in
      **Factsheet** field. New window may cover first window.

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

Steps -- Duplicate Open
-----------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title "Sample 1" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "sample 1.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** Edit factsheet title to "Sample 2" in **Factsheet** field.

   a. *Expect:* Title changes in field.

#. **Step:** Click Factsheet **Save as button** (window title on right
   near Save button).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "sample 1.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "sample 2.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button**.

   a. *Expect:* Dialog disappears.

#. **Step:** Click Factsheet **Open button** (window title on far
   left).
   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``sample 1.fsg`` and click **Open button**
   (dialog title on right).

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Sample 1" in **Factsheet**
      field. New window may cover first window.

#. **Step:** Select Factsheet **menu > Display ... > Open window**
   (right of **Factsheet** field).

   a. *Expect:* New window appears with factsheet title "Sample 1".
      New window may cover existing windows.

#. **Step:** Position windows so that "Sample 2" window covers parts
   of both "Sample 1" windows.

   a. *Expect:* "Sample 2" window is on top.

#. **Step:** Click Factsheet **Open button**.

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``sample 1.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Both Sample 1 windows cover parts of Sample 2 window.
   #. *Expect:* No new windows appear.

#. **Step:** Click Sample 1 window **close icon** (window title far
   right).

   a. *Expect:* Sample 1 window disappears.

#. **Step:** Click Sample 1 window **close icon**.

   a. *Expect:* Remaining Sample 1 window disappears.

#. **Step:** Click Sample 2 window **close icon**.

   a. *Expect:* Sample 2 indow disappears.
   #. *Expect:* Application closes.

Steps -- Data Loss and Overwrite Warnings
-----------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Type factsheet title "Guards" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit **Name** file to "guards.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click Save button (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File guards.sfg appears with current timestamp.

#. **Step:** Edit factsheet title to "Factsheet Safeguards" in
   **Factsheet** field.

   a. *Expect:* Updated title appears in field.

#. **Step:** Click window **close icon** (window title far right).

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button**

   a. *Expect:* Dialog disappears.

#. **Step:** In the test data directory create a file ``target.fsg``
   containing a short test string (e.g., "And now the Comfy chair!"

   a. *Expect:* Test data directory contains file ``target.fsg``.

#. **Step:** Click window **save as icon** (window title to right of
   **Save button**).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "guards.fsg".

#. **Step:** Select ``target.fsg`` and click **Save button** (dialog
   title on right)

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Cancel button**.

   a. *Expect:* Warning dialog disappears. Save dialog remains visible.

#. **Step:** List contents of ``target.fsg``

   a. *Expect:* Contents unchanged.

#. **Step:** Select ``target.fsg`` and click **Save button**.

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Replace button**.

   a. *Expect:* Warning dialog and Save dialog disappear.

#. **Step:** From console, open file ``target.fsg`` in hex editor
   (e.g. ``ghex``).

   a. *Expect:* File contains binary Pickle data.

#. **Step:** From console, display contents with ``python3 -m
   pickletools target.fsg``.

   a. *Expect:* Output includes Factsheet class names.
   #. *Expect:* Output includes Factsheet name and title text.

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

#. **Step:** Delete file ``target.fsg``.

   a. *Expect:* Test data directory does not contain the file.

Steps -- File Contents not Factsheet
------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Select Factsheet **menu > File ... > Open ...**.

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``invalid.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears. Second window appears. New
      window may cover first window.
   #. *Expect:* Window title is "OPEN ERROR".
   #. *Expect:* **Factsheet** field contains error message
      "Error opening file '/test/data/directory/invalid.fsg'".
   #. *Expect:* *Factsheet Summary* pane contains traceback data.

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

Teardown
--------
1. Delete test data directory along with its contents.
#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


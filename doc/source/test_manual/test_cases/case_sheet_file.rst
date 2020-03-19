Case Factsheet File
====================

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
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title "Sample" in **Factsheet** field.
   #. *Expect:* Title appears in field.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "Untitled.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "Sample.fsg"
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click Save button (dialog title on right).
   #. *Expect:* Dialog disappears.

#. a. **Step:** List test data directory contents (in shell or file
      browser).
   #. *Expect:* File ``Sample.fsg`` appears with current timestamp. Take
      note of file time and size.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Window disappears. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Click Factsheet **Open button** (window title on far
      left).
   #. *Expect:* Open dialog appears.

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Select ``Sample.fsg`` and click Open button (dialog title
      on right)
   #. *Expect:* Open dialog disappears. Second window appears with
      "Sample" in **Factsheet** field. New window may cover first window.

#. a. **Step:** Edit factsheet title to "Sample Factsheet" in
      **Factsheet** field.
   #. *Expect:* Updated title appears in field.

#. a. **Step:** Select Factsheet **menu > File ... > Save**.
      (right of **Factsheet** field).
   #. *Expect:* Menu disappears.

#. a. **Step:** List test data directory contents.
   #. *Expect:* File ``Sample.fsg`` appears with updated timestamp.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Window disappears.

#. a. **Step:** In original window, click window **close icon**.
   #. *Expect:* Window disappears. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > File ... > Open ...**.
   #. *Expect:* Open dialog appears. File **filter button** in lower
      right corner is labeled "Factsheet".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Click **filter button**.
   #. *Expect:* List of file filters pops up: "Factsheet" and "Any".

#. a. **Step:** Click "Any" filter.
   #. *Expect:* Pop up collapses to "Any" on **filter button**. File
      list includes ``test.txt``.

#. a. **Step:** Click **filter button**.
   #. *Expect:* List of file filters pops up: "Factsheet" and "Any".

#. a. **Step:** Click "Factsheet" filter.
   #. *Expect:* Pop up collapses to "Factsheet" on **filter button**. File
      list only includes files with ``fsg`` extension.

#. a. **Step:** Select ``Sample.fsg`` and click Open button.
   #. *Expect:* Open dialog disappears. Second window appears with
      "Sample Factsheet" in **Factsheet** field. New window may cover
      first window.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Window disappears.

#. a. **Step:** In original window, click window **close icon**.
   #. *Expect:* Window disappears. Application closes.

Steps -- Safety Checks
-----------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Type factsheet title "Guards" in **Factsheet** field.
   #. *Expect:* Title appears in field.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save dialog appears. Dialog Name field contains "Untitled.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit Name file to "Guard.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click Save button (dialog title on right).
   #. *Expect:* Dialog disappears.

#. a. **Step:** List test data directory contents (in shell or file
      browser).
   #. *Expect:* Guard.sfg appears with current timestamp.

#. a. **Step:** Edit factsheet title to "Factsheet Safeguards" in
      **Factsheet** field.
   #. *Expect:* Updated title appears in field.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button**
   #. *Expect:* Dialog disappears.

#. a. **Step:** In the test data directory create a file ``target.fsg``
      containing a short test string (e.g., "And now the Comfy chair!"
   #. *Expect:* Test data directory contains file ``target.fsg``.

#. a. **Step:** Click window **save as icon** (window title to right of
      **Save button**).
   #. *Expect:* Save dialog appears. Dialog Name field contains "Guard.fsg".

#. a. **Step:** Select ``target.fsg`` and click **Save button** (dialog
      title on right)
   #. *Expect:* Dialog appears warning file already exists.

#. a. **Step:** Click **Cancel button**.
   #. *Expect:* Warning dialog disappears. Save dialog remains visible.

#. a. **Step:** List contents of ``target.fsg``
   #. *Expect:* Contents unchanged.

#. a. **Step:** Select ``target.fsg`` and click **Save button**.
   #. *Expect:* Dialog appears warning file already exists.

#. a. **Step:** Click **Replace button**.
   #. *Expect:* Warning dialog and Save dialog disappear.

#. a. **Step:** Open file ``target.fsg`` in hex editor.
   #. *Expect:* File contains binary Pickle data.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Window disappears. Application closes.

#. a. **Step:** Delete file ``target.fsg``.
   #. *Expect:* Test data directory does not contain the file.

Steps -- File not Factsheet
---------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Select Factsheet **menu > File ... > Open ...**.
   #. *Expect:* Open dialog appears.

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Select ``invalid.fsg`` and click Open button.
   #. *Expect:* Open dialog disappears. Second window appears with
      error message "Error opening file
      '/test/data/directory/invalid.fsg'" in **Factsheet** field. New
      window may cover first window.

#. a. **Step:** Select ``target.fsg`` and click **Save button** (dialog
      title on right)
   #. *Expect:* Save dialog appears.

#. a. **Step:** Click **Cancel button**.
   #. *Expect:* Warning dialog disappears. Save dialog remains visible.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Window disappears.

#. a. **Step:** In original window, click window **close icon**.
   #. *Expect:* Window disappears. Application closes.

Teardown
--------
1. Delete test data directory along with its contents.


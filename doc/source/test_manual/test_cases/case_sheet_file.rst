Case Factsheet Save and Open
============================

**Purpose:** demonstrate Factsheet save to file and open from file.

.. include:: /icons/icons-include.txt

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).

#. In the test data directory create a file ``test.txt`` containing a
   short text string (e.g., "The Spanish Inquisition."

#. In the test data directory create a file ``Invalid.fsg`` containing a
   short test string (e.g., "No one expects the Spanish Inquisition."

Steps -- Save and Open
----------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Type title "Alpha" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "Alpha.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File ``Alpha.fsg`` appears with current timestamp.
   #. *Take note of file time and size.*

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Click *Factsheet* **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Alpha.fsg`` and click **Open button** (dialog
   title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Alpha" in *Factsheet*
      field.
   #. New window may cover first window.

#. **Step:** Edit factsheet title to "Alpha Plus" in
   **Factsheet** field.

   a. *Expect:* Updated title appears in field.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... >
   Save**.  (right of **Factsheet** field).

   a. *Expect:* Menu disappears.

#. **Step:** List test data directory contents.

   a. *Expect:* File ``Alpha.fsg`` appears with updated size and
      timestamp.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... > Open
   ...**.

   a. *Expect:* Open dialog appears.
   #. *Expect:* File **filter button** in lower right corner is labeled
      "Factsheet".

#. **Step:** In dialog, change to test data directory.

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

#. **Step:** Select ``Alpha.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Alpha Plus" in
      *Factsheet* field.
   #. New window may cover first window.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Steps -- Duplicate Open
-----------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Type factsheet title "Beta" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "Beta.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** Edit factsheet title to "Gamma" in **Factsheet** field.

   a. *Expect:* Title changes in field.

#. **Step:** Click *Factsheet* **Save as icon** |document-save-as|
   (window title on right near *Save button*).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "Beta.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "Gamma.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button**.

   a. *Expect:* Dialog disappears.

#. **Step:** Click *Factsheet* **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Beta.fsg`` and click **Open button**
   (dialog title on right).

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Beta" in *Factsheet*
      field.
   #. New window may cover first window.

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ... >
   Open window** (right of *Factsheet* field).

   a. *Expect:* New ``Beta`` window appears.
   #. New window may cover existing windows.

#. **Step:** Position windows so that ``Gamma`` window covers parts
   of both ``Beta`` windows.

   a. *Expect:* ``Gamma`` window obscures parts of ``Beta`` windows.

#. **Step:** Click *Factsheet* **Open button**.

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Beta.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Both ``Beta`` windows cover parts of ``Gamma`` window.
   #. *Expect:* No new windows appear.

#. **Step:** Click ``Beta`` window **close icon** |window-close| (window
   title far right).

   a. *Expect:* ``Beta`` window disappears.

#. **Step:** Click ``Beta`` window **close icon** |window-close|.

   a. *Expect:* Remaining ``Beta`` window disappears.

#. **Step:** Click ``Gamma`` window **close icon** |window-close|.

   a. *Expect:* ``Gamma`` indow disappears.
   #. *Expect:* *Application* closes.

Steps -- Data Loss and Overwrite Warnings
-----------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Type factsheet title "Guards" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit **Name** file to "Guards.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File guards.sfg appears with current timestamp.

#. **Step:** Edit factsheet title to "Safeguards" in **Factsheet**
   field.

   a. *Expect:* Updated title appears in field.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Cancel button**

   a. *Expect:* Dialog disappears.

#. **Step:** In the test data directory create a file ``Target.fsg``
   containing a short test string (e.g., "And now the Comfy chair!"

   a. *Expect:* Test data directory contains file ``Target.fsg``.

#. **Step:** Click window **Save as icon** |document-save-as| (window
   title to right of *Save button*).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "Guards.fsg".

#. **Step:** Select ``Target.fsg`` and click **Save button** (dialog
   title on right)

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Cancel button**.

   a. *Expect:* Warning dialog disappears. Save dialog remains visible.

#. **Step:** List contents of ``Target.fsg``

   a. *Expect:* Contents unchanged.

#. **Step:** Select ``Target.fsg`` and click **Save button**.

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Replace button**.

   a. *Expect:* Warning dialog and Save dialog disappear.

#. **Step:** From console, open file ``Target.fsg`` in hex editor
   (e.g. ``ghex``).

   a. *Expect:* File contains binary Pickle data.

#. **Step:** From console, display contents with ``python3 -m
   pickletools Target.fsg``.

   a. *Expect:* Output includes Factsheet class names.
   #. *Expect:* Output includes Factsheet name and title text.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Delete file ``Target.fsg``.

   a. *Expect:* Test data directory does not contain the file.

Steps -- File Contents not Factsheet
------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... > Open
   ...**.

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Invalid.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears. Second window appears.
   #. New window may cover first window.
   #. *Expect:* Window title is "OPEN ERROR".
   #. *Expect:* *Factsheet* field contains error message
      "Error opening file '/test/data/directory/Invalid.fsg'".
   #. *Expect:* *Factsheet Summary* pane contains traceback data.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Teardown
--------
1. Delete test data directory along with its contents.
#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


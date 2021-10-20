Case Factsheet Save and Open
============================

**Purpose:** demonstrate Factsheet save to file and open from file.

.. include:: /icons/icons-include.txt

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet_test``).

#. In the test data directory create a file ``test.txt`` containing a
   short text string (e.g., "The Spanish Inquisition."

Steps -- Save and Open
----------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Alpha".

   a. *Expect:* "Alpha" appears in field.

#. **Step:** Edit (|edit| icon on right) factsheet title to "First
   factsheet".

   a. *Expect:* "First factsheet" appears in field.

#. **Step:** Click inside the *Factsheet Summary* frame after existing
   text.

   a. *Expect:* A blinking text cursor (|) appears after existing text.

#. **Step:** Edit the summary to "This is the first factsheet."

   a. *Expect:* The text appears as entered.

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

   a. *Expect:* File ``Alpha.fsg`` appears with current time stamp.
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
   #. *Expect:* Second window appears with window title "Alpha".
   #. *Expect:* Name is "Alpha".
   #. *Expect:* Title is "First factsheet".
   #. *Expect:* Summary contains "This is the first factsheet."
   #. New window may cover first window.

#. **Step:** Edit *Alpha* factsheet name to "Alpha Plus".

   a. *Expect:* Updated title appears in field.

#. **Step:** Edit the summary to "This is the first factsheet with
   additions."

   a. *Expect:* The text appears as entered.

#. **Step:** Select *Factsheet* **menu** item **File ... > Save.**
   (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Menu disappears.

#. **Step:** List test data directory contents.

   a. *Expect:* File ``Alpha.fsg`` appears with updated size and
      time stamp.
   #. *Expect:* File ``Alpha.fsg~`` appears with size and time stamp of
      initial ``Alpha.fsg`` file.

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
   #. *Expect:* Second window appears with window title "Alpha Plus".
   #. *Expect:* Name is "Alpha Plus".
   #. *Expect:* Title is "First factsheet".
   #. *Expect:* Summary contains "This is the first factsheet with
      additions."
   #. New window may cover first window.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.

#. **Step:** In original window, click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Steps -- Save as
----------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "Beta".

   a. *Expect:* "Beta" appears in field.

#. **Step:** Edit (|edit| icon on right) factsheet title to "Second
   factsheet".

   a. *Expect:* "Second factsheet" appears in field.

#. **Step:** Click inside the *Factsheet Summary* frame after existing
   test.

   a. *Expect:* A blinking text cursor (|) appears after existing text.

#. **Step:** Edit the summary to "This is the second factsheet."

   a. *Expect:* The text appears as entered.

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

#. **Step:** List test data directory contents.

   a. *Expect:* Files ``Alpha.fsg`` and ``Beta.fsg`` appear is list.

#. **Step:** Edit *Beta* factsheet name to "Gamma".

   a. *Expect:* Updated name appears in field.
   #. *Expect:* Window title changes to "Gamma".

#. **Step:** Edit *Gamma* factsheet title to "Third factsheet".

   a. *Expect:* Updated title appears in field.

#. **Step:** Edit the summary to "This is the third factsheet.

   a. *Expect:* The text appears as entered.

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

#. **Step:** List test data directory contents.

   a. *Expect:* Files ``Alpha.fsg``, ``Beta.fsg``, and ``Gamma.fsg``
      appear is list.

#. **Step:** Select *Factsheet* **menu** item **File ... > Save as**.
   (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "Gamma.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "Delta.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button**.

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents.

   a. *Expect:* Files ``Alpha.fsg``, ``Beta.fsg``, ``Gamma.fsg``, and
      ``Delta.fsg`` appear is list.
   #. *Expect:* Files ``Gamma.fsg`` and ``Delta.fsg`` have the same
      size.

#. **Step:** in *Delta* window, click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Steps -- Duplicate Open
-----------------------
#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Click *Factsheet* **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Beta.fsg`` and click **Open button** (dialog
   title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with window title "Beta".
   #. *Expect:* Name is "Beta".
   #. *Expect:* Title is "Second factsheet".
   #. *Expect:* Summary contains "This is the second factsheet."
   #. New window may cover first window.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* New ``Beta`` window appears.
   #. New window may cover existing windows.

#. **Step:** Position windows so that ``Unamed`` window covers parts
   of both ``Beta`` windows.

   a. *Expect:* ``Unnamed`` window obscures parts of ``Beta`` windows.

#. **Step:** Click *Factsheet* **Open button**.

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``Beta.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Both ``Beta`` windows cover parts of ``Unnamed`` window.
   #. *Expect:* No new windows appear.

#. **Step:** In ``Beta`` window, select *Factsheet* **menu** item
   **File ... > Close.** (|menu| icon on far right of *Factsheet*
   identity line).

   a. *Expect:* Both ``Beta`` windows disappear.

#. **Step:** click ``Unnamed`` window **close icon** |window-close|.

   a. *Expect:* ``Unnamed`` window disappears.
   #. *Expect:* *application* closes.

Steps -- Data Loss and Overwrite Warnings
-----------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Edit (|edit| icon on left) factsheet name "Unnamed" to
   "<b>Guards</b>".

   a. *Expect:* "**Guards**" appears in field.
   #. *Expect:* "**Guards**" appears in window title.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** to "guards.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File ``guards.fsg`` appears with current time stamp.

#. **Step:** Edit (|edit| icon on right) factsheet title to "Guard
   factsheet".

   a. *Expect:* "Guard factsheet" appears in field.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* *Data Loss Warning* dialog appears.
   #. *Expect:* First warning line is: "Factsheet **Guards** contains
      unsaved changes. All unsaved changes will be discarded if you
      close."
   #. *Expect:* Second warning line is: "Cancel close, or continue to
      close and discard changes?"

#. **Step:** Click **Cancel button**

   a. *Expect:* Dialog disappears.

#. **Step:** In the test data directory create a file ``target.fsg``
   containing a short test string (e.g., "And now the comfy chair!"

   a. *Expect:* Test data directory contains file ``target.fsg``.

#. **Step:** Click window **Save as icon** |document-save-as| (window
   title to right of **Save button**).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog **Name** field contains "guards.fsg".

#. **Step:** Select ``target.fsg`` and click **Save button** (dialog
   title on right)

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Cancel button**.

   a. *Expect:* Warning dialog disappears.
   #. *Expect:* Save dialog remains visible.

#. **Step:** List contents of ``target.fsg``

   a. *Expect:* Contents unchanged.

#. **Step:** Select ``target.fsg`` and click **Save button**.

   a. *Expect:* Dialog appears warning file already exists.

#. **Step:** Click **Replace button**.

   a. *Expect:* Warning dialog and save dialog disappear.

#. **Step:** From console, open file ``target.fsg`` in hex editor
   (e.g. ``ghex``).

   a. *Expect:* File contains binary pickle data.
   #. Close hex editor after check.

#. **Step:** From console, display contents with ``python3 -m
   pickletools target.fsg``.

   a. *Expect:* Output includes factsheet class names.
   #. *Expect:* Output includes factsheet name and title text.
   #. Return to application after check.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Delete file ``target.fsg``.

   a. *Expect:* Test data directory does not contain the file.

Teardown
--------
1. Delete test data directory along with its contents.
#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


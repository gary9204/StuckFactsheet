Case Factsheet Titles
=====================

**Purpose:** confirm Factsheet window titles are correct and consistent.

.. include:: /icons/icons-include.txt

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).

Steps -- Window Title
---------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* Window title is "**Unnamed**".
   #. *Expect:* Window subtitle is "Unsaved (XXX-YYY)", where XXX
      is three hexadecimal digits identifying the factsheet and YYY is
      three hexadecimal digits identifying the window.

#. **Step:** Click *Factsheet* **open popup icon** |open-popup| (left of
   *Factsheet* field).

   a. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. **Step:** Type name "Arthur". Do not press Enter key.

   a. *Expect:* "Arthur" appears in Name field.
   #. *Expect:* Window title and subtitle do not change.

#. **Step:** Press Enter key.

   a. *Expect:* Edit Name popover disappears.
   #. *Expect:* Window title changes to "**Arthur**".
   #. *Expect:* Window subtitle does not change.

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ... >
   Show Name** (right of *Factsheet* field).

   a. *Expect:* Edit Name popover appears with "Arthur" in the edit
      field.

#. **Step:** Type name "Lancelot". Do not press Enter key.

   a. *Expect:* "Lancelot" appears in Name field.
   #. *Expect:* Window title and subtitle do not change.

#. **Step:** Click **Reset button** in Edit Name popover.

   a. *Expect:* Field changes back to "Arthur".
   #. *Expect:* Window title and subtitle do not change.

#. **Step:** Click window title outside of any control.

   a. *Expect:* Edit Name popover disappears.
   #. *Expect:* Window title and subtitle do not change.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* *Application* closes.

Steps -- Window Subtitle
------------------------
1. **Step** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* Window title is "**Unnamed**".
   #. *Expect:* Window subtitle is "Unsaved (UUU-VVV)", where UUU
      is three hexadecimal digits identifying the factsheet and VVV is
      three hexadecimal digits identifying the window.

      *Take note of UUU and VVV.*

#. **Step:** Type "Sample - Title Test" in *Factsheet* field.

   a. *Expect:* Text appears in field.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file Name field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file Name field to "TitleTest.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Subtitle changes to "TitleTest.fsg (UUU-VVV)".
   #. *Expect:* Facthseet identifier (UUU) and window identifier (VVV)
      are unchanged.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* Window title is "**Unnamed**".
   #. *Expect:* Window subtitle is "Unsaved (WWW-XXX)", where WWW
      is three hexadecimal digits identifying the factsheet and XXX is
      three hexadecimal digits identifying the window.

      *Take note of WWW and XXX.*

#. **Step:** Click *Factsheet* **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``TitleTest.fsg`` and click **Open button**
   (dialog title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Sample - Title Test" in
      *Factsheet* field.
   #. *Expect:*  Window subtitle is "TitleTest.fsg (YYY-ZZZ)".
   #. *Expect:*  *Factsheet* identifier (YYY) and window identifier
      (ZZZ)
      are distinct from those of the first window (WWW, XXX).

      *Take note of YYY and ZZZ.*

#. **Step:** Click *Factsheet* **Save as icon** |document-save-as|
   (window title to right of Save button).

   a. *Expect:* Save dialog appears.
   #. *Expect:*  Dialog file Name field contains "TitleTest.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file Name field to "TitleTestTwo.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* Subtitle changes to "TitleTestTwo.fsg (YYY-ZZZ)".
   #. *Expect:* *Factsheet* identifier (YYY) and window identifier (ZZZ)
      are unchanged.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* TitleTestTwo window disappears.

#. **Step:** Click first window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:*  *Application* closes.

Steps -- Multiple Windows and Sheets
------------------------------------
1. **Step** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:*  Window title is "**Unnamed**".
   #. *Expect:* Window subtitle is "Unsaved (UUU-VVV)", where UUU
      is three hexadecimal digits identifying the factsheet and VVV is
      three hexadecimal digits identifying the window.
   
      *Take note of UUU and VVV.*

#. **Step:** Select *Factsheet* **menu** |menu| item **Display ... >
   Open window** (right of *Factsheet* field).

   a. *Expect:* New window appears New window may cover existing windows.
   #. *Expect:* Window title is "**Unnamed**". 
   #. *Expect:* Window subtitle is "Unsaved (UUU-WWW).
   #. *Expect:* The factsheet identifier is the same as in the first
      window (UUU).
   #. *Expect:* The window identifiers are different (VVV and WWW).

      *Take note of WWW.*

#. **Step:** Click *Factsheet* **open popup icon** |open-popup| (left of
   *Factsheet* field).

   a. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. **Step:** Type name "Arthur". Do not press Enter key.

   a. *Expect:* Name appears in field.
   #. *Expect:* Window title and subtitle do not change in either
      window.

#. **Step:** Press Enter key.

   a. *Expect:* Edit Name popover disappears.
   #. *Expect:* Window title changes to "**Arthur**" in both windows.
   #. *Expect:* Window subtitles do not change.

#. **Step:** Click *Factsheet* **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file Name field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file Name field to "TitleTestMulti.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Subtitle changes to "TitleTestMulti.fsg (UUU-VVV)" in
      first window.
   #. *Expect:* Subtitle changes to "TitleTestMulti.fsg (UUU-WWW) in
      second window.

      *That is, facthseet identifier (UUU) and window identifiers (VVV
      and WWW) are unchanged.*

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... > New**.
   (right of *Factsheet* field).

   a. *Expect:* Third window appears. *New window may cover existing
      windows.*
   #. *Expect:* Window title is "**Unnamed**".
   #. *Expect:* Window subtitle is "Unsaved (XXX-YYY).
   #. *Expect:* The factsheet identifier (XXX) is distinct from the
      factsheet identifier in the *Arthur* windows (UUU).
   #. *Expect:* The window identifier (YYY) is different from the 
      *Arthur* windows identifiers (VVV and WWW).

      *Take note of XXX and YYY.*

#. **Step:** Click *Factsheet* **open popup icon** |open-popup|.

   a. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. **Step:** Type name "Lancelot". Do not press Enter key.

   a. *Expect:* "Lancelot" appears in Name field.
   #. *Expect:* Window title and subtitle do not change in either window.

#. **Step:** Press Enter key.

   a. *Expect:* Edit Name popover disappears.
   #. *Expect:* Window title changes to "**Lancelot**" in the third
      window.
   #. *Expect:* Window subtitle does not change.
   #. *Expect:* Window titles in the first two windows do not change.
   #. *Expect:* Window subtitles in the first two windows do not change.

#. **Step:** In the *Lancelot* window, click *Factsheet* **Save
   button**.

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file Name field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file Name field to "TitleTestMultiTwo.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The titles and subtitles in the *Arthur* windows are
      unchanged.
   #. *Expect:* In the *Lancelot* window, the title is unchanged.
   #. *Expect:* In the *Lancelot* window, the subtitle changes to
      "TitleTestMultiTwo.fsg (XXX-YYY)".

      *That is, in the Lancelot window the facthseet identifier (XXX)
      and window identifier (YYY) are unchanged.*

#. **Step:** In the *Lancelot* window, select *Factsheet* **menu >
   Display ... > Open window**.

   a. *Expect:* New window appears. *New window may cover existing
      windows.*
   #. *Expect:* New window title is "**Lancelot**".
   #. *Expect:* New window subtitle is "TitleTestMultiTwo.fsg (XXX-ZZZ).
   #. *Expect:* The factsheet identifier is the same as in the first
      *Lancelot* window (XXX).
   #. *Expect:* The window identifier is different from all other window
      identifiers (VVV, WWW, and YYY).

      *Take note of ZZZ.*

Teardown
--------
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* may appear for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

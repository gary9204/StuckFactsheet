Case Factsheet Titles
=====================

**Purpose:** confirm Factsheet window titles are correct and consistent.

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).

Steps -- Window Title
---------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. Window title is
      "**Unnamed**". Window subtitle is "Unsaved (XXX-YYY)", where XXX
      is three hexadecimal digits identifying the factsheet and YYY is
      three hexadecimal digits identifying the window.

#. a. **Step:** Click Factsheet **edit Name icon** (left of
      **Factsheet** field).
   #. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. #. **Step:** Type name "Arthur". Do not press Enter key.
   #. *Expect:* Name appears in field. Window title and subtitle do not
      change.

#. #. **Step:** Press Enter key.
   #. *Expect:* Edit Name popover disappears. Window title changes to
      "**Arthur**". Window subtitle does not change.

#. a. **Step:** Select Factsheet **menu > Display ... > Show Name**
      (right of **Factsheet** field).
   #. *Expect:* Edit Name popover appears with "Arthur" in the edit
      field.

#. #. **Step:** Type name "Lancelot". Do not press Enter key.
   #. *Expect:* Name appears in field. Window title and subtitle do not
      change.

#. #. **Step:** Click **Reset button** in Edit Name popover.
   #. *Expect:* Field changes back to "Arthur". Window title and
      subtitle do not change.

#. #. **Step:** Click window title outside of any control.
   #. *Expect:* Edit Name popover disappears. Window title and subtitle
      do not change.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and window disappear. Application closes.

Steps -- Window Subtitle
------------------------
1. a. **Step** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. Window title is
      "**Unnamed**". Window subtitle is "Unsaved (UUU-VVV)", where UUU
      is three hexadecimal digits identifying the factsheet and VVV is
      three hexadecimal digits identifying the window.

#. a. **Step:** Type factsheet title "Sample - Title Test" in
      **Factsheet** field.
   #. *Expect:* Title appears in field.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "factsheet.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "TitleTest.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click **Save button** (dialog title on right).
   #. *Expect:* Dialog disappears. Subtitle changes to "TitleTest.fsg
      (UUU-VVV)". Facthseet identifier (UUU) and window identifier (VVV)
      are unchanged.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Window disappears. Application closes.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. Window title is
      "**Unnamed**". Window subtitle is "Unsaved (WWW-XXX)", where WWW
      is three hexadecimal digits identifying the factsheet and XXX is
      three hexadecimal digits identifying the window.

#. a. **Step:** Click Factsheet **Open button** (window title on far
      left).
   #. *Expect:* Open dialog appears.

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Select ``TitleTest.fsg`` and click **Open button**
      (dialog title on right)
   #. *Expect:* Open dialog disappears. Second window appears with
      "Sample - Title Test" in **Factsheet** field. Window subtitle is
      "TitleTest.fsg (YYY-ZZZ)". Factsheet identifier (YYY) and window
      identifier (ZZZ) are distinct from those of the first window (WWW,
      XXX).

#. a. **Step:** Click Factsheet **Save as icon** (window title to right
      of Save button).
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "TitleTest.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "TitleTestTwo.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click **Save button**.
   #. *Expect:* Dialog disappears. Subtitle changes to "TitleTestTwo.fsg
      (YYY-ZZZ)". Factsheet identifier (YYY) and window identifier (ZZZ)
      are unchanged.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* TitleTestTwo window disappears.

#. a. **Step:** Click first window **close icon**.
   #. *Expect:* Window disappears. Application closes.

Steps -- Multiple Windows and Sheets
------------------------------------
1. a. **Step** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. Window title is
      "**Unnamed**". Window subtitle is "Unsaved (UUU-VVV)", where UUU
      is three hexadecimal digits identifying the factsheet and VVV is
      three hexadecimal digits identifying the window.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window**
      (right of **Factsheet** field).
   #. *Expect:* New window appears with window title "**Unnamed**".
      Window subtitle is "Unsaved (UUU-WWW). The factsheet identifier is
      the same as in the first window (UUU). The window identifiers are
      different (VVV and WWW).  New window may cover existing windows.

#. a. **Step:** Click Factsheet **edit Name icon** (left of
      **Factsheet** field).
   #. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. #. **Step:** Type name "Arthur". Do not press Enter key.
   #. *Expect:* Name appears in field. Window title and subtitle do not
      change in either window.

#. #. **Step:** Press Enter key.
   #. *Expect:* Edit Name popover disappears. Window title changes to
      "**Arthur**" in both windows. Window subtitles do not change.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "factsheet.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "MultiTest.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click **Save button** (dialog title on right).
   #. *Expect:* Dialog disappears. Subtitle changes to "MultiTest.fsg
      (UUU-VVV)" in first window and "MultiTest.fsg (UUU-WWW) in second.
      That is, facthseet identifier (UUU) and window identifiers (VVV
      and WWW) are unchanged.

#. a. **Step:** Select Factsheet **menu > File ... > New**.
      (right of **Factsheet** field).
   #. *Expect:* Third window appears with title "**Unnamed**".
      Window subtitle is "Unsaved (XXX-YYY). The factsheet identifier
      (XXX) is distinct from the factsheet identifier in the Arthur
      windows (UUU). The window identifier (YYY) is different from the 
      Arthur windows identifiers (VVV and WWW).  New window may cover
      existing windows.

#. a. **Step:** Click Factsheet **edit Name icon**.
   #. *Expect:* Edit Name popover appears with "Unnamed" in the edit
      field.

#. #. **Step:** Type name "Lancelot". Do not press Enter key.
   #. *Expect:* Name appears in field. Window title and subtitle do not
      change in either window.

#. #. **Step:** Press Enter key.
   #. *Expect:* Edit Name popover disappears. Window title changes to
      "**Lancelot**" in the third windows. Window titles in the first
      two windows do not change. Window subtitles do not change.

#. a. **Step:** In the Lancelot window, click Factsheet **Save button**.
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "factsheet.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "MultiTestTwo.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click **Save button**.
   #. *Expect:* Dialog disappears. The titles and subtitles in the
      Arthur windows are unchanged. In the Lancelot window, the title is
      unchanged and the subtitle changes to "MultiTestTwo.fsg
      (XXX-YYY)". That is, in the Lancelot window the facthseet
      identifier (XXX) and window identifier (YYY) are unchanged.

#. a. **Step:** In the Lancelot window, select Factsheet **menu >
      Display ... > Open window**.
   #. *Expect:* New window appears with window title "**Lancelot**".
      Window subtitle is "MultiTestTwo (XXX-ZZZ). The factsheet
      identifier is the same as in the first Lancelot window (XXX). The
      window identifier is different from all other window identifiers
      (VVV, WWW, and YYY).  New window may cover existing windows.

Teardown
--------
1. In each window, click **close icon**. Each window disappears. The
   application closes when the last window disappears.


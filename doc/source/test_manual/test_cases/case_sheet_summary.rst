Case Factsheet Summary
======================

**Purpose:** confirm Factsheet summary management is correct and
consistent.

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).

Steps -- Save and Load with Summary
-----------------------------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. *Factsheet
      Summary* pane is blank.

#. #. **Step:** Type summary "This sample factsheet includes a summary."
   #. *Expect:* Text appears in summary pane as typed.

#. a. **Step:** Select Factsheet **menu > Display ... > Summary**
      (right of **Factsheet** field).
   #. *Expect:* The *Factsheet Summary* pane disappears. The *Factsheet
      Topics* pane expands to replace it.  The popup menu remains
      visible. The check box to the left of **Summary** menu item is
      cleared. 

#. #. **Step:** Select **Summary** menu item
   #. *Expect:* The *Factsheet Summary* pane reappears. The pane
      contents are unchanged. The *Factsheet Topics* pane shrinks to
      accommodate it. The popup menu remains visible. The **Summary**
      check box is checked.

#. a. **Step:** Press Esc key.
   #. *Expect:* The popum menu disappears.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Cancel button** (dialog title far left).
   #. *Expect:* Dialog disappears. The window remains unchanged.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save dialog appears. Dialog file Name field contains
      "factsheet.fsg".

#. a. **Step:** Change to test data directory.
   #. *Expect:* Save dialog shows directory contents.

#. a. **Step:** Edit file Name field to "Summary Sample.fsg".
   #. *Expect:* Field contains new file name.

#. a. **Step:** Click **Save button** (dialog title on right).
   #. *Expect:* Dialog disappears. Subtitle changes to "Summary
      Sample.fsg (TTT-UUU)", where TTT identifies the factsheet and UUU
      identifies the window.

#. a. **Step:** Click window **close icon**.
   #. *Expect:* Window disappears. Application closes. There are no
      exceptions, GTK messages, or warning messages in the console.

#. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. *Factsheet
      Summary* pane is blank.

#. a. **Step:** Click Factsheet **Open button** (window title on far
      left).
   #. *Expect:* Open dialog appears.

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Select ``Summary Sample.fsg`` and click **Open button**
      (dialog title on right)
   #. *Expect:* Open dialog disappears. Second window appears with
      "This sample factsheet includes a summary." in *Factsheet Summary*
      pane. Window subtitle is "Summary Sample.fsg (VVV-WWW)".
      Factsheet identifier (VVV) and window identifier (WWW) are
      distinct from those of the first window.

Steps -- Edit and View Summary
------------------------------
1. a. **Step** Continue with **Summary Sample.fsg (VVV-WWW)** window.
   #. *Expect:* Summary Sample window contains "This sample factsheet
      includes a summary." in *Factsheet Summary* pane.

#. a. **Step:** Select and copy summary text. Paste into another
      application (e.g. Vim).
   #. *Expect:* Factsheet application highlights text when selected.
      Pasted text matches summary text.

#. #. **Step:** Add a long sentence to the summary.
   #. *Expect:* Summary text wraps when the sentence length exceeds the
      width of the window. Wrapping is at white space between words.

#. #. **Step:** Grab the lower right corner of the window and resize the
      window.
   #. *Expect:* Summary text wraps to fit the resized window.

#. #. **Step:** Copy "And now for something completely different!"
      including a new line and paste at the bottom of the summary.
   #. *Expect:* Copied text appears in summary and matches original.

#. #. **Step:** Repeat paste about 20 time at the bottom of the summary.
   #. *Expect:* Copied text appears in summary and matches original.
      Summary pane scrolls as needed to keep each paste visible.

#. #. **Step:** Move scroll slider to review summary content.
   #. *Expect:* Pane scrolls to cover all summary content.

#. #. **Step:** Lengthen window and move pane divider down to expose
      entire summary.
   #. *Expect:* Scrollbar disappears when entire summary is visible.

#. #. **Step:** Move pane divider up as far as possible.
   #. *Expect:* Pane divider stops with about three summary lines
      visible.

#. a. **Step:** Click Factsheet **Save button** (window title on right
      near center).
   #. *Expect:* Save button shows press-release color changes.

#. a. **Step:** Click Summary Sample window **close icon** (window title
      far right).
   #. *Expect:* Summary Sample window disappears.

#. a. **Step:** Click initial window **close icon**.
   #. *Expect:* Window disappears. Application closes. There are no
      exceptions, GTK messages, or warning messages in the console.

Steps -- Multiple Windows and Sheets
------------------------------------
1. a. **Step** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet. *Factsheet
      Summary* pane is blank.

#. a. **Step:** Click Factsheet **Open button** (window title on far
      left).
   #. *Expect:* Open dialog appears.

#. a. **Step:** Change to test data directory.
   #. *Expect:* Open dialog shows directory contents.

#. a. **Step:** Select ``Summary Sample.fsg`` and click **Open button**
      (dialog title on right)
   #. *Expect:* Open dialog disappears. Second window appears with
      "This sample factsheet includes a summary." along with added text
      in *Factsheet Summary* field. Window subtitle is "Summary
      Sample.fsg (XXX-YYY)".  Factsheet identifier (XXX) and window
      identifier (YYY) are distinct from those of the first window.

#. a. **Step:** Select Factsheet **menu > Display ... > Open window**
      (right of **Factsheet** field).
   #. *Expect:* New window appears with window subtitle "Summary
      Sample.fsgt (XXX-ZZZ)". The summary pane contents are the same.
      Wrapping and the visible portions of the windows may be different
      unless the windows have the same size and layout.

#. #. **Step:** Add "Our greatest weapon is fear and terror!" at the
      bottom of the second Summary Sample window.
   #. *Expect:* The same text appears in the first Summary Sample. In the
      initial window, *Factsheet Summary* pane remains blank.

#. #. **Step:** Select and delete the words "and terror" from the first
      Summary Sample window.
   #. *Expect:* The corresponding words are selected in the second
      Sample Summary window and then disappear.  In the initial window,
      the summary pane remains blank.

#. a. **Step:** In the first Summary Sample window, select Factsheet
      **menu > Display ... > Summary** (right of **Factsheet** field).
   #. *Expect:* In the first Summary Sample window, the *Factsheet
      Summary* pane disappears. The *Factsheet Topics* pane expands to
      replace it. There is no change in the second Summary Sample window
      or in the initial window.

#. #. **Step:** Select **Summary** menu item.
   #. *Expect:* The *Factsheet Summary* pane reappears in the first
      Summary Sample window. The pane contents are unchanged. The
      *Factsheet Topics* pane shrinks to accommodate it. Again, there is
      no change in the second Summary Sample window or in the initial
      window.

#. a. **Step:** Press Esc key.
   #. *Expect:* The popum menu disappears.

#. a. **Step:** In first Summary Sample window, select Factsheet **menu
      > File ... > Close.**
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Click **Discard button** (dialog title far right).
   #. *Expect:* Dialog and both Summary Sample windows disappear. The
      initial window remains.

#. a. **Step:** Click initial window **close icon**.
   #. *Expect:* Window disappears. Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


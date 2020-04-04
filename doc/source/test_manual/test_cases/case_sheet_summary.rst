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
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.
   #. *Expect:* *Factsheet Summary* pane is blank.

#. **Step:** Type summary "This sample factsheet includes a summary."

   a. *Expect:* Text appears in summary pane as typed.

#. **Step:** Select Factsheet **menu > Display ... > Summary**
   (right of **Factsheet** field).

   a. *Expect:* The *Factsheet Summary* pane disappears.
   #. *Expect:* The *Factsheet Topics* pane expands to replace it.
   #. *Expect:* The popup menu remains visible.
   #. *Expect:* The check box to the left of **Summary** menu item is cleared. 

#. **Step:** Select **Summary** menu item

   a. *Expect:* The *Factsheet Summary* pane reappears.
   #. *Expect:* The pane contents are unchanged.
   #. *Expect:* The *Factsheet Topics* pane shrinks to accommodate it.
   #. *Expect:* The popup menu remains visible.
   #. *Expect:* The **Summary** check box is checked.

#. **Step:** Press Esc key.

   a. *Expect:* The popum menu disappears.

#. **Step:** Click window **close icon** (window title far right).

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The window remains unchanged.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file Name field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file Name field to "summary sample.fsg".

   a. *Expect:* Field contains new file name.

#. **Step:** Click **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* Subtitle changes to "summary sample.fsg (TTT-UUU)",
      where TTT identifies the factsheet and UUU identifies the window.

      *Take note of TTT and UUU.*

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.
   #. *Expect:* There are no exceptions, GTK messages, or warning
      messages in the console.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.
   #. *Expect:* *Factsheet Summary* pane is blank.

#. **Step:** Click Factsheet **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``summary sample.fsg`` and click **Open button**
   (dialog title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "This sample factsheet
      includes a summary." in *Factsheet Summary* pane.
   #. *Expect:* Window subtitle is "summary sample.fsg (VVV-WWW)".
   #. *Expect:* Factsheet identifier (VVV) is distinct from that of the
      first window.
   #. *Expect:* Window identifier (WWW) is distinct from that of the
      first window.

      *Take note of VVV and WWW.*

      *An identifier may repeat in different Factsheet runs.*

Steps -- Edit and View Summary
------------------------------
1. **Step** Continue with **summary sample.fsg (VVV-WWW)** window.

   a. *Expect:* Summary Sample window contains "This sample factsheet
      includes a summary." in *Factsheet Summary* pane.

#. **Step:** Select and copy summary text. Paste into another
   application (e.g. Vim).

   a. *Expect:* Factsheet application highlights text when selected.
   #. *Expect:* Pasted text matches summary text.

#. **Step:** Add a long sentence to the summary.

   a. *Expect:* Summary text wraps when the sentence length exceeds the
      width of the window.
   #. *Expect:* Wrapping is at white space between words.

#. **Step:** Grab the lower right corner of the window and resize the
   window.

   a. *Expect:* Summary text wraps to fit the resized window.
   #. *Expect:* Wrapping is at white space between words.

#. **Step:** Copy "And now for something completely different!"
   including a new line and paste at the bottom of the summary.

   a. *Expect:* Copied text appears in summary and matches original.

#. **Step:** Repeat paste about 20 time at the bottom of the summary.

   a. *Expect:* Copied text appears in summary and matches original.
   #. *Expect:* Summary pane scrolls as needed to keep each paste
      visible.

#. **Step:** Move scroll slider to review summary content.

   a. *Expect:* Pane scrolls to cover all summary content.

#. **Step:** Lengthen window and move pane divider down to expose
   entire summary.

   a. *Expect:* Scrollbar disappears when entire summary is visible.

#. **Step:** Move pane divider up as far as possible.

   a. *Expect:* Pane divider stops with about three summary lines
      visible.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save button shows press-release color changes.

#. **Step:** Click Summary Sample window **close icon** (window title
   far right).

   a. *Expect:* Summary Sample window disappears.

#. **Step:** Click initial window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.
   #. *Expect:* There are no exceptions, GTK messages, or warning
      messages in the console.

Steps -- Multiple Windows and Sheets
------------------------------------
1. **Step** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.
   #. *Expect:* *Factsheet Summary* pane is blank.

#. **Step:** Click Factsheet **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``summary sample.fsg`` and click **Open button**
   (dialog title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "This sample factsheet
      includes a summary." along with added text in *Factsheet Summary*
      field.
   #. *Expect:* Window subtitle is "summary sample.fsg (XXX-YYY)".
   #. *Expect:* Factsheet identifier (XXX) is distinct from that of the
      first window.
   #. *Expect:* Window identifier (YYY) is distinct from that of the
      first window.

      *Take note of XXX and YYY.*

      *An identifier may repeat in different Factsheet runs.*

#. **Step:** Select Factsheet **menu > Display ... > Open window**
   (right of **Factsheet** field).

   a. *Expect:* New window appears with window subtitle "Summary
      Sample.fsgt (XXX-ZZZ)".
   #. *Expect:* The summary pane contents are the same.

      *Wrapping and the visible portions of the windows may be different
      unless the windows have the same size and layout.*

      *Take note of ZZZ.*

#. **Step:** Add "Our greatest weapon is fear and terror!" at the
   bottom of the second Summary Sample window.

   a. *Expect:* The same text appears in the first Summary Sample window.
   #. *Expect:* In the initial window, *Factsheet Summary* pane remains
      blank.

#. **Step:** Select and delete the words "and terror" from the first
   Summary Sample window.

   a. *Expect:* The corresponding words are selected in the second
      Sample Summary window and then disappear.
   #. *Expect:* In the initial window, the summary pane remains blank.

#. **Step:** In the first Summary Sample window, select Factsheet
   **menu > Display ... > Summary** (right of **Factsheet** field).

   a. *Expect:* In the first Summary Sample window, the *Factsheet
      Summary* pane disappears.
   #. *Expect:* The *Factsheet Topics* pane expands to replace it.
   #. *Expect:* There is no change in the second Summary Sample window
      or in the initial window.

#. **Step:** Select **Summary** menu item.

   a. *Expect:* The *Factsheet Summary* pane reappears in the first
      Summary Sample window.
   #. *Expect:* The pane contents are unchanged.
   #. *Expect:* The *Factsheet Topics* pane shrinks to accommodate it.
   #. *Expect:* Again, there is no change in the second Summary Sample
      window or in the initial window.

#. **Step:** Press Esc key.

   a. *Expect:* The popum menu disappears.

#. **Step:** In first Summary Sample window, select Factsheet **menu
   > File ... > Close.**

   a. *Expect:* Data Loss Warning dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog and both Summary Sample windows disappear.
   #. *Expect:* The initial window remains.

#. **Step:** Click initial window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


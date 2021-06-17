Case Factsheet Summary
======================

**Purpose:** confirm display and edit of Factsheet summary.

.. include:: /icons/icons-include.txt

Setup
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

Steps
-----
1. **Step:** Check window layout.

   a. *Expect:* A frame with collapser icon (|collapser|) and label
      "*Factsheet Summary*\ " appears immediately below the edit icon
      |edit| for the Factsheet name.

#. **Step:** Click inside the *Factsheet Summary* frame away from the
   margins. 

   a. *Expect:* A blinking text cursor (|) appears in the upper left
      corner of the frame.

#. **Step:** Edit the summary as follows: "There is a tide in the
   affairs of men, which taken at the flood, leads on to fortune.
   Omitted, all the voyage of their lives is bound in shallows and in
   misery."

   a. *Expect:* The text appears as entered.
   #. *Expect:* The text wraps to fit the frame.

#. **Step:** Grab the lower right corner of the window and resize the
   window.

   a. *Expect:* Summary text wraps to fit the resized frame.
   #. *Expect:* Wrapping is at white space between words.

#. **Step:** Select and copy summary text. Paste into another
   application (e.g. Vim).

   a. *Expect:* Factsheet application highlights text when selected.
   #. *Expect:* Pasted text matches summary text.

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

#. **Step:** Click initial window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.


Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

#. Transient Gdk-WARNING on 2021-06-16

   * *Warning:* (app.py:10104): Gdk-WARNING ...: Error writing selection
     data: Error writing to file descriptor: Broken pipe
   * *Reproduce:*

      a. Enter text in Factsheet Summary frame.
      #. Select text with mouse

   * *Notes:*

      a. I could reproduce the warning on June 16 but not the following
         day.
      #. On June 16, moving mouse cursor to change size of selection
         triggers multiple warnings.
      #. Double and triple clicking to select text does not trigger
         warning.
      #. Selecting text with arrow keys does not trigger warning.

Case Factsheet Save and Open with Topic
=======================================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet``).
#. Start application with :doc:`../test_helpers/help_start_application`
#. Add three topics with :doc:`../test_helpers/help_sheet_new_topic`.
   Use the following Name-Title pairs.
   
   * Name: "Topic 1" and Title: "First Topic"
   * Name: "Topic 2" and Title: "Second Topic"
   * Name: "Topic 3" and Title: "Third Topic"

Steps
-----
#. **Step:** Type title "Topics Check" in **Factsheet** field.

   a. *Expect:* Title appears in field.

#. **Step:** Click Factsheet **Save button** (window title on right
   near center).

   a. *Expect:* Save dialog appears.
   #. *Expect:* Dialog file **Name** field contains "factsheet.fsg".

#. **Step:** Change to test data directory.

   a. *Expect:* Save dialog shows directory contents.

#. **Step:** Edit file **Name** field to "TopicsSave.fsg"

   a. *Expect:* Field contains new file name.

#. **Step:** Click dialog **Save button** (dialog title on right).

   a. *Expect:* Dialog disappears.

#. **Step:** List test data directory contents (in shell or file
   browser).

   a. *Expect:* File ``TopicsSave.fsg`` appears with current timestamp.
   #. *Take note of file time and size.*

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

#. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Click Factsheet **Open button** (window title on far
   left).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``TopicsSave.fsg`` and click **Open button**
   (dialog title on right)

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears with "Topics Check" in
      **Factsheet** field.
   #. *Expect:* The topics outline contains three topics as entered in
      setup (*Topics* pane lower left).
   #. New window may cover first window.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.
#. In each window, click window **close icon** |window-close|.

   a. *Expect:* Windows disappears.
   #. *Expect:* *Application* closes with last window.


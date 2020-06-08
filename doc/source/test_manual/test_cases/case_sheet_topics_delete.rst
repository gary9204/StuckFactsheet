Case Factsheet Delete Topic
===========================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
1. Start application with :doc:`../test_helpers/help_start_application`
#. Add three topics with :doc:`../test_helpers/help_sheet_new_topic`.
   Name the topics "Alpha", "Beta",  and "Gamma".
#. Save factsheet to file for repeated use.
#. Open a second window with  *Factsheet* **menu** item **Display ... >
   Open window** (right of *Factsheet* field).

   .. note::
      Perform the following steps in the second window. Monitor
      the first window for unexpected behavior.

      At the first step, no topic should be selected (highlighted in
      blue). If a topic is selected, close the window and open a new
      one.

Steps - Delete Single Topic
---------------------------
1. **Step:** Select *Topics* menu |menu| item **Delete Topic**
   (pane toolbar, last icon on right).

   a. *Expect:* No change in the topic outline.
   #. *Expect:* No topic is selected.

#. **Step:** In *Topics* pane (lower left), click **Beta**.

   a. *Expect:* Topic ``Beta`` is selected (highlighted in blue).

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**.

   a. *Expect:* ``Beta`` disappears from the topic outline.
   #. *Expect:* ``Gamma`` is selected.

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**.

   a. *Expect:* ``Gamma`` disappears from the topic outline.
   #. *Expect:* ``Alpha`` is selected.

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**.

   a. *Expect:* ``Alpha`` disappears from the topic outline.
   #. *Expect:* The *Topics* pane outline is empty.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* The window closes.
   #. *Expect:* The original window remains.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* The dialog closes.
   #. *Expect:* The factsheet window closes.
   #. *Expect:* The application exits.

Steps - Delete All Topics
-------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* *Topics* pane contains a toolbar but no topics.

#. **Step:** Open the factsheet file containing the three topics.

   a. *Expect:* *Topics* pane contains topics ``Alpha``, ``Beta``, and
      ``Gamma``.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (right of *Factsheet* field).

   a. *Expect:* Second window appears with default factsheet.
   #. New window may cover first window.

   .. note:: Perform the following steps in the second window. Monitor
      the first window for unexpected behavior.

1. **Step:** Select *Topics* menu |menu| item **Clear All Topics**
   (pane toolbar, last icon on right).

   a. *Expect:* No topics appear in the *Topics* pane.

Teardown
--------
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* appears for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

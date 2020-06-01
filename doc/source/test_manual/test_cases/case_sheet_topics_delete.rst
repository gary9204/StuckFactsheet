Case Factsheet Delete Topic
===========================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
1. Start application with :doc:`../test_helpers/help_start_application`
#. Add three topics with :doc:`../test_helpers/help_sheet_new_topic`.
   Name the topics "Topic 1", "Topic 2",  and "Topic 3".

Steps
-----
1. **Step:** In *Topics* pane (lower left), click **Topic 2**.

   a. *Expect:* Topic ``Topic 2`` is selected (highlighted in blue).

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**
   (pane toolbar, last icon on right).

   a. *Expect:* ``Topic 2`` disappears from the topic outline.
   #. *Expect:* ``Topic 3`` is selected.

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**.

   a. *Expect:* ``Topic 3`` disappears from the topic outline.
   #. *Expect:* ``Topic 1`` is selected.

#. **Step:** Select *Topics* menu |menu| item **Delete Topic**.

   a. *Expect:* ``Topic 1`` disappears from the topic outline.
   #. *Expect:* The topic outline is empty.

.. admonition:: To Do

   Address situation where no topic is selected

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.


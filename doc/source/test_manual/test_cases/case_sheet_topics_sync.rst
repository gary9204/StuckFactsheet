Case Factsheet Windows with Topic
=================================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
1. Start application with :doc:`../test_helpers/help_start_application`

Steps
-----
#. **Step:** Click on Name **drop-down icon** |open-popup| (left of
   *Factsheet* field).

   a. *Expect:* *Edit Name* dropdown appears.
   #. *Expect:* Name entry field contains "Unnamed", which is selected
      (highlighted in blue).

#. **Step:** Type "Base" in Name entry field and press Enter.

   a. *Expect:* *Edit Name* dropdown disappears.
   #. *Expect:* Window title changes to ``Base``.

#. **Step:** Select Factsheet menu |menu| item **File ... > New**
   (right of *Factsheet* field).

   a. *Expect:* Second window appears with window title ``Unnamed``.
   #. New window may cover first window.

#. **Step:** In ``Unnamed`` window, click on Name **drop-down icon**
   |open-popup|.

   a. *Expect:* *Edit Name* dropdown appears.
   #. *Expect:* Name entry field contains "Unnamed", which is selected.
   #. Note window subtitle of the form "Unsaved XXX-YYY".

#. **Step:** Type "Topics" in Name entry field and press Enter.

   a. *Expect:* *Edit Name* dropdown disappears.
   #. *Expect:* Window title changes to ``Topics``.

#. **Step:** In ``Topics`` window, select Factsheet menu |menu| item
   **Display ... > Open Window**.

   a. *Expect:* Third window appears with window title ``Topics``.
   #. Note window subtitle of the form "Unsaved XXX-ZZZ".
   #. New window may cover first window.

#. **Step:** In window ``Topics -  ZZZ``, add a topic with
   :doc:`../test_helpers/help_sheet_new_topic`. Use name "Topic 1" and
   title "First Topic".

   a. *Expect:* ``Topic 1`` appears in *Topics* pane of window
      ``Topics - ZZZ``.
   #. *Expect:* ``Topic 1`` appears in *Topics* pane of window
      ``Topics - YYY``.
   #. *Expect:* Window ``Base`` is unchanged.

#. **Step:** In window ``Topics -  YYY``, add two topics with
   :doc:`../test_helpers/help_sheet_new_topic`. Use name "Topic 2" and
   title "Second Topic" for the first addition.  Use name "Topic 3" and
   title "Third Window" for the second addition.

   a. *Expect:* ``Topic 2`` and ``Topic 3`` appear in *Topics* pane of
      window ``Topics - YYY``.
   #. *Expect:* ``Topic 2`` and ``Topic 3`` appear in *Topics* pane of
      window ``Topics - ZZZ``.
   #. *Expect:* Window ``Base`` is unchanged.

#. **Step:** In window ``Topics - YYY``, click on ``Topic 1`` in the
   topics outline.

   a. *Expect:* ``Topic 1`` is selected in window ``Topics - YYY``
      (highlighted in blue).
   #. *Expect:* ``Topic 1`` is not selected in window ``Topics - ZZZ``.

#. **Step:** In window ``Topics - YYY``, select *Topics* menu |menu|
   item **Delete Topic** (pane toolbar, last icon on right).

   a. *Expect:* ``Topic 1`` disappears from window ``Topics - YYY``.
   #. *Expect:* ``Topic 2`` is selected in window ``Topics - YYY``
   #. *Expect:* ``Topic 1`` disappears from window ``Topics - ZZZ``.
   #. *Expect:* ``Topic 2`` is not selected in window ``Topics - ZZZ``.

#. **Step:** In window ``Topics - ZZZ``, click on ``Topic 3`` in the
   topics outline.

   a. *Expect:* ``Topic 3`` is selected in window ``Topics - ZZZ``.
   #. *Expect:* ``Topic 2`` is selected in window ``Topics - YYY``.

#. **Step:** In window ``Topics - ZZZ``, select *Topics* menu |menu|
   item **Delete Topic**.

   a. *Expect:* ``Topic 3`` disappears from window ``Topics - ZZZ``.
   #. *Expect:* ``Topic 2`` is selected in window ``Topics - ZZZ``
   #. *Expect:* ``Topic 3`` disappears from window ``Topics - YYY``.
   #. *Expect:* ``Topic 2`` is selected in window ``Topics - YYY``.

Teardown
--------
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* appears for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


Case Factsheet Searches
=======================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. include:: /icons/icons-include.txt

Setup
-----
Create a outline containing topics with the following name-title pairs.
See :doc:`../test_helpers/help_sheet_new_topic`.  

    | Name 0 - Title 0
    | Name 1 - Title 1
    |   Name 10 - Title 10 
    |      Name 100 - Title 100
    | Name 2 - Title 2
    | Title 1 - Name 1
    |    Title 10 - Name 10

Steps - Topics Outline
----------------------

#. **Step:** Click *Topics* **find icon** |edit-find| (*Topics* pane
   toolbar first icon from left).

   a. *Expect:* Find bar appears between toolbar and topics outline.
   #. *Expect:* Find bar contains a text entry field (light background
      box with magnifying glass icon).
   #. *Expect:* Find bar contains two check buttons labeled "By name"
      and "By title".  Both buttons are checked.

#. **Step:** Click *Topics* **find icon** |edit-find|.

   a. *Expect:* Find bar disappears.

#. **Step:** Click *Topics* **find icon** |edit-find|.

   a. *Expect:* Find bar reappears.

#. **Step:** Click in find entry field and press "N" key.

   a. *Expect:* Topic ``Name 0`` is selected.

#. **Step:** Continue typing "ame 1" in the find entry field.

   a. *Expect:* Topic ``Name 1`` is selected.

#. **Step:** Continue typing "0" in the find entry field.

   #. *Expect:* ``Name 1`` expander |expander| changes to collapser
      |collapser|.
   #. *Expect:* Topic ``Name 10`` appears indented under ``Name 1``.
   #. *Expect:* Topic ``Name 10`` is selected.

#. **Step:** Continue typing "0" in the find entry field.

   a. *Expect:* ``Name 10`` expander |expander| changes to collapser
      |collapser|.
   #. *Expect:* Topic ``Name 100`` appears indented under
      ``Name 100``.
   #. *Expect:* Topic ``Name 100`` is selected.

#. **Step:** Continue typing "0" in the find entry field.

   a. *Expect:* The entire outline of seven topics appears.
   #. *Expect:* No topic is selected.

#. **Step:** Backspace over the final "0" in the find entry field.

   a. *Expect:* Topic ``Name 100`` is selected.

#. **Step:** Continue backspacing over the find entry field until the
   field is empty.

   a. *Expect:* No topic is selected.

#. **Step:** Click **By name** check button.

   a. *Expect:* Button **By name** is cleared.
   #. *Expect:* Button **By title** remains checked.

#. **Step:** Click in find entry field and press "N" key.

   a. *Expect:* Topic with title ``Name 1`` is selected.  The topic name
      is ``Title 1``.

#. **Step:** Continue typing "ame 1" in the find entry field.

   a. *Expect:* Topic with name ``Title 1`` remains selected.

#. **Step:** Continue typing "0" in the find entry field.

   #. *Expect:* ``Title 1`` expander |expander| changes to collapser
      |collapser|.
   #. *Expect:* Topic with name ``Title 10`` appears indented under
      ``Title 1``.
   #. *Expect:* Topic ``Title 10`` is selected.

#. **Step:** Continue typing "0" in the find entry field.

   a. *Expect:* The entire outline of seven topics appears.
   #. *Expect:* No topic is selected.

#. **Step:** Backspace over the final "0" in the find entry field.

   a. *Expect:* Topic ``Title 10`` is selected.

#. **Step:** Backspace over the find entry field until the
   field is empty.

   a. *Expect:* No topic is selected.

#. **Step:** Click **By title** check button.

   a. *Expect:* Button **By title** is cleared.
   #. *Expect:* Button **By name** remains cleared.

#. **Step:** Click in find entry field and press "T" key.

   a. *Expect:* No topic is selected.

#. **Step:** Continue typing "Title 1" in the find entry field.

   a. *Expect:* No topic is selected.

#. **Step:** Backspace over the find entry field until the
   field is empty.

   a. *Expect:* No topic is selected.

#. **Step:** Click in find entry field and press "N" key.

   a. *Expect:* No topic is selected.

#. **Step:** Continue typing "ame 0" in the find entry field.

   a. *Expect:* No topic is selected.

#. **Step:** Continue backspacing over the find entry field until the
   field is empty.

   a. *Expect:* No topic is selected.

#. **Step:** Click **By name** check button.

   a. *Expect:* Button **By name** is checked.
   #. *Expect:* Button **By title** remains cleared.

#. **Step:** Click in find entry field and press "T" key.

   a. *Expect:* Topic with name ``Title 1`` is selected.

#. **Step:** Continue typing "itle 1" in the find entry field.

   a. *Expect:* Topic ``Title 1`` remains selected.

#. **Step:** Continue typing "0" in the find entry field.

   #. *Expect:* ``Title 1`` expander |expander| changes to collapser
      |collapser|.
   #. *Expect:* Topic with namne``Title 10`` appears indented under
      ``Title 1``.
   #. *Expect:* Topic ``Title 10`` is selected.

#. **Step:** Backspace over the find entry field until the field is
   empty.

   a. *Expect:* No topic is selected.

Steps - Templates Outline
-------------------------

.. admonition:: To Do

   Add steps to verify search function for template outlines.

Teardown
--------
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* may appear for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

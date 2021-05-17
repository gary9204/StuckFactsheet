Case Factsheet Topics Toolbar
=============================

**Purpose:** demonstrate features provided by the toolbar in the
*Topics* pane of a factsheet.

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
    | Name 3 - Title 3
    |   Name 30 - Title 30 
    |      Name 300 - Title 300
    |   Name 31 - Title 31 
    |      Name 310 - Title 310
    |      Name 311 - Title 311

Steps - Find Topic
------------------

Perform the Topic test cases in :doc:`case_sheet_search`.


Steps - Specify Topic
---------------------

Perform the test cases in :doc:`case_sheet_topics_new`.

Steps - Go To First Topic
-------------------------

1. **Step:** Click topic **Name 3** in *Topics* pane.

   a. *Expect:* Topic ``Name 3`` is selected (highlighted in blue).

#. **Step:** Click *Topics* **go first icon** |go-first| (*Topics* pane
   toolbar third icon from left).

   a. *Expect:* Topic ``Name 0`` is selected.

Steps - Go to Last Topic
------------------------

1. **Step:** Click *Topics* **go last icon** |go-last| (*Topics* pane
   toolbar fourth icon from left).

   a. *Expect:* Topics ``Name 30`` and ``Name 31`` appear indented under
      ``Name 3``.
   #. *Expect:* Topics ``Name 310`` and ``Name 311`` appear indented
      under ``Name 31``.
   #. *Expect:* Topic ``Name 311`` is selected.


Steps - Collapse Topics Outline
--------------------------------

1. **Step:** Click *Topics* **collapse all icon** |collapse-all|
   (*Topics* pane toolbar sixth icon from left).

   a. *Expect:* Topic ``Name 3`` is selected.
   #. *Expect:* *Topics* outline shows only topics ``Name 0``, ``Name
      1``, ``Name 2``, and ``Name 3``. 

Steps - Expand Topics Outline
-----------------------------

1. **Step:** Click *Topics* **expand all icon** |expand-all|
   (*Topics* pane toolbar fifth icon from left).

   a. *Expect:* Topic ``Name 3`` is selected.
   #. *Expect:* *Topics* outline shows all topics in the outline.

Steps - Topics Menu
-------------------

Perform the test steps in :doc:`case_sheet_topics_new`. Specifically,
**Steps - start topic specification**.

Perform the test steps in :doc:`case_sheet_topics_delete`.

Perform the test steps in :doc:`case_sheet_dialogs`. Specifically,
**Steps – Topics Help**.

Teardown
--------
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* may appear for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

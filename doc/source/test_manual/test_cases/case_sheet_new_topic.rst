Case Factsheet New Topic
========================

**Purpose:** demonstrate specifying a new topic in a factsheet.

Setup
-----
None

Steps - start topic specification
---------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.
   #. *Expect:* *Topics* pane contains a toolbar but no topics.

#. **Step:** Select *Topics* **menu > New Topic ...** (lower left
   pane).

   a. *Expect:* Select Template dialog appears.
   #. *Expect:* *Templates* pane in dialog contains templates named
      ``name_0xx`` and ``name_1xx``.
   #. *Expect:* *Summary* pane in dialog contains "Please select a
      **template**."

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Factsheet* **New Topic icon** (lower left pane
   toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears as before.

#. **Step:** Press Esc key.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

Steps - topic placement
-----------------------
.. helper TODO: help_sheet_place_topic.rst
    outline

1. **Step:** Select *Factsheet* **New Topic icon** (lower left
   pane toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears.

   .. admonition:: To Do

      Add placement feature to Factsheet and complete test section.

Steps - template selection
--------------------------
1. **Step:** Select *Topics* **New Topic icon** (lower left pane
   toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click on template ``name_0xx`` in *Templates* pane.

   a. *Expect:* Template ``name_0xx`` is selected (highlighted in blue).
   #. *Expect:* *Summary* pane content changes to "Stub summary_0xx".
   #. *Expect:* Specify button (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.

   .. admonition:: To Do
   
      Update when Template Completion feature is finished.  Cancel Template
      Completion.  Continue with template selection test cases.

#. **Step:** Select *Topics* **New Topic icon**.

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click **expander** of template ``name_0xx`` in *Templates*
   pane (right-pointing triangle at start of template line).

   a. *Expect:* Expander changes to collapser (down-pointing triangle).
   #. *Expect:* Templates ``name_00x`` and ``name_01x`` appear indented
      under ``name_0xx``.
   #. *Expect:* Template ``name_00x`` has a expander and template
      ``name_01x`` does not.

#. **Step:** Click **expander** of template ``name_00x``.

   a. *Expect:* Expander changes to collapser.
   #. *Expect:* Template ``name_000`` appears indented under
      ``name_00x``.

#. **Step:** Click **expander** of template ``name_1xx`` and
   **expanders** of all templates that appear.

   a. *Expect:* Each expander changes to a collapser.
   #. *Expect:* *Templates* outline contains templates under template
      ``name_1xx``.

#. **Step:** Drag the **divider** between the *Templates* and *Summary*
   panes up until *Templates* pane is as small as possible.

   a. *Expect:* Four templates show in the *Templates* pane.
   #. *Expect:* Scrolling *Templates* pane shows 10 templates.

#. **Step:** Drag the **divider** between the *Templates* and *Summary*
   panes up until *Summary* pane is as small as possible.  Increase the
   dialog height until white space shows at the bottom of the
   *Templates* pane.

   a. *Expect:* The *Templates* pane shows 10 templates.

#. **Step:** Click on template ``name_112`` in *Templates* outline pane.

   a. *Expect:* Template ``name_112`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_112".
   #. *Expect:* Specify button changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.

   .. admonition:: To Do
   
      Update when Template Completion feature is finished.  Cancel Template
      Completion.  Continue with template selection.

#. **Step:** Select *Topics* **New Topic icon**.

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click **collapser** of template ``name_0xx``.

   a. *Expect:* Templates ``name_00x``, ``name_000``, and ``name_01x``
      disappear.
   #. *Expect:* An expander replaces the collapser of template
      ``name_0xx``.

#. **Step:** Click **collapser** of template ``name_1xx``.

   a. *Expect:* All templates under ``name_1xx`` disappear.
   #. *Expect:* Templates ``name_1xx`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_1xx".

#. **Step:** Click on **find icon** (magnifying glass immediately left
   of **Specify button** in dialog title).

   a. *Expect:* Find bar appears between dialog title and *Templates*
      pane.
   #. *Expect:* Find bar contains two option buttons labeled "By name"
      and "By title".  "By name" is selected (filled button dot).
   #. *Expect:* Find bar contains a text entry field (light background
      box with magnifying glass icon).

#. **Step:** Click on **find icon** in dialog title.

   a. *Expect:* Find bar disappears.

#. **Step:** Click on **find icon** in dialog title.

   a. *Expect:* Find bar reappears.

#. **Step:** Click in find entry field and press "n" key.

   a. *Expect:* Template ``name_0xx`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_0xx".

#. **Step:** Continue typing "ame_00" in the find entry field.

   a. *Expect:* ``name_0xx`` expander changes to collapser.
   #. *Expect:* Templates ``name_00x`` and ``name_01x`` appear indented
      under ``name_0xx``.
   #. *Expect:* Template ``name_00x`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_00x".

#. **Step:** Continue typing "0" in the find entry field.

   a. *Expect:* ``name_00x`` expander changes to collapser.
   #. *Expect:* Template ``name_000`` appears indented under
      ``name_00x`` and is selected.
   #. *Expect:* *Summary* pane contents changes to "Stub summary_000".

#. **Step:** Continue typing "0" in the find entry field.

   a. *Expect:* The entire outline of 10 templates appears.
   #. *Expect:* No template is selected.
   #. *Expect:* *Summary* pane contents change to "Please select a
      **template**."

#. **Step:** Backspace over the final "0" in the find entry field.

   a. *Expect:* Template ``name_000`` is selected.
   #. *Expect:* *Summary* pane contents change to "Stub summary_000".

#. **Step:** Click **Cancel button**.

   a. *Expect:* Dialog disappears.

Steps - template completion
---------------------------
.. helper TODO: help_sheet_specify_topic.rst
    outline

.. admonition:: To Do

   Add template completion feature to Factsheet and complete test
   section.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

#. **Step:** Click window **close icon**.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.


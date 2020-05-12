Case Factsheet New Topic
========================

**Purpose:** demonstrate specifying a new topic in a factsheet.

.. |document-new| image::  /icons/document-new-symbolic.svg
   :alt: (page outline with plus)

.. |edit-find| image::  /icons/edit-find-symbolic.svg
   :alt: (magnifying glass)

.. |window-close| image::  /icons/window-close-symbolic.svg
   :alt: (x)

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

#. **Step:** Select *Factsheet* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears as before.

#. **Step:** Press Esc key.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

Steps - topic placement
-----------------------
.. helper TODO: help_sheet_place_topic.rst
    outline

1. **Step:** Select *Factsheet* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears.

   .. admonition:: To Do

      Add placement feature to Factsheet and complete test section.

Steps - template selection
--------------------------
1. **Step:** Select *Topics* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click on template ``name_0xx`` in *Templates* pane.

   a. *Expect:* Template ``name_0xx`` is selected (highlighted in blue).
   #. *Expect:* *Summary* pane content changes to "Stub summary_0xx".
   #. *Expect:* Specify button (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Specify button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* New Section dialog appears.

#. **Step:** Click dialog **Cancel button** (dialog title on far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

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
   #. *Expect:* New Section dialog appears.

#. **Step:** Click dialog **Cancel button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click **collapser** of template ``name_0xx``.

   a. *Expect:* Templates ``name_00x``, ``name_000``, and ``name_01x``
      disappear.
   #. *Expect:* An expander replaces the collapser of template
      ``name_0xx``.

#. **Step:** Click **collapser** of template ``name_1xx``.

   a. *Expect:* All templates under ``name_1xx`` disappear.
   #. *Expect:* Template ``name_1xx`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_1xx".

#. **Step:** Click on **find icon** |edit-find| (immediately left of
   Specify button in dialog title).

   a. *Expect:* Find bar appears between dialog title and *Templates*
      pane.
   #. *Expect:* Find bar contains two option buttons labeled "By name"
      and "By title".  "By name" is selected (filled button dot).
   #. *Expect:* Find bar contains a text entry field (light background
      box with magnifying glass icon).

#. **Step:** Click on **find icon** |edit-find| in dialog title.

   a. *Expect:* Find bar disappears.

#. **Step:** Click on **find icon** |edit-find| in dialog title.

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

1. **Step:** Select *Topics* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* Select Template dialog appears.

#. **Step:** Click on template ``name_0xx`` in *Templates* pane.

   a. *Expect:* Template ``name_0xx`` is selected (highlighted in blue).
   #. *Expect:* *Summary* pane content changes to "Stub summary_0xx".
   #. *Expect:* Specify button (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Specify button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* New Section dialog appears.
   #. *Expect:* Dialog displays page New Section.
   #. *Expect:* Page explains topic, assistant steps, and navegation
      buttons.

#. **Step:** Click **Next button** (dialog title far right)

   a. *Expect:* Dialog displays page Identity.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Page contains Name, Title, and Description fields.

#. **Step:** Click in **Name** field and type "Topic One".

   a. *Expect:* Field contents changes from "Enter section name" to
      "Topic One".

#. **Step:** Click in **Title** field and type "Initial Topic".

   a. *Expect:* Field contents changes from "Enter section title" to
      "Initial Topic".

#. **Step:** Click in **Description** field and type "This is the
   initial section added to the factsheet."

   a. *Expect:* Field contents matches typed text.

#. **Step:** Click **Back button** (dialog title on left next to Cancel
   button)

   a. *Expect:* Dialog displays page New Section.
   #. *Expect:* Page explains topic, assistant steps, and navegation
      buttons.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page Identity.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Name field contains "Topic One".
   #. *Expect:* Title field contains "Initial Topic".
   #. *Expect:* Summary field contains "This is the initial section
      added to the factsheet."

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page Confirm.
   #. *Expect:* Page explains **Apply** and **Back** buttons.
   #. *Expect:* Page displays Name value "Topic One".
   #. *Expect:* You can select but not edit the Name value.
   #. *Expect:* Page displays Title value "Initial Topic".
   #. *Expect:* You can select but not edit the Title value.
   #. *Expect:* Page diaplays Description value "This is the initial
      section added to the factsheet."
   #. *Expect:* You can select but not edit the Description value.

#. **Step:** Click **Back button**.

   a. *Expect:* Dialog displays page Identity.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Name field contains "Topic One".
   #. *Expect:* Title field contains "Initial Topic".
   #. *Expect:* Summary field contains "This is the initial section
      added to the factsheet."

#. **Step:** Click in **Name** field and edit to "Topic 1".

   a. *Expect:* Field contents changes from "Topic One" to
      "Topic 1".

#. **Step:** Click in **Title** field and edit to "First Topic".

   a. *Expect:* Field contents changes from "Initial Topic" to
      "First Topic".

#. **Step:** Click in **Description** field and edit "This is the
   first section added to the factsheet."

   a. *Expect:* Field contents matches edited text.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page Confirm.
   #. *Expect:* Page explains **Apply** and **Back** buttons.
   #. *Expect:* Page displays Name value "Topic 1".
   #. *Expect:* Page displays Title value "First Topic".
   #. *Expect:* Page diaplays Description value "This is the first
      section added to the factsheet."
   #. *Expect:* You can select but not edit the Name, Title, and
      Description values.

#. **Step:** Click **Apply button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains topic.
   #. *Expect:* "Topic 1" appears in Name column.
   #. *Expect:* "First Topic" appears in Title column.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* Application closes.


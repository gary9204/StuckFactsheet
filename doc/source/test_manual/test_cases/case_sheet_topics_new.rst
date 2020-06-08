Case Factsheet New Topic
========================

**Purpose:** demonstrate specifying a new topic in a factsheet. The
demonstration includes:

   * selecting a place for the topic,
   * selecting a template to specify the topic, and
   * specifying the topic.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps - Start Topic Specification
---------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* *Topics* pane contains a toolbar but no topics.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (right of *Factsheet* field).

   a. *Expect:* Second window appears with default factsheet.
   #. New window may cover first window.

   .. note:: Perform the following steps in the second window. Monitor
      the first window for unexpected behavior.

#. **Step:** Select *Topics* **menu** |menu| item **New Topic ...**
   (lower left pane toolbar, icon on far right).

   a. *Expect:* *Select Template* dialog appears.
   #. *Expect:* *Templates* pane in dialog contains templates with the
      first named ``Section``.
   #. *Expect:* *Summary* pane in dialog contains "Please select a
      **template**."

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Topics* **New Topic icon** |document-new|
   (lower left pane toolbar, second icon from left).

   a. *Expect:* *Select Template* dialog appears as before.

#. **Step:** Press Esc key.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

Steps - Topic Placement
-----------------------
.. helper TODO: help_sheet_place_topic.rst
    outline

1. **Step:** Select *Topics* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected (highlighted in blue).
   #. *Expect:* *Specify button* (dialog title far right) changes from
      disabled (gray) to enabled (blue).
   #. *Expect:* *Summary* pane content changes to the following.

      **Section Summary:** "You may group topics in the topics outline
      into sections.  Template Section creates a section heading in the
      outline where you may place or move topics."

#. **Step:** Click **Specify button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.
   #. *Expect:* Page explains topic, assistant steps, and navegation
      buttons.

#. **Step:** Click **Next button** (dialog title far right)

   a. *Expect:* Dialog displays page *Identity*.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Page contains Name, Title, and Description fields.

#. **Step:** Click in **Name** field and type "Alpha".

   a. *Expect:* Field contents changes from "Enter section name" to
      "Alpha".

#. **Step:** Click in **Title** field and type "Topic 1".

   a. *Expect:* Field contents changes from "Enter section title" to
      "Topic 1".

#. **Step:** Click in **Description** field and edit to "This section is
   for Topic 1."

   a. *Expect:* Field contents matches typed text.

#. **Step:** Click **Next button** (dialog title far right).

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page explains **Apply** and **Back** buttons.
   #. *Expect:* Page displays *Name* value "Alpha".
   #. *Expect:* Page displays *Title* value "Topic 1".
   #. *Expect:* Page diaplays Description value "This section is for
      Topic 1."

#. **Step:** Click **Apply button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains topic.
   #. *Expect:* ``Alpha`` appears in Name column.
   #. *Expect:* ``Topic 1`` appears in Title column.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Place New Topic* dialog appears.
   #. *Expect:* The *Topics* pane contains one topic with name ``Alpha`` and
      title ``Topic 1``.
   #. *Expect:* The *Summary* pane contains "Please select a topic."

#. **Step:** Click on topic ``Alpha`` ``Topic 1`` in *Topics* pane.

   a. *Expect:* Topic ``Alpha`` ``Topic 1`` is selected (highlighted in
      blue).
   #. *Expect:* *Summary* pane content changes to "This section is for
      Topic 1."
   #. *Expect:* *After* option is selected (filled dot to left of option).
   #. *Expect:* *Before* option is not selected (empty to left of
      option).
   #. *Expect:* *Child* option is not selected.
   #. *Expect:* *Place button* (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Place button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected.
   #. *Expect:* *Summary* pane content changes to **Section Summary**
      shown above.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Identity*.

#. **Step:** Enter "Beta" in **Name** field and "Topic 2" in **Title**
   field.

   a. *Expect:* Field contents changes to entered text in each field.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page displays *Name* value "Beta".
   #. *Expect:* Page displays *Title* value "Topic 2".

#. **Step:** Click **Apply button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains two topic.
   #. *Expect:* Topic ``Beta`` ``Topic 2`` appears immediately below
      topic ``Alpha`` ``Topic 1``.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Place New Topic* dialog appears.
   #. *Expect:* The *Topics* pane contains two topics ``Alpha`` ``Topic
      1`` and ``Beta`` ``Topic 2``.
   #. *Expect:* The *Summary* pane contains "Please select a topic."

#. **Step:** Click on topic ``Alpha`` ``Topic 1`` in *Topics* pane.

   a. *Expect:* Topic ``Alpha`` ``Topic 1`` is selected.
   #. *Expect:* *Summary* pane content changes to "This section is for
      Topic 1."
   #. *Expect:* *After* option is selected.
   #. *Expect:* *Before* and *Child* options are not selected.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Before option**.

   a. *Expect:* *Before* option is selected.
   #. *Expect:* *After* and *Child* options are not selected.

#. **Step:** Click **Place button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Identity*.

#. **Step:** Enter "Gamma" in **Name** field and "Topic 3" in **Title**
   field.

   a. *Expect:* Field contents changes to entered text in each field.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page displays *Name* value "Gamma".
   #. *Expect:* Page displays *Title* value "Topic 3".

#. **Step:** Click **Apply button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains three topic.
   #. *Expect:* The order of the topics are  ``Gamma`` ``Topic 3``,
      ``Alpha`` ``Topic 1``, and ``Beta`` ``Topic 2``.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Place New Topic* dialog appears.
   #. *Expect:* The *Topics* pane contains three topics: ``Gamma``
      ``Topic 3``, ``Alpha`` ``Topic 1`` and ``Beta`` ``Topic 2``.
   #. *Expect:* The *Summary* pane contains "Please select a topic."

#. **Step:** Click on topic ``Alpha`` ``Topic 1`` in *Topics* pane.

   a. *Expect:* Topic ``Alpha`` ``Topic 1`` is selected.
   #. *Expect:* *Summary* pane content changes to "This section is for
      Topic 1."
   #. *Expect:* *Before* option is selected.
   #. *Expect:* *After* and *Child* options are not selected.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Child option**.

   a. *Expect:* *Child* option is selected.
   #. *Expect:* *After* and *Before* options are not selected.

#. **Step:** Click **Place button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected.
   #. *Expect:* *Summary* pane content changes to **Section Summary**
      shown above.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Identity*.

#. **Step:** Enter "Delta" in **Name** field and "Topic 4" in **Title**
   field.

   a. *Expect:* Field contents changes to entered text in each field.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page displays *Name* value "Delta".
   #. *Expect:* Page displays *Title* value "Topic 4".

#. **Step:** Click **Apply button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains three topic.
   #. *Expect:* The order of the topics are  ``Gamma`` ``Topic 3``,
      ``Alpha`` ``Topic 1``, and ``Beta`` ``Topic 2``.
   #. *Expect:* There is an expander |expander| immediately left of
      ``Alpha`` ``Topic 1``.

#. **Step:** Click on the **expander** |expander| for ``Alpha`` ``Topic
   1``.

   a. *Expect:* *Topics* outline shows topic ``Delta`` ``Topic 4`` as a
      child of topic ``Alpha`` ``Topic 1``.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Place New Topic* dialog appears.
   #. *Expect:* The *Topics* pane contains three topics: ``Gamma``
      ``Topic 3``, ``Alpha`` ``Topic 1`` and ``Beta`` ``Topic 2``.
   #. *Expect:* The *Summary* pane contains "Please select a topic."

#. **Step:** Click on topic ``Alpha`` ``Topic 1`` in *Topics* pane.

   a. *Expect:* Topic ``Alpha`` ``Topic 1`` is selected.
   #. *Expect:* *Summary* pane content changes to "This section is for
      Topic 1."
   #. *Expect:* *Child* option is selected.
   #. *Expect:* *After* and *Before* options are not selected.
   #. *Expect:* *Place button* changes from disabled to enabled.

#. **Step:** Click **Place button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected.
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Identity*.

#. **Step:** Enter "Epsilon" in **Name** field and "Topic 5" in **Title**
   field.

   a. *Expect:* Field contents changes to entered text in each field.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page displays *Name* value "Epsilon".
   #. *Expect:* Page displays *Title* value "Topic 5".

#. **Step:** Click **Apply button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *Topics* pane contains three topic.
   #. *Expect:* The order of the topics are  ``Gamma`` ``Topic 3``,
      ``Alpha`` ``Topic 1``, and ``Beta`` ``Topic 2``.
   #. *Expect:* There is an collapser immediately left of
      ``Alpha`` ``Topic 1``.
   #. *Expect:* *Topics* outline shows two children of topic ``Alpha``
      ``Topic 1``: topic ``Delta`` ``Topic 4`` followed by topic ``Epsilon``
      ``Topic 5``.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Place New Topic* dialog appears.
   #. *Expect:* The *Topics* pane contains three topics: ``Gamma``
      ``Topic 3``, ``Alpha`` ``Topic 1`` and ``Beta`` ``Topic 2``.
   #. *Expect:* There is an expander immediately left of ``Alpha`` ``Topic
      1``.
   #. *Expect:* The *Summary* pane contains "Please select a topic."

#. **Step:** Click on the **expander** |expander| for ``Alpha`` ``Topic
   1``.

   #. *Expect:* *Topics* outline shows two children of topic ``Alpha``
      ``Topic 1``: topic ``Delta`` ``Topic 4`` followed by topic ``Epsilon``
      ``Topic 5``.

#. **Step:** Click **Cancel button** (dialog title far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet window is unchanged

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

Steps - Template Selection
--------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.
   #. *Expect:* *Topics* pane contains a toolbar but no topics.

#. **Step:** Select *Factsheet* **menu** item **Display ... > Open
   window** (right of *Factsheet* field).

   a. *Expect:* Second window appears with default factsheet.
   #. New window may cover first window.

   .. note:: Perform the following steps in the second window. Monitor
      the first window for unexpected behavior.

#. **Step:** Select *Topics* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected (highlighted in blue).
   #. *Expect:* *Summary* pane content changes to **Section Summary**
      shown above.
   #. *Expect:* *Specify button* (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Specify button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.

#. **Step:** Click dialog **Cancel button** (dialog title on far left).

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Select Template* dialog appears.

#. **Step:** Click **expander** |expander| of template ``Section`` in
   *Templates* pane (right-pointing triangle at start of template line).

   a. *Expect:* Expander changes to collapser (|collapser|).
   #. *Expect:* Templates ``name_00x`` and ``name_01x`` appear indented
      under ``Section``.
   #. *Expect:* Template ``name_00x`` has a expander and template
      ``name_01x`` does not.

#. **Step:** Click **expander** |expander| of template ``name_00x``.

   a. *Expect:* Expander changes to collapser.
   #. *Expect:* Template ``name_000`` appears indented under
      ``name_00x``.

#. **Step:** Click **expander** |expander| of template ``name_1xx`` and
   **expanders** |expander| of all templates that appear.

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
   #. *Expect:* *Specify button* changes from disabled to enabled.

#. **Step:** Click **Specify button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.

#. **Step:** Click dialog **Cancel button**.

   a. *Expect:* Dialog disappears.
   #. *Expect:* The factsheet remains unchanged.

#. **Step:** Select *Topics* **New Topic icon** |document-new|.

   a. *Expect:* *Select Template* dialog appears.

#. **Step:** Click **collapser** |collapser| of template ``Section``.

   a. *Expect:* Templates ``name_00x``, ``name_000``, and ``name_01x``
      disappear.
   #. *Expect:* An expander replaces the collapser of template
      ``Section``.

#. **Step:** Click **collapser** |collapser| of template ``name_1xx``.

   a. *Expect:* All templates under ``name_1xx`` disappear.
   #. *Expect:* Template ``name_1xx`` is selected.
   #. *Expect:* *Summary* pane content changes to "Stub summary_1xx".

#. **Step:** Click on **Find icon** |edit-find| (immediately left of
   *Specify button* in dialog title).

   a. *Expect:* Find bar appears between dialog title and *Templates*
      pane.
   #. *Expect:* Find bar contains two option buttons labeled "By name"
      and "By title".  "By name" is selected (filled button dot).
   #. *Expect:* Find bar contains a text entry field (light background
      box with magnifying glass icon).

#. **Step:** Click on **Find icon** |edit-find| in dialog title.

   a. *Expect:* Find bar disappears.

#. **Step:** Click on **Find icon** |edit-find| in dialog title.

   a. *Expect:* Find bar reappears.

#. **Step:** Click in find entry field and press "n" key.

   a. *Expect:* Template ``Section`` is selected.
   #. *Expect:* *Summary* pane content changes to **Section Summary**
      shown above.

#. **Step:** Continue typing "ame_00" in the find entry field.

   a. *Expect:* ``Section`` expander changes to collapser.
   #. *Expect:* Templates ``name_00x`` and ``name_01x`` appear indented
      under ``Section``.
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

Steps - Template Completion
---------------------------
.. helper TODO: help_sheet_specify_topic.rst
    outline

1. **Step:** Select *Topics* **New Topic icon** |document-new| (lower
   left pane toolbar, second icon from left).

   a. *Expect:* *Select Template* dialog appears.

#. **Step:** Click on template ``Section`` in *Templates* pane.

   a. *Expect:* Template ``Section`` is selected (highlighted in blue).
   #. *Expect:* *Summary* pane content changes to **Section Summary**
      shown above.
   #. *Expect:* *Specify button* (dialog title far right) changes from
      disabled (gray) to enabled (blue).

#. **Step:** Click **Specify button** (dialog title far right).

   a. *Expect:* Dialog disappears.
   #. *Expect:* *New Section* dialog appears.
   #. *Expect:* Dialog displays page *New Section*.
   #. *Expect:* Page explains topic, assistant steps, and navegation
      buttons.

#. **Step:** Click **Next button** (dialog title far right)

   a. *Expect:* Dialog displays page *Identity*.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Page contains Name, Title, and Description fields.

#. **Step:** Click in **Name** field and type "Alpha".

   a. *Expect:* Field contents changes from "Enter section name" to
      "Alpha".

#. **Step:** Click in **Title** field and type "Initial Topic".

   a. *Expect:* Field contents changes from "Enter section title" to
      "Initial Topic".

#. **Step:** Click in **Description** field and type "This is the
   initial section added to the factsheet."

   a. *Expect:* Field contents matches typed text.

#. **Step:** Click **Back button** (dialog title on left next to Cancel
   button)

   a. *Expect:* Dialog displays page *New Section*.
   #. *Expect:* Page explains topic, assistant steps, and navegation
      buttons.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Identity*.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Name field contains "Alpha".
   #. *Expect:* Title field contains "Initial Topic".
   #. *Expect:* Summary field contains "This is the initial section
      added to the factsheet."

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page explains **Apply** and **Back** buttons.
   #. *Expect:* Page displays *Name* value "Alpha".
   #. *Expect:* You can select but not edit the *Name* value.
   #. *Expect:* Page displays *Title* value "Initial Topic".
   #. *Expect:* You can select but not edit the Title value.
   #. *Expect:* Page diaplays Description value "This is the initial
      section added to the factsheet."
   #. *Expect:* You can select but not edit the Description value.

#. **Step:** Click **Back button**.

   a. *Expect:* Dialog displays page *Identity*.
   #. *Expect:* Page explains Name, Title, and Description fields.
   #. *Expect:* Name field contains "Alpha".
   #. *Expect:* Title field contains "Initial Topic".
   #. *Expect:* Summary field contains "This is the initial section
      added to the factsheet."

#. **Step:** Click in **Name** field and edit to "Topic 1".

   a. *Expect:* Field contents changes from "Alpha" to
      "Topic 1".

#. **Step:** Click in **Title** field and edit to "First Topic".

   a. *Expect:* Field contents changes from "Initial Topic" to
      "First Topic".

#. **Step:** Click in **Description** field and edit "This is the
   first section added to the factsheet."

   a. *Expect:* Field contents matches edited text.

#. **Step:** Click **Next button**.

   a. *Expect:* Dialog displays page *Confirm*.
   #. *Expect:* Page explains **Apply** and **Back** buttons.
   #. *Expect:* Page displays *Name* value "Topic 1".
   #. *Expect:* Page displays *Title* value "First Topic".
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
1. In each window, click window **close icon** |window-close|.

   | *Data Loss Warning* may appear for the last window of each
      sheet. Click **Discard button**.
   | Window disappears.
   | Application closes when last window closes.

#. Check console for exceptions, GTK errors, and warning messages. There
   should be none.

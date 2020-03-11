Case Factsheet Dialogs
======================

**Purpose:** demonstrate factsheet dialogs Help, Display Help, and Data
Loss Warning.

Setup
-----
None

Steps -- Help
--------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Click Factsheet **menu** (to right of **Sheet** field).
   #. *Expect:* Factsheet Menu appears.

#. a. **Step:** Click **Help** menu item.
   #. *Expect:* Factsheet Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, references, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog close button (dialog title upper right).
   #. *Expect:* Dialog disappears.

Steps -- Display Help
---------------------
1. a. **Step:** Click factsheet menu (to right of **Sheet** field).
   #. *Expect:* Factsheet Menu appears.

#. a. **Step:** Click **Display ...** menu item.
   #. *Expect:* Factsheet Display Menu appears.

#. a. **Step:** Click **Help** menu item.
   #. *Expect:* Factsheet Display Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, references, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog close button (title upper right).
   #. *Expect:* Dialog disappears.

Steps -- Data Loss Warning
--------------------------
1. a. **Step:** Type text in the **Factsheet** field (e.g. 'Sample').
   #. *Expect:* Text appears in field.

1. a. **Step:** Click application close icon (window title upper right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Review dialog contents (title, text, buttons, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click **Discard** button (dialog title upper right).
   #. *Expect:* Dialog disappears and application closes.

Teardown
--------
None


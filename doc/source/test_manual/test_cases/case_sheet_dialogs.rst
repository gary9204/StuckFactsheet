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

#. a. **Step:** Click Factsheet **menu > Help** (right of **Factsheet**
      field).
   #. *Expect:* Factsheet Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, references, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears.

Steps -- Display Help
---------------------
1. a. **Step:** Click factsheet **menu > Display ... > Help** (right of
      **Factsheet** field)
   #. *Expect:* Factsheet Display Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, references, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears.

Steps -- File Help
------------------
1. a. **Step:** Click factsheet **menu > File ... > Help** (right of
      **Factsheet** field)
   #. *Expect:* Factsheet File Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, references, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears.

Steps -- Data Loss Warning
--------------------------
1. a. **Step:** Type text in the **Factsheet** field (e.g. 'Sample').
   #. *Expect:* Text appears in field.

1. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Data Loss Warning dialog appears.

#. a. **Step:** Review dialog contents (title, text, buttons, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click **Discard** button (dialog title far right).
   #. *Expect:* Dialog disappears and application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


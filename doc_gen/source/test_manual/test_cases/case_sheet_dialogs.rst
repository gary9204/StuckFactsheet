Case Factsheet Dialogs
======================

**Purpose:** demonstrate factsheet dialogs Help, Display Help, and Data
Loss Warning.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps -- Help
--------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`.

   a. *Expect:* Application displays default factsheet.

#. **Step:** Click *Factsheet* **menu** |menu| item **Help** (right of
   *Factsheet* field).

   a. *Expect:* *Factsheet Help* dialog appears.

#. **Step:** Review dialog contents (title, text, references, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears.

Steps -- Display Help
---------------------
1. **Step:** Click *Factsheet* **menu** |menu| item **Display ... >
   Help** (right of *Factsheet* field).

   a. *Expect:* *Factsheet Display Help* dialog appears.

#. **Step:** Review dialog contents (title, text, references, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears.

Steps -- File Help
------------------
1. **Step:** Click *Factsheet* **menu** |menu| item **File ... > Help**
   (right of *Factsheet* field).

   a. *Expect:* *Factsheet File Help* dialog appears.

#. **Step:** Review dialog contents (title, text, references, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears.

Steps -- Topics Help
--------------------
1. **Step:** Click *Topics* **menu** |menu| item **Help** (pane toolbar,
   last icon on right).

   a. *Expect:* *Factsheet Topics Help* dialog appears.

#. **Step:** Review dialog contents (title, text, references, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears.

Steps -- Data Loss Warning
--------------------------
1. **Step:** Type text in the **Factsheet** field (e.g. 'Sample').

   a. *Expect:* Text appears in field.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Review dialog contents (title, text, buttons, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click **Discard button** (dialog title far right).

   a. *Expect:* Dialog disappears and application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


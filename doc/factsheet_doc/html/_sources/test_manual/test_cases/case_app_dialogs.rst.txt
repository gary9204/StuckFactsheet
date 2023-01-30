Case Application Dialogs
========================

**Purpose:** demonstrate application dialogs About, Help, and
Introduction.

.. include:: /icons/icons-include.txt

Setup
-----
None

Steps -- About
--------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* Application displays default factsheet.

#. **Step:** Click *Application* **menu** |menu| item **About** (window
   title on right).

   a. *Expect:* Application *About* dialog appears.

#. **Step:** Review dialog contents (title, version, text, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears. Factsheet window reamins visible.

Steps -- Help
-------------
1. **Step:** Click *Application* **menu** |menu| item **Help**.

   a. *Expect:* Application *Help* dialog appears.

#. **Step:** Review dialog contents (title, text, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears. Factsheet window remains visible.

Steps -- Introduction
---------------------
1. **Step:** Click *Application* **menu** |menu| item **Introduction**.

   a. *Expect:* Application *Introduction* dialog appears.

#. **Step:** Review dialog contents (title, text, etc.).

   a. *Expect:* Content is current and correct.

#. **Step:** Click dialog **close icon** |window-close| (dialog title
   far right).

   a. *Expect:* Dialog disappears.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* Window disappears and application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


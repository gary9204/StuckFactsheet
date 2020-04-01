Case Application Dialogs
========================

**Purpose:** demonstrate application dialogs About, Help, and
Introduction.

Setup
-----
None

Steps -- About
--------------
1. a. **Step:** Start application with
      :doc:`../test_helpers/help_start_application`
   #. *Expect:* Application displays default factsheet.

#. a. **Step:** Click Application **menu icon > About** (window title on right).
   #. *Expect:* Application About dialog appears.

#. a. **Step:** Review dialog contents (title, version, text, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears. Factsheet window reamins.

Steps -- Help
-------------
1. a. **Step:** Click Application **menu icon > Help** (window title on right).
   #. *Expect:* Application Help dialog appears.

#. a. **Step:** Review dialog contents (title, text, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears. Factsheet window remains.

Steps -- Introduction
---------------------
1. a. **Step:** Click Application **menu icon > Introduction** (window
      title on right).
   #. *Expect:* Application Introduction dialog appears.

#. a. **Step:** Review dialog contents (title, text, etc.).
   #. *Expect:* Content is current and correct.

#. a. **Step:** Click dialog **close icon** (dialog title far right).
   #. *Expect:* Dialog disappears.

#. a. **Step:** Click window **close icon** (window title far right).
   #. *Expect:* Window disappears and application closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


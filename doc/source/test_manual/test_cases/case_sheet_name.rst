Case Factsheet Name
===================

**Purpose:** confirm display and edit of Factsheet name.

.. include:: /icons/icons-include.txt

Setup
-----
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

Steps
-----
1. **Step:** Check window layout.

   a. *Expect:* The line immediately below the window title contains:
      |edit| (name edit icon), "Unnamed" (Factsheet name), |edit|
      (title edit icon), blank space, |menu| (Factsheet menu icon), and
      |help| (Factsheet Help icon).

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 
   #. *Expect:* Name edit popup contains: "\ **Name:**\ ", |apply|
      (apply edit icon), "Unnamed" highlighted, and |cancel| (cancel
      edit icon).

#. **Step:** Click the Factsheet window outside the name edit popup.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is unchanged ("Unnamed")

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 

#. **Step:** Press ``Esc`` key.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is unchanged ("Unnamed").

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 

#. **Step:** Click apply edit icon |apply|.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is unchanged ("Unnamed").

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 

#. **Step:** Edit name to "<b>Z". Do *not* close popup.

   a. *Expect:* "<b>Z" appears in both Factsheet name and popup.

#. **Step:** Edit name to "<b>Z</b>". Do *not* close popup.

   a. *Expect:* "<b>Z</b>" appears in popup.
   #. *Expect:* "\ **Z**\ " appears in Factsheet name.

#. **Step:** Press ``Enter`` key.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is "\ **Z**\ ".

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 

#. **Step:** Edit name to "<b>Z</b> 1". Do *not* close popup.

   a. *Expect:* "<b>Z</b> 1" appears in popup.
   #. *Expect:* "\ **Z** 1" appears in Factsheet name.

#. **Step:** Click apply icon |apply|.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is "\ **Z** 1".

#. **Step:** Edit name to "<b>Z</b> 2". Do *not* close popup.

   a. *Expect:* "<b>Z</b> 2" appears in popup.
   #. *Expect:* "\ **Z** 2" appears in Factsheet name.

#. **Step:** Click cancel icon |cancel|.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is "\ **Z** 1".

#. **Step:** Click name edit icon |edit| on far left.

   a. *Expect:* Name edit popup appears below |edit| icon. 

#. **Step:** Edit name to "<b>Z</b> 3". Do *not* close popup.

   a. *Expect:* "<b>Z</b> 3" appears in popup.
   #. *Expect:* "\ **Z** 3" appears in Factsheet name.

#. **Step:** Press ``Esc`` key.

   a. *Expect:* The popup disappears.
   #. *Expect:* Factsheet name is "\ **Z** 3".

#. **Step:** Click initial window **close icon** |window-close|.

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button**.

   a. *Expect:* Dialog and window disappear.
   #. *Expect:* *Application* closes.

Teardown
--------
1. Check console for exceptions, GTK errors, and warning messages. There
   should be none.


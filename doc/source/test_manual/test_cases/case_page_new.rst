Case Open Factsheet Window
==========================

**Purpose:** demonstrate opening of Factsheet pages.

Setup
-----
Apply :doc:`../test_helpers/help_start_application`

Steps
-----
1. a. **Step:** Type factsheet title in Sheet entry (e.g. First
      Sheet).
   #. *Expect:* Title appears in entry.

#. a. **Step:** Select Factsheet Menu > Display ... > Open window.
   #. *Expect:* Second window appears with same factsheet title as first
      window.  New window may cover first window.

#. a. **Step:** Change title in second window (e.g. Modified First Sheet).
   #. *Expect:* Title changes in both windows.

#. a. **Step:** Click new factsheet icon in first window title bar.
   #. *Expect:* Third window appears with blank factsheet title. New
      window may cover first or second window.

#. a. **Step:** Change title in third window (e.g. Second Sheet).
   #. *Expect:* Title changes in new window.  No change in first and
      second windows.

#. a. **Step:** In second sheet, select Factsheet Menu > Display ... >
      Open window.
   #. *Expect:* Fourth window appears with same factsheet title as
      second sheet.  New window may cover second sheet window.

#. a. **Step:** Change title in new window (e.g. Modified Second Sheet).
   #. *Expect:* Title changes in both second sheet windows.  Title is
      unchanged in both first sheet windows.

Teardown
--------
Close all windows to exit application.


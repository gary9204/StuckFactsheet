Case Factsheet File Errors
==========================

**Purpose:** demonstrate Factsheet response to file errors.

.. include:: /icons/icons-include.txt

Setup
-----
1. Create a test data directory (for example,
   ``/home/Scratch/factsheet_test``).

#. In the test data directory create a file ``invalid.fsg`` containing a
   short test string (e.g., "No one expects the Spanish Inquisition."

#. In the test data directory create a directory ``no_backup``.

#. In directory ``no_backup`` create a factsheet ``inquisition.fsg`` with
   name "Inquisition" and title "No one expects".

#. Set user permissions on directory ``no_backup`` to read-only,
   (e.g. ``chmod u-w no_backup``).

#. If you use a file browser, set browser to show hidden files.

Steps -- File Contents Not Factsheet
------------------------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **File ... > Open ...**.
   (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``invalid.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears.
   #. New window may cover first window.
   #. *Expect:* Window title is "OPEN ERROR".
   #. *Expect:* Factsheet name is "OPEN ERROR".
   #. *Expect:* Factsheet title is "Factsheet not opened."
   #. *Expect:* Factsheet summary includes the following, where
      local paths are replaced by ellipsis (...)::

        Factsheet not open! could not read file.
        Error source is UnpicklingError: could not find MARK.
        Path: .../invalid.fsg

#. **Step:** Check console for application "ERROR" log entries.

   a. *Expect:* Four "ERROR" entries::

        ERROR: Factsheet not open! could not read file.
        ERROR: Traceback (most recent call last):
        ERROR:    File ".../control_sheet.py", line nnn, in _model_from_path
            model = pickle.load(io_in)".
        ERROR: "_pickle.UnpicklingError: could not find MARK"

#. **Step:** Click *OPEN ERROR* window **close icon** |window-close|
   (window title far right).

   a. *Expect:* Window disappears.

#. **Step:** In *Unnamed* window, click window **close icon**
   |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Steps -- Save Failure
---------------------
1. **Step:** Start application with
   :doc:`../test_helpers/help_start_application`

   a. *Expect:* *Application* displays default factsheet.

#. **Step:** Select *Factsheet* **menu** item **File ... > Open ...**.
   (|menu| icon on far right of *Factsheet* identity line).

   a. *Expect:* Open dialog appears.

#. **Step:** Change to ``no_backup`` in test data directory.

   a. *Expect:* Open dialog shows directory contents.

#. **Step:** Select ``inquisition.fsg`` and click **Open button**.

   a. *Expect:* Open dialog disappears.
   #. *Expect:* Second window appears.
   #. New window may cover first window.
   #. *Expect:* Window title is "Inquisition".
   #. *Expect:* Factsheet name is "Inquisition".
   #. *Expect:* Factsheet title is "No one expects".
   #. *Expect:* Factsheet summary is "Edit factsheet description here.".

#. **Step:** In the ``Inquisition`` window, Edit (|edit| icon on left)
   factsheet title to "No one expects the Spanish Inquisition!"

   a. *Expect:* The text appears in field.

#. **Step:** Select *Factsheet* **menu** |menu| item **File ... > Save
   ...**.

   a. *Expect:* Error dialog appears with the following message, where
      local paths are replaced by ellipsis (...).::

        Factsheet not saved! could not make backujp.
        Error source is PermissionError: [Error 13] Permission denied:
        '.../inquisition.fsg' -> '.../inquisition.fsg~'

   #. *Expect:* The following message in the console log, where
      local paths, line numbers, and pathlib errors are replaced
      (..., nnn, and <pathlib error>, respectively).::

        ERROR: Factsheet not saved! could not make backup.
        ERROR: Traceback (most recent call last):
        ERROR:   File ".../control_sheet.py", line nnn, in _open_file_save
            io_out = self._path.open(mode='xb')
        ERROR:  <pathlib error>
        ERROR:  <pathlib error>
        ERROR: FileExistsError: [Errno 17] File exists: '.../inquisition.fsg'

   #. *Expect:* The following message in the console log, where
      local paths, line numbers, and pathlib errors are replaced
      (..., nnn, and <pathlib error>, respectively).::

        ERROR: During handling of the above exception, another exception
        occurred:
        ERROR: Traceback (most recent call last):
        ERROR:   File ".../control_sheet.py", line nnn, in _open_file_save
            self._path.replace(str(self._path) + '~')
        ERROR:  <pathlib error>
        ERROR: PermissionError: [Errno 13] Permission denied:
        '.../inquisition.fsg' -> '.../inquisition.fsg~'

   #. *Expect:* The following message in the console log, where
      local paths, line numbers, and pathlib errors are replaced
      (..., nnn, and <pathlib error>, respectively).::

        ERROR: The above exception was the direct cause of the following
        exception:
        ERROR: Traceback (most recent call last):
        ERROR:   File ".../view_sheet.py", line nnn, in save_sheet
            self._control.save(p_path_update)
        ERROR:   File ".../control_sheet.py", line nnn, in save
            with self._open_file_save() as io_out:
        ERROR:   File ".../control_sheet.py", line nnn, in _open_file_save
            raise BackupFileError from err_replace
        ERROR: factsheet.control.control_sheet.BackupFileError

#. **Step:** In error dialog, click **OK button**.

   a. *Expect:* Error dialog disappears.

#. **Step:** Click window **close icon** |window-close| (window title
   far right).

   a. *Expect:* *Data Loss Warning* dialog appears.

#. **Step:** Click **Discard button**

   a. *Expect:* Dialog disappears.
   #. *Expect:* `Inquisition` window disappears.

#. **Step:** Click window **close icon** |window-close|.

   a. *Expect:* Window disappears.
   #. *Expect:* *Application* closes.

Teardown
--------
1. Delete test data directory along with its contents.
#. Check console for exceptions, GTK errors, and warning messages. There
   should be none other than ERROR log entries identified in steps above.


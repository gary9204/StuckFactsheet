"""
Unit tests for classes that mediates factsheet-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_sheet`.

.. include:: /test/refs_include_pytest.txt
"""
import io
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.control.control_topic as CTOPIC
import factsheet.model.sheet as MSHEET
import factsheet.model.topic as MTOPIC


class PatchObserverControlSheet(CSHEET.ObserverControlSheet):
    """:class:`.ObserverControlSheet` subclass with stubs for methods."""

    def __init__(self, p_control):
        self._control = p_control
        self.called_erase = 0
        self.called_present = 0
        self.times = []

    def erase(self):
        self.called_erase = True

    def present(self, p_time):
        self.times.append(p_time)
        self.called_present = True


@pytest.fixture
def patch_g_control_app():
    """Pytest fixture with teardown: Reset :data:`.g_control_app`."""
    CSHEET.g_control_app = CSHEET.ControlApp()
    yield CSHEET.g_control_app
    CSHEET.g_control_app = CSHEET.ControlApp()


class TestControlApp:
    """Unit tests for :class:`.ControlApp`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = CSHEET.ControlApp()
        assert isinstance(target._roster_sheets, dict)
        assert not target._roster_sheets

    def test_close_factsheet(self, patch_g_control_app):
        """| Confirm tracking stops for given sheet with views removed.
        | Case: sheet tracked.

        :param patch_g_control_app: fixture :func:`patch_g_control_app`.
        """
        # Setup
        target = patch_g_control_app
        assert target is CSHEET.g_control_app
        N_CONTROLS = 4
        for _ in range(N_CONTROLS):
            control_sheet = target.open_factsheet(
                p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
            view = PatchObserverControlSheet(p_control=control_sheet)
            control_sheet.add_view(view)
        assert N_CONTROLS == len(target._roster_sheets)

        I_REMOVE = 1
        items = list(target._roster_sheets.items())
        (id_removed, control_removed) = items.pop(I_REMOVE)
        view_removed = next(iter(control_removed._roster_views.values()))
        # Test
        target.close_factsheet(p_control=control_removed)
        assert view_removed.called_erase
        assert not control_removed._roster_views
        assert id_removed not in target._roster_sheets.keys()
        assert len(items) == len(target._roster_sheets)
        for key, control in items:
            assert target._roster_sheets[key] is control

    def test_open_factsheet_none(self):
        """| Confirm factsheet return.
        | Case: path is None.
        """
        # Setup
        target = CSHEET.ControlApp()
        N_FACTSHEETS = 1
        # Test
        control_sheet = target.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        assert N_FACTSHEETS == len(target._roster_sheets)
        assert isinstance(control_sheet, CSHEET.ControlSheet)
        assert target._roster_sheets[control_sheet.tag] is control_sheet

    def test_open_factsheet_match(self, monkeypatch, tmp_path):
        """| Confirm factsheet return.
        | Case: path matches an existing file.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        class PatchPresent:
            def __init__(self):
                self.called = False

            def present_views(self, p_time):
                self.called = True
                self.time = p_time

        patch_present = PatchPresent()
        monkeypatch.setattr(
            CSHEET.ControlSheet, 'present_views', patch_present.present_views)
        target = CSHEET.ControlApp()
        N_FACTSHEETS = 5
        I_MATCH = 4
        PATH_BASE = Path(tmp_path)
        for i in range(N_FACTSHEETS):
            path = PATH_BASE / '/factsheet{}.fsg'.format(i)
            control = CSHEET.ControlSheet(p_path=path)
            target._roster_sheets[control.tag] = control
            if i == I_MATCH:
                path_match = path
        # Test
        control_sheet = target.open_factsheet(
            p_path=path_match, p_time=BUI.TIME_EVENT_CURRENT)
        assert control_sheet is None
        assert N_FACTSHEETS == len(target._roster_sheets)
        assert patch_present.called
        assert BUI.TIME_EVENT_CURRENT == patch_present.time

    def test_open_factsheet_no_match(self, tmp_path):
        """| Confirm factsheet return.
        | Case: path does not match an existing file.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        target = CSHEET.ControlApp()
        N_FACTSHEETS = 5
        PATH_BASE = Path(tmp_path)
        for i in range(N_FACTSHEETS):
            path = PATH_BASE / '/factsheet{}.fsg'.format(i)
            control = CSHEET.ControlSheet(p_path=path)
            target._roster_sheets[control.tag] = control
        PATH_DIFF = PATH_BASE / '/diff.fsg'
        # Test
        control_sheet = target.open_factsheet(
            p_path=PATH_DIFF, p_time=BUI.TIME_EVENT_CURRENT)
        assert isinstance(control_sheet, CSHEET.ControlSheet)
        assert PATH_DIFF == control_sheet._path
        assert N_FACTSHEETS + 1 == len(target._roster_sheets)
        assert control_sheet is target._roster_sheets[control_sheet.tag]

    @pytest.mark.skip
    def test_open_factsheet_except(self):
        """| Confirm factsheet open and return.
        | Case: file at path cannot be read.
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # # Test
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control

    @pytest.mark.skip
    def test_open_factsheet_multiple(self):
        """| Confirm factsheet open and return.
        | Case: file at path cannot be read.
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # # Test
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control

    def test_remove_factsheet(self):
        """| Confirm tracking stops for given sheet.
        | Case: sheet tracked.
        """
        # Setup
        target = CSHEET.ControlApp()
        N_CONTROLS = 4
        for _ in range(N_CONTROLS):
            _control_sheet = target.open_factsheet(
                p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        assert N_CONTROLS == len(target._roster_sheets)

        I_REMOVE = 1
        items = list(target._roster_sheets.items())
        (id_removed, control_removed) = items.pop(I_REMOVE)
        # Test
        target.remove_factsheet(p_control=control_removed)
        assert id_removed not in target._roster_sheets.keys()
        assert len(items) == len(target._roster_sheets)
        for key, control in items:
            assert target._roster_sheets[key] is control

    def test_remove_factsheet_warn(self, caplog):
        """| Confirm tracking stops for given sheet.
        | Case: sheet not tracked.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = CSHEET.ControlApp()
        N_CONTROLS = 4
        for _ in range(N_CONTROLS):
            _control_sheet = target.open_factsheet(
                p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        assert N_CONTROLS == len(target._roster_sheets)

        I_REMOVE = 1
        items = list(target._roster_sheets.items())
        (id_removed, control_removed) = items.pop(I_REMOVE)
        target._roster_sheets.pop(id_removed)

        N_LOGS = 1
        LAST = -1
        log_message = ('Missing control: 0x{:X} '
                       '(ControlApp.remove_factsheet)'.format(id_removed))
        # Test
        target.remove_factsheet(control_removed)
        assert id_removed not in target._roster_sheets
        assert len(items) == len(target._roster_sheets)
        for key, control in items:
            assert target._roster_sheets[key] is control
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname


class TestControlSheet:
    """Unit tests for :class:`~.ControlSheet`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Restore next line when stub removed.  See issue #253.
        # MODEL_DEFAULT = MSHEET.Sheet()
        # Test
        target = CSHEET.ControlSheet(p_path=None)
        assert target._path is None
        # Restore next line when stub removed.  See issue #253.
        # assert MODEL_DEFAULT == target._model
        model_name = target._model.name
        model_summary = target._model.summary
        model_title = target._model.title
        model_topics = target._model.outline_topics

        factory_display_name = target._factory_display_name
        assert isinstance(factory_display_name, CSHEET.FactoryDisplayName)
        assert factory_display_name._ui_model is model_name._ui_model
        factory_display_summary = target._factory_display_summary
        assert isinstance(
            factory_display_summary, CSHEET.FactoryDisplaySummary)
        assert factory_display_summary._ui_model is model_summary._ui_model
        factory_display_title = target._factory_display_title
        assert isinstance(factory_display_title, CSHEET.FactoryDisplayTitle)
        assert factory_display_title._ui_model is model_title._ui_model

        factory_editor_name = target._factory_editor_name
        assert isinstance(factory_editor_name, CSHEET.FactoryEditorName)
        assert factory_editor_name._ui_model is model_name._ui_model
        factory_editor_summary = target._factory_editor_summary
        assert isinstance(factory_editor_summary, CSHEET.FactoryEditorSummary)
        assert factory_editor_summary._ui_model is model_summary._ui_model
        factory_editor_title = target._factory_editor_title
        assert isinstance(factory_editor_title, CSHEET.FactoryEditorTitle)
        assert factory_editor_title._ui_model is model_title._ui_model

        factory_view_outline_topics = target._factory_view_topics
        assert (
            factory_view_outline_topics._ui_model is model_topics.ui_model)

        assert isinstance(target._roster_views, dict)
        assert not target._roster_views
        assert isinstance(target._roster_topics, dict)
        # Restore next line when stub removed.  See issue #253.
        # assert not target._roster_topics

    def test_add_view(self):
        """| Confirm tracking of given sheet view.
        | Case: view not tracked
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        # Test
        target.add_view(view)
        assert target._roster_views[id_view] is view

    def test_add_view_warn(self, caplog):
        """| Confirm tracking of given sheet view.
        | Case: duplicate view

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        log_message = ('Duplicate: sheet 0x{:X} add view 0x{:X}  '
                       '(ControlSheet.add_view)'.format(target.tag, id_view))
        N_LOGS = 1
        LAST = -1
        target.add_view(view)
        # Test
        target.add_view(view)
        assert target._roster_views[id_view] is view
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_clear(self, factory_control_sheet):
        """Confirm all controls and topics removed.

        :param factory_control_sheet: fixture :func:`factory_control_sheet`.
        """
        # Setup
        target = factory_control_sheet()
        # Test
        target.clear()
        assert not target._roster_topics
        with pytest.raises(StopIteration):
            _ = next(target._model.topics())

    def test_get_control_topic(self, factory_control_sheet):
        """| Confirm topic control returned
        | Case: topic at given line.

        :param factory_control_sheet: fixture :func:`factory_control_sheet`.
        """
        # Setup
        I_GET = 2
        target = factory_control_sheet()
        topics = list(target._model.topics())
        topic_get = topics[I_GET]
        control_get = target._roster_topics[topic_get.tag]
        for i, line_get in enumerate(target._model._topics.lines()):
            if i == I_GET:
                break
        # Test
        result = target.get_control_topic(line_get)
        assert result is control_get

    def test_get_control_topic_absent(
            self, monkeypatch, factory_control_sheet):
        """| Confirm topic control returned
        | Case: None at given line.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param factory_control_sheet: fixture :func:`factory_control_sheet`.
        """
        # Setup
        def patch_get_tag(self, p_line):
            del p_line
            NO_TAG = 0
            return NO_TAG

        monkeypatch.setattr(MSHEET.Sheet, 'get_tag', patch_get_tag)
        target = factory_control_sheet()
        line_get = next(target._model._topics.lines())
        # Test
        result = target.get_control_topic(line_get)
        assert result is None

    @pytest.mark.skip(reason='stub in place for issue #253.')
    @pytest.mark.parametrize('METHOD', [
        'insert_topic_after',
        'insert_topic_before',
        'insert_topic_child',
        ])
    def test_insert_topic(self, monkeypatch, METHOD):
        """Confirm each method adds control and relays request to model.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param METHOD: insert method under test.
        """
        # Setup
        class PatchInsert:
            def __init__(self):
                self.called = False
                self.topic = None
                self.line = 'Oops'
                self.result = 'Done'

            def insert(self, p_topic, p_line):
                self.called = True
                self.topic = p_topic
                self.line = p_line
                self.result = 'Done'
                return self.result

        patch_insert = PatchInsert()
        monkeypatch.setattr(MSHEET.Sheet, METHOD, patch_insert.insert)

        target = CSHEET.ControlSheet(p_path=None)
        target_method = getattr(target, METHOD)
        TOPIC = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        # Test
        result = target_method(TOPIC, None)
        control_new = target._roster_topics[TOPIC.tag]
        assert control_new._model is TOPIC
        assert patch_insert.called
        assert patch_insert.topic is TOPIC
        assert patch_insert.line is None
        assert result is patch_insert.result

    def test_insert_topic_control(self):
        """Confirm topic added to roster."""
        # Setup
        TOPIC = MTOPIC.Topic(p_name='', p_summary='', p_title='')
        CONTROL = CTOPIC.ControlTopic(p_model=TOPIC)
        target = CSHEET.ControlSheet(p_path=None)
        # Test
        target._insert_topic_control(p_control=CONTROL)
        assert target._roster_topics[TOPIC.tag] is CONTROL

    @pytest.mark.parametrize('METHOD, MODEL_IS_STALE', [
        ('is_fresh', False),
        ('is_fresh', True),
        ('is_stale', False),
        ('is_stale', True),
        ])
    def test_is_fresh_stale(self, METHOD, MODEL_IS_STALE):
        """Confirm model and control report same state of change.

        :param METHOD: method to test, which is ``is_fresh`` or ``is_stale``.
        :param MODEL_IS_STALE: state of change in model.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        method_model = getattr(target._model, METHOD)
        method_target = getattr(target, METHOD)
        target._model._stale = MODEL_IS_STALE
        # Test
        assert method_model() == method_target()

    def test_model_from_error(self, caplog):
        """Confirm return of error sheet.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        MESSAGE = 'One day this will all be yours!'
        TEXT_ERROR = 'What, the curtains?'
        ERROR = CSHEET.OpenFileError(TEXT_ERROR)
        target = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        I_MESSAGE = 0
        I_ERROR = -1
        SUMMARY = '\n'.join([
            MESSAGE,
            'Error source is OpenFileError: What, the curtains?',
            'Path: None',
            ])
        # Test
        model = target._model_from_error(p_err=ERROR, p_message=MESSAGE)
        assert caplog.records
        log_message = caplog.records[I_MESSAGE]
        assert 'ERROR' == log_message.levelname
        assert MESSAGE == log_message.message
        log_error = caplog.records[I_ERROR]
        assert 'ERROR' == log_error.levelname
        assert log_error.message.rstrip('\n').endswith(
            ': '.join([type(ERROR).__name__, TEXT_ERROR]))
        assert 'OPEN ERROR' == model.name.text
        assert SUMMARY == model.summary.text
        assert 'Factsheet not opened.' == model.title.text

    def test_model_from_path(self, tmp_path):
        """| Confirm model creation.
        | Case: file at path location constains factsheet model.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target = CSHEET.ControlSheet(p_path=None)
        target._model.set_stale()
        target.save(p_path=PATH)
        assert PATH.exists()
        # Test
        model = target._model_from_path(p_path=PATH)
        assert model is not None
        assert model == target._model
        assert target._model.is_fresh()

    def test_model_from_path_empty(self, tmp_path):
        """| Confirm model creation.
        | Case: no file at path location.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target = CSHEET.ControlSheet(p_path=None)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=PATH)
        assert model_default == model

    @pytest.mark.parametrize('ERROR, MESSAGE', [
        ('open', 'Factsheet not open! could not open file.'),
        ('pickle', 'Factsheet not open! could not read file.'),
        ])
    def test_model_from_path_except(
            self, ERROR, MESSAGE, monkeypatch, tmp_path):
        """| Confirm model creation.
        | Case: file at path location cannot be opened or loaded.

        :param ERROR: identifies where to raise exception.
        :param MESSAGE: first line of summary in error model.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        BYTES = b'Something completely different'
        with PATH.open(mode='wb') as io_out:
            io_out.write(BYTES)
        assert PATH.exists()

        def patch_except(*_args, **_kwargs): raise Exception(ERROR)

        if 'open' == ERROR:
            monkeypatch.setattr(Path, 'open', patch_except)
        elif 'pickle' == ERROR:
            monkeypatch.setattr(pickle, 'load', patch_except)
        else:
            assert False
        target = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        FIRST = 0
        # Test
        model = target._model_from_path(PATH)
        assert model is not None
        assert MESSAGE == model.summary.text.splitlines()[FIRST]

    def test_model_from_path_none(self):
        """| Confirm model creation.
        | Case: no path.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=None)
        assert model_default == model

    def test_open_file_save(self, tmp_path):
        """| Confirm file open.
        | Case: file does not exist.

        :param tmp_path: built-in fixture `Pytest tmp_path`_
        """
        # Setup
        MODE = 'xb'
        target = CSHEET.ControlSheet(p_path=None)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target._path = PATH
        # Test
        with target._open_file_save() as io_out:
            assert isinstance(io_out, io.BufferedWriter)
            assert MODE == io_out.mode

    @pytest.mark.parametrize('PATCH_EXC, REPLACE, RAISE, I_EXC', [
        ((ValueError('Error open'), Exception('Oops!'), Exception('Replace')),
            False, pytest.raises(CSHEET.OpenFileError), 0),
        ((FileExistsError('Oops!'), Exception('Error reopen'),
            Exception('Replace')), False,
            pytest.raises(CSHEET.OpenFileError), 1),
        ((FileExistsError('Oops!'), Exception('Oops'), Exception('Replace')),
            True, pytest.raises(CSHEET.BackupFileError), 2),
        ])
    def test_open_file_save_except(
            self, PATCH_EXC, REPLACE, RAISE, I_EXC, monkeypatch, tmp_path):
        """| Confirm file open.
        | Case: open raises unanticipated exception.

        :param PATCH_EXE: exceptions to raise in patched methods.
        :param REPLACE: when True, raise exception in`replace` patch.
        :param RAISE: expected exception.
        :param I_EXC: index in PATCH_EXE of expected exception cause.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        I_EXC_OPEN = 0
        I_EXC_REOPEN = 1
        I_EXC_REPLACE = 2

        class PatchPath:
            def __init__(self): self.called = 0

            def open(self, **_kwa):
                if I_EXC_OPEN == self.called:
                    self.called += 1
                    raise PATCH_EXC[I_EXC_OPEN]
                elif I_EXC_REOPEN == self.called:
                    self.called += 1
                    raise PATCH_EXC[I_EXC_REOPEN]
                else:
                    self.called += 1
                    return None

            def replace(self, _target):
                if REPLACE:
                    raise PATCH_EXC[I_EXC_REPLACE]
                return None

        patch_path = PatchPath()

        monkeypatch.setattr(Path, 'open', patch_path.open)
        monkeypatch.setattr(Path, 'replace', patch_path.replace)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target = CSHEET.ControlSheet(p_path=None)
        target._path = PATH
        # Test
        with RAISE as exc_info:
            with target._open_file_save() as _io_out:
                pass
        cause = exc_info.value.__cause__
        assert isinstance(cause, type(PATCH_EXC[I_EXC]))
        assert PATCH_EXC[I_EXC].args == cause.args
        assert str(PATCH_EXC[I_EXC]) == str(cause)

    def test_open_file_save_exists(self, tmp_path):
        """| Confirm file open.
        | Case: file exists.

        :param tmp_path: built-in fixture `Pytest tmp_path`_
        """
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TEXT = 'What, the curtains?'
        with PATH.open(mode='w') as io_out:
            io_out.write(TEXT)
        MODE = 'xb'
        target = CSHEET.ControlSheet(p_path=None)
        target._path = PATH
        BACKUP = PATH.with_name(PATH.name + '~')
        assert not BACKUP.exists()
        # Test
        with target._open_file_save() as io_out:
            assert isinstance(io_out, io.BufferedWriter)
            assert MODE == io_out.mode
            assert BACKUP.exists()
            with BACKUP.open(mode='r') as io_in:
                backup_text = io_in.read()
            assert TEXT == backup_text

    def test_open_file_save_no_path(self):
        """| Confirm file open.
        | Case: path is None.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        MESSAGE = 'Save: cannot open path None.'
        # Test
        with pytest.raises(CSHEET.NoFileError, match=MESSAGE):
            _io = target._open_file_save()

    def test_present_views(self):
        """Confirm sheet control notifies all its views."""
        # Setup
        class PatchObserver(CSHEET.ObserverControlSheet):
            def __init__(self, _control):
                self.called_present = False
                self.time = None

            def erase(self): pass

            def present(self, p_time):
                self.called_present = True
                self.time = p_time

        target = CSHEET.ControlSheet(p_path=None)
        N_VIEWS = 5
        for _ in range(N_VIEWS):
            view = PatchObserver(target)
            target.add_view(p_view=view)
        assert N_VIEWS == len(target._roster_views)
        # Test
        target.present_views(BUI.TIME_EVENT_CURRENT)
        for view in target._roster_views.values():
            assert view.called_present
            assert BUI.TIME_EVENT_CURRENT == view.time

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        # ('_model', 'model'),
        ('_factory_display_name', 'new_display_name'),
        ('_factory_editor_name', 'new_editor_name'),
        ('_factory_display_summary', 'new_display_summary'),
        ('_factory_editor_summary', 'new_editor_summary'),
        ('_factory_display_title', 'new_display_title'),
        ('_factory_editor_title', 'new_editor_title'),
        ('_factory_view_topics', 'new_view_topics'),
        ('_path', 'path'),
        ])
    def test_property(self, tmp_path, NAME_ATTR, NAME_PROP):
        """Confirm model property is get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete

        :param tmp_path: built-in fixture `Pytest tmp_path`_
        :param NAME_ATTR: name of attribute.
        :param NAME_PROP: name of property.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        PATH = Path(tmp_path / 'path_factsheet.fsg')
        target._path = PATH
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(CSHEET.ControlSheet, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: get
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no set
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.parametrize('NAME, ESCAPED', [
        ('<b>Parrot</b> Sketch', '<b>Parrot</b> Sketch'),
        ('<b>Parrot<b Sketch', '&lt;b&gt;Parrot&lt;b Sketch'),
        ])
    def test_property_name(self, NAME, ESCAPED):
        """| Confirm model name property is get-only without markup errors.
        | Case: name does not contain markup errors

        #. Case: get
        #. Case: no set
        #. Case: no delete

        :param NAME: name of factsheet.
        :param ESCAPED: name of factsheet with markup errors escaped.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        target_prop = getattr(CSHEET.ControlSheet, 'name')
        model_name = target._model.name
        model_name._set_persist(NAME)
        # Test: get
        assert target_prop.fget is not None
        assert ESCAPED == target.name
        # Test: no set
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_property_tag(self):
        """Confirm value and access limits of tag property."""
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        target_prop = getattr(CSHEET.ControlSheet, 'tag')
        # Test
        assert target_prop.fget is not None
        assert target._model.tag == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_remove_all_views(self, monkeypatch):
        """Confirm tracking stops for all sheet views.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchControlApp:
            def __init__(self):
                self.called = False
                self.control_sheet = None

            def remove_factsheet(self, p_control):
                self.called = True
                self.control_sheet = p_control

        patch = PatchControlApp()
        monkeypatch.setattr(
            CSHEET.ControlApp, 'remove_factsheet', patch.remove_factsheet)
        target = CSHEET.ControlSheet(p_path=None)
        N_VIEWS = 5
        for _ in range(N_VIEWS):
            view = PatchObserverControlSheet(p_control=target)
            target.add_view(p_view=view)
        # Test
        target.remove_all_views()
        assert not target._roster_views
        assert patch.called
        assert target is patch.control_sheet

    @pytest.mark.parametrize('I_REMOVE, I_REMOVE_END', [
        (0, 3),
        (3, 4),
        (1, 3),
        ])
    def test_remove_topic(self, factory_control_sheet, I_REMOVE, I_REMOVE_END):
        """Confirm method removes controls and relays request to model.

        :param factory_control_sheet: fixture :func:`factory_control_sheet`.
        :param I_REMOVE: index in list of topics fo topic to remove.
        :param I_REMOVE_END: index of first topic after removed topics.
        """
        # Setup
        target = factory_control_sheet()
        tags_before = [t.tag for t in target._model.topics()]
        for i, line_remove in enumerate(target._model._topics.lines()):
            if i == I_REMOVE:
                break
        tags_after = set(tags_before[:I_REMOVE] + tags_before[I_REMOVE_END:])
        # Test
        target.remove_topic(line_remove)
        tags_control = target._roster_topics.keys()
        assert tags_control == tags_after
        tags_model = {topic.tag for topic in target._model.topics()}
        assert tags_model == tags_after

    def test_remove_topic_none(self, factory_control_sheet):
        """Confirm topics and controls unchanged when line is None.

        :param factory_control_sheet: fixture :func:`factory_control_sheet`.
        """
        # Setup
        target = factory_control_sheet()
        tags_before = {t.tag for t in target._model.topics()}
        # Test
        target.remove_topic(None)
        tags_control = target._roster_topics.keys()
        assert tags_control == tags_before
        tags_model = {topic.tag for topic in target._model.topics()}
        assert tags_model == tags_before

    def test_remove_view_is_safe_fresh(self):
        """| Confirm return shows safe to erase.
        | Case: no unsaved changes
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        target._model.set_fresh()
        # Test
        assert target.remove_view_is_safe()

    def test_remove_view_is_safe_multi(self):
        """| Confirm return shows safe to erase.
        | Case: multiple windows
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        view_extra = PatchObserverControlSheet(p_control=target)
        target.add_view(view_extra)
        target._model.set_stale()
        # Test
        assert target.remove_view_is_safe()

    def test_remove_view_is_safe_unsafe(self):
        """Confirm return shows  not safe to erase."""
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        target._model.set_stale()
        # Test
        assert not target.remove_view_is_safe()

    def test_remove_view_multi(self):
        """| Confirm tracking stops for given sheet view.
        | Case: multiple views tracked.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        target.add_view(view)
        view_extra = PatchObserverControlSheet(p_control=target)
        target.add_view(view_extra)
        # Test
        target.remove_view(view)
        assert id_view not in target._roster_views

    def test_remove_view_single(self, monkeypatch):
        """| Confirm tracking stops for given sheet view.
        | Case: single view tracked.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchControlApp:
            def __init__(self):
                self.called = False
                self.control_sheet = None

            def remove_factsheet(self, p_control):
                self.called = True
                self.control_sheet = p_control

        patch = PatchControlApp()
        monkeypatch.setattr(
            CSHEET.ControlApp, 'remove_factsheet', patch.remove_factsheet)
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        target.add_view(view)
        # Test
        target.remove_view(view)
        assert id_view not in target._roster_views
        assert patch.called
        assert target is patch.control_sheet

    def test_remove_view_warn(self, caplog):
        """| Confirm tracking stops for given sheet view.
        | Case: view not tracked.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        N_LOGS = 1
        LAST = -1
        log_message = ('Missing: sheet 0x{:X} remove view 0x{:X}  '
                       '(ControlSheet.remove_view)'
                       ''.format(target.tag, id_view))
        # Test
        target.remove_view(view)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    def test_save(self, tmp_path):
        """| Confirm write to file.
        | Case: file does not exist.

        :param tmp_path: built-in fixture `Pytest tmp_path`_
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target._path = PATH
        target._model.set_stale()
        assert not PATH.exists()
        # Test
        target.save()
        assert target._model.is_fresh()
        assert PATH.exists()
        with PATH.open(mode='rb') as io_in:
            model_disk = pickle.load(io_in)
        assert model_disk is not None
        assert target._model == model_disk

    def test_save_except(self, monkeypatch, tmp_path):
        """| Confirm write to file.
        | Case: dump to file fails.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_
        """
        # Setup
        ERROR = 'Random Error'

        def patch_dump(_object, _file):
            raise pickle.PicklingError(ERROR)

        monkeypatch.setattr(pickle, 'dump', patch_dump)
        target = CSHEET.ControlSheet(p_path=None)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target._path = PATH
        target._model.set_stale()
        assert not PATH.exists()
        # Test
        with pytest.raises(CSHEET.DumpFileError) as exc_info:
            target.save()
        cause = exc_info.value.__cause__
        assert isinstance(cause, pickle.PicklingError)
        assert (ERROR,) == cause.args
        assert ERROR == str(cause)

    def test_save_new_path(self, tmp_path):
        """| Confirm write to file.
        | Case: replace path to save file.

        :param tmp_path: built-in fixture `Pytest tmp_path`_
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        target._model.set_stale()
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        assert not PATH.exists()
        # Test
        target.save(p_path=PATH)
        assert PATH is target.path
        assert target._model.is_fresh()
        assert PATH.exists()


class TestModule:
    """Unit tests for module-level components of :mod:`.control_sheet`."""

    @pytest.mark.parametrize('TARGET, SUPER', [
        (CSHEET.FactsheetError, Exception),
        (CSHEET.BackupFileError, CSHEET.FactsheetError),
        (CSHEET.DumpFileError, CSHEET.FactsheetError),
        (CSHEET.NoFileError, CSHEET.FactsheetError),
        (CSHEET.OpenFileError, CSHEET.FactsheetError),
        ])
    def test_exceptions(self, TARGET, SUPER):
        """Confirm presence of exceptions.

        :param TARGET: exception under test.
        :param SUPER: superclass of target exception.
        """
        # Setup
        # Test
        assert issubclass(TARGET, SUPER)

    def test_globals(self):
        """Confirm global definitions."""
        # Setup
        # Test
        assert isinstance(CSHEET.g_control_app, CSHEET.ControlApp)

    def test_id_view_sheet(self):
        """Confirm ID returned."""
        # Setup
        control = CSHEET.ControlSheet()
        view_sheet = PatchObserverControlSheet(p_control=control)
        # Test
        assert id(view_sheet) == CSHEET.id_view_sheet(p_view_sheet=view_sheet)

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (CSHEET.DisplayName, BUI.DisplayTextMarkup),
        (CSHEET.DisplaySummary, BUI.DisplayTextStyled),
        (CSHEET.DisplayTitle, BUI.DisplayTextMarkup),
        (CSHEET.EditorName, BUI.EditorTextMarkup),
        (CSHEET.EditorSummary, BUI.EditorTextStyled),
        (CSHEET.EditorTitle, BUI.EditorTextMarkup),
        (CSHEET.FactoryDisplayName, BUI.FactoryDisplayTextMarkup),
        (CSHEET.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (CSHEET.FactoryDisplayTitle, BUI.FactoryDisplayTextMarkup),
        (CSHEET.FactoryEditorName, BUI.FactoryEditorTextMarkup),
        (CSHEET.FactoryEditorSummary, BUI.FactoryEditorTextStyled),
        (CSHEET.FactoryEditorTitle, BUI.FactoryEditorTextMarkup),
        (CSHEET.FactoryViewTopics.__dict__['__origin__'],
            BUI.FactoryViewOutline),
        (CSHEET.FactoryViewTopics.__dict__['__args__'],
            (BUI.ViewOutline, MTOPIC.Topic)),
        (CSHEET.IdViewSheet.__qualname__, 'NewType.<locals>.new_type'),
        (CSHEET.IdViewSheet.__dict__['__supertype__'], int),
        (CSHEET.ViewTopics, BUI.ViewOutline),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestObserverControlSheet:
    """Unit tests for :class:`.ObserverControlSheet`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (CSHEET.ObserverControlSheet, 'erase'),
        (CSHEET.ObserverControlSheet, 'present'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: class under test.
        :param NAME_METHOD: name of method under test.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

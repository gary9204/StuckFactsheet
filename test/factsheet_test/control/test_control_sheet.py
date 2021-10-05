"""
Unit tests for class that mediates factsheet-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_sheet`.

Unit tests for class that tracks and maintains pool of active
factsheets.  See :mod:`.pool`.

.. include:: /test/refs_include_pytest.txt
"""
import io
# import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]
# import typing

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.model.sheet as MSHEET
# from factsheet.control import control_topic as CTOPIC
# from factsheet.control import pool as CPOOL
# from factsheet.model import topic as MTOPIC


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


@pytest.fixture  # (autouse=True)
def reset_g_test():
    CSHEET.g_test = ['item 3']


@pytest.mark.skip(reason='saving for additional experiments.')
class TestResetGTest:
    """Experiment to determine behavior of global variables."""

    def test_g_test_set(self):
        # Setup
        # Test
        print('Set p_test pre:  {}'.format(CSHEET.g_test))
        CSHEET.g_test.append('item 2')
        print('Set p_test_post: {}'.format(CSHEET.g_test))
        assert False

    def test_g_test_get(self):
        # Setup
        # Test
        print('Get p_test: {}'.format(CSHEET.g_test))
        assert False


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
        | Case: sheet tracked
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
        | Case: path is None
        """
        # Setup
        target = CSHEET.ControlApp()
        N_FACTSHEETS = 1
        # Test
        control_sheet = target.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        assert N_FACTSHEETS == len(target._roster_sheets)
        assert isinstance(control_sheet, CSHEET.ControlSheet)
        id_control_sheet = CSHEET.id_factsheet(control_sheet)
        assert target._roster_sheets[id_control_sheet] is control_sheet

    def test_open_factsheet_match(self, monkeypatch, tmp_path):
        """| Confirm factsheet return.
        | Case: path matches an existing file
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
            target._roster_sheets[id(control)] = control
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
        | Case: path does not match an existing file
        """
        # Setup
        target = CSHEET.ControlApp()
        N_FACTSHEETS = 5
        PATH_BASE = Path(tmp_path)
        for i in range(N_FACTSHEETS):
            path = PATH_BASE / '/factsheet{}.fsg'.format(i)
            control = CSHEET.ControlSheet(p_path=path)
            target._roster_sheets[id(control)] = control
        PATH_DIFF = PATH_BASE / '/diff.fsg'
        # Test
        control_sheet = target.open_factsheet(
            p_path=PATH_DIFF, p_time=BUI.TIME_EVENT_CURRENT)
        assert isinstance(control_sheet, CSHEET.ControlSheet)
        assert PATH_DIFF == control_sheet._path
        assert N_FACTSHEETS + 1 == len(target._roster_sheets)
        assert control_sheet is target._roster_sheets[id(control_sheet)]

    @pytest.mark.skip
    def test_open_factsheet_except(self):
        """| Confirm factsheet open and return.
        | Case: file at path cannot be read
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
        | Case: file at path cannot be read
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
        | Case: sheet tracked
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
        | Case: sheet not tracked
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
        MODEL_DEFAULT = MSHEET.Sheet()
        # Test
        target = CSHEET.ControlSheet(p_path=None)
        assert target._path is None
        assert MODEL_DEFAULT == target._model

        model_name = target._model.name
        factory_display_name = target._factory_display_name
        assert isinstance(factory_display_name, MSHEET.FactoryDisplayName)
        assert factory_display_name._ui_model is model_name._ui_model
        factory_editor_name = target._factory_editor_name
        assert isinstance(factory_editor_name, MSHEET.FactoryEditorName)
        assert factory_editor_name._ui_model is model_name._ui_model

        model_summary = target._model.summary
        factory_display_summary = target._factory_display_summary
        assert isinstance(
            factory_display_summary, MSHEET.FactoryDisplaySummary)
        assert factory_display_summary._ui_model is model_summary._ui_model
        factory_editor_summary = target._factory_editor_summary
        assert isinstance(factory_editor_summary, MSHEET.FactoryEditorSummary)
        assert factory_editor_summary._ui_model is model_summary._ui_model

        model_title = target._model.title
        factory_display_title = target._factory_display_title
        assert isinstance(factory_display_title, MSHEET.FactoryDisplayTitle)
        assert factory_display_title._ui_model is model_title._ui_model
        factory_editor_title = target._factory_editor_title
        assert isinstance(factory_editor_title, MSHEET.FactoryEditorTitle)
        assert factory_editor_title._ui_model is model_title._ui_model

        assert isinstance(target._roster_views, dict)
        assert not target._roster_views
        # assert not target._controls_topic

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
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        log_message = ('Duplicate: sheet 0x{:X} add view 0x{:X}  '
                       '(ControlSheet.add_view)'
                       ''.format(id(target), id_view))
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
        | Case: multiple views tracked
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
        | Case: single view tracked

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
        | Case: view not tracked

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
                       ''.format(id(target), id_view))
        # Test
        target.remove_view(view)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    @pytest.mark.skip
    def test_attach_view_topics(self, monkeypatch):
        """Confirm topics outline view addition."""
        # # Setup
        # class PatchModel:
        #     def __init__(self):
        #         self.called_attach_page = False
        #
        #     def attach_view_topics(self, _view):
        #         self.called_attach_view_topics = True
        #
        # patch_model = PatchModel()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'attach_view_topics',
        #     patch_model.attach_view_topics)
        #
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        # # Test
        # target.attach_view_topics(None)
        # assert patch_model.called_attach_view_topics

    @pytest.mark.skip
    def test_detach_view_topics(self, monkeypatch):
        """Confirm topics outline view removal."""
        # # Setup
        # class PatchModel:
        #     def __init__(self):
        #         self.called_detach_page = False
        #
        #     def detach_view_topics(self, _view):
        #         self.called_detach_view_topics = True
        #
        # patch_model = PatchModel()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'detach_view_topics',
        #     patch_model.detach_view_topics)
        #
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        # # Test
        # target.detach_view_topics(None)
        # assert patch_model.called_detach_view_topics

    @pytest.mark.skip
    def test_clear(self, monkeypatch):
        """Confirm method passes request to model."""
        # # Setup
        # class PatchClear:
        #     def __init__(self): self.called = False
        #
        #     def clear(self): self.called = True
        #
        # patch_clear = PatchClear()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'clear', patch_clear.clear)
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        # # Test
        # target.clear()
        # assert patch_clear.called

    @pytest.mark.skip
    def test_extract_topic(self, monkeypatch):
        """Confirm method passes request to model."""
        # # Setup
        # class PatchExtract:
        #     def __init__(self): self.called = False
        #
        #     def extract_topic(self, _index): self.called = True
        #
        # patch_extract = PatchExtract()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'extract_topic', patch_extract.extract_topic)
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        # # Test
        # _ = target.extract_topic(None)
        # assert patch_extract.called

    @pytest.mark.skip
    def test_get_control_topic(self):
        """| Confirm
        | Case: topic in model
        """
        # # Setup
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        #
        # N_TOPICS = 3
        # topics = [MTOPIC.Topic(p_name='Topic {}'.format(i))
        #           for i in range(N_TOPICS)]
        # for topic in topics:
        #     control_topic = CTOPIC.ControlTopic(p_model=topic)
        #     key_topic = topic.tag
        #     target._controls_topic[key_topic] = control_topic
        #
        # N_EXPECT = 1
        # topic_expect = topics[N_EXPECT]
        # id_expect = topic_expect.tag
        # # Test
        # control_actual = target.get_control_topic(topic_expect)
        # assert control_actual is target._controls_topic[id_expect]

    @pytest.mark.skip
    def test_get_control_topic_absent(self):
        """| Confirm
        | Case: topic in model
        """
        # # Setup
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        #
        # N_TOPICS = 3
        # topics = [MTOPIC.Topic(p_name='Topic {}'.format(i))
        #           for i in range(N_TOPICS)]
        # for topic in topics:
        #     control_topic = CTOPIC.ControlTopic(p_model=topic)
        #     key_topic = topic.tag
        #     target._controls_topic[key_topic] = control_topic
        #
        # topic_absent = MTOPIC.Topic(p_title="Spanish Inquisition")
        # # Test
        # control_actual = target.get_control_topic(topic_absent)
        # assert control_actual is None

    @pytest.mark.skip
    @pytest.mark.parametrize('NAME_METHOD', [
        # 'insert_topic_after',
        # 'insert_topic_before',
        # 'insert_topic_child',
        ])
    def test_insert_topic(self, monkeypatch, NAME_METHOD):
        """Confirm each insert method passes request to model."""
        # # Setup
        # class PatchInsert:
        #     def __init__(self): self.called = False
        #
        #     def insert_topic(self, _item, index):
        #         self.called = True
        #         return index
        #
        # patch_insert = PatchInsert()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, NAME_METHOD, patch_insert.insert_topic)
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet.new(sheets_active)
        # method = getattr(target, NAME_METHOD)
        #
        # TITLE = 'Something completely different.'
        # TOPIC = MTOPIC.Topic(pm_title=TITLE)
        # id_topic = TOPIC.tag
        # I_TOPIC = 'Parrot'
        # # Test
        # index_new, control_new = method(TOPIC, I_TOPIC)
        # assert patch_insert.called
        # assert index_new is I_TOPIC
        # assert isinstance(control_new, CTOPIC.ControlTopic)
        # assert target._controls_topic[id_topic] is control_new

    @pytest.mark.parametrize('METHOD, MODEL_IS_STALE', [
        ('is_fresh', False),
        ('is_fresh', True),
        ('is_stale', False),
        ('is_stale', True),
        ])
    def test_is_fresh_stale(self, METHOD, MODEL_IS_STALE):
        """Confirm model and control report same state of change.

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments.
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

    @pytest.mark.skip(reason='being replaced by model pass through')
    @pytest.mark.parametrize('NAME_METHOD, NAME_CHECK, CLASS', [
        # ('new_view_name_active', 'get_buffer', MSHEET.ViewNameSheetActive),
        # ('new_view_name_passive', 'get_label', MSHEET.ViewNameSheetPassive),
        # ('new_view_summary_active', 'get_buffer',
        #     MSHEET.ViewSummarySheetActive),
        # ('new_view_summary_passive', 'get_buffer',
        #     MSHEET.ViewSummarySheetPassive),
        # ('new_view_title_active', 'get_buffer', MSHEET.ViewTitleSheetActive),
        # ('new_view_title_passive', 'get_label', MSHEET.ViewTitleSheetPassive),
        ])
    def test_new_view(self, new_id_args, NAME_METHOD, NAME_CHECK, CLASS):
        """Confirm control relays requests for new views.

        :param new_id_args: fixture: factory for stock identity
            keyword arguments
        :param NAME_METHOD: name of method under test
        :param NAME_CHECK: name of method used to check view
        :param CLASS: expected view class
        """
        # Setup
        KWARGS = new_id_args()
        model = MSHEET.Sheet(**KWARGS)
        model_method = getattr(model, NAME_METHOD)
        model_view = model_method()
        model_check = getattr(model_view, NAME_CHECK)
        target = CSHEET.ControlSheet(p_model=model, p_path=None)
        target_method = getattr(target, NAME_METHOD)
        # Test
        target_view = target_method()
        assert isinstance(target_view, CLASS)
        target_check = getattr(target_view, NAME_CHECK)
        assert model_check() == target_check()
        # Teardown
        target_view.destroy()
        model_view.destroy()

    @pytest.mark.skip(reason='#229')
    def test_model_from_error(self, caplog):
        """Confirm return of error sheet."""
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
        assert 'OPEN ERROR' == model.name
        assert SUMMARY == model.summary
        assert 'Factsheet not opened.' == model.title

    def test_model_from_path(self, tmp_path):
        """| Confirm model creation.
        | Case: file at path location constains factsheet model
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
        | Case: no file at path location
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target = CSHEET.ControlSheet(p_path=None)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=PATH)
        assert model_default == model

    @pytest.mark.skip(reason='#229')
    @pytest.mark.parametrize('ERROR, MESSAGE', [
        ('open', 'Factsheet not open! could not open file.'),
        ('pickle', 'Factsheet not open! could not read file.'),
        ])
    def test_model_from_path_except(
            self, ERROR, MESSAGE, monkeypatch, tmp_path):
        """| Confirm model creation.
        | Case: file at path location cannot be opened or loaded

        :param ERROR: identifies where to raise exception.
        :param MESSAGE: first line of summary in error model.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param tmp_path: built-in fixture `Pytest tmp_path`_
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
        assert MESSAGE == model.summary.splitlines()[FIRST]

    def test_model_from_path_none(self):
        """| Confirm model creation.
        | Case: no path
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=None)
        assert model_default == model

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
        ('_model', 'model'),
        ('_path', 'path'),
        ])
    def test_property(self, tmp_path, NAME_ATTR, NAME_PROP):
        """Confirm model property is get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete

        :param NAME_ATTR: name of attribute.
        :param NAME_PROP: name of property.
        :param tmp_path: built-in fixture `Pytest tmp_path`_
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

    def test_save(self, tmp_path):
        """| Confirm write to file.
        | Case: file does not exist.
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target._path = PATH
        target.model.set_stale()
        assert not PATH.exists()
        # Test
        target.save()
        assert target.model.is_fresh()
        assert PATH.exists()
        with PATH.open(mode='rb') as io_in:
            model_disk = pickle.load(io_in)
        assert model_disk is not None
        assert target.model == model_disk

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
        target.model.set_stale()
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
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        target.model.set_stale()
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        assert not PATH.exists()
        # Test
        target.save(p_path=PATH)
        assert PATH is target.path
        assert target.model.is_fresh()
        assert PATH.exists()

    def test_open_file_save(self, tmp_path):
        """| Confirm file open.
        | Case: file does not exist.
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


class TestGlobal:
    """Unit tests for :data:`.g_roster_factsheets`."""

    def test_define(self):
        """Confirm global definition."""
        # Setup
        # Test
        assert isinstance(CSHEET.g_control_app, CSHEET.ControlApp)


class TestIdFactsheet:
    """unit tests for :func:`.id_view_sheet`."""

    def test_id_factsheetsheet(self):
        """Confirm id returned."""
        # Setup
        control_sheet = CSHEET.ControlSheet()
        # Test
        assert id(control_sheet) == CSHEET.id_factsheet(control_sheet)


class TestIdViewSheet:
    """unit tests for :func:`.id_view_sheet`."""

    def test_id_view_sheet(self):
        """Confirm id returned."""
        # Setup
        control = CSHEET.ControlSheet()
        view_sheet = PatchObserverControlSheet(p_control=control)
        # Test
        assert id(view_sheet) == CSHEET.id_view_sheet(p_view_sheet=view_sheet)


class TestTypes:
    """Unit tests for type hint definitions in :mod:`.control_sheet`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (CSHEET.IdFactsheet.__qualname__, 'NewType.<locals>.new_type'),
        (CSHEET.IdFactsheet.__dict__['__supertype__'], int),
        (CSHEET.IdViewSheet.__qualname__, 'NewType.<locals>.new_type'),
        (CSHEET.IdViewSheet.__dict__['__supertype__'], int),
        # (type(MIDCORE.ViewTitlePassive), typing.TypeVar),
        # (MIDCORE.ViewTitlePassive.__constraints__, (
        #     BUI.ViewTextTagged, BUI.ViewTextDisplay)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE


class TestExceptions:
    """Unit tests for exceptions defined in :mod:`.control_sheet`."""

    @pytest.mark.parametrize('TARGET, SUPER', [
        (CSHEET.ExceptionSheet, Exception),
        (CSHEET.BackupFileError, CSHEET.ExceptionSheet),
        (CSHEET.DumpFileError, CSHEET.ExceptionSheet),
        # (CSHEET.LoadFileError, CSHEET.ExceptionSheet),
        (CSHEET.NoFileError, CSHEET.ExceptionSheet),
        (CSHEET.OpenFileError, CSHEET.ExceptionSheet),
        ])
    def test_exceptions(self, TARGET, SUPER):
        """Confirm presence of exceptions."""
        # Setup
        # Test
        assert issubclass(TARGET, SUPER)


class TestObserverControlSheet:
    """Unit tests for :class:`ObserverControlSheet`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (CSHEET.ObserverControlSheet, 'erase'),
        (CSHEET.ObserverControlSheet, 'present'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

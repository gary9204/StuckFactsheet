"""
Unit tests for class that mediates factsheet-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_sheet`.

Unit tests for class that tracks and maintains pool of active
factsheets.  See :mod:`.pool`.
"""
import logging
from pathlib import Path
# import pickle
import pytest   # type: ignore[import]
# import typing

# from factsheet.abc_types import abc_sheet as ABC_SHEET
import factsheet.control.control_sheet as CSHEET
import factsheet.model.sheet as MSHEET
# from factsheet.control import control_topic as CTOPIC
# from factsheet.control import pool as CPOOL
# from factsheet.model import topic as MTOPIC


# @pytest.fixture
# def patch_model_safe():
#     class PatchSafe(MSHEET.Sheet):
#         def __init__(self, p_stale, p_n_pages):
#             super().__init__()
#             self._stale = p_stale
#             self._n_pages = p_n_pages
#             self.n_detach = 0
#
#         def n_pages(self) -> int:
#             return self._n_pages
#
#         def detach_page(self, _view):
#             self.n_detach += 1
#
#     return PatchSafe


class PatchObserverControlSheet(CSHEET.ObserverControlSheet):
    """:class:`.ObserverControlSheet` subclass with stubs for methods."""

    def __init__(self, p_control):
        self._control = p_control
        self.close_called = False
        self.present_called = False

    def erase(self):
        self._control.remove_view(self)
        self.close_called = True

    def present(self, p_time):
        _ = p_time
        self.present_called = True


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
            control_sheet = target.open_factsheet(p_path=None)
            view = PatchObserverControlSheet(p_control=control_sheet)
            control_sheet.add_view(view)
        assert N_CONTROLS == len(target._roster_sheets)

        I_REMOVE = 1
        items = list(target._roster_sheets.items())
        (id_removed, control_removed) = items.pop(I_REMOVE)
        view_removed = next(iter(control_removed._roster_views.values()))
        # Test
        target.close_factsheet(p_control=control_removed)
        assert view_removed.close_called
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
        control_sheet = target.open_factsheet()
        assert N_FACTSHEETS == len(target._roster_sheets)
        assert isinstance(control_sheet, CSHEET.ControlSheet)
        id_control_sheet = CSHEET.id_factsheet(control_sheet)
        assert target._roster_sheets[id_control_sheet] is control_sheet

    @pytest.mark.skip
    def test_open_factsheet_no_match(self, tmp_path):
        """| Confirm factsheet return.
        | Case: path does not match an existing file
        """
        # # Setup
        # CSHEET._m_factsheets.clear()
        # N_FACTSHEETS = 5
        # PATH_BASE = Path(tmp_path)
        # for i in range(N_FACTSHEETS):
        #     path = PATH_BASE / '/factsheet{}.fsg'.format(i)
        #     control = CSHEET.ControlSheet.open(path)
        #     CSHEET._m_factsheets[id(control)] = control
        # PATH_DIFF = PATH_BASE / '/scd.fsg'
        # # Test
        # target = CSHEET.open_factsheet(PATH_DIFF)
        # assert isinstance(target, CSHEET.ControlSheet)
        # assert PATH_DIFF == target._path
        # assert N_FACTSHEETS + 1 == len(CSHEET._m_factsheets)
        # assert target is CSHEET._m_factsheets[id(target)]

    @pytest.mark.skip
    def test_open_factsheet_match(self, tmp_path):
        """| Confirm factsheet return.
        | Case: path matches an existing file
        """
        # # Setup
        # CPOOL._m_factsheets.clear()
        # N_CONTROLS = 5
        # I_MATCH = 4
        # PATH_BASE = Path(tmp_path)
        # for i in range(N_CONTROLS):
        #     control = CPOOL.open_factsheet()
        #     path = PATH_BASE / '/factsheet{}.fsg'.format(i)
        #     control._path = path
        #     if i == I_MATCH:
        #         path_match = path
        #         control_match = control
        # # Test
        # target = CPOOL.open_factsheet(path_match)
        # assert isinstance(target, CPOOL.ControlSheet)
        # assert target is control_match
        # assert N_CONTROLS == len(CPOOL._m_factsheets)
        # assert target is CPOOL._m_factsheets[id(target)]

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
            _control_sheet = target.open_factsheet(p_path=None)
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
            _control_sheet = target.open_factsheet(p_path=None)
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
        PATH = None
        MODEL_DEFAULT = MSHEET.Sheet()
        # Test
        target = CSHEET.ControlSheet(p_path=PATH)
        assert target._path is None
        assert MODEL_DEFAULT == target._model
        assert isinstance(target._roster_views, dict)
        assert not target._roster_views
        assert not target._is_closing
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

    def test_add_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm tracking of given sheet view.
        | Case: duplicate view
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Duplicate: sheet 0x{:X} add view 0x{:X}  '
                       '(ControlSheet.add_view)'
                       ''.format(id_view, id(target)))
        # Test
        target.add_view(view)
        assert not patch_logger.called
        target.add_view(view)
        assert target._roster_views[id_view] is view
        assert patch_logger.called
        assert log_message == patch_logger.message

    def test_remove_all_views(self, monkeypatch):
        """Confirm tracking stops for all sheet views."""
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
        assert target._is_closing
        assert not target._roster_views
        assert patch.called
        assert target is patch.control_sheet

    def test_remove_view_is_safe_approved(self):
        """| Confirm return shows safe to erase.
        | Case: user approves
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        target._model.set_stale()
        target._is_closing = True
        # Test
        assert target.remove_view_is_safe()

    def test_remove_view_is_safe_fresh(self):
        """| Confirm return shows safe to erase.
        | Case: no unsaved changes
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        target._model.set_fresh()
        target._is_closing = False
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
        target._is_closing = False
        # Test
        assert target.remove_view_is_safe()

    def test_remove_view_is_safe_unsafe(self):
        """Confirm return shows  not safe to erase."""
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        target.add_view(view)
        target._model.set_stale()
        target._is_closing = False
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

    def test_remove_view_warn(self, PatchLogger, monkeypatch):
        """| Confirm tracking stops for given sheet view.
        | Case: view not tracked
        """
        # Setup
        target = CSHEET.ControlSheet(p_path=None)
        view = PatchObserverControlSheet(p_control=target)
        id_view = CSHEET.id_view_sheet(p_view_sheet=view)
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Missing: sheet 0x{:X} remove view 0x{:X}  '
                       '(ControlSheet.remove_view)'
                       ''.format(id(target), id_view))
        # Test
        target.remove_view(view)
        assert patch_logger.called
        assert log_message == patch_logger.message

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
            keyword arguments
        :param METHOD: method to test, which is ``is_fresh`` or ``is_stale``.
        :param MODEL_IS_STALE: state of change in model.
        """
        # Setup
        PATH = None
        target = CSHEET.ControlSheet(p_path=PATH)
        method_model = getattr(target._model, METHOD)
        method_target = getattr(target, METHOD)
        target._model._stale = MODEL_IS_STALE
        # Test
        assert method_model() == method_target()

    @pytest.mark.skip(reason='being replaced by model pass through')
    @pytest.mark.parametrize('NAME_METHOD, NAME_CHECK, CLASS', [
        ('new_view_name_active', 'get_buffer', MSHEET.ViewNameSheetActive),
        ('new_view_name_passive', 'get_label', MSHEET.ViewNameSheetPassive),
        ('new_view_summary_active', 'get_buffer',
            MSHEET.ViewSummarySheetActive),
        ('new_view_summary_passive', 'get_buffer',
            MSHEET.ViewSummarySheetPassive),
        ('new_view_title_active', 'get_buffer', MSHEET.ViewTitleSheetActive),
        ('new_view_title_passive', 'get_label', MSHEET.ViewTitleSheetPassive),
        ])
    def test_new_view(self, new_kwargs_idcore, NAME_METHOD, NAME_CHECK, CLASS):
        """Confirm control relays requests for new views.

        :param new_kwargs_idcore: fixture: factory for stock identity
            keyword arguments
        :param NAME_METHOD: name of method under test
        :param NAME_CHECK: name of method used to check view
        :param CLASS: expected view class
        """
        # Setup
        KWARGS = new_kwargs_idcore()
        model = MSHEET.Sheet(**KWARGS)
        model_method = getattr(model, NAME_METHOD)
        model_view = model_method()
        model_check = getattr(model_view, NAME_CHECK)
        PATH = None
        target = CSHEET.ControlSheet(p_model=model, p_path=PATH)
        target_method = getattr(target, NAME_METHOD)
        # Test
        target_view = target_method()
        assert isinstance(target_view, CLASS)
        target_check = getattr(target_view, NAME_CHECK)
        assert model_check() == target_check()
        # Teardown
        target_view.destroy()
        model_view.destroy()

    @pytest.mark.skip
    def test_model_from_path(self, tmp_path):
        """| Confirm model creation.
        | Case: file at path location constains factsheet model
        """
        # # Setup
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # source._path = PATH
        # assert not PATH.exists()
        # source.save()
        # # Test
        # target = CSHEET.ControlSheet.open(sheets_active, PATH)
        # assert source._model == target._model
        # assert target._model.is_fresh()

    def test_model_from_path_empty(self, tmp_path):
        """| Confirm model creation.
        | Case: no file at path location
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        target = CSHEET.ControlSheet(p_path=PATH)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=PATH)
        assert model_default == model

    @pytest.mark.skip
    def test_model_from_path_except(self, tmp_path):
        """| Confirm model creation.
        | Case: file at path location does not conatain factsheet
        """
        # # Setup
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # BYTES = b'Something completely different'
        # with PATH.open(mode='wb') as io_out:
        #     io_out.write(BYTES)
        # assert PATH.exists()
        # NAME = 'OPEN ERROR'
        # TITLE = 'Error opening file \'{}\''.format(PATH)
        # sheets_active = CPOOL.PoolSheets()
        # # Test
        # target = CSHEET.ControlSheet.open(sheets_active, PATH)
        # model = target._model
        # assert model is not None
        # assert NAME == model._infoid.name
        # assert model._infoid.summary
        # assert TITLE == model._infoid.title
        # assert target._path is None

    def test_model_from_path_none(self):
        """| Confirm model creation.
        | Case: no path
        """
        # Setup
        PATH = None
        target = CSHEET.ControlSheet(p_path=PATH)
        model_default = MSHEET.Sheet()
        # Test
        model = target._model_from_path(p_path=PATH)
        assert model_default == model

    @pytest.mark.skip
    def test_present_factsheet(self, monkeypatch):
        """Confirm factsheet notifies model."""
        # # Setup
        # class PatchPresentPages:
        #     def __init__(self): self.called = False
        #
        #     def present_pages(self, _time): self.called = True
        #
        # patch_present = PatchPresentPages()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'present_pages', patch_present.present_pages)
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # target = CSHEET.ControlSheet(sheets_active)
        # target._model = model
        # NO_TIME = 0
        # # Test
        # target.present_factsheet(NO_TIME)
        # assert patch_present.called

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_path', 'path'),
        ('_model', 'model'),
        ])
    def test_property(self, tmp_path, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
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
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    # @pytest.mark.skip
    # @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
    #     # ['_path', 'path'],
    #     # ['_sheets_active', 'sheets_active'],
    #     ])
    # def test_property(self, tmp_path, NAME_ATTR, NAME_PROP):
    #     """Confirm properties are get-only.
    #
    #     #. Case: get
    #     #. Case: no set
    #     #. Case: no delete
    #     """
    #     # # Setup
    #     # sheets_active = CPOOL.PoolSheets()
    #     # target = CSHEET.ControlSheet(sheets_active)
    #     # PATH = Path(tmp_path / 'path_factsheet.fsg')
    #     # target._path = PATH
    #     # value_attr = getattr(target, NAME_ATTR)
    #     # target_prop = getattr(CSHEET.ControlSheet, NAME_PROP)
    #     # value_prop = getattr(target, NAME_PROP)
    #     # # Test: read
    #     # assert target_prop.fget is not None
    #     # assert str(value_attr) == str(value_prop)
    #     # # Test: no replace
    #     # assert target_prop.fset is None
    #     # # Test: no delete
    #     # assert target_prop.fdel is None

    @pytest.mark.skip
    def test_save(self, tmp_path):
        """| Confirm write to file.
        | Case: file does not exist.
        """
        # # Setup
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # source._path = PATH
        # assert not PATH.exists()
        # # Test
        # source.save()
        # assert PATH.exists()
        # assert source._model.is_fresh()
        #
        # with PATH.open(mode='rb') as io_in:
        #     target = pickle.load(io_in)
        # assert target is not None
        # assert TITLE == target._infoid.title

    @pytest.mark.skip
    def test_save_as(self, monkeypatch, tmp_path):
        """Confirm write to file at new path."""
        # # Setup
        # class PatchModel:
        #     def __init__(self):
        #         self.called = False
        #         self.base = ''
        #
        #     def update_titles(self, p_base):
        #         self.called = True
        #         self.base = p_base
        #
        # patch_model = PatchModel()
        # monkeypatch.setattr(
        #     MSHEET.Sheet, 'update_titles', patch_model.update_titles)
        #
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # assert not PATH.exists()
        # # Test
        # source.save_as(PATH)
        # assert PATH == source._path
        # assert PATH.exists()
        # assert source._model.is_fresh()
        #
        # with PATH.open(mode='rb') as io_in:
        #     target = pickle.load(io_in)
        # assert target is not None
        # assert TITLE == target._infoid.title
        # assert patch_model.called
        # assert PATH.name == patch_model.base

    @pytest.mark.skip
    def test_save_oserror(self, monkeypatch, tmp_path):
        """| Confirm write to file.
        | Case: unexpected operating system exception.
        """
        # # Setup
        # def open_oserror(_s, **_kwa): raise OSError
        #
        # monkeypatch.setattr(Path, 'open', open_oserror)
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # source._path = PATH
        # # Test
        # with pytest.raises(OSError):
        #     source.save()

    @pytest.mark.skip
    def test_save_exists(self, tmp_path):
        """| Confirm write to file.
        | Case: file exists.
        """
        # # Setup
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # TEXT = 'Existing content'
        # with PATH.open(mode='w') as io_out:
        #     io_out.write(TEXT)
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # model.set_stale()
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # source._path = PATH
        # assert PATH.exists()
        # BACKUP = PATH.with_name(PATH.name + '~')
        # assert not BACKUP.exists()
        # # Test
        # source.save()
        # assert PATH.exists()
        # assert source._model.is_fresh()
        #
        # with PATH.open(mode='rb') as io_in:
        #     target = pickle.load(io_in)
        # assert target is not None
        #
        # assert BACKUP.exists()
        # with BACKUP.open(mode='r') as io_in:
        #     backup_text = io_in.read()
        # assert TEXT == backup_text

    @pytest.mark.skip
    def test_save_no_path(self, PatchLogger, monkeypatch):
        """| Confirm write to file.
        | Case: no file path.
        """
        # # Setup
        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = ('No file path (ControlSheet.save)')
        # TITLE = 'Parrot Sketch'
        # model = MSHEET.Sheet(p_title=TITLE)
        # sheets_active = CPOOL.PoolSheets()
        # source = CSHEET.ControlSheet(sheets_active)
        # source._model = model
        # source._path = None
        # # Test
        # source.save()
        # assert patch_logger.called
        # assert log_message == patch_logger.message


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

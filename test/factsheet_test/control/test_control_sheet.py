"""
Unit tests for class that mediates factsheet-level interactions from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.  See
:mod:`~.control_sheet`.
"""
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import control_sheet as CSHEET
from factsheet.control import control_topic as CTOPIC
from factsheet.control import pool as CPOOL
from factsheet.model import sheet as MSHEET
from factsheet.model import topic as MTOPIC
import typing


@pytest.fixture
def patch_model_safe():
    class PatchSafe(MSHEET.Sheet):
        def __init__(self, p_stale, p_n_pages):
            super().__init__()
            self._stale = p_stale
            self._n_pages = p_n_pages
            self.n_detach = 0

        def n_pages(self) -> int:
            return self._n_pages

        def detach_page(self, _view):
            self.n_detach += 1

    return PatchSafe


class TestControlSheet:
    """Unit tests for :class:`~.ControlSheet`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.ControlSheet(sheets_active)
        assert target._model is None
        assert target._path is None
        assert target._sheets_active is sheets_active
        assert sheets_active._controls[id(target)] is target
        assert isinstance(target._controls_topic, typing.Dict)
        assert not target._controls_topic

    def test_attach_page(self, monkeypatch):
        """Confirm page addition."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_attach_page = False
                self.called_update_titles = False
                self.base = ''

            def attach_page(self, _page):
                self.called_attach_page = True

            def update_titles(self, p_base):
                self.called_update_titles = True
                self.base = p_base

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'attach_page', patch_model.attach_page)
        monkeypatch.setattr(
            MSHEET.Sheet, 'update_titles', patch_model.update_titles)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        target.attach_page(None)
        assert patch_model.called_attach_page
        assert patch_model.called_update_titles

    def test_attach_view_topics(self, monkeypatch):
        """Confirm topics outline view addition."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_attach_page = False

            def attach_view_topics(self, _view):
                self.called_attach_view_topics = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'attach_view_topics', patch_model.attach_view_topics)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        target.attach_view_topics(None)
        assert patch_model.called_attach_view_topics

    def test_detach_view_topics(self, monkeypatch):
        """Confirm topics outline view removal."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called_detach_page = False

            def detach_view_topics(self, _view):
                self.called_detach_view_topics = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_view_topics', patch_model.detach_view_topics)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        target.detach_view_topics(None)
        assert patch_model.called_detach_view_topics

    def test_clear(self, monkeypatch):
        """Confirm method passes request to model."""
        # Setup
        class PatchClear:
            def __init__(self): self.called = False

            def clear(self): self.called = True

        patch_clear = PatchClear()
        monkeypatch.setattr(
            MSHEET.Sheet, 'clear', patch_clear.clear)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        target.clear()
        assert patch_clear.called

    def test_delete_force(self, monkeypatch):
        """Confirm unconditional deletion."""
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        assert sheets_active._controls[id(target)] is target
        # Test
        target.delete_force()
        assert patch_model.called
        assert id(target) not in sheets_active._controls.keys()

    def test_delete_safe_fresh(self, monkeypatch):
        """| Confirm deletion with guard for unsaved changes.
        | Case: no unsaved changes
        """
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)
        monkeypatch.setattr(
            MSHEET.Sheet, 'is_stale', lambda _s: False)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        response = target.delete_safe()
        assert patch_model.called
        assert response is ABC_SHEET.EffectSafe.COMPLETED

    def test_delete_safe_stale(self, monkeypatch):
        """| Confirm deletion with guard for unsaved changes.
        | Case: unsaved changes
        """
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)
        monkeypatch.setattr(
            MSHEET.Sheet, 'is_stale', lambda _s: True)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        response = target.delete_safe()
        assert not patch_model.called
        assert response is ABC_SHEET.EffectSafe.NO_EFFECT

    def test_detach_page_force(self, patch_model_safe):
        """| Confirm page removed unconditionally.
        | Case: not last page."""
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = patch_model
        assert sheets_active._controls[id(target)] is target
        N_DETACH = 1
        # Test
        target.detach_page_force(None)
        assert N_DETACH == patch_model.n_detach
        assert id(target) in sheets_active._controls.keys()

    def test_detach_page_force_last(self, patch_model_safe):
        """| Confirm page removed unconditionally.
        | Case: last page."""
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=0)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = patch_model
        assert sheets_active._controls[id(target)] is target
        N_DETACH = 1
        # Test
        target.detach_page_force(None)
        assert N_DETACH == patch_model.n_detach
        assert id(target) not in sheets_active._controls.keys()

    def test_detach_page_safe_fresh(self, patch_model_safe):
        """| Confirm page removal with guard for unsaved changes.
        | Case: no unsaved changes
        """
        # Setup
        patch_model = patch_model_safe(p_stale=False, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = patch_model
        N_DETACH = 1
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.COMPLETED)
        assert N_DETACH == patch_model.n_detach

    def test_detach_page_safe_stale_multiple(self, patch_model_safe):
        """| Confirm page removal with guard for unsaved changes.
        | Case: unsaved changes, multiple pages
        """
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=2)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = patch_model
        N_DETACH = 1
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.COMPLETED)
        assert N_DETACH == patch_model.n_detach

    def test_detach_page_safe_stale_single(self, patch_model_safe):
        """| Confirm page removal with guard for unsaved changes.
        | Case: unsaved changes, single page
        """
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = patch_model
        N_DETACH = 0
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.NO_EFFECT)
        assert N_DETACH == patch_model.n_detach

    def test_extract_topic(self, monkeypatch):
        """Confirm method passes request to model."""
        # Setup
        class PatchExtract:
            def __init__(self): self.called = False

            def extract_topic(self, _index): self.called = True

        patch_extract = PatchExtract()
        monkeypatch.setattr(
            MSHEET.Sheet, 'extract_topic', patch_extract.extract_topic)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        # Test
        _ = target.extract_topic(None)
        assert patch_extract.called

    def test_get_control_topic(self):
        """| Confirm
        | Case: topic in model
        """
        # Setup
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)

        N_TOPICS = 3
        topics = [MTOPIC.Topic(p_name='Topic {}'.format(i))
                  for i in range(N_TOPICS)]
        for topic in topics:
            control_topic = CTOPIC.ControlTopic(p_model=topic)
            key_topic = topic.tag
            target._controls_topic[key_topic] = control_topic

        N_EXPECT = 1
        topic_expect = topics[N_EXPECT]
        id_expect = topic_expect.tag
        # Test
        control_actual = target.get_control_topic(topic_expect)
        assert control_actual is target._controls_topic[id_expect]

    def test_get_control_topic_absent(self):
        """| Confirm
        | Case: topic in model
        """
        # Setup
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)

        N_TOPICS = 3
        topics = [MTOPIC.Topic(p_name='Topic {}'.format(i))
                  for i in range(N_TOPICS)]
        for topic in topics:
            control_topic = CTOPIC.ControlTopic(p_model=topic)
            key_topic = topic.tag
            target._controls_topic[key_topic] = control_topic

        topic_absent = MTOPIC.Topic(p_title="Spanish Inquisition")
        # Test
        control_actual = target.get_control_topic(topic_absent)
        assert control_actual is None

    @pytest.mark.parametrize('NAME_METHOD', [
        'insert_topic_after',
        'insert_topic_before',
        'insert_topic_child',
        ])
    def test_insert_topic(self, monkeypatch, NAME_METHOD):
        """Confirm each insert method passes request to model."""
        # Setup
        class PatchInsert:
            def __init__(self): self.called = False

            def insert_topic(self, _item, index):
                self.called = True
                return index

        patch_insert = PatchInsert()
        monkeypatch.setattr(
            MSHEET.Sheet, NAME_METHOD, patch_insert.insert_topic)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        method = getattr(target, NAME_METHOD)

        TITLE = 'Something completely different.'
        TOPIC = MTOPIC.Topic(pm_title=TITLE)
        id_topic = TOPIC.tag
        I_TOPIC = 'Parrot'
        # Test
        index_new, control_new = method(TOPIC, I_TOPIC)
        assert patch_insert.called
        assert index_new is I_TOPIC
        assert isinstance(control_new, CTOPIC.ControlTopic)
        assert target._controls_topic[id_topic] is control_new

    def test_new(self):
        """Confirm control creation with default model."""
        # Setup
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.ControlSheet.new(sheets_active)
        assert isinstance(target, CSHEET.ControlSheet)
        assert isinstance(target._model, MSHEET.Sheet)

    def test_new_name(self, monkeypatch):
        """| Confirm model gets new name notice.
        | Case: factsheet path is defined.
        """
        # Setup
        class PatchModel:
            def __init__(self):
                self.called = False
                self.base = ''

            def update_titles(self, p_base):
                self.called = True
                self.base = p_base

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'update_titles', patch_model.update_titles)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        PARENT = '/home/scratch'
        FILE = 'larch.fsg'
        target._path = Path(PARENT) / FILE
        # Test
        target.new_name()
        assert patch_model.called
        assert FILE == patch_model.base

    def test_new_name_unsaved(self, monkeypatch):
        """| Confirm model gets new name notice.
        | Case: factsheet path is not defined.
        """
        # Setup
        class PatchModel:
            def __init__(self):
                self.called = False
                self.base = ''

            def update_titles(self, p_base):
                self.called = True
                self.base = p_base

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'update_titles', patch_model.update_titles)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet.new(sheets_active)
        DEFAULT = 'Unsaved'
        # Test
        target.new_name()
        assert patch_model.called
        assert DEFAULT == patch_model.base

    def test_open(self, tmp_path):
        """| Confirm control creation from file.
        | Case: path to file with model contents
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        source._path = PATH
        assert not PATH.exists()
        source.save()
        # Test
        target = CSHEET.ControlSheet.open(sheets_active, PATH)
        assert source._model == target._model
        assert target._model.is_fresh()

    def test_open_empty(self, tmp_path):
        """| Confirm control creation from file.
        | Case: path not to a file
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        NAME = 'OPEN ERROR'
        TITLE = 'Error opening file \'{}\''.format(PATH)
        assert not PATH.exists()
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.ControlSheet.open(sheets_active, PATH)
        model = target._model
        assert model is not None
        assert NAME == model._infoid.name
        assert model._infoid.summary is not None
        assert model._infoid.summary
        assert TITLE == model._infoid.title
        assert target._path is None

    def test_open_except(self, tmp_path):
        """| Confirm control creation from file.
        | Case: path to file with unloadable contents
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        BYTES = b'Something completely different'
        with PATH.open(mode='wb') as io_out:
            io_out.write(BYTES)
        assert PATH.exists()
        NAME = 'OPEN ERROR'
        TITLE = 'Error opening file \'{}\''.format(PATH)
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.ControlSheet.open(sheets_active, PATH)
        model = target._model
        assert model is not None
        assert NAME == model._infoid.name
        assert model._infoid.summary
        assert TITLE == model._infoid.title
        assert target._path is None

    def test_present_factsheet(self, monkeypatch):
        """Confirm factsheet notifies model."""
        # Setup
        class PatchPresentPages:
            def __init__(self): self.called = False

            def present_pages(self, _time): self.called = True

        patch_present = PatchPresentPages()
        monkeypatch.setattr(
            MSHEET.Sheet, 'present_pages', patch_present.present_pages)
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
        target._model = model
        NO_TIME = 0
        # Test
        target.present_factsheet(NO_TIME)
        assert patch_present.called

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_path', 'path'],
        ['_sheets_active', 'sheets_active'],
        ])
    def test_property(self, tmp_path, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.ControlSheet(sheets_active)
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

    def test_save(self, tmp_path):
        """| Confirm write to file.
        | Case: file does not exist.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        source._path = PATH
        assert not PATH.exists()
        # Test
        source.save()
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None
        assert TITLE == target._infoid.title

    def test_save_as(self, monkeypatch, tmp_path):
        """Confirm write to file at new path."""
        # Setup
        class PatchModel:
            def __init__(self):
                self.called = False
                self.base = ''

            def update_titles(self, p_base):
                self.called = True
                self.base = p_base

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'update_titles', patch_model.update_titles)

        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        assert not PATH.exists()
        # Test
        source.save_as(PATH)
        assert PATH == source._path
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None
        assert TITLE == target._infoid.title
        assert patch_model.called
        assert PATH.name == patch_model.base

    def test_save_oserror(self, monkeypatch, tmp_path):
        """| Confirm write to file.
        | Case: unexpected operating system exception.
        """
        # Setup
        def open_oserror(_s, **_kwa): raise OSError

        monkeypatch.setattr(Path, 'open', open_oserror)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        source._path = PATH
        # Test
        with pytest.raises(OSError):
            source.save()

    def test_save_exists(self, tmp_path):
        """| Confirm write to file.
        | Case: file exists.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TEXT = 'Existing content'
        with PATH.open(mode='w') as io_out:
            io_out.write(TEXT)
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        source._path = PATH
        assert PATH.exists()
        BACKUP = PATH.with_name(PATH.name + '~')
        assert not BACKUP.exists()
        # Test
        source.save()
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None

        assert BACKUP.exists()
        with BACKUP.open(mode='r') as io_in:
            backup_text = io_in.read()
        assert TEXT == backup_text

    def test_save_no_path(self, PatchLogger, monkeypatch):
        """| Confirm write to file.
        | Case: no file path.
        """
        # Setup
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('No file path (ControlSheet.save)')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.ControlSheet(sheets_active)
        source._model = model
        source._path = None
        # Test
        source.save()
        assert patch_logger.called
        assert log_message == patch_logger.message

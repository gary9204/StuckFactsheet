"""
Unit tests for topic-level model. See :mod:`~.section.section_topic`.
"""
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

from factsheet.model import infoid as MINFOID
from factsheet.content.section import section_topic as XTOPIC


class TestTopic:
    """Unit tests for :class:`~.model.topic.Topic`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: Equivalence
        """
        # Setup
        TITLE_SOURCE = 'The Parrot Sketch'
        source = XTOPIC.Topic(p_title=TITLE_SOURCE)
        # Test: type difference
        assert not source.__eq__(TITLE_SOURCE)
        # Test: InfoId difference
        TITLE_TARGET = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_TARGET)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = XTOPIC.Topic(p_title=TITLE_SOURCE)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_class_pane_topic):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        TITLE_MODEL = 'Something completely different.'
        source = XTOPIC.Topic(p_title=TITLE_MODEL)
        source._stale = True

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        for view in views:
            source.attach_view(view)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert isinstance(target._views, dict)
        assert not target._views
        assert source._infoid == target._infoid
        assert not target._stale

    def test_init(self, args_infoid_stock):
        """Confirm initialization."""
        # Setup
        NAME = args_infoid_stock['p_name']
        SUMMARY = args_infoid_stock['p_summary']
        TITLE = args_infoid_stock['p_title']
        # Test
        target = XTOPIC.Topic(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target._infoid.name
        assert SUMMARY == target._infoid.summary
        assert TITLE == target._infoid.title

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = XTOPIC.Topic()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title

    def test_attach_view(self, patch_class_pane_topic):
        """Confirm view addition.
        Case: view not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        assert views[0].get_infoid().title != target._infoid.title
        # Test
        for view in views:
            target.attach_view(view)
            assert target._infoid.title == view.get_infoid().title
            assert target._views[id(view)] is view
        assert len(views) == len(target._views)

    def test_attach_view_warn(
            self, patch_class_pane_topic, PatchLogger, monkeypatch):
        """Confirm view addition.
        Case: view attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        assert views[0].get_infoid().title != target._infoid.title
        for view in views:
            target.attach_view(view)
        assert N_VIEWS == len(target._views)
        I_DUPLIDATE = 1
        view_dup = views[I_DUPLIDATE]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} (Topic.attach_view)'
            ''.format(hex(id(view_dup))))
        assert not patch_logger.called
        # Test
        target.attach_view(view_dup)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_all(self, monkeypatch, patch_class_pane_topic):
        """Confirm removals."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        assert N_VIEWS == len(target._views)
        # Test
        target.detach_all()
        assert not target._views
        assert N_VIEWS == patch_detach.n_calls

    def test_detach_view(self, monkeypatch, patch_class_pane_topic):
        """Confirm view removal.
        Case: view attached initially
        """
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        I_REMOVE = 1
        view_rem = views.pop(I_REMOVE)
        # Test
        target.detach_view(view_rem)
        assert N_REMOVE == patch_infoid.n_calls
        assert len(views) == len(target._views)
        for view in views:
            assert target._views[id(view)] is view

    def test_detach_attribute_views(
            self, monkeypatch, patch_class_pane_topic):
        """Confirm removal of attribute views."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        view = patch_class_pane_topic()
        target.attach_view(view)
        # Test
        target._detach_attribute_views(view)
        assert patch_infoid.called

    def test_detach_view_warn(
            self, patch_class_pane_topic, PatchLogger, monkeypatch):
        """Confirm view removal.
        Case: view not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = XTOPIC.Topic(p_title=TITLE_MODEL)

        N_VIEWS = 3
        views = [patch_class_pane_topic() for _ in range(N_VIEWS)]
        assert views[0].get_infoid().title != target._infoid.title
        for view in views:
            target.attach_view(view)
        I_DUPLICATE = 1
        view_dup = views.pop(I_DUPLICATE)
        target.detach_view(view_dup)
        assert len(views) == len(target._views)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} (Topic.detach_view)'
            ''.format(hex(id(view_dup))))
        # Test
        target.detach_view(view_dup)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_is_fresh(self):
        """Confirm return is accurate.

        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic fresh, identification information fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = XTOPIC.Topic(p_title=TEXT_TITLE)
        # Test: InfoId stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, identification information fresh
        assert not target.is_fresh()
        target._stale = False
        target._infoid.set_fresh()
        assert target.is_fresh()
        assert not target._stale

    def test_is_stale(self):
        """Confirm return is accurate.

        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic fresh, identification information fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = XTOPIC.Topic(p_title=TEXT_TITLE)
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    @pytest.mark.parametrize('NAME_PROP', [
        'name',
        'title',
        ])
    def test_property_infoid(self, NAME_PROP):
        """Confirm pass-through InfoId properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = XTOPIC.Topic(p_name='Parrot', p_title='Parrot Sketch')
        value_attr = getattr(target._infoid, NAME_PROP)
        target_prop = getattr(XTOPIC.Topic, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr == value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_set_fresh(self):
        """Confirm all attributes set.

        #. Case: Topic fresh, identification information fresh
        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic stale, identification information stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = XTOPIC.Topic(p_title=TEXT_TITLE)
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()

    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Topic fresh, identification information fresh
        #. Case: Topic stale, identification information fresh
        #. Case: Topic fresh, identification information stale
        #. Case: Topic stale, identification information stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = XTOPIC.Topic(p_title=TEXT_TITLE)
        # Test: Topic fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Topic fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Topic stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()

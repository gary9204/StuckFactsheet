"""
Unit tests for factsheet-level model.

See :mod:`~factsheet.model`.
"""
import re
import logging
from pathlib import Path
import pickle

from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content.outline import topic as XTOPIC
from factsheet.model import infoid as MINFOID
from factsheet.model import sheet as MSHEET


class TestSheet:
    """Unit tests for :class:`~.model.sheet.Sheet`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: topic outline difference
        #. Case: Equivalence
        """
        # Setup
        TITLE_SOURCE = 'The Parrot Sketch'
        source = MSHEET.Sheet(p_title=TITLE_SOURCE)
        # Test: type difference
        assert not source.__eq__(TITLE_SOURCE)
        # Test: InfoId difference
        TITLE_TARGET = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_TARGET)
        assert not source.__eq__(target)
        # Test: topic outline difference
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        topic = XTOPIC.Topic(p_name='Killer Rabbit')
        _index = target._topics.insert_child(topic, None)

        assert not source.__eq__(target)
        # Test: Equivalence
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, patch_class_page_sheet):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        TITLE_MODEL = 'Something completely different.'
        source = MSHEET.Sheet(p_title=TITLE_MODEL)
        source._stale = True

        topic = XTOPIC.Topic(p_name='Killer Rabbit')
        _index = source._topics.insert_child(topic, None)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            source.attach_page(page)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert source._infoid == target._infoid
        assert source._topics == target._topics
        assert not target._stale
        assert isinstance(target._pages, dict)
        assert not target._pages

    def test_init(self, args_infoid_stock):
        """Confirm initialization."""
        # Setup
        ASPECT = MSHEET.Sheet.ASPECT
        NAME = args_infoid_stock['p_name']
        SUMMARY = args_infoid_stock['p_summary']
        TITLE = args_infoid_stock['p_title']
        # Test
        target = MSHEET.Sheet(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert isinstance(target._pages, dict)
        assert not target._pages
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert ASPECT == target._infoid.aspect
        assert NAME == target._infoid.name
        assert SUMMARY == target._infoid.summary
        assert TITLE == target._infoid.title
        assert isinstance(target._topics, ABC_OUTLINE.AbstractOutline)

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = 'Unnamed'
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = MSHEET.Sheet()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title

    def test_attach_page(self, patch_class_page_sheet):
        """Confirm page addition.
        Case: page not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        # Test
        for page in pages:
            target.attach_page(page)
            assert target._infoid.title == page.get_infoid().title
            assert target._topics._gtk_model is (
                page._topics.gtk_view.get_model())
            assert target._pages[id(page)] is page
        assert len(pages) == len(target._pages)

    def test_attach_page_warn(
            self, patch_class_page_sheet, PatchLogger, monkeypatch):
        """Confirm page addition.
        Case: page attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        for page in pages:
            target.attach_page(page)
        assert N_PAGES == len(target._pages)
        I_DUPLIDATE = 1
        page_dup = pages[I_DUPLIDATE]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate page: {} (Sheet.attach_page)'
            ''.format(hex(id(page_dup))))
        # Test
        target.attach_page(page_dup)
        assert len(pages) == len(target._pages)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_detach_all(self, monkeypatch, patch_class_page_sheet):
        """Confirm notifications and removals."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            target.attach_page(page)
        assert N_PAGES == len(target._pages)
        # Test
        target.detach_all()
        assert not target._pages
        assert N_PAGES == patch_detach.n_calls
        for page in pages:
            assert page.called_close

    def test_detach_page(self, monkeypatch, patch_class_page_sheet):
        """Confirm page removal.
        Case: page attached initially
        """
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            target.attach_page(page)
        N_REMOVE = 1
        I_REMOVE = 1
        page_rem = pages.pop(I_REMOVE)
        # Test
        target.detach_page(page_rem)
        assert N_REMOVE == patch_infoid.n_calls
        assert len(pages) == len(target._pages)
        for page in pages:
            assert target._pages[id(page)] is page

    def test_detach_attribute_views(
            self, monkeypatch, patch_class_page_sheet):
        """Confirm removal of views."""
        # Setup
        class PatchInfoIdDetach:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_infoid = PatchInfoIdDetach()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        class PatchTopicsDetach:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_topics = PatchTopicsDetach()
        monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic, 'detach_view',
                            patch_topics.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        page = patch_class_page_sheet()
        target.attach_page(page)
        # Test
        target._detach_attribute_views(page)
        assert patch_infoid.called
        assert patch_topics.called

    def test_detach_page_warn(
            self, patch_class_page_sheet, PatchLogger, monkeypatch):
        """Confirm page removal.
        Case: page not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        for page in pages:
            target.attach_page(page)
        I_DUPLICATE = 1
        page_dup = pages.pop(I_DUPLICATE)
        target.detach_page(page_dup)
        assert len(pages) == len(target._pages)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing page: {} (Sheet.detach_page)'
            ''.format(hex(id(page_dup))))
        # Test
        target.detach_page(page_dup)
        assert len(pages) == len(target._pages)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_extract_topic(self, monkeypatch):
        """Confirm method passes request to outline."""
        # Setup
        class PatchExtract:
            def __init__(self): self.called = False

            def extract_section(self, _index): self.called = True

        patch_outline = PatchExtract()
        monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic, 'extract_section',
                            patch_outline.extract_section)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        # Test
        _ = target.extract_topic(None)
        assert patch_outline.called

    def test_insert_topic_after(self, monkeypatch):
        """Confirm method passes request to outline."""
        # Setup
        class PatchInsertAfter:
            def __init__(self): self.called = False

            def insert_after(self, _item, _index): self.called = True

        patch_outline = PatchInsertAfter()
        monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
                            'insert_after', patch_outline.insert_after)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_topic_after(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_insert_topic_before(self, monkeypatch):
        """Confirm method passes request to outline."""
        # Setup
        class PatchInsertBefore:
            def __init__(self): self.called = False

            def insert_before(self, _item, _index): self.called = True

        patch_outline = PatchInsertBefore()
        monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
                            'insert_before', patch_outline.insert_before)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_topic_before(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_insert_topic_child(self, monkeypatch):
        """Confirm method passes request to outline."""
        # Setup
        class PatchInsertChild:
            def __init__(self): self.called = False

            def insert_child(self, _item, _index): self.called = True

        patch_outline = PatchInsertChild()
        monkeypatch.setattr(ASHEET.AdaptTreeStoreTopic,
                            'insert_child', patch_outline.insert_child)
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)
        target.set_fresh()
        # Test
        _ = target.insert_topic_child(None, None)
        assert patch_outline.called
        assert target.is_stale()

    def test_is_fresh(self):
        """Confirm return is accurate.

        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet fresh, identification information fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)
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

        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet fresh, ID info fresh, leaf topic stale
        #. Case: Sheet fresh, ID info fresh, last topic stale
        #. Case: Sheet fresh, ID info fresh, topics fresh
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            topic = XTOPIC.Topic(p_name='Topic {}'.format(i))
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        parent = target._topics._gtk_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = XTOPIC.Topic(p_name=name)
            parent = target.insert_topic_child(topic, parent)
        I_LEAF = 2
        I_LAST = 4
        # Test: Sheet stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        assert not target.is_stale()
        assert not target._stale
        # Test: Sheet fresh, ID info fresh, leaf topic stale
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._topics.indices()):
            topic = target._topics.get_item(index)
            if i == I_LEAF:
                topic.set_stale()
            else:
                topic.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, last topic stale
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._topics.indices()):
            topic = target._topics.get_item(index)
            if i == I_LAST:
                topic.set_stale()
            else:
                topic.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: Sheet fresh, ID info fresh, topics fresh
        target._stale = False
        target._infoid.set_fresh()
        for i, index in enumerate(target._topics.indices()):
            topic = target._topics.get_item(index)
            topic.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    def test_n_pages(self, patch_class_page_sheet):
        """Confrim reported number of pages."""
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        # Test
        for i, page in enumerate(pages):
            assert i == target.n_pages()
            target.attach_page(page)
        assert N_PAGES == target.n_pages()

    def test_present_pages(self, patch_class_page_sheet):
        """Confirm all pages get present notice."""
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            target.attach_page(page)
        NO_TIME = 0
        # Test
        target.present_pages(NO_TIME)
        for page in pages:
            assert page.called_present

    def test_set_fresh(self):
        """Confirm all attributes set.

        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet stale, identification information stale
        #. Case: Sheet fresh, topics stale
        #. Case: Sheet stale, topics stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)

        N_TOPICS = 3
        for i in range(N_TOPICS):
            topic = XTOPIC.Topic(p_name='Topic {}'.format(i))
            target.insert_topic_before(topic, None)
        N_DESCEND = 2
        parent = target._topics._gtk_model.get_iter_first()
        for j in range(N_DESCEND):
            name = '\t'*(j+1) + 'Topic {}'.format(j + N_TOPICS)
            topic = XTOPIC.Topic(p_name=name)
            parent = target.insert_topic_child(topic, parent)
        # Test: Sheet fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet fresh, topics stale
        target._false = True
        target._infoid.set_stale()
        for i, index in enumerate(target._topics.indices()):
            topic = target._topics.get_item(index)
            if i % 2:
                topic.set_stale()
            else:
                topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        for index in target._topics.indices():
            topic = target._topics.get_item(index)
            assert topic.is_fresh()
        # Test: Sheet stale, topics stale
        target._stale = True
        target._infoid.set_stale()
        for i, index in enumerate(target._topics.indices()):
            topic = target._topics.get_item(index)
            if not i % 2:
                topic.set_stale()
            else:
                topic.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._infoid.is_fresh()
        for index in target._topics.indices():
            topic = target._topics.get_item(index)
            assert topic.is_fresh()

    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet stale, identification information stale
        #. Case: Sheet fresh, ID info fresh, topics fresh
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)
        # Test: Sheet fresh, identification information fresh
        target._stale = False
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet stale, identification information fresh
        target._stale = True
        target._infoid.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        # Test: Sheet fresh, identification information stale
        target._stale = False
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Sheet stale, identification information stale
        target._stale = True
        target._infoid.set_stale()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_stale()
        # Test: Sheet fresh, ID info fresh, topics fresh
        target._stale = True
        target._infoid.set_fresh()
        for index in target._topics.indices():
            topic = target._topics.get_item(index)
            topic.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._infoid.is_fresh()
        for index in target._topics.indices():
            topic = target._topics.get_item(index)
            assert topic.is_fresh()

    def test_update_titles(self, patch_class_page_sheet):
        """Confirm all pages get update notice."""
        # Setup
        NAME_MODEL = 'The Larch'
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_name=NAME_MODEL, p_title=TITLE_MODEL)
        SUBTITLE_BASE = '/home/larch.fsg'
        SUBTITLE_TARGET = (
            r'/home/larch\.fsg \([0-9A-Fa-f]{3}:[0-9A-Fa-f]{3}\)')

        N_PAGES = 3
        pages = [patch_class_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            target.attach_page(page)
        # Test
        target.update_titles(SUBTITLE_BASE)
        for page in pages:
            assert page.called_set_titles
            assert re.match(SUBTITLE_TARGET, page.subtitle)

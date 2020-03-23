"""
Unit tests for :mod:`~factsheet.model` for Factsheet document.
"""
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

from factsheet.model import infoid as MINFOID
from factsheet.model import sheet as MSHEET
from factsheet.view import page_sheet as VSHEET


@pytest.fixture
def factory_page_sheet(patch_factsheet, capfd):
    """Test fixture based on `test_page_sheet.ui` definition."""
    def new_page_sheet():
        PATH_DIR_UI_TEST = Path(__file__).parent.parent / 'view'
        NAME_FILE_UI_TEST = str(PATH_DIR_UI_TEST / 'test_page_sheet.ui')
        PatchPageSheet = VSHEET.PageSheet
        PatchPageSheet.NAME_FILE_SHEET_UI = NAME_FILE_UI_TEST

        factsheet = patch_factsheet()
        page_sheet = PatchPageSheet(px_app=factsheet)
        _snapshot = capfd.readouterr()   # Resets the internal buffer
        return page_sheet

    return new_page_sheet


class TestSheet:
    """Unit tests for :mod:`~factsheet.model` class :class:`Sheet`."""

    def test_eq(self):
        """Confirm equivalence operator

        #. Case: type difference
        #. Case: InfoId difference
        #. Case: Equivalence
        """
        # Setup
        TITLE_SOURCE = 'Parrot Sketch.'
        source = MSHEET.Sheet(p_title=TITLE_SOURCE)
        # Test: type difference
        assert not source.__eq__(TITLE_SOURCE)
        # Test: InfoId difference
        TITLE_TARGET = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_TARGET)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = MSHEET.Sheet(p_title=TITLE_SOURCE)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_get_set_state(self, tmp_path, factory_page_sheet):
        """Confirm conversion to and from pickle format."""
        # Setup
        path = Path(str(tmp_path / 'get_set.fsg'))

        TITLE_MODEL = 'Something completely different.'
        source = MSHEET.Sheet(p_title=TITLE_MODEL)
        source._stale = True

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            source.attach_page(page)
        # Test
        with path.open(mode='wb') as io_out:
            pickle.dump(source, io_out)

        with path.open(mode='rb') as io_in:
            target = pickle.load(io_in)

        assert source._infoid == target._infoid
        assert not target._stale
        assert isinstance(target._pages, dict)
        assert not target._pages
        # Teardown
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

    def test_init(self):
        """Confirm initialization."""
        # Setup
        ASPECT = MSHEET.Sheet.ASPECT
        TEXT_TITLE = 'Something completely different'
        # Test
        target = MSHEET.Sheet(p_title=TEXT_TITLE)
        assert not target._stale
        assert isinstance(target._pages, dict)
        assert not target._pages
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert ASPECT == target._infoid.aspect
        assert TEXT_TITLE == target._infoid.title

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        TEXT_TITLE_DEFAULT = ''
        # Test
        target = MSHEET.Sheet()
        assert TEXT_TITLE_DEFAULT == target._infoid.title

    def test_attach_page(self, factory_page_sheet):
        """Confirm page addition.
        Case: page not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        # Test
        for page in pages:
            target.attach_page(page)
            assert target._infoid.title == page.get_infoid().title
            assert target._pages[id(page)] is page
        assert len(pages) == len(target._pages)
        # Teardown
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

    def test_attach_page_warn(
            self, factory_page_sheet, PatchLogger, monkeypatch):
        """Confirm page addition.
        Case: page attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
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
        # Teardown
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

    def test_detach_all(self, monkeypatch, factory_page_sheet):
        """Confirm notifications and removals."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.n_calls = 0

            def detach_view(self, _v): self.n_calls += 1

        patch_detach = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_detach.detach_view)

        class PatchPage:
            def __init__(self): self.n_calls = 0

            def close_page(self): self.n_calls += 1

        patch_close = PatchPage()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'close_page', patch_close.close_page)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
        for page in pages:
            target.attach_page(page)
        assert N_PAGES == len(target._pages)
        # Test
        target.detach_all()
        assert not target._pages
        assert N_PAGES == patch_detach.n_calls
        assert N_PAGES == patch_close.n_calls
        # Teardown
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

    def test_detach_page(self, monkeypatch, factory_page_sheet):
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
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
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
        # Teardown
        app = page_rem._window.get_application()
        page_rem._window.destroy()
        del page_rem._window
        del app
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

    def test_detach_page_views(self, monkeypatch, factory_page_sheet):
        """Confirm removal of views."""
        # Setup
        class PatchInfoIdModel:
            def __init__(self): self.called = False

            def detach_view(self, _v): self.called = True

        patch_infoid = PatchInfoIdModel()
        monkeypatch.setattr(
            MINFOID.InfoId, 'detach_view', patch_infoid.detach_view)

        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        page = factory_page_sheet()
        target.attach_page(page)
        # Test
        target._detach_page_views(page)
        assert patch_infoid.called
        # Teardown
        app = page._window.get_application()
        page._window.destroy()
        del page._window
        del app

    def test_detach_page_warn(
            self, factory_page_sheet, PatchLogger, monkeypatch):
        """Confirm page removal.
        Case: page not attached initially
        """
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
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
        # Teardown
        app = page_dup._window.get_application()
        page_dup._window.destroy()
        del page_dup._window
        del app
        for page in pages:
            app = page._window.get_application()
            page._window.destroy()
            del page._window
            del app

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
        """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)
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

    def test_n_pages(self, factory_page_sheet):
        """Confrim reported number of pages."""
        # Setup
        TITLE_MODEL = 'Something completely different.'
        target = MSHEET.Sheet(p_title=TITLE_MODEL)

        N_PAGES = 3
        pages = [factory_page_sheet() for _ in range(N_PAGES)]
        assert pages[0].get_infoid().title != target._infoid.title
        # Test
        for i, page in enumerate(pages):
            assert i == target.n_pages()
            target.attach_page(page)
        assert N_PAGES == target.n_pages()

#     def test_present_pages(self, monkeypatch, factory_page_sheet):
#         """Confirm presentation of all pages of a factsheet."""
#         # Setup
#         def patch_present(self):
#             self._window.set_visible(True)
# 
#         monkeypatch.setattr(
#             VSHEET.PageSheet, 'present', patch_present, False)
# 
#         TITLE_MODEL = 'Something completely different.'
#         target = MSHEET.Sheet(p_title=TITLE_MODEL)
# 
#         N_PAGES = 3
#         pages = [factory_page_sheet() for _ in range(N_PAGES)]
#         assert pages[0].get_infoid().title != target._infoid.title
#         for page in pages:
#             target.attach_page(page)
#             page.hide()
#             assert not page._window.get_visible()
#         # Test
#         target.present_pages()
#         for page in pages:
#             assert page._window.get_visible()
#         # Teardown
#         for page in pages:
#             app = page._window.get_application()
#             page._window.destroy()
#             del page._window
#             del app

    def test_set_fresh(self):
        """Confirm all attributes set.

        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet stale, identification information stale
         """
        # Setup
        TEXT_TITLE = 'Something completely different'
        target = MSHEET.Sheet(p_title=TEXT_TITLE)
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

    def test_set_stale(self):
        """Confirm all attributes set.

        #. Case: Sheet fresh, identification information fresh
        #. Case: Sheet stale, identification information fresh
        #. Case: Sheet fresh, identification information stale
        #. Case: Sheet stale, identification information stale
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

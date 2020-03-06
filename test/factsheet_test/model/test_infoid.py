"""
Unit tests for Factsheet :mod:`~factsheet.model` component
identification information.

See :mod:`.infoid`.
"""
import copy
import gi   # type: ignore[import]
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.model import infoid as MINFOID
from factsheet.view import view_infoid as VINFOID
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def factory_view_infoid():
    """Test fixture based on `test_view_infoid.ui`."""
    def new_view_info():
        PATH_DIR_UI = Path(__file__).parent.parent / 'view'
        NAME_FILE_UI = str(PATH_DIR_UI / 'test_view_infoid.ui')

        builder = Gtk.Builder.new_from_file(NAME_FILE_UI)
        get_object = builder.get_object
        view_infoid = VINFOID.ViewInfoId(get_object)
        return view_infoid

    return new_view_info


@pytest.fixture
def args_infoid_stock():
    return dict(
        p_aspect='section',
        # p_name='Stock InfoId Name',
        p_title='Stock InfoId Title',
        # p_summary='This summarizes a stock identification.',
        )


class TestInfoId:
    """Unit tests for :class:`.InfoId`."""

    def test_eq(self, args_infoid_stock):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: title difference.
        #. Case: aspect difference.
        #. Case: equivalent
        """
        # Setup
        source = MINFOID.InfoId(**args_infoid_stock)
        # Test: type difference.
        assert not source.__eq__('Something completely different')
        # Test: aspect difference.
        target = copy.deepcopy(source)
        target._aspect = 'Something completely different'
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target._title._buffer.set_text('Something completely different', -1)
        assert not source.__eq__(target)
        # Test: equivalent
        target = copy.deepcopy(source)
        target._stale = True
        view = UI.FACTORY_INFOID.new_view_title()
        target._title.attach_view(view)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, args_infoid_stock):
        """Confirm initialization."""
        # Setup
        # Test
        target = MINFOID.InfoId(**args_infoid_stock)

        assert args_infoid_stock['p_aspect'] == target._aspect
        assert id(target) == target._id_model
        assert not target._stale

        assert isinstance(target._title, ABC_INFOID.AbstractTextModel)
        assert args_infoid_stock['p_title'] == str(target._title)

    def test_init_default(self, args_infoid_stock):
        """Confirm initialization with default arguments."""
        # Setup
        # Test
        target = MINFOID.InfoId(p_aspect=args_infoid_stock['p_aspect'])
        assert '' == str(target._title)

    def test_attach_view(self, factory_view_infoid, args_infoid_stock):
        """Confirm view addition."""
        # Setup
        TEXT_TITLE_UI = 'Page title'
        view_infoid = factory_view_infoid()
        assert TEXT_TITLE_UI == view_infoid._view_title.get_text()

        target = MINFOID.InfoId(**args_infoid_stock)
        # Test
        target.attach_view(view_infoid)
        assert view_infoid.title == str(target._title)

    def test_detach_view(self, factory_view_infoid, args_infoid_stock):
        """Confirm view removal."""
        # Setup
        TEXT_TITLE_UI = 'Page title'
        view_infoid = factory_view_infoid()
        assert TEXT_TITLE_UI == view_infoid._view_title.get_text()

        target = MINFOID.InfoId(**args_infoid_stock)
        target.attach_view(view_infoid)
        assert view_infoid._view_title.get_text() == str(target._title)
        # Test
        target.detach_view(view_infoid)
        assert args_infoid_stock['p_title'] == str(target._title)
        assert '' == view_infoid._view_title.get_text()

    def test_is_fresh(self, args_infoid_stock):
        """Confirm return is accurate.

        #. Case: InfoId stale, title fresh
        #. Case: InfoId fresh, title stale
        #. Case: InfoId fresh, title fresh
        """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId stale, title fresh
        target._stale = True
        target._title.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, title stale
        target._stale = False
        target._title.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        assert target.is_fresh()
        assert not target._stale

    def test_is_stale(self, args_infoid_stock):
        """Confirm return is accurate.

        #. Case: InfoId stale, title fresh
        #. Case: InfoId fresh, title stale
        #. Case: InfoId fresh, title fresh
        """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId stale, title fresh
        target._stale = True
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, title stale
        target._stale = False
        target._title.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    @pytest.mark.parametrize('name_attr, name_prop', [
        ['_aspect', 'aspect'],
        ['_id_model', 'id_model'],
        ['_title', 'title'],
        ])
    def test_property(self, args_infoid_stock, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: read
        #. Case: no replace
        #. Case: no delete
        """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        value_attr = getattr(target, name_attr)
        target_prop = getattr(MINFOID.InfoId, name_prop)
        value_prop = getattr(target, name_prop)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_set_fresh(self, args_infoid_stock):
        """Confirm all attributes set.

        #. Case: InfoId fresh, title fresh
        #. Case: InfoId stale, title fresh
        #. Case: InfoId fresh, title stale
        #. Case: InfoId stale, title stale
         """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: InfoId stale, title fresh
        target._stale = True
        target._title.set_fresh()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: InfoId fresh, title stale
        target._stale = False
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()
        # Test: InfoId stale, title stale
        target._stale = True
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._title.is_fresh()

    def test_set_stale(self, args_infoid_stock):
        """Confirm all attributes set.

        #. Case: InfoId fresh, title fresh
        #. Case: InfoId stale, title fresh
        #. Case: InfoId fresh, title stale
        #. Case: InfoId stale, title stale
         """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId fresh, title fresh
        target._stale = False
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._title.is_fresh()
        # Test: InfoId stale, title fresh
        target._stale = True
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._title.is_fresh()
        # Test: InfoId fresh, title stale
        target._stale = False
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._title.is_stale()
        # Test: InfoId stale, title stale
        target._stale = True
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._title.is_stale()

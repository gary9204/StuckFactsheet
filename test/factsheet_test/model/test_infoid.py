"""
Unit tests for Factsheet :mod:`~factsheet.model` component
identification information.

See :mod:`.infoid`.
"""
import copy
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.model import infoid as MINFOID
from factsheet.view import ui as UI


@pytest.fixture
def args_infoid_target():
    return dict(
        p_aspect='section',
        p_name='Target InfoId Name',
        p_title='Target InfoId Title',
        p_summary='This summarizes target identification.',
        )


class TestInfoId:
    """Unit tests for :class:`.InfoId`."""

    def test_eq(self, args_infoid_target):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: aspect difference.
        #. Case: name difference.
        #. Case: summary difference.
        #. Case: title difference.
        #. Case: equivalent
        """
        # Setup
        source = MINFOID.InfoId(**args_infoid_target)
        # Test: type difference.
        assert not source.__eq__('Something completely different')
        # Test: aspect difference.
        target = copy.deepcopy(source)
        target._aspect = 'Something completely different'
        assert not source.__eq__(target)
        # Test: name difference.
        target = copy.deepcopy(source)
        target._name._buffer.set_text('Something completely different', -1)
        assert not source.__eq__(target)
        # Test: summary difference.
        target = copy.deepcopy(source)
        target._summary._buffer.set_text(
            'Something completely different', -1)
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

        assert isinstance(target._name, ABC_INFOID.AbstractTextModel)
        assert args_infoid_stock['p_name'] == str(target._name)

        assert isinstance(target._summary, ABC_INFOID.AbstractTextModel)
        assert args_infoid_stock['p_summary'] == str(target._summary)

        assert isinstance(target._title, ABC_INFOID.AbstractTextModel)
        assert args_infoid_stock['p_title'] == str(target._title)

    def test_init_default(self, args_infoid_stock):
        """Confirm initialization with default arguments."""
        # Setup
        # Test
        target = MINFOID.InfoId(p_aspect=args_infoid_stock['p_aspect'])
        assert '' == str(target._name)
        assert '' == str(target._summary)
        assert '' == str(target._title)

    def test_attach_view(self, patch_class_view_infoid, args_infoid_target):
        """Confirm view addition."""
        # Setup
        patch_view = patch_class_view_infoid()

        target = MINFOID.InfoId(**args_infoid_target)
        # Test
        target.attach_view(patch_view)
        assert patch_view.name == str(target._name)
        assert patch_view.summary == str(target._summary)
        assert patch_view.title == str(target._title)

    def test_detach_view(self, patch_class_view_infoid, args_infoid_target):
        """Confirm view removal."""
        # Setup
        patch_view = patch_class_view_infoid()

        target = MINFOID.InfoId(**args_infoid_target)
        target.attach_view(patch_view)
        patch_view._name.set_visible(True)
        assert patch_view.summary == str(target._summary)
        patch_view._title.set_visible(True)
        # Test
        target.detach_view(patch_view)
        assert not patch_view._name.get_visible()
        assert patch_view.summary != str(target._summary)
        assert not patch_view._title.get_visible()

    def test_is_fresh(self, args_infoid_stock):
        """Confirm return is accurate.

        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name stale, summary fresh, title fresh
        #. Case: InfoId fresh, name fresh, summary stale, title fresh
        #. Case: InfoId fresh, name fresh, summary fresh, title stale
        #. Case: InfoId fresh, name, summary, and title fresh
        """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId stale, name and title fresh
        target._stale = True
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, name stale, summary fresh, title fresh
        target._stale = False
        target._name.set_stale()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, name fresh, summary stale, title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_stale()
        target._title.set_fresh()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, name fresh, summary fresh, title stale
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_stale()
        assert not target.is_fresh()
        assert target._stale
        # Test: InfoId fresh, name, summary, and title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert target.is_fresh()
        assert not target._stale

    def test_is_stale(self, args_infoid_stock):
        """Confirm return is accurate.

        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name stale, summary fresh, title fresh
        #. Case: InfoId fresh, name fresh, summary stale, title fresh
        #. Case: InfoId fresh, name fresh, summary fresh, title stale
        #. Case: InfoId fresh, name, summary, and title fresh
        """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId stale, name, summary, and title fresh
        target._stale = True
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, name stale, summary fresh, title fresh
        target._stale = False
        target._name.set_stale()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, name fresh, summary stale, title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_stale()
        target._title.set_fresh()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, name fresh, summary fresh, title stale
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_stale()
        assert target.is_stale()
        assert target._stale
        # Test: InfoId fresh, name, summary and title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        assert not target.is_stale()
        assert not target._stale

    @pytest.mark.parametrize('name_attr, name_prop', [
        ['_aspect', 'aspect'],
        ['_id_model', 'id_model'],
        ['_name', 'name'],
        ['_summary', 'summary'],
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

        #. Case: InfoId fresh, name, summary, and title stale
        #. Case: InfoId stale, name, summary, and title stale
         """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId fresh, name and title stale
        target._stale = False
        target._name.set_stale()
        target._summary.set_stale()
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._name.is_fresh()
        assert target._summary.is_fresh()
        assert target._title.is_fresh()
        # Test: InfoId stale, name and title stale
        target._stale = True
        target._name.set_stale()
        target._summary.set_stale()
        target._title.set_stale()
        target.set_fresh()
        assert not target._stale
        assert target._name.is_fresh()
        assert target._summary.is_fresh()
        assert target._title.is_fresh()

    def test_set_stale(self, args_infoid_stock):
        """Confirm all attributes set.

        #. Case: InfoId fresh, name, summary, and title fresh
        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name, summary, and title stale
        #. Case: InfoId stale, name, summary, and title stale
         """
        # Setup
        target = MINFOID.InfoId(**args_infoid_stock)
        # Test: InfoId fresh, name, summary, and title fresh
        target._stale = False
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._name.is_fresh()
        assert target._summary.is_fresh()
        assert target._title.is_fresh()
        # Test: InfoId stale, name, summary, and title fresh
        target._stale = True
        target._name.set_fresh()
        target._summary.set_fresh()
        target._title.set_fresh()
        target.set_stale()
        assert target._stale
        assert target._name.is_fresh()
        assert target._summary.is_fresh()
        assert target._title.is_fresh()
        # Test: InfoId fresh, name, summary, and title stale
        target._stale = False
        target._name.set_stale()
        target._summary.set_stale()
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._name.is_stale()
        assert target._summary.is_stale()
        assert target._title.is_stale()
        # Test: InfoId stale, name, summary, and title stale
        target._stale = True
        target._name.set_stale()
        target._summary.set_stale()
        target._title.set_stale()
        target.set_stale()
        assert target._stale
        assert target._name.is_stale()
        assert target._summary.is_stale()
        assert target._title.is_stale()

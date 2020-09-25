"""
Unit tests for Factsheet :mod:`~factsheet.model` component
identification information.  See :mod:`.infoid`.
"""
import copy
import dataclasses as DC
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.model import infoid as MINFOID
from factsheet.adapt_gtk import adapt_infoid as AINFOID


class TestInfoId:
    """Unit tests for :class:`.InfoId`."""

    def test_eq(self, patch_args_infoid):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: name difference.
        #. Case: summary difference.
        #. Case: title difference.
        #. Case: equivalent
        """
        # Setup
        ARGS = patch_args_infoid
        source = MINFOID.InfoId()
        source.init_identity(**DC.asdict(ARGS))
        TEXT = 'Something completely different.'
        # Test: type difference.
        assert not source.__eq__(TEXT)
        # Test: name difference.
        target = copy.deepcopy(source)
        target._name._buffer.set_text(TEXT, -1)
        assert not source.__eq__(target)
        # Test: summary difference.
        target = copy.deepcopy(source)
        target._summary._buffer.set_text(TEXT, -1)
        assert not source.__eq__(target)
        # Test: title difference.
        target = copy.deepcopy(source)
        target._title._buffer.set_text(TEXT, -1)
        assert not source.__eq__(target)
        # Test: equivalent
        target = copy.deepcopy(source)
        target._stale = True
        # view = UI.FACTORY_INFOID.new_view_title()
        view = AINFOID.AdaptEntry()
        target._title.attach_view(view)
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        BLANK = ''
        # Test
        target = MINFOID.InfoId()

        assert BLANK == str(target._name)
        assert BLANK == str(target._summary)
        assert id(target) == target._tag
        assert BLANK == str(target._title)
        assert not target._stale

    def test_init_identity(self, patch_args_infoid):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        # Test
        target.init_identity(**DC.asdict(ARGS))

        assert isinstance(target._name, ABC_INFOID.AbstractTextModel)
        assert ARGS.p_name == str(target._name)

        assert isinstance(target._summary, ABC_INFOID.AbstractTextModel)
        assert ARGS.p_summary == str(target._summary)

        assert isinstance(target._title, ABC_INFOID.AbstractTextModel)
        assert ARGS.p_title == str(target._title)

    def test_init_identity_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        BLANK = ''
        TEXT = 'Something completely different.'
        target = MINFOID.InfoId()
        target._name._buffer.set_text(TEXT, -1)
        target._summary._buffer.set_text(TEXT, -1)
        target._title._buffer.set_text(TEXT, -1)
        # Test
        target.init_identity()
        assert BLANK == str(target._name)
        assert BLANK == str(target._summary)
        assert BLANK == str(target._title)

    def test_attach_view(self, interface_view_infoid, patch_args_infoid):
        """Confirm view addition."""
        # Setup
        patch_view = interface_view_infoid()
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
        # Test
        target.attach_view(patch_view)
        assert patch_view.name == str(target._name)
        assert patch_view.summary == str(target._summary)
        assert patch_view.title == str(target._title)

    def test_detach_view(self, interface_view_infoid, patch_args_infoid):
        """Confirm view removal."""
        # Setup
        patch_view = interface_view_infoid()
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
        target.attach_view(patch_view)
        patch_view._name.set_visible(True)
        assert patch_view.summary == str(target._summary)
        patch_view._title.set_visible(True)
        # Test
        target.detach_view(patch_view)
        assert not patch_view._name.get_visible()
        assert patch_view.summary != str(target._summary)
        assert not patch_view._title.get_visible()

    def test_is_fresh(self, patch_args_infoid):
        """Confirm return is accurate.

        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name stale, summary fresh, title fresh
        #. Case: InfoId fresh, name fresh, summary stale, title fresh
        #. Case: InfoId fresh, name fresh, summary fresh, title stale
        #. Case: InfoId fresh, name, summary, and title fresh
        """
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
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

    def test_is_stale(self, patch_args_infoid):
        """Confirm return is accurate.

        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name stale, summary fresh, title fresh
        #. Case: InfoId fresh, name fresh, summary stale, title fresh
        #. Case: InfoId fresh, name fresh, summary fresh, title stale
        #. Case: InfoId fresh, name, summary, and title fresh
        """
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
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
        ['_name', 'name'],
        ['_summary', 'summary'],
        ['_tag', 'tag'],
        ['_title', 'title'],
        ])
    def test_property(self, patch_args_infoid, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
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

    def test_set_fresh(self, patch_args_infoid):
        """Confirm all attributes set.

        #. Case: InfoId fresh, name, summary, and title stale
        #. Case: InfoId stale, name, summary, and title stale
         """
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
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

    def test_set_stale(self, patch_args_infoid):
        """Confirm all attributes set.

        #. Case: InfoId fresh, name, summary, and title fresh
        #. Case: InfoId stale, name, summary, and title fresh
        #. Case: InfoId fresh, name, summary, and title stale
        #. Case: InfoId stale, name, summary, and title stale
         """
        # Setup
        ARGS = patch_args_infoid
        target = MINFOID.InfoId()
        target.init_identity(**DC.asdict(ARGS))
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


class TestTypes:
    """Unit tests for type definitions in :mod:`.infoid`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert MINFOID.TagInfoId is not None

"""
Unit tests for identification information abstract data type classes.

See :mod:`.abc_infoid`.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.adapt_gtk import adapt_view as AVIEW


class TestAbstractTextModel:
    """Unit tests for interfaces common to model text attributes.
    See :class:`.AbstractTextModel`."""

    def test_abstract(self):
        """Confirm class is abstract."""
        # No Setup
        # Test
        with pytest.raises(TypeError):
            _target = ABC_INFOID.AbstractTextModel()

    def test_eq(self):
        """Confirm equivalence comparison.

        #. Case: different type
        #. Case: different text
        #. Case: same text
        #. Case: confirm not-equal defined
        """
        # Setup
        class PatchTextModel(ABC_INFOID.AbstractTextModel):
            def __init__(self, p_text): self.text = p_text

            def __str__(self): return self.text

            def attach_view(self, _v): pass

            def detach_view(self, _v): pass

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        text = 'The Spanish Inquisition'
        source = PatchTextModel(text)
        # Test: different type
        target = text
        assert not source.__eq__(target)
        # Test: different text
        target = PatchTextModel('Something completely different')
        assert not source.__eq__(target)
        # Test: same text
        target = PatchTextModel(text)
        assert source.__eq__(target)
        # Test: confirm not-equal defined
        assert not source.__ne__(target)

    @pytest.mark.parametrize('name_method', [
        '__str__',
        'attach_view',
        'detach_view',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchTextModel(ABC_INFOID.AbstractTextModel):
            def __eq__(self, _o): return False

            def __str__(self): super().__str__()

            def attach_view(self): super().attach_view(None)

            def detach_view(self): super().detach_view(None)

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchTextModel()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


# class TestAbstractTextView:
#     """Unit tests for type :data:`.AbstractTextView`."""
#
#     def test_constraints(self):
#         """Confirm definition of :data:`.AbstractTextView`."""
#         # Setup
#         constraints = [AVIEW.AdaptEntry, AVIEW.AdaptTextView]
#         # Test
#         target = ABC_INFOID.AbstractTextView.__constraints__
#         for c in constraints:
#             assert c in target
#         assert len(constraints) == len(target)


class TestInterfaceViewInfoId:
    """Unit tests for :class:`.InterfaceViewInfoId`."""

    def test_abstract(self):
        """Confirm class is abstract."""
        # No Setup
        # Test
        with pytest.raises(TypeError):
            _target = ABC_INFOID.InterfaceViewInfoId()

    @pytest.mark.parametrize('name_method', [
        'get_view_title',
        'title',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchInterface(ABC_INFOID.InterfaceViewInfoId):
            def get_view_title(self): super().get_view_title()

            def title(self): super().title()

        target = PatchInterface()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()

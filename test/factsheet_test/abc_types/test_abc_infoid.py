"""
Unit tests for identification information abstract classes and
interfaces.

See :mod:`.abc_infoid`.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_infoid as ABC_INFOID


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


class TestInterfaceViewInfoId:
    """Unit tests for :class:`.InterfaceViewInfoId`."""

    def test_abstract(self):
        """Confirm class is abstract."""
        # No Setup
        # Test
        with pytest.raises(TypeError):
            _target = ABC_INFOID.InterfaceViewInfoId()

    @pytest.mark.parametrize('name_method', [
        'get_view_name',
        'get_view_summary',
        'get_view_title',
        # 'name',
        # 'summary',
        # 'title',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchInterface(ABC_INFOID.InterfaceViewInfoId):
            def get_view_name(self): super().get_view_name()

            def get_view_summary(self): super().get_view_summary()

            def get_view_title(self): super().get_view_title()

        target = PatchInterface()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()

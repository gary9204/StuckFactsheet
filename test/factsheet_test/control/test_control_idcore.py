"""
Unit tests for generic control to add and remove views of
:class:`~.IdCore` identity attributes.  See :mod:`~.control_idcore`.
"""
import pytest   # type: ignore[import]

import factsheet.control.control_idcore as CIDCORE
import factsheet.model.idcore as MIDCORE


PatchControl = CIDCORE.ControlIdCore[
    MIDCORE.ViewNameActive, MIDCORE.ViewSummaryActive, MIDCORE.ViewTitleActive]


class TestControlIdCore:
    """Unit tests for :class:`.ControlIdCore`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (CIDCORE.ControlIdCore, 'new_view_name'),
        (CIDCORE.ControlIdCore, 'new_view_summary'),
        (CIDCORE.ControlIdCore, 'new_view_title'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    # def test_init(self, patch_idcore):
    #     """Confirm initialization."""
    #     # Setup
    #     NAME = 'Parrot'
    #     SUMMARY = 'The parrot is a Norwegian Blue.'
    #     TITLE = 'The Parrot Sketch'
    #     IDCORE = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     # Test
    #     target = PatchControl(p_idcore=IDCORE)
    #     assert target._idcore is IDCORE

    # @pytest.mark.parametrize('NEW_VIEW, ATTR', [
    #     ('new_view_name', '_name'),
    #     ('new_view_summary', '_summary'),
    #     ('new_view_title', '_title'),
    #     ])
    # def test_new_view(self, patch_idcore, NEW_VIEW, ATTR):
    #     """Confirm control relays requests to identity."""
    #     # Setup
    #     NAME = 'Parrot'
    #     SUMMARY = 'The parrot is a Norwegian Blue.'
    #     TITLE = 'The Parrot Sketch'
    #     IDCORE = patch_idcore(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     target = PatchControl(p_idcore=IDCORE)
    #     new_view = getattr(target, NEW_VIEW)
    #     attr = getattr(IDCORE, ATTR)
    #     # Test
    #     view = new_view()
    #     assert view.get_buffer() is attr._model

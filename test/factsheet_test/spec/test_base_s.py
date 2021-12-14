"""
Unit tests for base classes for topic specification.  See
:class:`~.spec.base_s.Base`.
"""
import pytest  # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.topic as MTOPIC
import factsheet.spec.base_s as SBASE


class TestBase:
    """Unit tests for :class:`~.spec.base_s.Base`."""

    def test_init(self):
        """| Confirm initialization.
        | Case: TBD
        """
        # Setup
        NAME_SPEC = 'Spec'
        # Test
        target = SBASE.Base(p_name=NAME_SPEC)
        assert isinstance(target._name_spec, BUI.ModelTextMarkup)
        assert NAME_SPEC == target._name_spec.text

    def test_init_name_topic(self):
        """| Confirm initialization.
        | Case: topic name store and view factories
        """
        # Setup
        BLANK = ''
        NAME_SPEC = 'Spec'
        # Test
        target = SBASE.Base(p_name=NAME_SPEC)
        assert isinstance(target._name_topic, MTOPIC.Name)
        assert BLANK == target._name_topic.text
        assert isinstance(
            target._new_display_name_topic, BUI.FactoryDisplayTextMarkup)
        assert target._new_display_name_topic._ui_model is (
            target._name_topic._ui_model)
        assert isinstance(
            target._new_editor_name_topic, BUI.FactoryEditorTextMarkup)
        assert target._new_editor_name_topic._ui_model is (
            target._name_topic._ui_model)

    @pytest.mark.parametrize('CONSTANT, VALUE', [
        (SBASE.Base.MARK_FILE_SPEC, '_s.py'),
        (SBASE.Base.MARK_FILE_ASSIST, '_a.ui'),
        ])
    def test_constants(self, CONSTANT, VALUE):
        """Confirm class contant definitions."""
        # Setup
        # Test
        assert CONSTANT == VALUE

    def test_reset(self):
        """Confirm default topic identity and location restored."""
        # Setup
        BLANK = ''
        NAME_SPEC = 'Spec'
        target = SBASE.Base(p_name=NAME_SPEC)
        target._name_topic._set_persist('Oops!')
        # Test
        target.reset()
        assert BLANK == target._name_topic.text

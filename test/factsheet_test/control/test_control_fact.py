"""
Unit test for control that provides views of :class:`~.Fact'
attributes.  See :mod:`~.control_fact`.
"""
import pytest  # type: ignore[import]

import factsheet.control.control_fact as CFACT


@pytest.fixture
def control_sample(fact_sample):
    """Fixture to return factory for sample controls."""
    def _new_control(p_fact=None):
        fact = p_fact
        if fact is None:
            fact = fact_sample()
            NOTE = 'Something completely different'
            fact._note.text = NOTE
            VALUE = 'This parrot is no more'
            fact._value = VALUE
            fact.check()
        control = CFACT.ControlFact(p_fact=fact)
        return control

    return _new_control


@pytest.fixture
def views_aspect(request, control_sample):
    """| Fixture to return corresponding views from a control and its fact.
    | Case: named aspect views
    """
    name_aspect = request.param
    control = control_sample()
    view_control = control.new_view_aspect(p_name_aspect=name_aspect)
    view_fact = control._fact.new_view_aspect(p_name_aspect=name_aspect)
    yield view_fact, view_control
    # Teardown
    view_fact.destroy()
    view_control.destroy()


@pytest.fixture
def views(request, control_sample):
    """| Fixture to return corresponding views from a control and its fact.
    | Case: mutable text views
    """
    name_method = request.param
    control = control_sample()
    method_control = getattr(control, name_method)
    view_control = method_control()
    method_fact = getattr(control._fact, name_method)
    view_fact = method_fact()
    yield view_fact, view_control
    # Teardown
    view_fact.destroy()
    view_control.destroy()


class TestControlFact:
    """Unit tests for :class:`.ControlFact`."""

    def test_init(self, fact_sample):
        """Confirm initialization."""
        # Setup
        FACT = fact_sample()
        # Test
        target = CFACT.ControlFact(p_fact=FACT)
        assert target._fact is FACT

    @pytest.mark.parametrize('views_aspect', [
        'Plain',
        'Oops',
        ], indirect=True)
    def test_new_view_aspect(self, views_aspect):
        """| Confirm view associated with attribute of fact.
        | Case: named aspect attributes
        """
        # Setup
        view_fact, view_control = views_aspect
        # Test
        assert isinstance(view_control, type(view_fact))
        assert view_fact.get_label() == view_control.get_label()

    @pytest.mark.parametrize('views, NAME_GET', [
        ('new_view_name', 'get_buffer'),
        ('new_view_names_aspects', 'get_model'),
        ('new_view_note', 'get_buffer'),
        ('new_view_status', 'get_label'),
        ('new_view_summary', 'get_buffer'),
        ('new_view_title', 'get_buffer'),
        ('new_view_tag', 'get_label'),
        ], indirect=['views'])
    def test_new_view(self, views, NAME_GET):
        """| Confirm view associated with attribute of fact.
        | Case: names of aspects attribute
        """
        # Setup
        view_fact, view_control = views
        fact_get = getattr(view_fact, NAME_GET)
        control_get = getattr(view_control, NAME_GET)
        # Test
        assert isinstance(view_control, type(view_fact))
        assert fact_get() == control_get()

"""
Unit tests for class for collection of views.
See :mod:`.view_stack`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import logging
import pytest  # type: ignore[import]
import collections.abc as CABC

import factsheet.view.view_stack as VSTACK

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestViewStack:
    """Unit tests for :class:`.ViewStack`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VSTACK.ViewStack()
        assert isinstance(target._ui_view, Gtk.Stack)
        assert not target._ui_view.get_children()
        assert isinstance(target._pinned, list)
        assert not target._pinned

    def test_add_view(self):
        """| Confirm add view with name.
        | Case: view not in collection.
        """
        # Setup
        target = VSTACK.ViewStack()
        NAME = 'Parrot'
        VIEW = Gtk.Label(label=NAME)
        VIEW.hide()
        # Test
        target.add_view(VIEW, NAME)
        child = target._ui_view.get_child_by_name(NAME)
        assert child is VIEW
        assert child.get_visible()
        assert NAME == target._ui_view.get_visible_child_name()

    def test_add_view_warn(self, caplog):
        """| Confirm add view with name.
        | Case: view in collection.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 3
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        ID_PRESENT = 1
        name_dup = hex(ID_PRESENT)
        view_dup = Gtk.Label(label='Parrot')
        N_LOGS = 1
        LAST = -1
        log_message = ('Duplicate view \'{}\' for name {} '
                       '(ViewStack.add_view)'.format(view_dup, name_dup))
        # Test
        target.add_view(view_dup, name_dup)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert len(views) == len(target._ui_view)
        view = target._ui_view.get_child_by_name(name_dup)
        assert view is views[ID_PRESENT]

    def test_clear(self):
        """Confirm collection contains only pinned item views."""
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 5
        I_PINNED = [1, 3, 4]
        views = dict()
        pinned = list()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
            if i in I_PINNED:
                pinned.append(views[i])
                target.pin_view(hex(i))
        # Test
        target.clear()
        assert len(pinned) == len(target._ui_view.get_children())
        assert pinned == list(target._ui_view.get_children())

    @pytest.mark.parametrize('VALUE, EXPECT', [
        (42, False),
        ('Oops', False),
        ('0x3', True),
        ])
    def test_contains(self, VALUE, EXPECT):
        """| Confirm containment for in operator.

        :param VALUE: value to test for containment.
        :param EXPECT: expected result.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 5
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        # Test
        assert isinstance(target, CABC.Container)
        result = VALUE in target
        assert result is EXPECT

    def test_get_view_visible(self):
        """| Confirm name of visible view.
        | Case: a view is visible.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 5
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        I_VISIBLE = 1
        name_visible = hex(I_VISIBLE)
        view_visible = views[I_VISIBLE]
        target._ui_view.set_visible_child(view_visible)
        # Test
        assert name_visible == target.get_name_visible()

    def test_get_view_visible_none(self):
        """| Confirm name of visible view.
        | Case: no view is visible.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 5
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
            views[i].hide()
        # Test
        assert target.get_name_visible() is None

    def test_pin_view(self):
        """| Confirm pinning of view by name.
        | Case: collection contains view with name unpinned.
        """
        # Setup
        NAME = 'Parrot'
        VIEW = Gtk.Label(label=NAME)
        target = VSTACK.ViewStack()
        target.add_view(VIEW, NAME)
        # Test
        target.pin_view(NAME)
        assert NAME in target._pinned

    def test_pin_view_absent(self, caplog):
        """| Confirm pinning of view by name.
        | Case: collection does not contains view with given name.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = VSTACK.ViewStack()
        NAME = 'Parrot'
        N_LOGS = 1
        LAST = -1
        log_message = ('No view named \'{}\' (ViewStack.pin_view)'
                       ''.format(NAME))
        # Test
        target.pin_view(NAME)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert not target._pinned

    def test_pin_view_pinned(self, caplog):
        """| Confirm pinning of view by name.
        | Case: collection contains view with name pinned.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = VSTACK.ViewStack()
        NAME = 'Parrot'
        VIEW = Gtk.Label(label='The Parrot Sketch')
        target.add_view(VIEW, NAME)
        target.pin_view(NAME)
        n_pinned = len(target._pinned)
        N_LOGS = 1
        LAST = -1
        log_message = ('View named \'{}\' already pinned '
                       '(ViewStack.pin_view)'.format(NAME))
        # Test
        target.pin_view(NAME)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert n_pinned == len(target._pinned)

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        target = VSTACK.ViewStack()
        attr = getattr(target, NAME_ATTR)
        CLASS = VSTACK.ViewStack
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None

    def test_remove_view(self):
        """| Confirm removal of view from collection.
        | Case: view in collection and not pinned.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 3
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))

        ID_REMOVE = 1
        _ = views.pop(ID_REMOVE)
        name_remove = hex(ID_REMOVE)
        # Test
        target.remove_view(name_remove)
        assert len(views) == len(target._ui_view)
        for key, view in views.items():
            assert view is target._ui_view.get_child_by_name(hex(key))

    def test_remove_view_absent(self, caplog):
        """| Confirm removal of view from collection.
        | Case: view not in collection.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 3
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        N_LOGS = 1
        LAST = -1
        NAME_ABSENT = 'Parrot'
        log_message = ('No item view named \'{}\' '
                       '(ViewStack.remove_view)'.format(NAME_ABSENT))
        # Test
        target.remove_view(NAME_ABSENT)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert N_VIEWS == len(target._ui_view)

    def test_remove_view_pinned(self, caplog):
        """| Confirm removal of view from collection.
        | Case: view in collection but pinned.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 3
        views = dict()
        for i in range(N_VIEWS):
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        I_PINNED = 2
        NAME_PINNED = hex(I_PINNED)
        target.pin_view(NAME_PINNED)
        N_LOGS = 1
        LAST = -1
        log_message = ('Pinned item view named \'{}\' cannot be removed '
                       '(ViewStack.remove_view)'.format(NAME_PINNED))
        # Test
        target.remove_view(NAME_PINNED)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert N_VIEWS == len(target._ui_view)

    def test_show_view(self):
        """| Confirm view selection.
        | Case: named view in collection.
        """
        # Setup
        target = VSTACK.ViewStack()
        N_VIEWS = 3
        views = dict()
        for i in range(N_VIEWS):
            view = Gtk.Label(label='Item {}'.format(i))
            view.show()
            views[i] = view
            target.add_view(views[i], hex(i))
        ID_VISIBLE = 0
        target._ui_view.set_visible_child(views[ID_VISIBLE])
        ID_SHOW = 2
        name_show = hex(ID_SHOW)
        # Test
        name_shown = target.show_view(name_show)
        assert name_show == name_shown
        assert target._ui_view.get_visible_child() is views[ID_SHOW]

    def test_show_view_absent(self, caplog):
        """| Confirm view selection.
        | Case: named view not in collection.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        N_VIEWS = 3
        target = VSTACK.ViewStack()
        views = dict()
        for i in range(N_VIEWS):
            view = Gtk.Label(label='Item {}'.format(i))
            view.show()
            views[i] = Gtk.Label(label='Item {}'.format(i))
            target.add_view(views[i], hex(i))
        ID_VISIBLE = 0
        NAME_VISIBLE = hex(ID_VISIBLE)
        target._ui_view.set_visible_child_name(NAME_VISIBLE)
        NAME_SHOW = 'Something completely different'
        N_LOGS = 1
        LAST = -1
        log_message = ('No item view named \'{}\' '
                       '(ViewStack.show_view)'.format(NAME_SHOW))
        # Test
        name_shown = target.show_view(NAME_SHOW)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert NAME_VISIBLE == name_shown
        assert target._ui_view.get_visible_child() is views[ID_VISIBLE]

    def test_unpin_view(self):
        """| Confirm unpinning of item view.
        | Case: named view is pinned.
        """
        # Setup
        NAME = 'Parrot'
        VIEW = Gtk.Label(label=NAME)
        target = VSTACK.ViewStack()
        target.add_view(VIEW, NAME)
        target.pin_view(NAME)
        # Test
        target.unpin_view(NAME)
        assert NAME not in target._pinned

    def test_unpin_view_unpinned(self, caplog):
        """| Confirm unpinning of item view.
        | Case: named view is not pinned.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        NAME = 'Parrot'
        VIEW = Gtk.Label(label='The Parrot Sketch')
        target = VSTACK.ViewStack()
        target.add_view(VIEW, NAME)
        N_LOGS = 1
        LAST = -1
        log_message = ('View named \'{}\' not pinned '
                       '(ViewStack.unpin_view)'.format(NAME))
        # Test
        target.unpin_view(NAME)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname
        assert not target._pinned


class TestModule:
    """Unit tests for module-level components of :mod:`.view_stack`."""

    @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
        (VSTACK.logger, logging.Logger),
        ])
    def test_attributes(self, ATTR, TYPE_EXPECT):
        """Confirm global attribute definitions.

        :param ATTR: attribute under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert isinstance(ATTR, TYPE_EXPECT)

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (VSTACK.NameView, str),
        (VSTACK.UiViewStack, Gtk.Stack),
        (VSTACK.ViewItem, Gtk.Widget),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type and type alias definitions.

        :param TYPE_TARGET: type or type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT

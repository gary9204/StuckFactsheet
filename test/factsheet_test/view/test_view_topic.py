"""
Unit tests for class to display topic view in a Factsheet window pane.
See :mod:`.view_topic`.

.. include:: /test/refs_include_pytest.txt
"""
# import dataclasses as DC
import pytest   # type: ignore[import]

import factsheet.control.control_topic as CTOPIC
import factsheet.model.topic as MTOPIC
import factsheet.view.ui as UI
import factsheet.view.view_topic as VTOPIC

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def new_model_control_view(request, new_model_topic):
    """Pytest fixture with teardown: return topic model, control, and view.

    :param request: built-in fixture `Pytest request`_.
    :param new_model_topic: fixture :func:`.new_model_topic`.
    """
    marker = request.node.get_closest_marker("n_facts")
    n_facts = 5
    if marker is not None:
        try:
            n_facts = marker.kwargs['n_facts']
        except KeyError:
            pass

    model = new_model_topic(n_facts)
    control = CTOPIC.ControlTopic(p_model=model)
    view = VTOPIC.ViewTopic(p_control=control)
    yield model, control, view
    view._ui_pane.hide()
    # view._ui_pane.destroy()
    # del view._ui_pane


class TestViewTopic:
    """Unit tests for :class:`.ViewTopic`."""

    @pytest.mark.n_facts(n_facts=5)
    def test_init(self, new_model_control_view):
        """Confirm initialization.

        :param new_model_control_view: fixture
            :func:`.new_model_control_view`.
        """
        # Setup
        # Test
        _model, control, target = new_model_control_view
        assert target._control is control
        assert isinstance(target._ui_pane, Gtk.Box)
        assert target._ui_pane.is_visible()
        actions_topic = target._ui_pane.get_action_group('topic')
        assert isinstance(actions_topic, Gio.SimpleActionGroup)

        # Components: see helper tests.

        # Dialogs
        assert actions_topic.lookup_action('show-help-topic') is not None
        assert actions_topic.lookup_action(
            'show-help-topic-display') is not None

    # @pytest.mark.skip
    # def test_init_activate(self, patch_control_topic):
    #     """Confirm initialization.
    #
    #     Case: name view activation signal."""
    #     # Setup
    #     entry_gtype = GO.type_from_name(GO.type_name(Gtk.Entry))
    #     delete_signal = GO.signal_lookup('activate', entry_gtype)
    #     CONTROL = patch_control_topic
    #     # Test
    #     target = VTOPIC.ViewTopic(p_control=CONTROL)
    #     entry = target._infoid.get_view_name()
    #     activate_id = GO.signal_handler_find(
    #         entry, GO.SignalMatchType.ID, delete_signal,
    #         0, None, None, None)
    #     assert 0 != activate_id
    #     # Teardown
    #     target._ui_pane.destroy()
    #     del target._ui_pane

    def test_helper_init_menu_display(self, new_model_control_view):
        """Confirm helper binds display menu buttons to topic components.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_
        :param new_model_control_view: fixture :func:`new_model_control_view`.
        """
        # Setup
        _model, _control, target = new_model_control_view

        class PatchGetObject:
            def __init__(self):
                self.ui_elements = dict()
                self.name_all = 'ui_show_all'
                self.button_all = Gtk.CheckButton(active=True)
                self.ui_elements[self.name_all] = self.button_all
                self.pairs_name_ui = [
                    ('ui_show_summary', 'ui_expander_summary'),
                    ('ui_show_facts', 'ui_expander_facts'),
                    ('ui_show_fact_current', 'ui_expander_fact_current'),
                    ('ui_show_topics_related', 'ui_expander_topics_related'),
                    ]
                self.pairs_ui = list()
                for name_button, name_expander in self.pairs_name_ui:
                    button = Gtk.CheckButton(active=True)
                    self.ui_elements[name_button] = button
                    expander = Gtk.Expander(visible=True)
                    self.ui_elements[name_expander] = expander
                    pair = (button, expander)
                    self.pairs_ui.append(pair)

            def get_object(self, p_name_ui):
                return self.ui_elements[p_name_ui]

        patch_get = PatchGetObject()

        # Test
        target._init_menu_display(patch_get.get_object)
        for button, expander in patch_get.pairs_ui:
            button.set_active(False)
            assert not button.get_active() and not expander.get_visible()
            expander.set_visible(True)
            assert button.get_active() and expander.get_visible()
        patch_get.button_all.set_active(False)
        for button, _ in patch_get.pairs_ui:
            assert not button.get_active()
            button.set_active(True)
            assert not patch_get.button_all.get_active()
            button.set_active(False)
        patch_get.button_all.set_active(True)
        for button, _ in patch_get.pairs_ui:
            assert button.get_active()
            button.set_active(False)
            assert patch_get.button_all.get_active()

    def test_helper_init_summary(self, monkeypatch, new_model_control_view):
        """Confirm helper creates summary fields in topic view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_
        :param new_model_control_view: fixture :func:`new_model_control_view`.
        """
        # Setup
        _model, _control, target = new_model_control_view
        NAME_SITE = 'ui_site_summary'
        TYPE_CONTENT = MTOPIC.EditorSummary

        class PatchGetObject:
            def __init__(self):
                self.name_site = None

            def get_object(self, p_name_site):
                self.name_site = p_name_site
                return Gtk.Box()

        patch_get = PatchGetObject()

        class PatchAdd:
            def __init__(self):
                self.content = None

            def add(self, p_widget):
                self.content = p_widget

        patch_add = PatchAdd()
        monkeypatch.setattr(Gtk.Box, 'add', patch_add.add)
        # Test
        target._init_summary_topic(patch_get.get_object)
        assert NAME_SITE == patch_get.name_site
        assert isinstance(patch_add.content, TYPE_CONTENT)

    @pytest.fixture
    def patch_view_display_editor(self, new_model_control_view, monkeypatch):
        """Pytest fixture with teardown: return patched view of topic.

        Component patch provides access to component initialization
        calls as well as teardown.
        """
        _model, _control, view = new_model_control_view

        class PatchDisplayEditor:
            def __init__(self):
                self.called = False
                self.display = None
                self.editor = 'Oops'
                self.content = ''
                self.ui_view = Gtk.Box()

            def init(self, p_display, p_editor, p_type):
                self.called = True
                self.display = p_display
                self.editor = p_editor
                self.content = p_type

        patch_display_editor = PatchDisplayEditor()
        monkeypatch.setattr(
            VTOPIC.VMARKUP.ViewMarkup, '__init__', patch_display_editor.init)
        monkeypatch.setattr(
            VTOPIC.VMARKUP.ViewMarkup, 'ui_view', patch_display_editor.ui_view)
        yield view, patch_display_editor
        patch_display_editor.display.destroy()

    @pytest.mark.parametrize('HELPER, CONTENT, SITE', [
        ('_init_name_topic', 'Name', 'ui_site_name_topic'),
        ('_init_title_topic', 'Title', 'ui_site_title_topic'),
        ])
    def test_helper_init_view(self, monkeypatch, patch_view_display_editor,
                              HELPER, CONTENT, SITE):
        """Confirm helper creates name and title fields in topic view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param patch_view_display_editor: fixture
            :func:`.patch_view_display_eidtor`.
        :param HELPER: initialization helper method under test.
        :param CONTENT: name of view type.
        :param SITE: expected locaton for new view.
        """
        # Setup
        target, display_editor = patch_view_display_editor
        target_method = getattr(target, HELPER)

        class PatchGetObject:
            def __init__(self):
                self.called = False
                self.site_ui = ''

            def get_object(self, p_site_ui):
                self.called = True
                self.site_ui = p_site_ui
                return Gtk.Box()

        patch_get_object = PatchGetObject()

        class PatchSite:
            def __init__(self):
                self.called = False
                self.ui_view = None
                self.expand_okay = None
                self.fill_okay = None
                self.n_padding = 0

            def pack_start(
                    self, p_view, p_exapnd_okay, p_fill_okay, p_n_padding):
                self.called = True
                self.ui_view = p_view
                self.expand_okay = p_exapnd_okay
                self.fill_okay = p_fill_okay
                self.n_padding = p_n_padding

        patch_site = PatchSite()
        monkeypatch.setattr(Gtk.Box, 'pack_start', patch_site.pack_start)

        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        # Test
        target_method(patch_get_object.get_object)
        assert display_editor.called
        assert isinstance(display_editor.display, Gtk.Label)
        assert isinstance(display_editor.editor, Gtk.Entry)
        assert CONTENT == display_editor.content
        assert patch_get_object.called
        assert SITE == patch_get_object.site_ui
        assert patch_site.called
        assert display_editor.ui_view is patch_site.ui_view
        assert EXPAND_OKAY == patch_site.expand_okay
        assert FILL_OKAY == patch_site.fill_okay
        assert N_PADDING == patch_site.n_padding

    # @pytest.mark.skip
    # @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
    #     ['_ui_pane', 'gtk_pane'],
    #     ])
    # def test_property(self, patch_control_topic, NAME_ATTR, NAME_PROP):
    #     """Confirm properties are get-only.
    #
    #     #. Case: get
    #     #. Case: no set
    #     #. Case: no delete
    #     """
    #     # Setup
    #     CONTROL = patch_control_topic
    #     target = VTOPIC.ViewTopic(p_control=CONTROL)
    #     value_attr = getattr(target, NAME_ATTR)
    #     target_prop = getattr(VTOPIC.ViewTopic, NAME_PROP)
    #     value_prop = getattr(target, NAME_PROP)
    #     # Test: read
    #     assert target_prop.fget is not None
    #     assert str(value_attr) == str(value_prop)
    #     # Test: no replace
    #     assert target_prop.fset is None
    #     # Test: no delete
    #     assert target_prop.fdel is None

    def test_on_show_dialog(self, new_model_control_view, monkeypatch):
        """| Confirm handler runs dialog.
        | Case: topic view in top-level window.

        See manual tests for dialog content checks.

        :param new_model_control_view: fixture
            :func:`.new_model_control_view`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        _model, _control, target = new_model_control_view

        window = Gtk.ApplicationWindow()
        monkeypatch.setattr(
            Gtk.Widget, 'get_toplevel', lambda *_args: window)
        dialog = Gtk.Dialog()
        dialog.show()
        # Test
        target.on_show_dialog(None, None, dialog)
        assert patch.called
        assert not dialog.is_visible()
        assert dialog.get_transient_for() is window

    def test_on_show_dialog_no_top(
            self, new_model_control_view, monkeypatch):
        """| Confirm handler runs dialog.
        | Case: topic view not in top-level window.

        :param new_model_control_view: fixture
            :func:`.new_model_control_view`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        _model, _control, target = new_model_control_view

        monkeypatch.setattr(
            Gtk.Widget, 'get_toplevel', lambda *_args: target._ui_pane)
        window = Gtk.ApplicationWindow()
        dialog = Gtk.Dialog()
        dialog.set_transient_for(window)
        dialog.show()
        # Test
        target.on_show_dialog(None, None, dialog)
        assert patch.called
        assert not dialog.is_visible()
        assert dialog.get_transient_for() is None

    @pytest.mark.parametrize('DIALOG', [
        UI.HELP_TOPIC,
        UI.HELP_TOPIC_DISPLAY,
        ])
    def test_on_show_dialog_input(self, DIALOG):
        """Confirm presence of shared dialogs.

        :param DIALOG: dialog under test.
        """
        # Setup
        # Test
        assert isinstance(DIALOG, Gtk.Dialog)

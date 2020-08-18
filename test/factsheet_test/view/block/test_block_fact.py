"""
Unit tests for class to display fact in topic pane.  See
:mod:`.block_fact`.
"""
import dataclasses as DC
import logging
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

from factsheet.model import fact as MFACT
from factsheet.control import control_fact as CFACT
from factsheet.view import scenes as VSCENES
from factsheet.view import view_infoid as VINFOID
from factsheet.view.block import block_fact as VFACT

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]  # noqa:E402


@DC.dataclass
class ArgsSelectorName:
    """Convenience class for pytest fixture.

    Class assembles arguments to :class:`.SelectorName` method ``__init__``.
    """
    p_view: Gtk.ComboBox
    p_on_select: typing.Callable[[str], None]


@pytest.fixture
def patch_args_selector_name():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.SelectorName` object.
    """
    def ON_SELECT(p_name): pass
    NAMES = ['Brie', 'Cheddar', 'Munster', 'Provolone']
    model = Gtk.ListStore(str)
    for n in NAMES:
        model.append([n])
    view = Gtk.ComboBox(model=model)
    C_ACTIVE = 0
    NAME_ACTIVE = 1
    view.set_id_column(C_ACTIVE)
    view.set_active_id(NAMES[NAME_ACTIVE])
    return ArgsSelectorName(
        p_view=view,
        p_on_select=ON_SELECT
        )


@pytest.fixture
def patch_control_fact(patch_args_infoid):
    """Pytest fixture returns a stock :class:`.ControlFact`."""
    ARGS = patch_args_infoid
    fact = MFACT.Fact(**DC.asdict(ARGS))
    control = CFACT.ControlFact(p_fact=fact)
    return control


# class TestAspectValue:
#     """Unit tests for :class:`.AspectValue`."""
#
#     def test_init(self):
#         """Confirm initialization."""
#         # Setup
#         # Test
#         target = VFACT.AspectValue()
#         assert isinstance(target._aspect_gtk, Gtk.ScrolledWindow)
#         # assert isinstance(target._content_gtk, Gtk.Label)
#
#     # def test_get_content(self):
#     #     """Confirm return is content presentation element."""
#     #     # Setup
#     #     CONTENT = Gtk.TreeView()
#     #     target = VFACT.AspectValue()
#     #     target._content_gtk = CONTENT
#     #     # Test
#     #     target_content = target.get_content()
#     #     assert CONTENT is target_content
#
#     def test_set_content(self):
#         """Confirm content added to scene."""
#         # Setup
#         CONTENT = Gtk.TreeView()
#         target = VFACT.AspectValue()
#         # Test
#         target.set_content(CONTENT)
#         assert target._aspect_gtk.get_child() is CONTENT
#         # assert target._content_gtk is CONTENT
#
#     @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
#         ('_aspect_gtk', 'aspect_gtk'),
#         ])
#     def test_property(self, NAME_ATTR, NAME_PROP):
#         """Confirm properties are get-only.
#
#         #. Case: get
#         #. Case: no set
#         #. Case: no delete
#         """
#         # Setup
#         target = VFACT.AspectValue()
#         value_attr = getattr(target, NAME_ATTR)
#         target_prop = getattr(VFACT.AspectValue, NAME_PROP)
#         value_prop = getattr(target, NAME_PROP)
#         # Test: read
#         assert target_prop.fget is not None
#         assert str(value_attr) == str(value_prop)
#         # Test: no replace
#         assert target_prop.fset is None
#         # Test: no delete
#         assert target_prop.fdel is None


class TestBlockFact:
    """Unit tests for :class:`.BlockFact`."""

    def test_init(self, patch_control_fact):
        """Confirm initialization."""
        # Setup
        CONTROL = patch_control_fact
        fact = CONTROL._fact
        NAME_SELECT = 'Synopsis'
        NAMES = [NAME_SELECT, 'Plain']
        # Test
        assert VFACT.BlockFact.NAME_FILE_FACT_UI is not None
        target = VFACT.BlockFact(p_control=CONTROL)
        assert target._value is VFACT.StatusOfFact.BLOCKED
        assert target._control is CONTROL

        assert isinstance(target._infoid, VINFOID.ViewInfoId)
        assert target._infoid.name is not None
        assert target._infoid.summary is not None
        assert target._infoid.title is not None

        assert isinstance(target._block_gtk, Gtk.Box)
        actions_fact = target._block_gtk.get_action_group('fact')
        assert isinstance(actions_fact, Gio.SimpleActionGroup)

        assert isinstance(target._aspects, VSCENES.Scenes)
        assert isinstance(target._new_aspect, dict)
        assert target.synopsis == target._new_aspect['Synopsis']
        assert target.plain == target._new_aspect['Plain']

        assert isinstance(target._names, VFACT.SelectorName)
        assert NAME_SELECT == target._name_default
        assert NAMES == list(target._names)
        assert NAME_SELECT == target._aspects.get_scene_visible()
        assert target._block_gtk.is_visible()
        assert target in fact._blocks.values()

        # Topic Menu
        assert actions_fact.lookup_action('show-help-fact') is not None

        # Topic Display Menu
        assert actions_fact.lookup_action('show-help-fact-display') is not None

        # Teardown
        target._block_gtk.destroy()
        del target._block_gtk

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_block_gtk', 'block_gtk'),
        ])
    def test_property(self, patch_control_fact, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        # Test
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VFACT.BlockFact, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_get_infoid(self, patch_control_fact):
        """Confirm returns :class:`.InfoId` attribute."""
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        # Test
        assert target._infoid is target.get_infoid()
        # Teardown
        target._block_gtk.destroy()
        del target._block_gtk

    def test_plain(self, patch_control_fact):
        """Confirm plaintext aspect construction."""
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact[str](p_control=CONTROL)
        PLAINTEXT = 'A Norwegian Blue.'
        target._value = PLAINTEXT
        # Test
        plaintext = target.plain()
        assert isinstance(plaintext, Gtk.ScrolledWindow)
        viewport = plaintext.get_child()
        label = viewport.get_child()
        assert isinstance(label, Gtk.Label)
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_line_wrap()
        assert label.get_line_wrap_mode() is Pango.WrapMode.WORD_CHAR
        assert label.get_selectable()
        assert PLAINTEXT == label.get_label()

    def test_select_aspect(self, patch_control_fact):
        """| Confirm value and aspect updates.
        | Case: aspect present.
        """
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        target._aspects.add_scene(target.synopsis(), 'Synopsis')
        target._aspects.add_scene(target.plain(), 'Plain')
        # view_init = target._aspects.show_scene('Plain')
        NAME_SELECT = 'Synopsis'
        # Test
        target.select_aspect(NAME_SELECT)
        assert NAME_SELECT == target._aspects.get_scene_visible()

    def test_select_aspect_absent(self, patch_control_fact):
        """| Confirm value and aspect updates.
        | Case: aspect absent with supported aspect name.
        """
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        target._aspects.add_scene(target.plain(), 'Plain')
        # view_init = target._aspects.show_scene('Plain')
        NAME_SELECT = 'Synopsis'
        # Test
        target.select_aspect(NAME_SELECT)
        assert NAME_SELECT == target._aspects.get_scene_visible()

    @pytest.mark.parametrize('NAME_SELECT', [
        'Something completely different',
        None,
        ])
    def test_select_aspect_warn(self, patch_control_fact, PatchLogger,
                                monkeypatch, NAME_SELECT):
        """| Confirm value and aspect updates.
        | Case: aspect absent with unsupported aspect name.
        """
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        VALUE_INIT = 'A Norwegian Blue'
        target._value = VALUE_INIT
        target._aspects.add_scene(target.plain(), 'Plain')
        scene_init = target._aspects.show_scene('Plain')

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Unsupported aspect: \'{}\' '
                       '(BlockFact.select_aspect)'.format(NAME_SELECT))
        assert not patch_logger.called
        # Test
        target.select_aspect(NAME_SELECT)
        assert scene_init == target._aspects.get_scene_visible()
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_synopsis(self, patch_control_fact):
        """Confirm synopsis aspect construction."""
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact[str](p_control=CONTROL)
        WIDTH_DEFAULT = 30
        WIDTH_MAX = 50
        MARKUP = 'A Norwegian Blue.'
        target._value = MARKUP
        # Test
        synopsis = target.synopsis()
        assert isinstance(synopsis, Gtk.ScrolledWindow)
        viewport = synopsis.get_child()
        label = viewport.get_child()
        assert isinstance(label, Gtk.Label)
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_width_chars() is WIDTH_DEFAULT
        assert label.get_max_width_chars() is WIDTH_MAX
        assert label.get_ellipsize() is Pango.EllipsizeMode.MIDDLE
        assert label.get_selectable()
        assert MARKUP == label.get_label()

    def test_update_value(self, patch_control_fact):
        """Confirm value and aspect updates."""
        # Setup
        CONTROL = patch_control_fact
        target = VFACT.BlockFact(p_control=CONTROL)
        target._aspects.add_scene(target.synopsis(), 'Synopsis')
        target._aspects.add_scene(target.plain(), 'Plain')
        VALUE_NEW = 'Something completely different'
        N_ASPECTS = 1
        # Test
        target.update_value(VALUE_NEW)
        assert VALUE_NEW == target._value
        assert N_ASPECTS == len(target._aspects._stack_gtk)
        assert target._name_default == target._aspects.get_scene_visible()


class TestSelectorName:
    """Unit tests for :class:`.SelectorName`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        def ON_SELECT(p_name): pass
        VIEW = Gtk.ComboBox()
        # Test
        target = VFACT.SelectorName(p_view=VIEW, p_on_select=ON_SELECT)
        assert target._selector_gtk is VIEW

    def test_iter(self):
        """Confirm iteration over names."""
        # Setup
        def ON_SELECT(p_name): pass
        NAMES = ['Brie', 'Cheddar', 'Munster', 'Provolone']
        model = Gtk.ListStore(str)
        for name in NAMES:
            model.append([name])
        view = Gtk.ComboBox(model=model)
        target = VFACT.SelectorName(p_view=view, p_on_select=ON_SELECT)
        # Test
        assert NAMES == list(target)

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_selector_gtk', Gtk.ComboBox, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        def ON_SELECT(p_name): pass
        VIEW = Gtk.ComboBox()
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target = VFACT.SelectorName(
            p_view=VIEW, p_on_select=ON_SELECT)
        attribute = getattr(target, NAME_ATTRIBUTE)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    def test_add_name(self, patch_args_selector_name):
        """| Confirm name addition.
        | Case: name not in list and select unchanged.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        NAME = 'Colby Jack'
        NAMES_INIT = list(target)
        N_NEW = len(NAMES_INIT) + 1
        # Test
        target.add_name(p_name=NAME, p_select=False)
        names_new = list(target)
        assert N_NEW == len(names_new)
        assert NAME in names_new
        assert NAME != target._selector_gtk.get_active_id()

    def test_add_name_default(self, patch_args_selector_name):
        """| Confirm name addition.
        | Case: name not in list and select new.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        NAME = 'Colby Jack'
        NAMES_INIT = list(target)
        N_NEW = len(NAMES_INIT) + 1
        # Test
        target.add_name(p_name=NAME)
        names_new = list(target)
        assert N_NEW == len(names_new)
        assert NAME == target._selector_gtk.get_active_id()

    def test_add_name_warn(
            self, patch_args_selector_name, PatchLogger, monkeypatch):
        """| Confirm name addition.
        | Case: name in list.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        NAMES = list(target)
        I_DUP = 2
        name_dup = NAMES[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Duplicate name: {} (SelectorName.add_name)'
                       ''.format(name_dup))
        assert not patch_logger.called
        # Test
        target.add_name(p_name=name_dup)
        assert NAMES == list(target)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_remove_name(self, patch_args_selector_name):
        """| Confirm name removal.
        | Case: name in list.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        NAMES = list(target)
        I_REM = 2
        name_rem = NAMES.pop(I_REM)
        # Test
        target.remove_name(p_name=name_rem)
        assert NAMES == list(target)

    def test_remove_name_warn(
            self, patch_args_selector_name, PatchLogger, monkeypatch):
        """| Confirm name removal.
        | Case: name not in list.
        """
        # Setup
        NAME = 'Colby Jack'
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        NAMES = list(target)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('Missing name: {} (SelectorName.remove_name)'
                       ''.format(NAME))
        assert not patch_logger.called
        # Test
        target.remove_name(p_name=NAME)
        assert NAMES == list(target)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_select(self, patch_args_selector_name):
        """| Confirm name selection.
        | Case: name in list of names.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        names = list(target)
        I_INIT = 3
        name_init = names[I_INIT]
        target._selector_gtk.set_active_id(name_init)
        I_NEW = 1
        name_new = names[I_NEW]
        # Test
        target.select(name_new)
        assert name_new == target._selector_gtk.get_active_id()

    @pytest.mark.parametrize('NAME_NEW', [
        'Something completely different',
        None,
        ])
    def test_select_absent(self, patch_args_selector_name, NAME_NEW):
        """| Confirm name selection.
        | Case: name not in list of names.
        """
        # Setup
        ARGS = patch_args_selector_name
        target = VFACT.SelectorName(
            p_view=ARGS.p_view, p_on_select=ARGS.p_on_select)
        names = list(target)
        I_INIT = 3
        name_init = names[I_INIT]
        target._selector_gtk.set_active_id(name_init)
        # Test
        target.select(NAME_NEW)
        assert name_init == target._selector_gtk.get_active_id()

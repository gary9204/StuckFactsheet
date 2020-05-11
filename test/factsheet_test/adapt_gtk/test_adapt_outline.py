"""
Unit tests for generic, GTK-based classes implementing abstract outline
classes. See :mod:`.adapt_outline`.
"""
import gi   # type: ignore[import]
import itertools as IT
import logging
import pickle
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_outline as AOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchItem:
    """Placeholder item class for unit tests."""
    def __init__(
            self, p_name='Parrot', p_tag='Source'):
        self.name = p_name
        self.title = p_tag

    def __eq__(self, px_other):
        if not isinstance(px_other, PatchItem):
            return False
        return (self.name == px_other.name
                ) and (self.title == px_other.title)


class PatchOutline(AOUTLINE.AdaptTreeStore[PatchItem]):
    """Specialization of generic :class:`.AdaptTreeStore` with
    placeholder :class:`.PatchItem` items for unit tests."""
    pass


@pytest.fixture
def new_outline_model():
    """Pytest fixture returns outline model factory.  Parameter p_tag
    labels each item in title.  The structure of each model is as
    follows.

        | name_0xx
        |     name_00x
        |         name_000
        |     name_01x
        | name_1xx
        |     name_10x
        |     name_11x
        |         name_110
        |         name_111
        |         name_112
    """
    def new_model(p_tag='Target'):
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

        item = PatchItem('name_0xx', p_tag)
        i_0xx = model.append(None, [item])
        item = PatchItem('name_00x', p_tag)
        i_00x = model.append(i_0xx, [item])
        item = PatchItem('name_000', p_tag)
        _i_000 = model.append(i_00x, [item])
        item = PatchItem('name_01x', p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = PatchItem('name_1xx', p_tag)
        i_1xx = model.append(None, [item])
        item = PatchItem('name_10x', p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = PatchItem('name_11x', p_tag)
        i_11x = model.append(i_1xx, [item])
        item = PatchItem('name_110', p_tag)
        _i_110 = model.append(i_11x, [item])
        item = PatchItem('name_111', p_tag)
        _i_111 = model.append(i_11x, [item])
        item = PatchItem('name_112', p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


class TestAdaptIndex:
    """Unit tests for supporting abstract types."""

    def test_types(self):
        """Confirm supporting types defined."""
        # Setup
        # Test
        assert AOUTLINE.AdaptIndex is not None
        assert issubclass(Gtk.TreeIter, AOUTLINE.AdaptIndex)


class TestAdaptTreeStore:
    """Unit tests for :class:`.AdaptTreeStore`."""

    def test_eq_ne_type(self):
        """| Confirm equivalence comparison.
        | Case: type difference
        """
        # Setup
        source = Gtk.TreeStore(str)
        target = PatchOutline()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_n_columns(self):
        """| Confirm equivalence comparison.
        | Case: different number of columns
        """
        # Setup
        source = PatchOutline()
        source._gtk_model = Gtk.TreeStore(
            GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT)
        target = PatchOutline()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_column_types(self):
        """| Confirm equivalence comparison.
        | Case: different column types
        """
        # Setup
        source = PatchOutline()
        source._gtk_model = Gtk.TreeStore(int)
        target = PatchOutline()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_content_length(self, new_outline_model):
        """| Confirm equivalence comparison.
        | Case: different content length
        """
        # Setup
        model_source = new_outline_model('Source')
        PATH_REMOVE = '1:1:1'
        i_remove = model_source.get_iter_from_string(PATH_REMOVE)
        model_source.remove(i_remove)
        source = PatchOutline()
        source._gtk_model = model_source
        target = PatchOutline()
        target._gtk_model = new_outline_model()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_structure(self, new_outline_model):
        """| Confirm equivalence comparison.
        | Case: different content structure
        """
        # Setup
        model_source = new_outline_model('Source')
        PATH_FIRST = '0'
        i_first = model_source.get_iter_from_string(PATH_FIRST)
        PATH_SECOND = '1'
        i_last = model_source.get_iter_from_string(PATH_SECOND)
        model_source.move_after(i_first, i_last)
        source = PatchOutline()
        source._gtk_model = model_source
        target = PatchOutline()
        target._gtk_model = new_outline_model()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_content(self, new_outline_model):
        """| Confirm equivalence comparison.
        | Case: different content values
        """
        # Setup
        source = PatchOutline()
        model_source = new_outline_model()
        source._gtk_model = model_source
        PATH_ITEM = '0:1'
        i_item = model_source.get_iter_from_string(PATH_ITEM)
        item = model_source.get_value(i_item, source.N_COLUMN_ITEM)
        NAME_NEW = 'Something completely different'
        item.name = NAME_NEW
        target = PatchOutline()
        target._gtk_model = new_outline_model()
        # Test
        assert not target.__eq__(source)
        assert target.__ne__(source)

    def test_eq_ne_equivalent(self, new_outline_model):
        """| Confirm equivalence comparison.
        | Case: equivalent structure and content
        """
        # Setup
        source = PatchOutline()
        source._gtk_model = new_outline_model()
        target = PatchOutline()
        target._gtk_model = new_outline_model()
        # Test
        assert target.__eq__(source)
        assert not target.__ne__(source)

    def test_get_set_state(self, tmp_path):
        """Confirm conversions to and from pickable format"""
        # Setup
        def new_pickle_model(p_tag='Sorce'):
            model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

            item = PatchItem('name_0xx', p_tag)
            i_0xx = model.append(None, [item])
            item = PatchItem('name_00x', p_tag)
            i_00x = model.append(i_0xx, [item])
            item = PatchItem('name_000', p_tag)
            _i_000 = model.append(i_00x, [item])
            item = PatchItem('name_01x', p_tag)
            i_0xx = model.append(i_0xx, [item])
            item = PatchItem('name_1xx', p_tag)
            i_1xx = model.append(None, [item])
            item = PatchItem('name_10x', p_tag)
            _i_10x = model.append(i_1xx, [item])
            item = PatchItem('name_11x', p_tag)
            i_11x = model.append(i_1xx, [item])
            item = PatchItem('name_110', p_tag)
            _i_110 = model.append(i_11x, [item])
            item = PatchItem('name_111', p_tag)
            _i_111 = model.append(i_11x, [item])
            item = PatchItem('name_112', p_tag)
            _i_112 = model.append(i_11x, [item])
            return model

        PATH = tmp_path / 'get_set.fsg'

        source = PatchOutline()
        source._gtk_model = new_pickle_model()

        N_VIEWS = 3
        views = [AOUTLINE.AdaptTreeView() for _ in range(N_VIEWS)]
        for view in views:
            source.attach_view(view)
        # Test
        with PATH.open(mode='wb') as out_io:
            pickle.dump(source, out_io)
        with PATH.open(mode='rb') as in_io:
            target = pickle.load(in_io)

        assert target == source
        assert not target._views
        assert not hasattr(target, 'ex_model')

    def test_init(self):
        """Confirm initialization."""
        # Setup
        N_COLUMNS = 1
        C_ITEM = 0
        NAME_PYOBJECT = GO.type_name(GO.TYPE_PYOBJECT)
        # Test
        target = PatchOutline()
        assert target is not None
        assert isinstance(target._gtk_model, Gtk.TreeStore)
        assert N_COLUMNS == target._gtk_model.get_n_columns()
        name_type = GO.type_name(target._gtk_model.get_column_type(C_ITEM))
        assert NAME_PYOBJECT == name_type
        assert isinstance(target._views, dict)
        assert not target._views

    def test_attach_view(self, new_outline_model):
        """| Confirm addition of view.
        | Case: view not attached initially
        """
        # Setup
        target = PatchOutline()
        target._gtk_model = new_outline_model()

        N_VIEWS = 3
        views = [AOUTLINE.AdaptTreeView() for _ in range(N_VIEWS)]
        # Test
        for view in views:
            target.attach_view(view)
            assert target._gtk_model is view._gtk_view.get_model()
            assert target._views[id(view)] is view
        assert len(views) == len(target._views)

    def test_attach_view_warn(
            self, new_outline_model, PatchLogger, monkeypatch):
        """| Confirm addition of view.
        | Case: view attached initially
        """
        # Setup
        class PatchSetModel:
            def __init__(self): self.called = False

            def set_model(self, _model): self.called = True

        target = PatchOutline()
        target._gtk_model = new_outline_model()

        N_VIEWS = 3
        views = [AOUTLINE.AdaptTreeView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUPLICATE = 1
        view_duplicate = views[I_DUPLICATE]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate view: {} (PatchOutline.attach_view)'
            ''.format(hex(id(view_duplicate))))

        patch_set_model = PatchSetModel()
        monkeypatch.setattr(
            Gtk.TreeView, 'set_model', patch_set_model.set_model)
        # Test
        target.attach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert not patch_set_model.called
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    @pytest.mark.parametrize('PATH_SOURCE, PATH_TARGET, N_INSERT', [
        (None, None, 10),
        ('0', None, 10),
        ('1:1', None, 10),
        ('0:0:0', None, 10),
        (None, '0', 4),
        ('0', '0', 4),
        ('1:1', '0', 4),
        ('0:0:0', '0', 4),
        (None, '1:0', 6),
        ('0', '1:0', 6),
        ('1:1', '1:0', 6),
        ('0:0:0', '1:0', 6),
        (None, '1:1:1', 9),
        ('0', '1:1:1', 9),
        ('1:1', '1:1:1', 9),
        ('0:0:0', '1:1:1', 9),
        ])
    def test_deecopy_section_child(
            self, PATH_SOURCE, PATH_TARGET, N_INSERT, new_outline_model):
        """Confirm topic inserted at correct index for all levels."""
        # Setup
        source = PatchOutline()
        model = new_outline_model('Source')
        source._gtk_model = model
        if PATH_SOURCE is None:
            i_source = None
        else:
            i_source = model.get_iter_from_string(PATH_SOURCE)

        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        if PATH_TARGET is None:
            i_target = None
        else:
            i_target = target._gtk_model.get_iter_from_string(PATH_TARGET)
        slot_insert = target._gtk_model.iter_n_children(i_target)

        items_before = [target.get_item(i) for i in target.indices()]
        items_section = [source.get_item(i) for i in source.indices(i_source)]
        items_after = (
            items_before[:N_INSERT] + items_section + items_before[N_INSERT:])
        # Test
        i_target = target.deepcopy_section_child(source, i_source, i_target)
        items_target = [target.get_item(i) for i in target.indices()]
        assert items_after == items_target

        if PATH_TARGET is None:
            i_parent = None
        else:
            i_parent = target._gtk_model.get_iter_from_string(PATH_TARGET)
        items_insert = list()
        i_insert = target._gtk_model.iter_nth_child(i_parent, slot_insert)
        while i_insert is not None:
            items_insert += [
                target.get_item(i) for i in target.indices(i_insert)]
            i_insert = target._gtk_model.iter_next(i_insert)
        assert items_section == items_insert

    def test_detach_view(self, new_outline_model):
        """| Confirm removal of view.
        | Case: view attached initially
        """
        # Setup
        target = PatchOutline()
        target._gtk_model = new_outline_model()

        N_VIEWS = 3
        views = [AOUTLINE.AdaptTreeView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        N_REMOVE = 1
        view_remove = views.pop(N_REMOVE)
        # Test
        target.detach_view(view_remove)
        assert len(views) == len(target._views)
        for view in views:
            assert target._gtk_model is view._gtk_view.get_model()
            assert target._views[id(view)] is view
        assert target._gtk_model is not view_remove._gtk_view.get_model()

    def test_detach_view_warn(
            self, new_outline_model, monkeypatch, PatchLogger):
        """| Confirm removal of view.
        | Case: view not attached initially
        """
        # Setup
        target = PatchOutline()
        target._gtk_model = new_outline_model()

        N_VIEWS = 3
        views = [AOUTLINE.AdaptTreeView() for _ in range(N_VIEWS)]
        for view in views:
            target.attach_view(view)
        I_DUPLICATE = 1
        view_duplicate = views.pop(I_DUPLICATE)

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'critical', patch_logger.critical)
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing view: {} (PatchOutline.detach_view)'
            ''.format(hex(id(view_duplicate))))
        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        # Test
        target.detach_view(view_duplicate)
        assert len(views) == len(target._views)
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_find_next_all(self, new_outline_model):
        """| Confirm search results.
        | Case: match, no wrap - check entire outline, no key
        """
        # Setup
        PATH_VALUE = '1:1:2'
        # PATH_AFTER n/a. Default px_i_after is None.
        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        i_value = target._gtk_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value)
        # Test
        i_match = target.find_next(value)
        assert PATH_VALUE == target._gtk_model.get_string_from_iter(i_match)

    def test_find_next_none(self, new_outline_model):
        """| Confirm search results.
        | Case: no match, no wrap - check entire outline, no key
        """
        # Setup
        VALUE = 'Something completely different'
        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        # Test
        i_match = target.find_next(VALUE)
        assert i_match is None

    def test_find_next_no_key(self, new_outline_model):
        """| Confirm search results.
        | Case: match, wrap, no key
        """
        # Setup
        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        PATH_VALUE = '0:0'
        i_value = target._gtk_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value)
        PATH_AFTER = '0:0'
        i_after = target._gtk_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_next(
            value, px_i_after=i_after)
        assert PATH_VALUE == target._gtk_model.get_string_from_iter(i_match)

    def test_find_next_no_match(self, new_outline_model):
        """| Confirm search results.
        | Case: no match, wrap, key
        """
        # Setup
        def derive_name(px_obj): return px_obj.name

        VALUE = 'Something completely different'
        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        PATH_AFTER = '0:1'
        i_after = target._gtk_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_next(
            VALUE, px_i_after=i_after, px_derive=derive_name)
        assert i_match is None

    def test_find_next_no_wrap(self, new_outline_model):
        """| Confirm search results.
        | Case: match, no wrap, key
        """
        # Setup
        def derive_name(px_obj): return px_obj.name

        target = PatchOutline()
        target._gtk_model = new_outline_model('Target')
        PATH_VALUE = '1:1:2'
        i_value = target._gtk_model.get_iter_from_string(PATH_VALUE)
        value = derive_name(target.get_item(i_value))
        PATH_AFTER = '0'
        i_after = target._gtk_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_next(
            value, px_i_after=i_after, px_derive=derive_name)
        assert PATH_VALUE == target._gtk_model.get_string_from_iter(i_match)

    @pytest.mark.parametrize('PATH_PARENT, N_CUT_BEGIN, N_CUT_END', [
        (None, 0, 10),
        ('0', 0, 4),
        ('0:0', 1, 3),
        ('1:1:1', 8, 9),
        ])
    def test_extract_topic(
            self, new_outline_model, PATH_PARENT, N_CUT_BEGIN, N_CUT_END):
        """Confirm topic removed from collection."""
        # Setup
        target = PatchOutline()
        model = new_outline_model('Target')
        target._gtk_model = model

        names_before = [target.get_item(i).name for i in target.indices()]
        names_after = names_before[:N_CUT_BEGIN] + names_before[N_CUT_END:]

        if PATH_PARENT is None:
            i_target = None
        else:
            i_target = target._gtk_model.get_iter_from_string(PATH_PARENT)
        # Test
        target.extract_section(i_target)
        names_target = [target.get_item(i).name for i in target.indices()]
        assert names_after == names_target

    @pytest.mark.parametrize('PATH_TARGET', [
        '1',
        '0:0',
        '1:1:0',
        ])
    def test_get_item(
            self, PATH_TARGET, new_outline_model):
        """Confirm returns correct item at all levels."""
        # Setup
        model = new_outline_model('Source')
        i_target = model.get_iter_from_string(PATH_TARGET)
        source = PatchOutline()
        source._gtk_model = model
        item_source = source._gtk_model.get_value(
            i_target, source.N_COLUMN_ITEM)
        # Test
        target = source.get_item(i_target)
        assert target is item_source

    def test_get_item_invalid(self, PatchLogger, monkeypatch,
                              new_outline_model):
        """Confirm returns correct when index is None."""
        # Setup
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)

        model = new_outline_model('Source')
        PATH_TARGET = '1:1'
        i_target = model.get_iter_from_string(PATH_TARGET)
        log_message = ('Invalid item index ({}): (get_item_gtk)'
                       ''.format(hex(id(i_target))))
        source = PatchOutline()
        source._gtk_model = model
        assert source._gtk_model.get_value(
            i_target, source.N_COLUMN_ITEM) is not None
        source._gtk_model.clear()
        # Test
        target = source.get_item(i_target)
        assert target is None
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_get_item_none(self, PatchLogger, monkeypatch,
                           new_outline_model):
        """Confirm returns correct when index is None."""
        # Setup
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = 'Invalid item index (None): (get_item_gtk)'

        model = new_outline_model('Source')
        i_target = None
        source = PatchOutline()
        source._gtk_model = model
        item_source = None
        # Test
        target = source.get_item(i_target)
        assert target is item_source
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    @pytest.mark.parametrize('PATH_TARGET, NAMES', [
        (None, ['name_0xx', 'name_00x', 'name_000', 'name_01x',
                'name_1xx', 'name_10x', 'name_11x',
                'name_110', 'name_111', 'name_112']),
        ('0', ['name_0xx', 'name_00x', 'name_000', 'name_01x']),
        ('1:1', ['name_11x', 'name_110', 'name_111', 'name_112']),
        ('0:0:0', ['name_000']),
        ])
    def test_indices(
            self, PATH_TARGET, NAMES, new_outline_model):
        """Confirm iteration over outline indices at all levels."""
        # Setup
        model = new_outline_model('Target')
        i_target = None
        if PATH_TARGET is not None:
            i_target = model.get_iter_from_string(PATH_TARGET)
        target = PatchOutline()
        target._gtk_model = model
        # Tests
        indices = target.indices(i_target)
        target_names = [target.get_item(i).name for i in indices]
        assert NAMES == target_names

    @pytest.mark.parametrize('PATH_INSERT, PATH_ITEM, N_INSERT', [
        (None, '0', 0),
        ('0', '1', 4),
        ('1:0', '1:1', 6),
        ('1:1:2', '1:1:3', 10),
        ])
    def test_insert_after(self, PATH_INSERT, PATH_ITEM, N_INSERT,
                          new_outline_model):
        """Confirm topic inserted at correct index for all levels."""
        # Setup
        model = new_outline_model('Target')
        if PATH_INSERT is None:
            i_insert = None
        else:
            i_insert = model.get_iter_from_string(PATH_INSERT)
        target = PatchOutline()
        target._gtk_model = model

        NAME = 'Something Different'
        item = PatchItem(p_name=NAME)

        names_before = [target.get_item(i).name for i in target.indices()]
        names_after = (
            names_before[:N_INSERT] + [item.name] + names_before[N_INSERT:])
        # Test
        i_target = target.insert_after(item, i_insert)
        assert PATH_ITEM == target._gtk_model.get_string_from_iter(i_target)
        assert target.get_item(i_target) is item
        names_target = [target.get_item(i).name for i in target.indices()]
        assert names_after == names_target

    @pytest.mark.parametrize('PATH_INSERT, PATH_ITEM, N_INSERT', [
        (None, '2', 10),
        ('0', '0', 0),
        ('0:1', '0:1', 3),
        ('1:1:2', '1:1:2', 9),
        ])
    def test_insert_before(self, PATH_INSERT, PATH_ITEM, N_INSERT,
                           new_outline_model):
        """Confirm topic inserted at correct index for all levels."""
        # Setup
        model = new_outline_model('Target')
        if PATH_INSERT is None:
            i_insert = None
        else:
            i_insert = model.get_iter_from_string(PATH_INSERT)
        target = PatchOutline()
        target._gtk_model = model

        NAME = 'Something Different'
        item = PatchItem(p_name=NAME)

        names_before = [target.get_item(i).name for i in target.indices()]
        names_after = (
            names_before[:N_INSERT] + [item.name] + names_before[N_INSERT:])
        # Test
        i_target = target.insert_before(item, i_insert)
        assert target.get_item(i_target) is item
        assert PATH_ITEM == target._gtk_model.get_string_from_iter(i_target)
        names_target = [target.get_item(i).name for i in target.indices()]
        assert names_after == names_target

    @pytest.mark.parametrize('PATH_INSERT, PATH_ITEM, N_INSERT', [
        (None, '2', 10),
        ('0', '0:2', 4),
        ('1:1', '1:1:3', 10),
        ('0:0:0', '0:0:0:0', 3),
        ])
    def test_insert_child(self, PATH_INSERT, PATH_ITEM, N_INSERT,
                          new_outline_model):
        """Confirm topic inserted at correct index for all levels."""
        # Setup
        model = new_outline_model('Target')
        if PATH_INSERT is None:
            i_insert = None
        else:
            i_insert = model.get_iter_from_string(PATH_INSERT)
        target = PatchOutline()
        target._gtk_model = model

        NAME = 'Something Different'
        item = PatchItem(p_name=NAME)

        names_before = [target.get_item(i).name for i in target.indices()]
        names_after = (
            names_before[:N_INSERT] + [item.name] + names_before[N_INSERT:])
        # Test
        i_target = target.insert_child(item, i_insert)
        assert target.get_item(i_target) is item
        assert PATH_ITEM == target._gtk_model.get_string_from_iter(i_target)
        names_target = [target.get_item(i).name for i in target.indices()]
        for expect, actual in IT.zip_longest(names_after, names_target):
            print('{:8} - {:8}'.format(expect, actual))
        assert names_after == names_target

#     @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
#         ['_model', 'model'],
#         ])
#     def test_property(self, NAME_ATTR, NAME_PROP):
#         """Confirm properties are get-only.

#         #. Case: get
#         #. Case: no set
#         #. Case: no delete
#         """
#         # Setup
#         target = PatchOutline()
#         value_attr = getattr(target, NAME_ATTR)
#         target_prop = getattr(PatchOutline, NAME_PROP)
#         value_prop = getattr(target, NAME_PROP)
#         # Test: read
#         assert target_prop.fget is not None
#         assert str(value_attr) == str(value_prop)
#         # Test: no replace
#         assert target_prop.fset is None
#         # Test: no delete
#         assert target_prop.fdel is None


class TestAdaptTreeView:
    """Unit tests for :class:`.AdaptTreeView`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = AOUTLINE.AdaptTreeView()
        assert isinstance(target._gtk_view, Gtk.TreeView)
        assert isinstance(target._selection, Gtk.TreeSelection)
        assert Gtk.SelectionMode.BROWSE == target._selection.get_mode()

    def test_get_selected(self, new_outline_model):
        """| Confirm returns selected item.
        | Case: item selected
        """
        # Setup
        outline = PatchOutline()
        outline._gtk_model = new_outline_model('Model')
        PATH_ITEM = '0:1'
        i_item = outline._gtk_model.get_iter_from_string(PATH_ITEM)
        target = AOUTLINE.AdaptTreeView()
        outline.attach_view(target)
        target._gtk_view.expand_all()
        target._selection.select_iter(i_item)
        # Test
        i_target = target.get_selected()
        path_target = target._gtk_view.get_model(
            ).get_string_from_iter(i_target)
        assert PATH_ITEM == path_target

    def test_get_selected_none(self, new_outline_model):
        """| Confirm returns selected item.
        | Case: no item selected
        """
        # Setup
        outline = PatchOutline()
        outline._gtk_model = new_outline_model('Model')
        target = AOUTLINE.AdaptTreeView()
        outline.attach_view(target)
        target._gtk_view.expand_all()
        target._selection.unselect_all()
        # Test
        assert target.get_selected() is None

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_gtk_view', 'gtk_view'],
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = AOUTLINE.AdaptTreeView()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(AOUTLINE.AdaptTreeView, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_select(self, new_outline_model):
        """| Confirm selection set.
        | Case: set to item.
        """
        # Setup
        outline = PatchOutline()
        outline._gtk_model = new_outline_model('Model')
        PATH_ITEM = '1:1'
        i_item = outline._gtk_model.get_iter_from_string(PATH_ITEM)
        target = AOUTLINE.AdaptTreeView()
        outline.attach_view(target)
        target._gtk_view.expand_all()
        target._selection.unselect_all()
        # Test
        target.select(i_item)
        i_target = target.get_selected()
        path_target = target._gtk_view.get_model(
            ).get_string_from_iter(i_target)
        assert PATH_ITEM == path_target

    def test_select_none(self, new_outline_model):
        """| Confirm selection set.
        | Case: set to None.
        """
        # Setup
        outline = PatchOutline()
        outline._gtk_model = new_outline_model('Model')
        PATH_ITEM = '1:1'
        i_item = outline._gtk_model.get_iter_from_string(PATH_ITEM)
        target = AOUTLINE.AdaptTreeView()
        outline.attach_view(target)
        target._gtk_view.expand_all()
        target._selection.select_iter(i_item)
        # Test
        target.select()
        assert target.get_selected() is None

    def test_unselect_all(self, new_outline_model):
        """Confirm selection cleared."""
        # Setup
        outline = PatchOutline()
        outline._gtk_model = new_outline_model('Model')
        PATH_ITEM = '1:1:0'
        i_item = outline._gtk_model.get_iter_from_string(PATH_ITEM)
        target = AOUTLINE.AdaptTreeView()
        outline.attach_view(target)
        target._gtk_view.expand_all()
        target._selection.select_iter(i_item)
        # Test
        target.unselect_all()
        assert target.get_selected() is None


class TestFunctions:
    """Unit tests for generic function defined in :mod:`.adapt_outline`."""

    @pytest.mark.parametrize('PATH_TARGET', [
        '0',
        '1:0',
        '0:0:0',
        '1:1:2',
        ])
    def test_get_item_gtk(
            self, PATH_TARGET, new_outline_model):
        """Confirm returns correct item at all levels."""
        # Setup
        model = new_outline_model('Source')
        i_target = model.get_iter_from_string(PATH_TARGET)
        item = model.get_value(
            i_target, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM)
        # Test
        target = AOUTLINE.get_item_gtk(model, i_target)
        assert target is item

    def test_get_item_gtk_invalid(
            self, PatchLogger, monkeypatch, new_outline_model):
        """Confirm returns correct when index is None."""
        # Setup
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)

        model = new_outline_model('Source')
        PATH_TARGET = '1:1'
        i_target = model.get_iter_from_string(PATH_TARGET)
        log_message = ('Invalid item index ({}): (get_item_gtk)'
                       ''.format(hex(id(i_target))))
        item = model.get_value(
            i_target, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM)
        assert item is not None
        model.clear()
        # Test
        target = AOUTLINE.get_item_gtk(model, i_target)
        assert target is None
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

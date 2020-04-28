"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_sheet`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchTemplate(ABC_SHEET.AbstractTemplate):
    """Placeholder template item class for unit tests."""
    def __init__(self, p_name='Parrot',
                 p_summary='This parrot is no more.',
                 p_title='The Dead Parrot Sketch'):
        self._name = p_name
        self._summary = p_summary
        self._title = p_title

    def __call__(self): return 'Topic Stub'

    def __eq__(self, px_other):
        if not isinstance(px_other, PatchTemplate):
            return False
        return (self.name == px_other.name
                ) and (self.summary == px_other.summary
                       ) and (self.title == px_other.title)

    @property
    def name(self): return self._name

    @property
    def summary(self): return self._summary

    @property
    def title(self): return self._title


@pytest.fixture
def new_outline_model():
    """Pytest fixture returns outline model factory.  Parameter p_tag
    labels each item in summary.  The structure of each model is as
    follows.

        | name_0xx | title_0xx
        |     name_00x | title_00x
        |         name_000 | title_000
        |     name_01x | title_01x
        | name_1xx | title_1xx
        |     name_10x | title_10x
        |     name_11x | title_11x
        |         name_110 | title_110
        |         name_111 | title_111
        |         name_112 | title_112
    """
    def new_model(p_tag='Target'):
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

        item = PatchTemplate('name_0xx', p_title='title_0xx', p_summary=p_tag)
        i_0xx = model.append(None, [item])
        item = PatchTemplate('name_00x', p_title='title_00x', p_summary=p_tag)
        i_00x = model.append(i_0xx, [item])
        item = PatchTemplate('name_000', p_title='title_000', p_summary=p_tag)
        _i_000 = model.append(i_00x, [item])
        item = PatchTemplate('name_01x', p_title='title_01x', p_summary=p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = PatchTemplate('name_1xx', p_title='title_1xx', p_summary=p_tag)
        i_1xx = model.append(None, [item])
        item = PatchTemplate('name_10x', p_title='title_10x', p_summary=p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = PatchTemplate('name_11x', p_title='title_11x', p_summary=p_tag)
        i_11x = model.append(i_1xx, [item])
        item = PatchTemplate('name_110', p_title='title_110', p_summary=p_tag)
        _i_110 = model.append(i_11x, [item])
        item = PatchTemplate('name_111', p_title='title_111', p_summary=p_tag)
        _i_111 = model.append(i_11x, [item])
        item = PatchTemplate('name_112', p_title='title_112', p_summary=p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_outline(new_outline_model):
    """Pytext fixture returns stub template outline."""
    outline = ASHEET.AdaptTreeStoreTemplate()
    outline._model = new_outline_model(p_tag='Stub template outline.')
    return outline


class TestAdaptTreeStoreTemplate:
    """Unit tests for :class:`.AdaptTreeStoreTemplate`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        patch_template = PatchTemplate()
        INDEX = None
        # Test
        target = ASHEET.AdaptTreeStoreTemplate()
        assert target is not None
        index_new = target.insert_before(patch_template, INDEX)
        assert index_new is not None
        assert isinstance(index_new, AOUTLINE.AdaptIndex)

    def test_find_name(self, new_outline_model):
        """| Confirm search by template name.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        PATH_VALUE = '1:1:1'
        i_value = target._model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).name
        PATH_AFTER = '1:1:1'
        i_after = target._model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_name(value, i_after)
        assert PATH_VALUE == target._model.get_string_from_iter(i_match)

    def test_find_name_absent(self, new_outline_model):
        """| Confirm search by template name.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        # Test
        i_match = target.find_name(VALUE)
        assert i_match is None

    def test_find_title(self, new_outline_model):
        """| Confirm search by template title.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        PATH_VALUE = '0:1'
        i_value = target._model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).title
        PATH_AFTER = '0:1'
        i_after = target._model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_title(value, i_after)
        assert PATH_VALUE == target._model.get_string_from_iter(i_match)

    def test_find_title_absent(self, new_outline_model):
        """| Confirm search by template name.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        # Test
        i_match = target.find_title(VALUE)
        assert i_match is None


class TestAdaptTreeViewTemplate:
    """Unit tests for :class:`.AdaptTreeViewTemplate`."""

    def test_init(self, monkeypatch):
        """Confirm initialization."""
        # Setup
        class PatchSetFunc:
            def __init__(self): self.called = False

            def set_search_equal_func(self, *_a): self.called = True

        patch_func = PatchSetFunc()
        monkeypatch.setattr(Gtk.TreeView, 'set_search_equal_func',
                            patch_func.set_search_equal_func)
        # Test
        target = ASHEET.AdaptTreeViewTemplate()
        assert isinstance(target._view, Gtk.TreeView)
        assert target._view.get_model() is None
        assert target.ViewFields.NAME
        assert target.ViewFields.TITLE
        assert target._active_field is target.ViewFields.NAME
        assert patch_func.called

    def test_name_cell_data(self, patch_outline):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = patch_outline
        PATH_ITEM = '1'
        i_target = OUTLINE._model.get_iter_from_string(PATH_ITEM)
        template = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        target.set_model(OUTLINE)
        # Test
        target._name_cell_data(
            None, renderer, OUTLINE._model, i_target, None)
        assert template.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert template.name == renderer.get_property('markup')

    @pytest.mark.parametrize('FIELD, PATH_ITEM, VALUE, EXPECT', [
        (ASHEET.AdaptTreeViewTemplate.ViewFields.NAME,
         '0', 'name_0xx', False),
        (ASHEET.AdaptTreeViewTemplate.ViewFields.NAME,
         '0', 'title_0xx', True),
        (ASHEET.AdaptTreeViewTemplate.ViewFields.TITLE,
         '1:1:2', 'name_112', True),
        (ASHEET.AdaptTreeViewTemplate.ViewFields.TITLE,
         '0:1', 'title_01x', False),
        (None, '1:0', 'title_01x', True),
        ])
    def test_test_field_eq(
            self, FIELD, PATH_ITEM, VALUE, EXPECT, patch_outline):
        """Confirm results of Gtk.TreeView search equal function."""
        # Setup
        OUTLINE = patch_outline
        i_item = OUTLINE._model.get_iter_from_string(PATH_ITEM)
        target = ASHEET.AdaptTreeViewTemplate()
        target.set_model(OUTLINE)
        target._active_field = FIELD
        # Test
        actual = target._test_field_ne(
            OUTLINE._model, OUTLINE.C_ITEM, VALUE, i_item, None)
        assert actual is EXPECT

    def test_title_cell_data(self, patch_outline):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = patch_outline
        PATH_ITEM = '0:0'
        i_target = OUTLINE._model.get_iter_from_string(PATH_ITEM)
        template = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        target.set_model(OUTLINE)
        # Test
        target._title_cell_data(
            None, renderer, OUTLINE._model, i_target, None)
        assert template.title == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert template.name == renderer.get_property('markup')

    def test_set_model(self, patch_outline):
        """Confirm initialization."""
        # Setup
        OUTLINE = patch_outline
        N_FIELD_NAME = 0
        N_FIELD_TITLE = 1
        N_FIELD_PAD = 2
        N_CELLS = 1
        target = ASHEET.AdaptTreeViewTemplate()
        # Test
        target.set_model(OUTLINE)
        assert target._view.get_model() is OUTLINE._model
        assert OUTLINE.C_ITEM == target._view.get_search_column()
        assert target._view.get_enable_search()

        name_column = target._view.get_column(N_FIELD_NAME)
        assert 'Name' == name_column.get_title()
        assert name_column.get_clickable()
        assert name_column.get_resizable()
        assert N_CELLS == len(name_column.get_cells())

        title_column = target._view.get_column(N_FIELD_TITLE)
        assert 'Title' == title_column.get_title()
        assert title_column.get_clickable()
        assert title_column.get_resizable()
        assert N_CELLS == len(title_column.get_cells())

        pad_column = target._view.get_column(N_FIELD_PAD)
        assert pad_column is not None
        assert pad_column.get_expand()

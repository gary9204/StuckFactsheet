"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_sheet`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content.note import topic_note as XNOTE

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
def new_model_templates():
    """Pytest fixture returns templates outline model factory.
    Parameter p_tag labels each item in summary.  The structure of each
    model is as follows.

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

        item = PatchTemplate(
            p_name='name_0xx', p_title='title_0xx', p_summary=p_tag)
        i_0xx = model.append(None, [item])
        item = PatchTemplate(
            p_name='name_00x', p_title='title_00x', p_summary=p_tag)
        i_00x = model.append(i_0xx, [item])
        item = PatchTemplate(
            p_name='name_000', p_title='title_000', p_summary=p_tag)
        _i_000 = model.append(i_00x, [item])
        item = PatchTemplate(
            p_name='name_01x', p_title='title_01x', p_summary=p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = PatchTemplate(
            p_name='name_1xx', p_title='title_1xx', p_summary=p_tag)
        i_1xx = model.append(None, [item])
        item = PatchTemplate(
            p_name='name_10x', p_title='title_10x', p_summary=p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = PatchTemplate(
            p_name='name_11x', p_title='title_11x', p_summary=p_tag)
        i_11x = model.append(i_1xx, [item])
        item = PatchTemplate(
            p_name='name_110', p_title='title_110', p_summary=p_tag)
        _i_110 = model.append(i_11x, [item])
        item = PatchTemplate(
            p_name='name_111', p_title='title_111', p_summary=p_tag)
        _i_111 = model.append(i_11x, [item])
        item = PatchTemplate(
            p_name='name_112', p_title='title_112', p_summary=p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def new_model_topics():
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

        item = XNOTE.Note()
        item.init_identity(
            p_name='name_0xx', p_title='title_0xx', p_summary=p_tag)
        i_0xx = model.append(None, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_00x', p_title='title_00x', p_summary=p_tag)
        i_00x = model.append(i_0xx, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_000', p_title='title_000', p_summary=p_tag)
        _i_000 = model.append(i_00x, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_01x', p_title='title_01x', p_summary=p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_1xx', p_title='title_1xx', p_summary=p_tag)
        i_1xx = model.append(None, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_10x', p_title='title_10x', p_summary=p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_11x', p_title='title_11x', p_summary=p_tag)
        i_11x = model.append(i_1xx, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_110', p_title='title_110', p_summary=p_tag)
        _i_110 = model.append(i_11x, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_111', p_title='title_111', p_summary=p_tag)
        _i_111 = model.append(i_11x, [item])
        item = XNOTE.Note()
        item.init_identity(
            p_name='name_112', p_title='title_112', p_summary=p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def new_templates(new_model_templates):
    """Pytext fixture returns stub outline."""
    def new_outline_templates(p_tag='Stub templates_outline.'):
        outline = ASHEET.AdaptTreeStoreTemplate()
        outline._ui_model = new_model_templates(p_tag=p_tag)
        return outline

    return new_outline_templates


@pytest.fixture
def new_topics(new_model_topics):
    """Pytext fixture returns stub outline."""
    def new_outline_topics(p_tag='Stub topics outline.'):
        outline = ASHEET.AdaptTreeStoreTopic()
        outline._ui_model = new_model_topics(p_tag=p_tag)
        return outline

    return new_outline_topics


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
        assert isinstance(index_new, AOUTLINE.IndexGtk)

    def test_find_name(self, new_model_templates):
        """| Confirm search by template name.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._ui_model = new_model_templates(p_tag='Target')
        PATH_VALUE = '1:1:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        assert i_value
        value = target.get_item(i_value).name
        PATH_AFTER = '1:1:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_name(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_name_absent(self, new_model_templates):
        """| Confirm search by template name.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._ui_model = new_model_templates(p_tag='Target')
        # Test
        i_match = target.find_name(VALUE)
        assert i_match is None

    def test_find_title(self, new_model_templates):
        """| Confirm search by template title.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._ui_model = new_model_templates(p_tag='Target')
        PATH_VALUE = '0:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).title
        PATH_AFTER = '0:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_title(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_title_absent(self, new_model_templates):
        """| Confirm search by template title.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._ui_model = new_model_templates(p_tag='Target')
        # Test
        i_match = target.find_title(VALUE)
        assert i_match is None


class TestAdaptTreeStoreTopic:
    """Unit tests for :class:`.AdaptTreeStoreTopic`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        INDEX = None
        topic = XNOTE.Note()
        topic.init_identity(p_name='Parrot', p_title='The Parrot Sketch')
        # Test
        target = ASHEET.AdaptTreeStoreTopic()
        assert target is not None
        index_new = target.insert_before(topic, INDEX)
        assert index_new is not None
        assert isinstance(index_new, AOUTLINE.IndexGtk)

    def test_find_name(self, new_model_topics):
        """| Confirm search by topic name.
        | Case: matching topic in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTopic()
        target._ui_model = new_model_topics(p_tag='Target')
        PATH_VALUE = '1:1:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).name
        PATH_AFTER = '1:1:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_name(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_name_absent(self, new_model_topics):
        """| Confirm search by topic name.
        | Case: no matching topic in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTopic()
        target._ui_model = new_model_topics(p_tag='Target')
        # Test
        i_match = target.find_name(VALUE)
        assert i_match is None

    def test_find_title(self, new_model_topics):
        """| Confirm search by topic title.
        | Case: matching topic in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTopic()
        target._ui_model = new_model_topics(p_tag='Target')
        PATH_VALUE = '0:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).title
        PATH_AFTER = '0:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_title(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_title_absent(self, new_model_topics):
        """| Confirm search by topic title.
        | Case: no matching topic in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTopic()
        target._ui_model = new_model_topics(p_tag='Target')
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
        N_FIELD_NAME = 0
        N_FIELD_TITLE = 1
        N_FIELD_PAD = 2
        N_CELLS = 1
        # Test
        target = ASHEET.AdaptTreeViewTemplate()
        assert isinstance(target._gtk_view, Gtk.TreeView)
        assert target._gtk_view.get_model() is None
        assert isinstance(target._scope_search, ASHEET.FieldsTemplate)
        assert target._scope_search is ASHEET.FieldsTemplate.VOID
        assert patch_func.called

        assert AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM == (
            target._gtk_view.get_search_column())
        assert target._gtk_view.get_enable_search()

        name_column = target._gtk_view.get_column(N_FIELD_NAME)
        assert 'Name' == name_column.get_title()
        assert name_column.get_clickable()
        assert name_column.get_resizable()
        assert N_CELLS == len(name_column.get_cells())

        title_column = target._gtk_view.get_column(N_FIELD_TITLE)
        assert 'Title' == title_column.get_title()
        assert title_column.get_clickable()
        assert title_column.get_resizable()
        assert N_CELLS == len(title_column.get_cells())

        pad_column = target._gtk_view.get_column(N_FIELD_PAD)
        assert pad_column is not None
        assert pad_column.get_expand()

    def test_name_cell_data(self, new_templates):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = new_templates()
        PATH_ITEM = '1'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        template = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        OUTLINE.attach_view(target)
        # Test
        target._name_cell_data(
            None, renderer, OUTLINE._ui_model, i_target, None)
        assert template.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert template.name == renderer.get_property('markup')

    @pytest.mark.parametrize(
        'SEARCH, PATH_ITEM, VALUE, EXPECT, EXPANDED', [
            (ASHEET.FieldsTopic.VOID, '1:0', 'title_10x', True, False),
            (ASHEET.FieldsTemplate.NAME, '0', 'name_0xx', False, False),
            (ASHEET.FieldsTemplate.NAME, '0', 'title_0xx', True, True),
            (~ASHEET.FieldsTemplate.VOID, '0', 'title_0xx', False, False),
            (ASHEET.FieldsTemplate.TITLE, '1:1:2', 'name_112', True, True),
            (ASHEET.FieldsTemplate.TITLE, '0:1', 'title_01x', False, False),
            (ASHEET.FieldsTemplate.TITLE, '0:1', 't', False, False),
            (ASHEET.FieldsTemplate.TITLE, '0:1', 'ti', False, False),
            (ASHEET.FieldsTemplate.TITLE, '0:1', 'tiX', True, True),
            (None, '1:0', 'title_01x', True, False),
        ])
    def test_test_field_eq(self, monkeypatch, SEARCH, PATH_ITEM, VALUE,
                           EXPECT, EXPANDED, new_templates):
        """Confirm results of Gtk.TreeView search equal function."""
        # Setup
        class PatchExpand:
            def __init__(self):
                self.called = False
                self.path = None

            def expand_row(self, p, _a):
                self.called = True
                self.path = p

        patch_expand = PatchExpand()
        monkeypatch.setattr(
            Gtk.TreeView, 'expand_row', patch_expand.expand_row)

        OUTLINE = new_templates()
        i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        target = ASHEET.AdaptTreeViewTemplate()
        OUTLINE.attach_view(target)
        target._scope_search = SEARCH
        # Test
        actual = target._test_field_ne(
            OUTLINE._ui_model, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM,
            VALUE, i_item, None)
        assert actual is EXPECT
        assert patch_expand.called is EXPANDED
        if EXPANDED:
            assert PATH_ITEM == patch_expand.path.to_string()

    def test_title_cell_data(self, new_templates):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = new_templates()
        PATH_ITEM = '0:0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        template = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        OUTLINE.attach_view(target)
        # Test
        target._title_cell_data(
            None, renderer, OUTLINE._ui_model, i_target, None)
        assert template.title == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert template.name == renderer.get_property('markup')

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_scope_search', 'scope_search'],
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: set
        #. Case: no delete
        """
        # Setup
        target = ASHEET.AdaptTreeViewTemplate()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(ASHEET.AdaptTreeViewTemplate, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is not None
        target.scope_search = ASHEET.FieldsTemplate.NAME
        assert target._scope_search is ASHEET.FieldsTemplate.NAME
        # Test: no delete
        assert target_prop.fdel is None


class TestAdaptTreeViewTopic:
    """Unit tests for :class:`.AdaptTreeViewTopic`."""

    def test_init(self, monkeypatch):
        """Confirm initialization."""
        # Setup
        class PatchSetFunc:
            def __init__(self): self.called = False

            def set_search_equal_func(self, *_a): self.called = True

        patch_func = PatchSetFunc()
        monkeypatch.setattr(Gtk.TreeView, 'set_search_equal_func',
                            patch_func.set_search_equal_func)
        N_FIELD_NAME = 0
        N_FIELD_TITLE = 1
        N_FIELD_PAD = 2
        N_CELLS = 1
        # Test
        target = ASHEET.AdaptTreeViewTopic()
        assert isinstance(target._gtk_view, Gtk.TreeView)
        assert target._gtk_view.get_model() is None
        assert isinstance(target._scope_search, ASHEET.FieldsTopic)
        assert target._scope_search is ASHEET.FieldsTopic.VOID
        assert patch_func.called

        assert AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM == (
            target._gtk_view.get_search_column())
        assert target._gtk_view.get_enable_search()

        name_column = target._gtk_view.get_column(N_FIELD_NAME)
        assert 'Name' == name_column.get_title()
        assert name_column.get_clickable()
        assert name_column.get_resizable()
        assert N_CELLS == len(name_column.get_cells())

        title_column = target._gtk_view.get_column(N_FIELD_TITLE)
        assert 'Title' == title_column.get_title()
        assert title_column.get_clickable()
        assert title_column.get_resizable()
        assert N_CELLS == len(title_column.get_cells())

        pad_column = target._gtk_view.get_column(N_FIELD_PAD)
        assert pad_column is not None
        assert pad_column.get_expand()

    def test_name_cell_data(self, new_topics):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = new_topics()
        PATH_ITEM = '0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        topic = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTopic()
        OUTLINE.attach_view(target)
        # Test
        target._name_cell_data(
            None, renderer, OUTLINE._ui_model, i_target, None)
        assert topic.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert topic.name == renderer.get_property('markup')

    @pytest.mark.parametrize(
        'SEARCH, PATH_ITEM, VALUE, EXPECT, EXPANDED', [
            (ASHEET.FieldsTopic.VOID, '1:0', 'title_10x', True, False),
            (ASHEET.FieldsTopic.NAME, '0:1', 'name_01x', False, False),
            (ASHEET.FieldsTopic.NAME, '0:1', 'title_01x', True, True),
            (ASHEET.FieldsTopic.TITLE, '0:0:0', 'name_000', True, True),
            (ASHEET.FieldsTopic.TITLE, '1:1', 'title_11x', False, False),
            (ASHEET.FieldsTopic.TITLE, '1:1', 't', False, False),
            (ASHEET.FieldsTopic.TITLE, '1:1', 'ti', False, False),
            (ASHEET.FieldsTopic.TITLE, '1:1', 'tiX', True, True),
            ])
    def test_test_field_eq(self, monkeypatch, SEARCH, PATH_ITEM, VALUE,
                           EXPECT, EXPANDED, new_topics):
        """Confirm results of Gtk.TreeView search equal function."""
        # Setup
        class PatchExpand:
            def __init__(self):
                self.called = False
                self.path = None

            def expand_row(self, p, _a):
                self.called = True
                self.path = p

        patch_expand = PatchExpand()
        monkeypatch.setattr(
            Gtk.TreeView, 'expand_row', patch_expand.expand_row)

        OUTLINE = new_topics()
        i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        target = ASHEET.AdaptTreeViewTopic()
        OUTLINE.attach_view(target)
        target._scope_search = SEARCH
        # Test
        actual = target._test_field_ne(
            OUTLINE._ui_model, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM,
            VALUE, i_item, None)
        assert actual is EXPECT
        assert patch_expand.called is EXPANDED
        if EXPANDED:
            assert PATH_ITEM == patch_expand.path.to_string()

    def test_title_cell_data(self, new_topics):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = new_topics()
        PATH_ITEM = '0:0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        template = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTopic()
        OUTLINE.attach_view(target)
        # Test
        target._title_cell_data(
            None, renderer, OUTLINE._ui_model, i_target, None)
        assert template.title == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert template.name == renderer.get_property('markup')

#     def test_clone(self):
#         """Confirm view duplication with shared model."""
#         # Setup
#         MODEL = Gtk.TreeStore(GO.TYPE_PYOBJECT)
#         source = ASHEET.AdaptTreeViewTopic()
#         source.gtk_view.set_model(MODEL)
#         # Test
#         target = source.clone()
#         assert isinstance(target, ASHEET.AdaptTreeViewTopic)
#         assert target.gtk_view.get_model() is source.gtk_view.get_model()

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_scope_search', 'scope_search'],
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: set
        #. Case: no delete
        """
        # Setup
        target = ASHEET.AdaptTreeViewTopic()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(ASHEET.AdaptTreeViewTopic, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is not None
        target.scope_search = ASHEET.FieldsTopic.NAME
        assert target._scope_search is ASHEET.FieldsTopic.NAME
        # Test: no delete
        assert target_prop.fdel is None


class TestFieldsTemplate:
    """Unit tests for :class:`.FieldsTemplate`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(ASHEET.FieldsTemplate.VOID)
        assert ASHEET.FieldsTemplate.NAME
        assert ASHEET.FieldsTemplate.TITLE


class TestFieldsTopic:
    """Unit tests for :class:`.FieldsTopic`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(ASHEET.FieldsTopic.VOID)
        assert ASHEET.FieldsTopic.NAME
        assert ASHEET.FieldsTopic.TITLE


class TestTypes:
    """Unit tests for type definitions in :mod:`.adapt_sheet`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ASHEET.IndexTemplate is AOUTLINE.IndexGtk
        assert ASHEET.IndexTopic is AOUTLINE.IndexGtk

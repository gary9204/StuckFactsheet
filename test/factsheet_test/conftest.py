"""
Test fixtures for Factsheet as a whole.
"""
import pytest   # type: ignore[import]
import typing

import factsheet.adapt_gtk.adapt as ADAPT
import factsheet.model.idcore as MIDCORE
# import factsheet.abc_types.abc_fact as ABC_FACT
# import factsheet.abc_types.abc_infoid as ABC_INFOID
# import factsheet.model.element as MELEMENT
# import factsheet.model.fact as MFACT
# import factsheet.model.setindexed as MSET
# import factsheet.model.table as MTABLE
# import factsheet.model.topic as MTOPIC

# import gi   # type: ignore[import]
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gio   # type: ignore[import]    # noqa: E402
# from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
# from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchAdaptText(ADAPT.AdaptText[typing.Any, typing.Any]):
    """:class:`.AdaptText` subclass with stub text property."""

    def __init__(self):
        super().__init__()
        self.bound = []
        self.loosed = []

    def _bind_store(self, p_view):
        self.bound.append(p_view)

    def _loose_store(self, p_view):
        self.loosed = [p_view]

    def _new_store_gtk(self):
        return str()

    @property
    def text(self): return self._text_gtk

    @text.setter
    def text(self, p_text): self._text_gtk = p_text


@pytest.fixture
def patch_adapt_text():
    """Pytest fixture: return :class:`.AdaptText` subclass with stub
    text property.
    """
    return PatchAdaptText


class PatchIdCore(MIDCORE.IdCore):
    """:class:`.IdCore` subclass with stubs for properties."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = PatchAdaptText()
        self._summary = PatchAdaptText()
        self._title = PatchAdaptText()

    @property
    def name(self):
        return self._name

    @property
    def summary(self):
        return self._summary

    @property
    def title(self):
        return self._title


@pytest.fixture
def patch_idcore():
    """Pytest fixture: return :class:`.IdCore` subclass with stub
    identity properties.
    """
    return PatchIdCore


class PatchIdCoreAbstract(MIDCORE.IdCore):
    """:class:`.IdCore` subclass with pass-through stubs for abstract
    properties.
    """

    def __init__(self):
        super().__init__()
        self._name = PatchAdaptText()
        self._summary = PatchAdaptText()
        self._title = PatchAdaptText()

    @property
    def name(self):
        prop = getattr(MIDCORE.IdCore, 'name')
        prop.fget(self)

    @property
    def summary(self):
        prop = getattr(MIDCORE.IdCore, 'summary')
        prop.fget(self)

    @property
    def title(self):
        prop = getattr(MIDCORE.IdCore, 'title')
        prop.fget(self)


@pytest.fixture
def patch_idcore_abstract():
    """Pytest fixture: return :class:`.IdCore` subclass with
    pass-through stubs for abstract properties.
    """
    return PatchIdCoreAbstract

# @pytest.fixture
# def interface_view_infoid(patch_args_infoid):
#     """Pytest fixture: return stub class implementing
#     :class:`.InterfaceViewInfoId`.
#      """
#     class PatchViewInfoId(ABC_INFOID.InterfaceViewInfoId):
#         ALL_TEXT = -1
#         INCLUDE_HIDDEN = True
# 
#         def __init__(self):
#             ARGS = patch_args_infoid
#             # self._name = UI.FACTORY_INFOID.new_view_name()
#             self._name = AINFOID.AdaptEntry()
#             self._name.set_text(ARGS.p_name)
#             # self._summary = UI.FACTORY_INFOID.new_view_summary()
#             self._summary = AINFOID.AdaptTextView()
#             buffer_summary = self._summary.get_buffer()
#             buffer_summary.set_text(
#                 ARGS.p_summary, self.ALL_TEXT)
#             # self._title = UI.FACTORY_INFOID.new_view_title()
#             self._title = AINFOID.AdaptEntry()
#             self._title.set_text(ARGS.p_title)
# 
#         def get_view_name(self): return self._name
# 
#         def get_view_summary(self): return self._summary
# 
#         def get_view_title(self): return self._title
# 
#         @property
#         def name(self): return self._name.get_text()
# 
#         @property
#         def summary(self):
#             text = AINFOID.str_adapt_textview(self.get_view_summary())
#             return text
# 
#         @property
#         def title(self): return self._title.get_text()
# 
#     return PatchViewInfoId


# @pytest.fixture
# def patch_class_block_fact(interface_view_infoid):
#     """Pytest fixture: return stub :class:`.InterfaceBlockFact` class.
#     """
#     class PatchClassBlockFact(ABC_FACT.InterfaceBlockFact):
#         def __init__(self):
#             self._infoid = interface_view_infoid()
#             self.called_update = False
# 
#         def get_infoid(self): return self._infoid
# 
#         def update(self, p_status, p_value) -> None:
#             self.called_update = True
#             self.update_status = p_status
#             self.update_value = p_value
# 
#     return PatchClassBlockFact


# class PatchFact(MFACT.Fact[MTOPIC.Topic, int]):
#     """Stub :class:`.Fact` class with complete check and clear methods."""
# 
#     VALUE = 42
# 
#     def check(self) -> MFACT.StatusOfFact:
#         """Set fact value and set corresponding state of fact check."""
#         self._value = 42
#         self._status = MFACT.StatusOfFact.DEFINED
#         return super().check()
# 
#     def clear(self) -> None:
#         """Clear fact value and set corresponding state of fact check."""
#         self._value = None
#         self._status = MFACT.StatusOfFact.UNCHECKED
#         super().clear()


# @pytest.fixture
# def patch_class_fact():
#     """Pytest fixture: return stub :class:`.Fact` class with complete
#     check and clear methods.
#     """
#     return PatchFact


# @pytest.fixture
# def factory_topic():
#     """Pytest fixture: return factory for :class:`Topic` with facts
#     outline.
# 
#     :param p_top_facts: number of top-level facts.
#     :param p_depth_facts: number of outline levels below top level.
#     """
#     def new_topic(*, p_top_facts=3, p_depth_facts=2):
#         TITLE_MODEL = 'Something completely different.'
#         topic = MTOPIC.Topic()
#         topic.init_identity(p_title=TITLE_MODEL)
# 
#         for i in range(p_top_facts):
#             fact = PatchFact(p_topic=topic)
#             fact.init_identity(p_name='Fact {}'.format(i))
#             topic.insert_fact_before(fact, None)
#         parent = topic._facts._gtk_model.get_iter_first()
#         for j in range(p_depth_facts):
#             name = '\t'*(j+1) + 'Fact {}'.format(j + p_top_facts)
#             fact = PatchFact(p_topic=topic)
#             fact.init_identity(p_name=name)
#             parent = topic.insert_fact_child(fact, parent)
#         return topic
# 
#     return new_topic


# class Factsheet(Gtk.Application):
#     """Stub :class:`.Factsheet` class."""
# 
#     def __init__(self, *args, **kwargs):
#         super().__init__(application_id='com.novafolks.factsheet',
#                          flags=Gio.ApplicationFlags.FLAGS_NONE,
#                          *args, **kwargs)
# 
#     def do_activate(self):
#         pass
# 
#     def do_startup(self):
#         Gtk.Application.do_startup(self)


# @pytest.fixture
# def patch_factsheet():
#     """Pytest fixture: return stub :class:`.Factsheet` class."""
#     return Factsheet


# @DC.dataclass
# class ArgsInfoId:
#     """Convenience class for assembling arguments to
#     :class:`.InfoId` method ``__init__``.
#     """
#     p_name: str
#     p_summary: str
#     p_title: str


# @pytest.fixture
# def patch_args_infoid():
#     """Pytest fixture: return set of argument values to construct a
#     stock :class:`InfoId` object.
#     """
#     return ArgsInfoId(
#         p_name='Parrot',
#         p_summary='The parrot is a Norwegian Blue.',
#         p_title='The Parrot Sketch',
#         )


# @DC.dataclass
# class ArgsArray:
#     """Convenience class for assembling arguments to
#     :class:`.Array` constructor expression.
#     """
#     p_rows: Gtk.ListStore
#     p_cols: typing.Sequence
#     p_styles: typing.Sequence[MELEMENT.Style]
#     p_title: str
#     p_symbol_row: str
#     p_symbol_col: str
#     p_symbol_entry: str


# @pytest.fixture
# def patch_args_array():
#     """Pytest fixture: return argument list to construct a stock
#     :class:`.Array` object.
#     """
#     Set = MSET.SetIndexed[int]
#     Element = MELEMENT.ElementOpaque[int]
#     N_ROWS = 3
#     N_COLUMNS = 4
#     size = N_ROWS * N_COLUMNS
#     range_r = range(0, size, N_COLUMNS)
#     range_c = range(0, size, N_ROWS)
#     ROWS = Gtk.ListStore(*[GO.TYPE_PYOBJECT]*(1+N_COLUMNS))
#     for i, r in enumerate(range_r):
#         row = [Element(p_member=r, p_index=i)]
#         entries = Set([(r+c) % size for c in range_c])
#         row.extend(entries)
#         ROWS.append(row)
#     set_cols = Set(range_c)
#     COLS = list(set_cols)
#     STYLES = [MELEMENT.Style('Label'), MELEMENT.Style('Element'),
#               MELEMENT.Style('Index'), MELEMENT.Style('Member'),
#               MELEMENT.Style('Plain'), MELEMENT.Style('Oops!'),
#               ]
#     TITLE = 'Array'
#     SYMBOL_ROW = 'r'
#     SYMBOL_COL = 'c'
#     SYMBOL_ENTRY = 'e'
#     return ArgsArray(
#         p_rows=ROWS,
#         p_cols=COLS,
#         p_styles=STYLES,
#         p_title=TITLE,
#         p_symbol_row=SYMBOL_ROW,
#         p_symbol_col=SYMBOL_COL,
#         p_symbol_entry=SYMBOL_ENTRY,
#         )


# @DC.dataclass
# class ArgsTable:
#     """Convenience class assembles arguments to
#     :meth:`.TableElements.__init__` for pytest fixture.
#     """
#     rows: Gtk.ListStore
#     columns: typing.Sequence[MTABLE.InfoColumn]


# @pytest.fixture
# def patch_args_table():
#     """Pytest fixture: return arguments for
#     :meth:`.TableElements.__init__`.
#     """
#     set_int = MSET.SetIndexed[int]([0, 2, 4, 6, 8])
#     set_str = MSET.SetIndexed[str](['a', 'e', 'i', 'o', 'u'])
#     list_mix = [MELEMENT.ElementOpaque('x', 0), None,
#                 MELEMENT.ElementOpaque('y', 1), None,
#                 MELEMENT.ElementOpaque('z', 2)]
#     rows = Gtk.ListStore(GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT)
#     for e_int, e_str, e_mix in zip(set_int, set_str, list_mix):
#         rows.append([e_int, e_str, e_mix])
#     info_int = MTABLE.InfoColumn(title='Integers', symbol='i', styles=[
#         'Label', 'Element', 'Index', 'Member', 'Plain'])
#     info_str = MTABLE.InfoColumn(title='Strings', symbol='s', styles=[
#         'Label', 'Element', 'Index', 'Member', 'Plain', 'Oops'])
#     info_mix = MTABLE.InfoColumn(title='Mixed', symbol='m', styles=[
#         'Label', 'Element', 'Index', 'Member', 'Plain'])
#     columns = [info_int, info_str, info_mix]
#     return ArgsTable(
#         rows=rows,
#         columns=columns,
#         )


@pytest.fixture
def PatchLogger():
    """Pytest fixture: return stub `logging.logger <LoggingLogger_>`_.

    .. _LoggingLogger: https://docs.python.org/3.7/library/logging.html
       #logger-objects
    """
    class Logger:
        T_CRITICAL = 'critical'
        T_DEBUG = 'debug'
        T_ERROR = 'error'
        T_NONE = 'none'
        T_WARNING = 'warning'

        def __init__(self):
            self.called = False
            self.level = self.T_NONE
            self.message = "No log call"

        def critical(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_CRITICAL
            self.message = p_message

        def debug(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_DEBUG
            self.message = p_message

        def error(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_ERROR
            self.message = p_message

        def warning(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_WARNING
            self.message = p_message

    return Logger

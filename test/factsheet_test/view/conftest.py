"""
Test fixtures for :mod:`~.factsheet.view` unit tests.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET
from factsheet.model import table as MTABLE
from factsheet.model import topic as MTOPIC
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def new_outline_topics():
    """Pytest fixture returns outline model factory.  The structure of
    each model is as follows.

        | name_0xx | title_0xx | summary_0xx
        |     name_00x | title_00x | summary_00x
        |         name_000 | title_000 | summary_000
        |     name_01x | title_01x | summary_01x
        | name_1xx | title_1xx | summary_1xx
        |     name_10x | title_10x | summary_10x
        |     name_11x | title_11x | summary_11x
        |         name_110 | title_110 | summary_110
        |         name_111 | title_111 | summary_111
        |         name_112 | title_112 | summary_112
    """
    def new_model():
        model = UI.FACTORY_SHEET.new_model_outline_topics()
        gtk_model = model._gtk_model

        item = MTOPIC.Topic(
            p_name='name_0xx', p_title='title_0xx', p_summary='summary_0xx')
        i_0xx = gtk_model.append(None, [item])
        item = MTOPIC.Topic(
            p_name='name_00x', p_title='title_00x', p_summary='summary_00x')
        i_00x = gtk_model.append(
            i_0xx, [item])
        item = MTOPIC.Topic(
            p_name='name_000', p_title='title_000', p_summary='summary_000')
        _i_000 = gtk_model.append(i_00x, [item])
        item = MTOPIC.Topic(
            p_name='name_01x', p_title='title_01x', p_summary='summary_01x')
        i_0xx = gtk_model.append(i_0xx, [item])
        item = MTOPIC.Topic(
            p_name='name_1xx', p_title='title_1xx', p_summary='summary_1xx')
        i_1xx = gtk_model.append(None, [item])
        item = MTOPIC.Topic(
            p_name='name_10x', p_title='title_10x', p_summary='summary_10x')
        _i_10x = gtk_model.append(i_1xx, [item])
        item = MTOPIC.Topic(
            p_name='name_11x', p_title='title_11x', p_summary='summary_11x')
        i_11x = gtk_model.append(i_1xx, [item])
        item = MTOPIC.Topic(
            p_name='name_110', p_title='title_110', p_summary='summary_110')
        _i_110 = gtk_model.append(i_11x, [item])
        item = MTOPIC.Topic(
            p_name='name_111', p_title='title_111', p_summary='summary_111')
        _i_111 = gtk_model.append(i_11x, [item])
        item = MTOPIC.Topic(
            p_name='name_112', p_title='title_112', p_summary='summary_112')
        _i_112 = gtk_model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_dialog_run():
    """Pytest fixture returns stub `GtkDialog <GtkDialog_>`_.

    .. _GtkDialog: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/Dialog.html
    """
    class PatchDialog:
        def __init__(self, p_response):
            self.called = False
            self.response = p_response

        def run(self):
            self.called = True
            return self.response

    return PatchDialog


@pytest.fixture
def text_ui_infoid():
    """Pytest fixture returns set of argument values to construct
    a stock :class:`.ViewInfoId` object.
    """
    return dict(
        name='UI InfoId Name',
        title='UI InfoId Title',
        summary='This summarizes UI identification.',
        )


@pytest.fixture
def patch_ui_infoid(text_ui_infoid):
    """Pytest fixture returns stub builder defintion for
    :class:`.ViewInfoId`.
    """
    ui_infoid = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.22.1 -->
        <interface>
          <requires lib="gtk+" version="3.20"/>
          <object class="GtkEntry" id="ui_name_infoid">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="text" translatable="yes">{name}</property>
          </object>
          <object class="GtkTextBuffer" id="buffer_summary">
            <property name="text" translatable="yes">{summary}</property>
          </object>
          <object class="GtkTextView" id="ui_summary_infoid">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="buffer">buffer_summary</property>
          </object>
          <object class="GtkEntry" id="ui_title_infoid">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="text" translatable="yes">{title}</property>
          </object>
        </interface>
        '''.format(**text_ui_infoid)
    builder = Gtk.Builder.new_from_string(ui_infoid, -1)
    return builder.get_object

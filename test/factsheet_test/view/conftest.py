"""
Test fixtures for :mod:`~.factsheet.view` unit tests.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


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

"""
factsheet_test.view.conftest - test fixtures for View classes.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def text_ui_infoid():
    return dict(
        name='UI InfoId Name',
        title='UI InfoId Title',
        # summary='This summarizes UI identification.',
        )


@pytest.fixture
def patch_ui_infoid(text_ui_infoid):
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
          <object class="GtkEntry" id="ui_title_infoid">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="text" translatable="yes">{title}</property>
          </object>
        </interface>
        '''.format(**text_ui_infoid)
    builder = Gtk.Builder.new_from_string(ui_infoid, -1)
    return builder.get_object

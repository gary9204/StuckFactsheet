"""
TBD
"""
from gi.repository import Gtk   # type: ignore[import]

import logging

logger = logging.getLogger('Main.ui_factory')

if 3 == Gtk.MAJOR_VERSION:
    import factsheet.ui_bricks.ui_gtk3.new_brick_gtk3 as NEWBRICK
else:
    message_error = (
        'Unsupported user interface toolkit: GTK {}.{}.{}'
        ''.format(Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION))
    print(message_error)
    logger.critical(message_error)
    raise NotImplementedError

new_brick = NEWBRICK.NewBrickGtk3()

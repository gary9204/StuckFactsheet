# noqa
"""
Defines classes to adapt Factsheet model to GTK widget toolkit.
"""
from . import adapt_text as ATEXT

from . import adapt_value as AVALUE
from . adapt_value import AspectValueOpaque  # noqa
from . adapt_value import ValueOpaque  # noqa

AdaptText = ATEXT.AdaptText
AdaptTextFormat = ATEXT.AdaptTextFormat
AdaptTextMarkup = ATEXT.AdaptTextMarkup
AdaptTextStatic = ATEXT.AdaptTextStatic
AdaptValue = AVALUE.AdaptValue

AspectValueText = AVALUE.AspectValueText

ValueAny = AVALUE.ValueAny

ViewTextFormat = ATEXT.ViewTextFormat
ViewTextMarkup = ATEXT.ViewTextMarkup
ViewTextStatic = ATEXT.ViewTextStatic

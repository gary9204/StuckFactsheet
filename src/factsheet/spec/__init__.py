"""
Specifications to define topics with facts for Factsheet content.
"""
import factsheet.bridge_ui as BUI
import factsheet.spec.base_s as SBASE
from . import sets as SSETS
from . import ops as SOPS


g_specs = BUI.ModelOutlineMulti[SBASE.Base]()

_line_basic = g_specs.insert_after(p_item=SBASE.g_spec_basic)
g_specs.insert_section(SSETS.g_specs, _line_basic)
g_specs.insert_section(SOPS.g_specs, _line_basic)

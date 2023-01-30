"""
Defines Sets section of Factsheet specifications.  See :mod:`~.factsheet.spec`.
"""
import factsheet.bridge_ui as BUI
import factsheet.spec.base_s as SBASE

_spec_sets = SBASE.Base(
    p_name='Stub Sets',
    p_summary=('Stub for Sets section of Factsheet specifications.'
               ),
    p_title='Stub Sets Topic')


g_specs = BUI.ModelOutlineMulti[SBASE.Base]()

_ = g_specs.insert_after(p_item=_spec_sets)

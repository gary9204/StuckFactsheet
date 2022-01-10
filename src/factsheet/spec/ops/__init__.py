"""
Defines Operations section of Factsheet specifications.
See :mod:`~.factsheet.spec`.
"""
import factsheet.bridge_ui as BUI
import factsheet.spec.base_s as SBASE

_spec_ops = SBASE.Base(
    p_name='Stub Operations',
    p_summary=('Stub for Operations section of Factsheet specifications.'
               ),
    p_title='Stub Ops Topic')


g_specs = BUI.ModelOutlineMulti[SBASE.Base]()

_ = g_specs.insert_after(p_item=_spec_ops)

"""
Defines class to display fact in a topic pane.  See :mod:`.pane_topic`.
"""
from factsheet.abc_types import abc_fact as ABC_FACT
from factsheet.abc_types import abc_infoid as ABC_INFOID


ValueOfFact = ABC_FACT.ValueOfFact


class BlockFact(ABC_FACT.InterfaceBlockFact[ValueOfFact]):
    """STUB - Display fact and translate user actions. """

    def checked(self, p_value: ValueOfFact) -> None:
        pass

    def cleared(self, p_value: ValueOfFact) -> None:
        pass

    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        pass

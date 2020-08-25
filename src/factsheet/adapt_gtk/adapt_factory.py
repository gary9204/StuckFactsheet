"""
Defines GTK-based classes that implement abstract factories in
:mod:`.abc_factory`.

.. data:: IndexOutline

    Type for index to item in an outline.

.. data:: OutlineTemplates

    Type for outline containing templates.

.. data:: OutlineTopics

    Type for outline containing topics.
"""
# import logging
# import typing

# from factsheet.abc_types import abc_fact as ABC_FACT
# from factsheet.abc_types import abc_factory as ABC_FACTORY
# from factsheet.abc_types import abc_topic as ABC_TOPIC
# from factsheet.adapt_gtk import adapt_infoid as AINFOID
# from factsheet.adapt_gtk import adapt_outline as AOUTLINE
# from factsheet.adapt_gtk import adapt_sheet as ASHEET
# from factsheet.adapt_gtk import adapt_topic as ATOPIC
# # ERROR: Circular import
# # from factsheet.view.block import block_fact as VFACT

# logger = logging.getLogger('Main.model.adapt_factory')


# class FactoryFact(ABC_FACTORY.FactoryFact):
#     """Implements factory for abstract factory
#     :class:`~.abc_factory.FactoryFact`.
#     """

#     def __init__(self):
#         self._fact_to_block: typing.MutableMapping[
#             typing.Type[ABC_FACT.AbstractFact],
#             typing.Type[ABC_FACT.InterfaceBlockFact]] = dict()
#         # ERROR: Circular import
#         self._block_default = None  # VFACT.BlockFact

#     def new_block_fact(self, p_fact: ABC_FACT.AbstractFact
#                        ) -> ABC_FACT.InterfaceBlockFact:
#         """Return new fact block instance suited to display given fact.

#         :param p_fact: fact to display.
#         """
#         class_block = self._fact_to_block.get(
#             type(p_fact), self._block_default)
#         assert class_block is not None
#         return class_block()

#     def register_block(
#             self, p_class_fact: typing.Type[ABC_FACT.AbstractFact],
#             p_class_block: typing.Type[ABC_FACT.InterfaceBlockFact]) -> None:
#         """Associate block class with fact class.

#         Method logs a warning when called with distince block classes
#         and a common fact class.

#         Method :meth:`.new_block_fact` uses the association from fact
#         classes to block classes when creating block instances.

#         :param p_class_fact: target fact class.
#         :param p_class_block: block class for fact class.
#         """
#         # self._fact_to_block[p_class_fact] = p_class_block
#         class_block = self._fact_to_block.setdefault(
#             p_class_fact, p_class_block)
#         if class_block is not p_class_block:
#             logger.warning(
#                 'Fact class assigned duplicate block class:\n\t{} <- {} '
#                 '({}.{}).'.format(
#                     p_class_fact.__name__, p_class_block.__name__,
#                     self.__class__.__name__, self.register_block.__name__))


# class FactoryInfoId(ABC_FACTORY.FactoryInfoId):
#     """Implements GTK-based factory for abstract factory
#     :class:`.abc_factory.FactoryInfoId`."""

#     def new_model_name(self, p_text: str = '') -> AINFOID.AdaptEntryBuffer:
#         """Return new instance of Gtk-based :mod:`~factsheet.model` name."""
#         return AINFOID.AdaptEntryBuffer(p_text=p_text)

#     def new_model_summary(self, p_text: str = '') -> AINFOID.AdaptTextBuffer:
#         """Return new instance of Gtk-based :mod:`~factsheet.model`
#         summary.
#         """
#         return AINFOID.AdaptTextBuffer(p_text=p_text)

#     def new_model_title(self, p_text: str = '') -> AINFOID.AdaptEntryBuffer:
#         """Return new instance of Gtk-based :mod:`~factsheet.model` title."""
#         return AINFOID.AdaptEntryBuffer(p_text=p_text)


# IndexOutline = AOUTLINE.AdaptIndex
# OutlineTemplates = ASHEET.AdaptTreeStoreTemplate
# OutlineTopics = ASHEET.AdaptTreeStoreTopic
# ViewOutlineTemplates = ASHEET.AdaptTreeViewTemplate
# ViewOutlineTopics = ASHEET.AdaptTreeViewTopic


# class FactorySheet(ABC_FACTORY.FactorySheet):
#     """Implements GTK-based factory for abstract factory
#     :class:`.abc_factory.FactorySheet`."""

#     def new_model_outline_templates(self) -> OutlineTemplates:
#         """Return new instance of Gtk-based template outline"""
#         return OutlineTemplates()

#     def new_model_outline_topics(self) -> OutlineTopics:
#         """Return new instance of Gtk-based topic outline."""
#         return OutlineTopics()


# IdTopic = ABC_TOPIC.IdTopic
# OutlineFacts = ATOPIC.AdaptTreeStoreFact
# ViewOutlineFacts = ATOPIC.AdaptTreeViewFact


# class FactoryTopic(ABC_FACTORY.FactoryTopic):
#     """Implements GTK-based factory for abstract factory
#     :class:`.abc_factory.FactoryTopic`."""

#     def new_model_outline_facts(self) -> OutlineFacts:
#         """Return new instance of Gtk-based fact outline."""
#         return OutlineFacts()

#     def new_view_outline_facts(self) -> ViewOutlineFacts:
#         """Return new instance of Gtk-based fact view outline."""
#         return ViewOutlineFacts()

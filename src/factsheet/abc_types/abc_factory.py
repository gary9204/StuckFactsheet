"""
Defines abstract factory classes.

:doc:`../guide/devel_notes` describes the use of abstract classes to
encapsulate dependencies of :mod:`~factsheet.model` on a user interface
widget toolkit.  Module ``abc_factory`` defines abstract factories for
component classes of :class:`.InfoId`.
"""
# import abc
# import typing

# from factsheet.abc_types import abc_fact as ABC_FACT
# from factsheet.abc_types import abc_infoid as ABC_INFOID
# from factsheet.abc_types import abc_outline as ABC_OUTLINE


# class FactoryFact(abc.ABC):
#     """Defines abstract factory to produce factsheet components for
#     :class:`.Fact` and :class:`.BlockFact`.
#     """

#     @abc.abstractmethod
#     def new_block_fact(self, p_fact: ABC_FACT.AbstractFact
#                        ) -> ABC_FACT.InterfaceBlockFact:
#         """Return new block to display given fact.

#         :param p_fact: fact to display.
#         """
#         raise NotImplementedError

#     @abc.abstractmethod
#     def register_block(
#             self, p_class_fact: typing.Type[ABC_FACT.AbstractFact],
#             p_class_type: typing.Type[ABC_FACT.InterfaceBlockFact]) -> None:
#         """Associate block class with fact class.

#         Method :meth:`.new_block_fact` uses the association from fact
#         classes to block classes when creating block instances.

#         :param p_class_fact: target fact class.
#         :param p_class_block: block class for fact class.
#         """
#         raise NotImplementedError


# class FactoryInfoId(abc.ABC):
#     """Defines abstract factory to produce identification information
#     components for :class:`~.InfoId` and :class:`~.ViewInfoId`.
#     """

#     @abc.abstractmethod
#     def new_model_name(
#             self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
#         """Return new instance of name for :class:`.InfoId`.
#         """
#         raise NotImplementedError

#     @abc.abstractmethod
#     def new_model_summary(
#             self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
#         """Return new instance of summary for :class:`.InfoId`.
#         """
#         raise NotImplementedError

#     @abc.abstractmethod
#     def new_model_title(
#             self, p_text: str = '') -> ABC_INFOID.AbstractTextModel:
#         """Return new instance of title for :class:`.InfoId`.
#         """
#         raise NotImplementedError


# class FactorySheet(abc.ABC):
#     """Defines abstract factory to produce factsheet components for
#     :class:`~.model.sheet.Sheet` and :class:`.PageSheet`.
#     """

#     @abc.abstractmethod
#     def new_model_outline_templates(self) -> ABC_OUTLINE.AbstractOutline:
#         """Return new instance of templates outline class for
#         :class:`~.model.sheet.Sheet`.
#         """
#         raise NotImplementedError

#     @abc.abstractmethod
#     def new_model_outline_topics(self) -> ABC_OUTLINE.AbstractOutline:
#         """Return new instance of topics outline class for
#         :class:`~.model.sheet.Sheet`.
#         """
#         raise NotImplementedError


# class FactoryTopic(abc.ABC):
#     """Defines abstract factory to produce components for
#     :class:`.Topic` and :class:`.PaneTopic`.
#     """

#     @abc.abstractmethod
#     def new_model_outline_facts(self) -> ABC_OUTLINE.AbstractOutline:
#         """Return new instance of facts outline class for
#         :class:`.Topic`.
#         """
#         raise NotImplementedError

#     @abc.abstractmethod
#     def new_view_outline_facts(self) -> ABC_OUTLINE.AbstractViewOutline:
#         """Return new instance of facts outline view class for
#         :class:`.PaneTopic`.
#         """
#         raise NotImplementedError

"""
Unit tests for GTK-based factories.  See :mod:`.adapt_factory`.
"""
# import logging
# import pytest   # type: ignore[import]
# import typing

# from factsheet.abc_types import abc_fact as ABC_FACT
# from factsheet.abc_types import abc_infoid as ABC_INFOID
# from factsheet.abc_types import abc_topic as ABC_TOPIC
# from factsheet.adapt_gtk import adapt_factory as AFACTORY
# from factsheet.adapt_gtk import adapt_infoid as AINFOID
# from factsheet.adapt_gtk import adapt_outline as AOUTLINE
# from factsheet.adapt_gtk import adapt_sheet as ASHEET
# from factsheet.adapt_gtk import adapt_topic as ATOPIC
# from factsheet.view.block import block_fact as VFACT


# class PatchClassFact(ABC_FACT.AbstractFact):
#     """Defines test stub for :class:`.AbstractFact`."""

#     def id_fact(self):
#         return ABC_FACT.IdFact(id(self))

#     @property
#     def name(self):
#         return 'No name.'

#     @property
#     def status(self):
#         return ABC_FACT.StatusOfFact.BLOCKED

#     @property
#     def summary(self):
#         return 'No summary.'

#     @property
#     def title(self):
#         return 'No title.'

#     def is_fresh(self):
#         return False

#     def is_stale(self):
#         return False

#     def set_fresh(self):
#         pass

#     def set_stale(self):
#         pass


# ValueInt = typing.Union[ABC_FACT.StatusOfFact, int]


# class PatchClassBlockFact(ABC_FACT.InterfaceBlockFact[int]):
#     """Defines test stub for  :class:`.InterfaceBlockFact`.
#     """

#     def update_value(self, p_value: ValueInt) -> None:
#         pass

#     def cleared(self, p_value: ValueInt) -> None:
#         pass

#     def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
#         pass


# @pytest.fixture
# def patch_pairs_class():
#     CLASS_FACT = PatchClassFact

#     class CLASS_FACT_1(CLASS_FACT):
#         pass

#     class CLASS_FACT_2(CLASS_FACT):
#         pass

#     CLASS_BLOCK = PatchClassBlockFact

#     class CLASS_BLOCK_1(CLASS_BLOCK):
#         pass

#     pairs = [(CLASS_FACT, CLASS_BLOCK),
#              (CLASS_FACT_1, CLASS_BLOCK_1),
#              (CLASS_FACT_2, CLASS_BLOCK), ]
#     return pairs


# class TestFactoryFact:
#     """Unit tests for :class:`~.adapt_factory.FactoryFact`."""

#     @pytest.mark.skip(reason='Pending resolution of circular import.')
#     def test_init(self):
#         """Confirm initialization."""
#         # Setup
#         # Test
#         target = AFACTORY.FactoryFact()
#         assert target is not None
#         assert isinstance(target._fact_to_block, dict)
#         assert target._block_default is VFACT.BlockFact

#     def test_new_block_fact(self, patch_pairs_class):
#         """| Confirm block class returned.
#         | Case: block class registered for fact class.
#         """
#         # Setup
#         PAIRS = patch_pairs_class
#         I_FACT = 0
#         I_BLOCK = 1
#         target = AFACTORY.FactoryFact()
#         for c_fact, c_block in PAIRS:
#             target.register_block(c_fact, c_block)

#         I_TARGET = 1
#         class_fact = PAIRS[I_TARGET][I_FACT]
#         fact = class_fact()
#         class_block = PAIRS[I_TARGET][I_BLOCK]
#         # Test
#         result = target.new_block_fact(fact)
#         assert isinstance(result, class_block)

#     @pytest.mark.skip(reason='Pending resolution of circular import.')
#     def test_new_block_fact_default(self, patch_pairs_class):
#         """| Confirm block class returned.
#         | Case: no block class registered for fact class.
#         """
#         # Setup
#         PAIRS = patch_pairs_class
#         target = AFACTORY.FactoryFact()
#         for c_fact, c_block in PAIRS:
#             target.register_block(c_fact, c_block)

#         class ClassMissing(PatchClassFact):
#             pass
#         fact = ClassMissing()
#         # Test
#         result = target.new_block_fact(fact)
#         assert isinstance(result, target._block_default)

#     def test_register_block(self, patch_pairs_class):
#         """Confirm association from fact class to view class."""
#         PAIRS = patch_pairs_class
#         target = AFACTORY.FactoryFact()
#         # Test
#         for class_fact, class_block in PAIRS:
#             target.register_block(class_fact, class_block)
#             assert target._fact_to_block[class_fact] is class_block

#     def test_register_block_warn(
#             self, PatchLogger, monkeypatch, patch_pairs_class):
#         """Confirm association from fact class to view class."""
#         # Setup
#         PAIRS = patch_pairs_class
#         I_FACT = 0
#         I_BLOCK = 1
#         target = AFACTORY.FactoryFact()
#         for c_fact, c_block in PAIRS:
#             target.register_block(c_fact, c_block)

#         I_DUP = 2
#         class_fact_dup = PAIRS[I_DUP][I_FACT]
#         I_NEW = 1
#         class_block_new = PAIRS[I_NEW][I_BLOCK]

#         patch_logger = PatchLogger()
#         monkeypatch.setattr(logging.Logger, 'warning', patch_logger.warning)
#         log_message = (
#             'Fact class assigned duplicate block class:\n\t{} <- {} '
#             '(FactoryFact.register_block).'
#             ''.format(class_fact_dup.__name__, class_block_new.__name__))
#         # Test
#         target.register_block(class_fact_dup, class_block_new)
#         assert patch_logger.called
#         assert PatchLogger.T_WARNING == patch_logger.level
#         assert log_message == patch_logger.message


# class TestFactoryInfoId:
#     """Unit tests for :class:`~.adapt_factory.FactoryInfoId`."""

#     @pytest.mark.parametrize('NAME_METHOD, CLASS_ATTR', [
#         ('new_model_name', AINFOID.AdaptEntryBuffer),
#         ('new_model_summary', AINFOID.AdaptTextBuffer),
#         ('new_model_title', AINFOID.AdaptEntryBuffer),
#         ])
#     def test_new_attr_model(self, NAME_METHOD, CLASS_ATTR):
#         """Confirm factory produces instance of each
#         :mod:`~factsheet.model` attribute.
#         """
#         # Setup
#         factory = AFACTORY.FactoryInfoId()
#         TEXT = 'Something completely different'
#         target = getattr(factory, NAME_METHOD)
#         # Test
#         attr_model = target(p_text=TEXT)
#         assert isinstance(attr_model, CLASS_ATTR)
#         assert TEXT == str(attr_model)


# class TestFactorySheet:
#     """Unit tests for :class:`~.adapt_factory.FactorySheet`."""

#     @pytest.mark.parametrize('NAME_METHOD, CLASS_ATTR', [
#         ('new_model_outline_templates', ASHEET.AdaptTreeStoreTemplate),
#         # ('new_view_outline_templates', ASHEET.AdaptTreeViewTemplate),
#         ('new_model_outline_topics', ASHEET.AdaptTreeStoreTopic),
#         # ('new_view_outline_topics', ASHEET.AdaptTreeViewTopic),
#         ])
#     def test_new_attr(self, NAME_METHOD, CLASS_ATTR):
#         """Confirm factory produces instance of each
#         :mod:`~factsheet.model` and each :mod:`~factsheet.view`
#         attribute.
#         """
#         # Setup
#         FACTORY = AFACTORY.FactorySheet()
#         target = getattr(FACTORY, NAME_METHOD)
#         # Test
#         attr_model = target()
#         assert isinstance(attr_model, CLASS_ATTR)

#     def test_types(self):
#         """Confirm alias definitions for type hints."""
#         # Setup
#         # Test
#         assert AFACTORY.IndexOutline is AOUTLINE.AdaptIndex
#         assert AFACTORY.OutlineTemplates is ASHEET.AdaptTreeStoreTemplate
#         assert AFACTORY.OutlineTopics is ASHEET.AdaptTreeStoreTopic
#         assert AFACTORY.ViewOutlineTemplates is ASHEET.AdaptTreeViewTemplate
#         assert AFACTORY.ViewOutlineTopics is ASHEET.AdaptTreeViewTopic


# class TestFactoryTopic:
#     """Unit tests for :class:`~.adapt_factory.FactoryTopic`."""

#     @pytest.mark.parametrize('NAME_METHOD, CLASS_ATTR', [
#         ('new_model_outline_facts', ATOPIC.AdaptTreeStoreFact),
#         ('new_view_outline_facts', ATOPIC.AdaptTreeViewFact),
#         ])
#     def test_new_attr(self, NAME_METHOD, CLASS_ATTR):
#         """Confirm factory produces instance of each
#         :mod:`~factsheet.model` and each :mod:`~factsheet.view`
#         attribute.
#         """
#         # Setup
#         FACTORY = AFACTORY.FactoryTopic()
#         target = getattr(FACTORY, NAME_METHOD)
#         # Test
#         attr_model = target()
#         assert isinstance(attr_model, CLASS_ATTR)

#     def test_types(self):
#         """Confirm types defined."""
#         # Setup
#         # Test
#         assert AFACTORY.IdTopic is ABC_TOPIC.IdTopic
#         assert AFACTORY.OutlineFacts is ATOPIC.AdaptTreeStoreFact
#         assert AFACTORY.ViewOutlineFacts is ATOPIC.AdaptTreeViewFact

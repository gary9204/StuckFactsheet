"""
Unit tests for abstract factory classes.  See :mod:`.abc_factory`.
"""

# import pytest   # type: ignore[import]

# from factsheet.abc_types import abc_factory as ABC_FACTORY


class TestFactoryFact:
    """Unit tests for abstract factory :class:`~.abc_factory.FactoryFact`."""

    pass

    # def test_abstract_class(self):
    #     """Confirm the factory class is abstract."""
    #     # Setup
    #     # Test
    #     with pytest.raises(TypeError):
    #         _ = ABC_FACTORY.FactoryFact()

    # @pytest.mark.parametrize('NAME_METHOD', [
    #     'new_block',
    #     'register',
    #     ])
    # def test_must_override(self, NAME_METHOD):
    #     """Confirm each method must be overridden."""
    #     # Setup
    #     class PatchFactory(ABC_FACTORY.FactoryFact):

    #         def new_block(self):
    #             super().new_block(None)

    #         def register(self):
    #             super().register(None, None)

    #     target = PatchFactory()
    #     # Test
    #     with pytest.raises(NotImplementedError):
    #         method = getattr(target, NAME_METHOD)
    #         method()


class TestFactoryInfoId:
    """Unit tests for abstract factory :class:`~.abc_factory.FactoryInfoId`."""

    pass

    # def test_abstract_class(self):
    #     """Confirm the factory class is abstract."""
    #     # Setup
    #     # Test
    #     with pytest.raises(TypeError):
    #         _ = ABC_FACTORY.FactoryInfoId()

    # @pytest.mark.parametrize('NAME_METHOD', [
    #     'new_model_name',
    #     'new_model_summary',
    #     'new_model_title',
    #     # 'new_view_name',
    #     # 'new_view_summary',
    #     # 'new_view_title',
    #     ])
    # def test_must_override(self, NAME_METHOD):
    #     """Confirm each method must be overridden."""
    #     # Setup
    #     class PatchFactory(ABC_FACTORY.FactoryInfoId):
    #         def new_model_name(self): super().new_model_name()

    #         def new_model_summary(self): super().new_model_summary()

    #         def new_model_title(self): super().new_model_title()

    #         # def new_view_name(self): super().new_view_name()

    #         # def new_view_summary(self): super().new_view_summary()

    #         # def new_view_title(self): super().new_view_title()

    #     target = PatchFactory()
    #     # Test
    #     with pytest.raises(NotImplementedError):
    #         method = getattr(target, NAME_METHOD)
    #         method()


class TestFactorySheet:
    """Unit tests for abstract factory :class:`~.abc_factory.FactorySheet`."""

    pass

    # def test_abstract_class(self):
    #     """Confirm the factory class is abstract."""
    #     # Setup
    #     # Test
    #     with pytest.raises(TypeError):
    #         _ = ABC_FACTORY.FactorySheet()

    #    @pytest.mark.parametrize('NAME_METHOD', [
    #        'new_model_outline_templates',
    #        # 'new_view_outline_templates',
    #        'new_model_outline_topics',
    #        # 'new_view_outline_topics',
    #        ])
    #    def test_must_override(self, NAME_METHOD):
    #        """Confirm each method must be overridden."""
    #        # Setup
    #        class PatchFactory(ABC_FACTORY.FactorySheet):
    #            def new_model_outline_templates(self):
    #                super().new_model_outline_templates()

    #            # def new_view_outline_templates(self):
    #            #     super().new_view_outline_templates()

    #            def new_model_outline_topics(self):
    #                super().new_model_outline_topics()

    #            # def new_view_outline_topics(self):
    #            #     super().new_view_outline_topics()

    #        target = PatchFactory()
    #        # Test
    #        with pytest.raises(NotImplementedError):
    #            method = getattr(target, NAME_METHOD)
    #            method()


class TestFactoryTopic:
    """Unit tests for abstract factory :class:`~.abc_factory.FactoryTopic`."""

    pass

    # def test_abstract_class(self):
    #     """Confirm the factory class is abstract."""
    #     # Setup
    #     # Test
    #     with pytest.raises(TypeError):
    #         _ = ABC_FACTORY.FactoryTopic()

    # @pytest.mark.parametrize('NAME_METHOD', [
    #     'new_model_outline_facts',
    #     'new_view_outline_facts',
    #     ])
    # def test_must_override(self, NAME_METHOD):
    #     """Confirm each method must be overridden."""
    #     # Setup
    #     class PatchFactory(ABC_FACTORY.FactoryTopic):
    #         def new_model_outline_facts(self):
    #             super().new_model_outline_facts()

    #         def new_view_outline_facts(self):
    #             super().new_view_outline_facts()

    #     target = PatchFactory()
    #     # Test
    #     with pytest.raises(NotImplementedError):
    #         method = getattr(target, NAME_METHOD)
    #         method()

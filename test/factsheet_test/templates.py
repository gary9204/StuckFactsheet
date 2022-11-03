"""
Templates for tests common to multiple classes.

Test class names include prefix "Temp".  Test method names include
prefix "temp_".  These prefixes prefent pytest from collectiong the
templates.
"""
import pytest
import typing


class TempClassAbc:

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        # (MODULE.Class, 'method_name'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: class that should be abstract.
        :param NAME_METHOD: method that should be abstract.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when other is equivalent to self.

        In progress: fix for equal method (not yet a test)
        See: https://stackoverflow.com/questions/54020772/
            get-the-type-of-the-super-class-in-python-3
                Consider duck-typing comment
        See: https://stackoverflow.com/questions/10386166/
            python-self-class-vs-typeself
                Note reference is 13 years old

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, type(self)):
            raise NotImplemented
        return False


# import typing
class TempTestModule:
    """Unit tests for module-level components of :mod:`.name_module`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        # (MODULE.TypeNew.__dict__['__supertype__'], type),
        # (type(MODULE.TypeVariable), typing.TypeVar),
        # (type(MODULE.TypeVariableConstrained), typing.TypeVar),
        # (MODULE.TypeVariableConstrained.__dict__['__constraints__'],
        #     (MODULE.Constraint01, MODULE.Constraint02)),
        ])
    def temp_test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT

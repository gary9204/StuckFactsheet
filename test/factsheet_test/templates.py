"""
Templates for tests common to multiple classes.

Test class names include prefix "Temp".  Test method names include
prefix "temp_".  These prefixes prefent pytest from collectiong the
templates.
"""
import pytest
import typing


class TempClassAbc:
    """Unit test templates for classes with abstract methods."""

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


class TempProperties:
    """Unit test templates for classes with properties."""

    @pytest.mark.parametrize('PROP, ATTR', [
        ('TBD property', 'TBD attribute'),
        ])
    def test_property_access(self, PROP, ATTR):
        """Confirm access limits of each property.

        :param PROP: name of property under test.
        :param ATTR: name of attribute for property.
        """
        # Setup
        CLASS = bool  # TBD class uder test
        target = CLASS()
        attr = getattr(target, ATTR)
        target_prop = getattr(CLASS, PROP)
        # Test
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None


# import typing
class TempTestModule:
    """Unit tests for module-level components of :mod:`.TBD module`."""

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

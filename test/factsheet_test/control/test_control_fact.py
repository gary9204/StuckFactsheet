"""
Unit tests for class that mediates fact-level interactions from
:class:`.BlockFact` to :class:`.Fact`.  See :mod:`~.control_fact`.
"""
import typing

import factsheet.control.control_fact as CFACT
import factsheet.model.fact as MFACT

from factsheet.abc_types.abc_fact import ValueOpaque


class TestControlFact:
    """Unit tests for :class:`.ControlFact`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = None
        fact = Fact(p_topic=TOPIC)
        NAME = 'Parrot'
        fact.init_identity(p_name=NAME)
        # Test
        target = CFACT.ControlFact(fact)
        assert target._fact is fact

    def test_attach_block(self, monkeypatch):
        """Confirm fact block addition."""
        # Setup
        class PatchFact:
            def __init__(self):
                self.called_attach_block = False

            def attach_block(self, _block):
                self.called_attach_block = True

        patch_fact = PatchFact()
        monkeypatch.setattr(
            MFACT.Fact, 'attach_block', patch_fact.attach_block)

        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = None
        fact = Fact(p_topic=TOPIC)
        NAME = 'Parrot'
        fact.init_identity(p_name=NAME)
        target = CFACT.ControlFact(fact)
        # Test
        target.attach_block(None)
        assert patch_fact.called_attach_block

    def test_detach_block(self, monkeypatch):
        """Confirm fact block removal."""
        # Setup
        class PatchFact:
            def __init__(self):
                self.called_detach_block = False

            def detach_block(self, _block):
                self.called_detach_block = True

        patch_fact = PatchFact()
        monkeypatch.setattr(
            MFACT.Fact, 'detach_block', patch_fact.detach_block)

        Fact = MFACT.Fact[typing.Any, MFACT.ValueOpaque]
        TOPIC = None
        fact = Fact(p_topic=TOPIC)
        NAME = 'Parrot'
        fact.init_identity(p_name=NAME)
        target = CFACT.ControlFact(fact)
        # Test
        target.detach_block(None)
        assert patch_fact.called_detach_block


class TestTypes:
    """Unit tests for type definitions in :mod:`.Fact`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert CFACT.ValueOpaque is ValueOpaque

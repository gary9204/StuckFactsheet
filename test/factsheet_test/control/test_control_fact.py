"""
Unit tests for class that mediates fact-level interactions from
:class:`.BlockFact` to :class:`.Fact`.  See :mod:`~.control_fact`.
"""
from factsheet.control import control_fact as CFACT
from factsheet.model import fact as MFACT


class TestTopic:
    """Unit tests for :class:`.ControlFact`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = 'Parrot'
        fact = MFACT.Fact(p_name=NAME)
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

        NAME = 'Parrot'
        fact = MFACT.Fact(p_name=NAME)
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

        NAME = 'Parrot'
        fact = MFACT.Fact(p_name=NAME)
        target = CFACT.ControlFact(fact)
        # Test
        target.detach_block(None)
        assert patch_fact.called_detach_block

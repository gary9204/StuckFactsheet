"""
Unit tests for note topic class. See :mod:`~.topic_note`.
"""
# import factsheet.model.infoid as MINFOID
import factsheet.model.topic as MTOPIC
import factsheet.content.note.topic_note as XNOTE


class TestNote:
    """Unit tests for :class:`~.Note`."""

    def test_specialize(self):
        """Confirm specialization of :class:`.Note`."""
        # Setup
        # Test
        assert issubclass(XNOTE.Note, MTOPIC.Topic)
        assert not issubclass(MTOPIC.Topic, XNOTE.Note)

    # def test_init(self, patch_args_infoid):
    #     """Confirm initialization."""
    #     # Setup
    #     ARGS = patch_args_infoid
    #     NAME = ARGS.p_name
    #     SUMMARY = ARGS.p_summary
    #     TITLE = ARGS.p_title
    #     # Test
    #     target = XNOTE.Note(
    #         p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     assert not target._stale
    #     assert isinstance(target._forms, dict)
    #     assert not target._forms
    #     assert isinstance(target._infoid, MINFOID.InfoId)
    #     assert NAME == target._infoid.name
    #     assert SUMMARY == target._infoid.summary
    #     assert TITLE == target._infoid.title

    # def test_init_default(self):
    #     """Confirm initialization with default arguments."""
    #     # Setup
    #     NAME_DEFAULT = ''
    #     SUMMARY_DEFAULT = ''
    #     TITLE_DEFAULT = ''
    #     # Test
    #     target = XNOTE.Note()
    #     assert NAME_DEFAULT == target._infoid.name
    #     assert SUMMARY_DEFAULT == target._infoid.summary
    #     assert TITLE_DEFAULT == target._infoid.title

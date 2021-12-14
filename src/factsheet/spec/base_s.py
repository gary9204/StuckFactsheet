"""
Defines base classes for topic specification.
"""
import factsheet.bridge_ui as BUI


class Base(object):
    """Base spec for Factsheet topics.

    A spec provides a user the means to create a class of topics.  A
    spec embodies a template for the class.  It queries the user to
    complete the template for a specific topic.  The spec also queries
    the user of the location of the new topic in the Factsheet's
    outline of topics.
    """

    MARK_FILE_SPEC = '_s.py'
    MARK_FILE_ASSIST = '_a.ui'

    def __init__(self, *, p_name: str) -> None:
        """Initialize spec identity and topic identity including location.

        :param p_name: name of specification.
        """
        self._name_spec = BUI.ModelTextMarkup(p_text=p_name)

        self._init_name_topic()

    def _init_name_topic(self) -> None:
        """ Initialize"""
        self._name_topic = BUI.ModelTextMarkup(p_text='')
        self._new_display_name_topic = (
            BUI.FactoryDisplayTextMarkup(p_model=self._name_topic))
        self._new_editor_name_topic = (
            BUI.FactoryEditorTextMarkup(p_model=self._name_topic))

    def __call__(self):
        """ """
        # i_end_root = __file__.rfind(Base.MARK_FILE_SPEC)
        # file_assist = __file__[:i_end_root] + Base.MARK_FILE_ASSIST
        pass

    def name(self) -> str:
        pass

    def on_apply(self, p_assistant) -> None:
        pass

    def on_cancel(self, p_assistant) -> None:
        pass

    def on_prepare(self, p_assistant) -> None:
        pass

    def reset(self) -> None:
        """Reset topic identity and location to initial values."""
        raise NotImplementedError
        self._name_topic._set_persist('')

    def summary(self) -> str:
        pass

    def title(self) -> str:
        pass

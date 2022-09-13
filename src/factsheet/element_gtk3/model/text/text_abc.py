"""
Define abstract base class for facade classes of text storage elements.
"""
import typing

import factsheet.element_gtk3.model.model_abc as EMABC


class TextAbc(EMABC.ModelGtk3[EMABC.UiModelOpaque, str],
              typing.Generic[EMABC.UiModelOpaque]):
    """Common ancestor of facade classes for text storage elements.

    Class extends
    :class:`.element_gtk3.model.model_abc.ModelGtk3` with property to
    set and get text stored in memory.

    .. admonition:: Plan

        The current plan is to move consistency checks to control
        classes.  The goal is to eliminate transient data associated
        with model components.

        The wisdom of the move is uncertain.  Hence, consistency
        methods, tests, and documentation are commented out pending the
        move.::

            Class adds interface
            :class:`.element_gtk3.model.model_abc.Consistency` to track
            in-memory text against text in file.

            .. admonition:: About Equality

                Consistency between in-memory text and text in file is a
                transient state.  Consistency is not saved to file and
                is not considered when testing for equality.  Class
                extends methods :meth:`ModelGtk3.__getstate___` and
                :meth:`.ModelGtk3.__setstate__` to set consistency when
                class is written to or read from file.
    """

    # def __getstate__(self) -> typing.Dict:
    #     """Return text storage element in form pickle can persist.
    #
    #     Extends method to remove consistency state.
    #     """
    #     state = super().__getstate__()
    #     # del state['_stale']
    #     return state

    def __init__(self, p_text: str = '') -> None:
        """Extend initialization with text and consistency state.

        :param p_text: initial text content.
        """
        super().__init__()
        self.set_internal(p_text)
        # self._stale = False

    # def __setstate__(self, p_state: typing.MutableMapping) -> None:
    #     """Extend text bridge reconstruction with change state.
    #
    #     Reconstructed text bridge is marked consistent with file.
    #
    #     :param p_state: unpickled content.
    #     """
    #     super().__setstate__(p_state)
    #     # self._stale = False

    # def alike(self) -> bool:
    #     """Return True when there are no unsaved changes to stored text."""
    #     pass
    #     # return not self.is_stale()

    # def differ(self) -> bool:
    #     """Return True when there is at least one unsaved change to
    #     stored text.
    #     """
    #     pass
    #     # return self._stale

    # def set_alike(self) -> None:
    #     """Mark text stored in memory consistent with text in file."""
    #     raise NotImplementedError
    #     # self._stale = False

    # def set_differ(self) -> None:
    #     """Mark text stored in memory different from text in file."""
    #     raise NotImplementedError
    #     # self._stale = True

    @property
    def text(self) -> str:
        """Return model text."""
        return self.to_external()

    @text.setter
    def text(self, p_text: str) -> None:
        """Set model text."""
        self.set_internal(p_text)

"""
Test fixtures for :mod:`~.factsheet_test.model` unit tests.
"""
# import dataclasses as DC
import pytest   # type: ignore[import]

# from factsheet.abc_types import abc_outline as ABC_OUTLINE
# from factsheet.abc_types import abc_sheet as ABC_SHEET
# from factsheet.abc_types import abc_topic as ABC_TOPIC
# from factsheet.view import types_view as VTYPES


# @pytest.fixture
# def interface_form_topic(interface_view_infoid):
#     """Pytest fixture returns stub class for
#     :class:`.InterfaceFormTopic`.
#     """
#     class PatchFormTopic(ABC_TOPIC.InterfaceFormTopic):
#         def __init__(self):
#             self._infoid = interface_view_infoid()
#             self._facts = VTYPES.ViewOutlineFacts()
# 
#         def get_infoid(self): return self._infoid
# 
#         def get_view_facts(self): return self._facts
# 
#     return PatchFormTopic


# @pytest.fixture
# def patch_class_view_topics():
#     """Pytest fixture returns stub class implementing
#     :class:`.InterfaceFormTopic`.
#     """
#     class PatchViewTopics(ABC_OUTLINE.AbstractViewOutline):
#         def __init__(self):
#             self.called_get_selected = False
#             self.called_select = False
#             self.called_set_model = False
#             self.called_unselect_all = False
# 
#         def get_selected(self): self.called_get_selected = True
# 
#         def select(self): self.called_select = True
# 
#         def unselect_all(self): self.called_unselect_all = True
# 
#     return PatchViewTopics


# @pytest.fixture
# def interface_page_sheet(interface_view_infoid):
#     """Pytest fixture returns stub class implementing
#     :class:`.InterfacePageSheet`.
#     """
#     class PatchPageSheet(ABC_SHEET.InterfacePageSheet):
#         def __init__(self):
#             self._infoid = interface_view_infoid()
#             self._topics = VTYPES.ViewOutlineTopics()
#             self.called_close_page = False
#             self.called_close_topic = 0
#             self.closed_topics = []
#             self.called_present = False
#             self.called_set_titles = False
#             self.subtitle = None
# 
#         def close_page(self): self.called_close_page = True
# 
#         def close_topic(self, id_topic):
#             self.called_close_topic += 1
#             self.closed_topics.append(id_topic)
# 
#         def get_infoid(self): return self._infoid
# 
#         def get_view_topics(self): return self._topics
# 
#         def present(self, _time): self.called_present = True
# 
#         def set_titles(self, p_subtitle):
#             self.called_set_titles = True
#             self.subtitle = p_subtitle
# 
#     return PatchPageSheet

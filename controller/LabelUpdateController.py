from PyQt5.QtCore import QObject, pyqtSlot

from utils import ApplicationContext
from view import Renderer


class LabelUpdateController(QObject):
    def __init__(self, main_page):
        super(LabelUpdateController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot(str, str)
    def change_label(self, tuple_pair_id, new_label):
        ApplicationContext.COMPLETE_DATA_FRAME.loc[ApplicationContext.COMPLETE_DATA_FRAME['_id'] == int(tuple_pair_id), 'label'] = new_label
        self.main_page.setHtml(
            Renderer.render_main_page(
                current_page_tuple_pairs=
                ApplicationContext.TUPLE_PAIR_DISPLAY_CONTROLLER.get_tuples_for_page(ApplicationContext.current_page_number),
                match_count=
                ApplicationContext.current_data_frame[ApplicationContext.current_data_frame.label == ApplicationContext.MATCH].shape[0],
                not_match_count=
                ApplicationContext.current_data_frame[ApplicationContext.current_data_frame.label == ApplicationContext.NON_MATCH].shape[0],
                not_sure_count=
                ApplicationContext.current_data_frame[ApplicationContext.current_data_frame.label == ApplicationContext.NOT_SURE].shape[0],
                unlabeled_count=
                ApplicationContext.current_data_frame[ApplicationContext.current_data_frame.label == ApplicationContext.NOT_LABELED].shape[0],
            )
        )

    @pyqtSlot(str, result=str)
    def show_tuple_pair(self, tuple_pair_id):
        string = Renderer.render_tuple_pair(
            ApplicationContext.COMPLETE_DATA_FRAME.loc[ApplicationContext.COMPLETE_DATA_FRAME['_id'] == int(tuple_pair_id)])
        return string

    @pyqtSlot(str, str)
    def edit_tags(self, tuple_pair_id, tags):
        ApplicationContext.COMPLETE_DATA_FRAME.loc[
            ApplicationContext.COMPLETE_DATA_FRAME['_id'] == int(tuple_pair_id), ApplicationContext.TAGS_COLUMN] = tags

    @pyqtSlot(str, str)
    def edit_comments(self, tuple_pair_id, comments):
        ApplicationContext.COMPLETE_DATA_FRAME.loc[
            ApplicationContext.COMPLETE_DATA_FRAME['_id'] == int(tuple_pair_id), ApplicationContext.COMMENTS_COLUMN] = comments

from PyQt5.QtCore import QObject, pyqtSlot

from utils import ApplicationContext
from view import Renderer


class LabelUpdateController(QObject):
    def __init__(self, main_page):
        super(LabelUpdateController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot(str, str)
    def change_label(self, tuple_pair_id, new_label):
        ApplicationContext.complete_data.loc[ApplicationContext.complete_data['_id'] == int(tuple_pair_id), 'label'] = new_label

    @pyqtSlot(str, result=str)
    def show_tuple_pair(self, tuple_pair_id):
        string = Renderer.render_tuple_pair(ApplicationContext.complete_data.loc[ApplicationContext.complete_data['_id'] == int(tuple_pair_id)])
        print(string)
        return string

    @pyqtSlot(str, str)
    def edit_tags(self, tuple_pair_id, tags):
        ApplicationContext.complete_data.loc[ApplicationContext.complete_data['_id'] == int(tuple_pair_id), ApplicationContext.TAGS_COLUMN] = tags

    @pyqtSlot(str, str)
    def edit_comments(self, tuple_pair_id, comments):
        ApplicationContext.complete_data.loc[
            ApplicationContext.complete_data['_id'] == int(tuple_pair_id), ApplicationContext.COMMENTS_COLUMN] = comments

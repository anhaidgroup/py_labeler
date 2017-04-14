from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication

from utils import Constants
from view import Renderer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect


# todo 3/31/17 move this to a separate file

class PopUpPage(QWebEnginePage):
    def __init__(self):
        super(PopUpPage, self).__init__(None)


class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)


class LabelUpdateController(QObject):
    def __init__(self, main_page):
        super(LabelUpdateController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot(str, str)
    def change_label(self, tuple_pair_id, new_label):
        Constants.complete_data.loc[Constants.complete_data['_id'] == int(tuple_pair_id), 'label'] = new_label
        # self.data_frame['label'][tuple_id] = new_label
        # print('hello')

    @pyqtSlot(str, result=str)
    def show_tuple_pair(self, tuple_pair_id):
        # self.w = MyPopup()
        # self.w.setGeometry(QRect(100, 100, 400, 200))
        # self.w.show();
        string = Renderer.render_tuple_pair(Constants.complete_data.loc[Constants.complete_data['_id'] == int(tuple_pair_id)])
        print(string)
        return string

    @pyqtSlot(str, str)
    def edit_tags(self, tuple_pair_id, tags):
        Constants.complete_data.loc[Constants.complete_data['_id'] == int(tuple_pair_id), Constants.TAGS_COLUMN] = tags

    @pyqtSlot(str, str)
    def edit_comments(self, tuple_pair_id, comments):
        Constants.complete_data.loc[Constants.complete_data['_id'] == int(tuple_pair_id), Constants.COMMENTS_COLUMN] = comments

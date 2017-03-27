from PyQt5.QtCore import QObject, pyqtSlot


class LabelUpdateController(QObject):
    data_frame = None

    def __init__(self, main_page, data_frame):
        super(LabelUpdateController, self).__init__(None)
        self.main_page = main_page
        self.data_frame = data_frame

    @pyqtSlot(str, str)
    def change_label(self, tuple_id, new_label):
        self.data_frame.loc[self.data_frame['_id'] == int(tuple_id), 'label'] = new_label
        # self.data_frame['label'][tuple_id] = new_label
        # print('hello')

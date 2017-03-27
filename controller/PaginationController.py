from PyQt5.QtCore import QObject, pyqtSlot
from math import ceil

from utils.Constants import MATCH, NON_MATCH, NOT_SURE
from view import Renderer

# todo 3/26/17
COUNT_PER_PAGE = 10
CURRENT_PAGE = 1


class PaginationController(QObject):
    data_frame = None

    def __init__(self, main_page):
        super(PaginationController, self).__init__(None)
        self.main_page = main_page

    def set_data(self, data_frame):
        self.data_frame = data_frame

    @pyqtSlot()
    def set_per_page_count(self, count_per_page):
        """ Set the number of tuple pairs to be shown per page

        :param count_per_page: value to set
        :return:
        """
        assert count_per_page > 0, "count of tuple pairs per page can not be negative"
        # todo 3/26/17 this does not work
        COUNT_PER_PAGE = count_per_page

    @pyqtSlot()
    def set_current_page(self, current_page):
        assert current_page > 0
        # todo 3/26/17 this does not work
        CURRENT_PAGE = current_page

    @pyqtSlot(int)
    def get_page(self, page_number):
        assert page_number >= 0
        return self.data_frame.iloc[page_number * COUNT_PER_PAGE: page_number * COUNT_PER_PAGE + COUNT_PER_PAGE]

    @pyqtSlot(str)
    def respond(self, text):
        print(" in the pagination controller")

    @pyqtSlot()
    def get_current_page(self):
        return CURRENT_PAGE

    @pyqtSlot()
    def get_per_page_count(self):
        return COUNT_PER_PAGE

    @pyqtSlot()
    def get_number_of_pages(self, data_frame):
        return ceil(data_frame.shape[0] / COUNT_PER_PAGE)

    @pyqtSlot(int)
    def get_page_html(self, page_number):
        self.main_page.setHtml(
            Renderer.render_main_page(self.get_page(page_number), page_number, COUNT_PER_PAGE,
                                      ceil(self.data_frame.shape[0] / COUNT_PER_PAGE),
                                      self.data_frame[self.data_frame.label == MATCH].shape[0],
                                      self.data_frame[self.data_frame.label == NON_MATCH].shape[0],
                                      self.data_frame[self.data_frame.label == NOT_SURE].shape[0],
                                      self.data_frame.shape[0]))

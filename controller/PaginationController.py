from PyQt5.QtCore import QObject, pyqtSlot
from math import ceil

from utils import Constants
from view import Renderer


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
        assert current_page >= 0
        # todo 3/26/17 this does not work
        Constants.CURRENT_PAGE = current_page

    @pyqtSlot(int)
    def get_page(self, page_number):
        assert page_number >= 0
        return self.data_frame.iloc[page_number * Constants.COUNT_PER_PAGE: page_number * Constants.COUNT_PER_PAGE + Constants.COUNT_PER_PAGE]

    @pyqtSlot(str)
    def respond(self, text):
        print(" in the pagination controller")

    @pyqtSlot()
    def get_current_page(self):
        return Constants.CURRENT_PAGE

    @pyqtSlot()
    def get_per_page_count(self):
        return Constants.COUNT_PER_PAGE

    @pyqtSlot()
    def get_number_of_pages(self, data_frame):
        return ceil(data_frame.shape[0] / Constants.COUNT_PER_PAGE)

    @pyqtSlot(int)
    def get_page_html(self, page_number):
        self.main_page.setHtml(
            Renderer.render_main_page(self.get_page(page_number), ["ID", "birth_year", "name"], page_number,
                                      Constants.COUNT_PER_PAGE, ceil(self.data_frame.shape[0] / Constants.COUNT_PER_PAGE),
                                      total_count=self.data_frame.shape[0],
                                      match_count=self.data_frame[self.data_frame.label == Constants.MATCH].shape[0],
                                      not_match_count=self.data_frame[self.data_frame.label == Constants.NON_MATCH].shape[0],
                                      not_sure_count=self.data_frame[self.data_frame.label == Constants.NOT_SURE].shape[0],
                                      unlabeled_count=self.data_frame[self.data_frame.label == Constants.NOT_LABELED].shape[0],
                                      tokens_per_attribute=20)
        )

        # todo 4/7/17 clean this

    @pyqtSlot(str)
    def change_layout(self, layout):
        Constants.CURRENT_TEMPLATE = layout
        if layout == 'single':
            Constants.COUNT_PER_PAGE = 1
        else:
            Constants.COUNT_PER_PAGE = Constants.HORIZONTAL_COUNT_PER_PAGE
        self.get_page_html(0)

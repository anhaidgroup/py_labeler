from PyQt5.QtCore import QObject, pyqtSlot
from math import ceil

from utils import ApplicationContext
from view import Renderer


class PaginationController(QObject):
    def __init__(self, main_page):
        super(PaginationController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot()
    def set_per_page_count(self, count_per_page):
        """ Set the number of tuple pairs to be shown per page

        :param count_per_page: value to set
        :return:
        """
        assert count_per_page > 0, "count of tuple pairs per page can not be negative"
        # todo 3/26/17 this does not work
        ApplicationContext.COUNT_PER_PAGE = count_per_page

    @pyqtSlot()
    def set_current_page(self, current_page):
        assert current_page >= 0
        # todo 3/26/17 this does not work
        ApplicationContext.CURRENT_PAGE = current_page

    @pyqtSlot(int)
    def get_page(self, page_number):
        assert page_number >= 0
        return ApplicationContext.current_data.iloc[page_number * ApplicationContext.COUNT_PER_PAGE: page_number * ApplicationContext.COUNT_PER_PAGE + ApplicationContext.COUNT_PER_PAGE]

    @pyqtSlot(str)
    def respond(self, text):
        print(" in the pagination controller")

    @pyqtSlot()
    def get_current_page(self):
        return ApplicationContext.CURRENT_PAGE

    @pyqtSlot()
    def get_per_page_count(self):
        return ApplicationContext.COUNT_PER_PAGE

    @pyqtSlot()
    def get_number_of_pages(self, data_frame):
        return ceil(data_frame.shape[0] / ApplicationContext.COUNT_PER_PAGE)

    @pyqtSlot(int)
    def get_page_html(self, page_number):
        self.main_page.setHtml(
            Renderer.render_main_page(tuple_pairs=self.get_page(page_number), attributes=ApplicationContext.attributes, current_page=page_number,
                                      count_per_page=ApplicationContext.COUNT_PER_PAGE,
                                      number_of_pages=ceil(ApplicationContext.current_data.shape[0] / ApplicationContext.COUNT_PER_PAGE),
                                      total_count=ApplicationContext.current_data.shape[0],
                                      match_count=ApplicationContext.current_data[ApplicationContext.current_data.label == ApplicationContext.MATCH].shape[0],
                                      not_match_count=ApplicationContext.current_data[ApplicationContext.current_data.label == ApplicationContext.NON_MATCH].shape[0],
                                      not_sure_count=ApplicationContext.current_data[ApplicationContext.current_data.label == ApplicationContext.NOT_SURE].shape[0],
                                      unlabeled_count=ApplicationContext.current_data[ApplicationContext.current_data.label == ApplicationContext.NOT_LABELED].shape[0],
                                      tokens_per_attribute=ApplicationContext.TOKENS_PER_ATTRIBUTE)
        )

        # todo 4/7/17 clean this

    @pyqtSlot(str)
    def change_layout(self, layout):
        ApplicationContext.CURRENT_TEMPLATE = layout
        if layout == 'single':
            ApplicationContext.COUNT_PER_PAGE = 1
        else:
            ApplicationContext.COUNT_PER_PAGE = ApplicationContext.HORIZONTAL_COUNT_PER_PAGE
        self.get_page_html(0)

    @pyqtSlot(str)
    def save_data(self, save_file_name):
        # todo 4/26/17 handle no such directory errors
        ApplicationContext.complete_data.to_csv(ApplicationContext.SAVEPATH + save_file_name)
        ApplicationContext.SAVE_FILE_NAME = save_file_name

    @pyqtSlot(int)
    def change_token_count(self, token_count):
        # todo 4/26/17 minimum 3 for jinja
        ApplicationContext.TOKENS_PER_ATTRIBUTE = token_count
        self.get_page_html(ApplicationContext.CURRENT_PAGE)

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
        ApplicationContext.tuple_pair_count_per_page = count_per_page

    @pyqtSlot()
    def set_current_page(self, current_page):
        assert current_page >= 0
        # todo 3/26/17 this does not work
        ApplicationContext.current_page_number = current_page

    @pyqtSlot(int)
    def get_page(self, page_number):
        assert page_number >= 0
        return ApplicationContext.current_data_frame.iloc[
               page_number * ApplicationContext.tuple_pair_count_per_page: page_number * ApplicationContext.tuple_pair_count_per_page + ApplicationContext.tuple_pair_count_per_page]

    @pyqtSlot()
    def get_current_page(self):
        return ApplicationContext.current_page_number

    @pyqtSlot()
    def get_per_page_count(self):
        return ApplicationContext.tuple_pair_count_per_page

    @pyqtSlot()
    def get_number_of_pages(self, data_frame):
        return ceil(data_frame.shape[0] / ApplicationContext.tuple_pair_count_per_page)

    @pyqtSlot(int)
    def get_page_html(self, page_number):
        self.main_page.setHtml(
            Renderer.render_main_page(
                current_page_tuple_pairs=
                self.get_page(page_number),
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

        # todo 4/7/17 clean this

    @pyqtSlot(str)
    def change_layout(self, layout):
        ApplicationContext.current_layout = layout
        if layout == 'single':
            ApplicationContext.tuple_pair_count_per_page = 1
        else:
            ApplicationContext.tuple_pair_count_per_page = ApplicationContext.DEFAULT_TUPLE_PAIR_COUNT_PER_PAGE
        self.get_page_html(0)

    @pyqtSlot(str)
    def save_data(self, save_file_name):
        # todo 4/26/17 handle no such directory errors
        ApplicationContext.COMPLETE_DATA_FRAME.to_csv(ApplicationContext.SAVEPATH + save_file_name)
        ApplicationContext.save_file_name = save_file_name

    @pyqtSlot(int)
    def change_token_count(self, token_count):
        # todo 4/26/17 minimum 3 for jinja
        ApplicationContext.alphabets_per_attribute_display = token_count
        self.get_page_html(ApplicationContext.current_page_number)

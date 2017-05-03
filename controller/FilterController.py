from math import ceil

from PyQt5.QtCore import QObject, pyqtSlot, QJsonValue

from utils import ApplicationContext
from view import Renderer


class FilterController(QObject):
    def __init__(self, main_page):
        super(FilterController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot(str)
    def get_matching_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently "MATCH"

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.MATCH]

    @pyqtSlot()
    def get_non_matched_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check if assertion is correct thing to do
        return ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NON_MATCH]

    @pyqtSlot()
    def get_non_sure_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NOT_SURE]

    @pyqtSlot()
    def get_not_labeled_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NOT_LABELED]

    @pyqtSlot(str)
    def get_filtered_tuple_pairs(self, label):
        data = None
        if label == ApplicationContext.MATCH:
            data = self.get_matching_tuple_pairs()
        elif label == ApplicationContext.NON_MATCH:
            data = self.get_non_matched_tuple_pairs()
        elif label == ApplicationContext.NOT_SURE:
            data = self.get_non_sure_tuple_pairs()
        elif label == ApplicationContext.NOT_LABELED:
            data = self.get_not_labeled_tuple_pairs()
        elif label == ApplicationContext.ALL:
            data = ApplicationContext.complete_data

        ApplicationContext.current_data = data
        data = data.iloc[0 * ApplicationContext.COUNT_PER_PAGE: 0 * ApplicationContext.COUNT_PER_PAGE + ApplicationContext.COUNT_PER_PAGE]
        # todo 4/7/17 get attributes from data
        self.main_page.setHtml(
            Renderer.render_main_page(tuple_pairs=data, attributes=ApplicationContext.attributes, current_page=0,
                                      count_per_page=ApplicationContext.COUNT_PER_PAGE,
                                      number_of_pages=ceil(ApplicationContext.current_data.shape[0] / ApplicationContext.COUNT_PER_PAGE),
                                      total_count=ApplicationContext.complete_data.shape[0],
                                      match_count=ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.MATCH].shape[0],
                                      not_match_count=ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NON_MATCH].shape[0],
                                      not_sure_count=ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NOT_SURE].shape[0],
                                      unlabeled_count=ApplicationContext.complete_data[ApplicationContext.complete_data.label == ApplicationContext.NOT_LABELED].shape[0],
                                      tokens_per_attribute=ApplicationContext.TOKENS_PER_ATTRIBUTE)
        )

    @pyqtSlot(str)
    def filter_attribute(self, attributes):
        attributes = attributes.split(",")
        if "_show_all" in attributes:
            ApplicationContext.attributes = ApplicationContext.ALL_ATTRIBUTES
        else:
            attributes.remove("")
            ApplicationContext.attributes = attributes

        from Main import pagination_contoller
        # todo 5/3/17 this is causing a new window to open?
        from Main import stats_controller
        html = Renderer.render_main_page(tuple_pairs=pagination_contoller.get_page(0),
                                         attributes=ApplicationContext.attributes, current_page=0,
                                         count_per_page=ApplicationContext.COUNT_PER_PAGE,
                                         number_of_pages=ceil(ApplicationContext.current_data.shape[0] / ApplicationContext.COUNT_PER_PAGE),
                                         total_count=stats_controller.count_tuple_pairs(ApplicationContext.current_data),
                                         match_count=stats_controller.count_matched_tuple_pairs(ApplicationContext.current_data),
                                         not_match_count=stats_controller.count_non_matched_tuple_pairs(ApplicationContext.current_data),
                                         not_sure_count=stats_controller.count_not_sure_tuple_pairs(ApplicationContext.current_data),
                                         unlabeled_count=stats_controller.count_not_labeled_tuple_pairs(ApplicationContext.current_data),
                                         tokens_per_attribute=ApplicationContext.TOKENS_PER_ATTRIBUTE
                                         )
        self.main_page.setHtml(html)
        print(attributes)

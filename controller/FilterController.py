from PyQt5.QtCore import QObject, pyqtSlot

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
        return ApplicationContext.COMPLETE_DATA_FRAME[ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.MATCH]

    @pyqtSlot()
    def get_non_matched_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check if assertion is correct thing to do
        return ApplicationContext.COMPLETE_DATA_FRAME[ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NON_MATCH]

    @pyqtSlot()
    def get_non_sure_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return ApplicationContext.COMPLETE_DATA_FRAME[ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NOT_SURE]

    @pyqtSlot()
    def get_not_labeled_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return ApplicationContext.COMPLETE_DATA_FRAME[ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NOT_LABELED]

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
            data = ApplicationContext.COMPLETE_DATA_FRAME

        ApplicationContext.current_data_frame = data
        data = data.iloc[
               0 * ApplicationContext.tuple_pair_count_per_page: 0 * ApplicationContext.tuple_pair_count_per_page + ApplicationContext.tuple_pair_count_per_page]
        self.main_page.setHtml(
            Renderer.render_main_page(current_page_tuple_pairs=data,
                                      match_count=ApplicationContext.COMPLETE_DATA_FRAME[
                                          ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.MATCH].shape[0],
                                      not_match_count=ApplicationContext.COMPLETE_DATA_FRAME[
                                          ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NON_MATCH].shape[0],
                                      not_sure_count=ApplicationContext.COMPLETE_DATA_FRAME[
                                          ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NOT_SURE].shape[0],
                                      unlabeled_count=ApplicationContext.COMPLETE_DATA_FRAME[
                                          ApplicationContext.COMPLETE_DATA_FRAME.label == ApplicationContext.NOT_LABELED].shape[0]
                                      )
        )

    @pyqtSlot(str)
    def filter_attribute(self, attributes):
        attributes = attributes.split(",")
        if "_show_all" in attributes:
            ApplicationContext.current_attributes = ApplicationContext.ALL_ATTRIBUTES
        else:
            attributes.remove("")
            ApplicationContext.current_attributes = attributes
        html = Renderer.render_main_page(current_page_tuple_pairs=ApplicationContext.PAGINATION_CONTROLLER.get_tuples_for_page(0),
                                         match_count=ApplicationContext.STATS_CONTROLLER.count_matched_tuple_pairs(
                                             ApplicationContext.current_data_frame),
                                         not_match_count=ApplicationContext.STATS_CONTROLLER.count_non_matched_tuple_pairs(
                                             ApplicationContext.current_data_frame),
                                         not_sure_count=ApplicationContext.STATS_CONTROLLER.count_not_sure_tuple_pairs(
                                             ApplicationContext.current_data_frame),
                                         unlabeled_count=ApplicationContext.STATS_CONTROLLER.count_not_labeled_tuple_pairs(
                                             ApplicationContext.current_data_frame)
                                         )
        self.main_page.setHtml(html)

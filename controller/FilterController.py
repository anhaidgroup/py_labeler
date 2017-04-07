from math import ceil

from PyQt5.QtCore import QObject, pyqtSlot

from utils import Constants
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
        return Constants.complete_data[Constants.complete_data.label == Constants.MATCH]

    @pyqtSlot()
    def get_non_matched_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check if assertion is correct thing to do
        return Constants.complete_data[Constants.complete_data.label == Constants.NON_MATCH]

    @pyqtSlot()
    def get_non_sure_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return Constants.complete_data[Constants.complete_data.label == Constants.NOT_SURE]

    @pyqtSlot()
    def get_not_labeled_tuple_pairs(self):
        """Gets tuple pairs whose label value is currently NON-MATCH

        :param
            dataFrame: Data Frame consisting of matched and non-matched tuple pairs
        :return:
            Data frame with tuple pairs whose label value is currently NON-MATCH
        """
        # todo check data type of label column
        return Constants.complete_data[Constants.complete_data.label == Constants.NOT_LABELED]

    @pyqtSlot(str)
    def get_filtered_tuple_pairs(self, label):
        data = None
        if label == Constants.MATCH:
            data = self.get_matching_tuple_pairs()
        elif label == Constants.NON_MATCH:
            data = self.get_non_matched_tuple_pairs()
        elif label == Constants.NOT_SURE:
            data = self.get_non_sure_tuple_pairs()
        elif label == Constants.NOT_LABELED:
            data = self.get_not_labeled_tuple_pairs()
        elif label == Constants.ALL:
            data = Constants.complete_data

        Constants.current_data = data
        data = data.iloc[0 * Constants.COUNT_PER_PAGE: 0 * Constants.COUNT_PER_PAGE + Constants.COUNT_PER_PAGE]
        # todo 4/7/17 get attributes from data
        self.main_page.setHtml(
            Renderer.render_main_page(tuple_pairs=data, attributes=["ID", "birth_year", "name"], current_page=0,
                                      count_per_page=Constants.COUNT_PER_PAGE,
                                      number_of_pages=ceil(Constants.current_data.shape[0] / Constants.COUNT_PER_PAGE),
                                      total_count=Constants.complete_data.shape[0],
                                      match_count=Constants.complete_data[Constants.complete_data.label == Constants.MATCH].shape[0],
                                      not_match_count=Constants.complete_data[Constants.complete_data.label == Constants.NON_MATCH].shape[0],
                                      not_sure_count=Constants.complete_data[Constants.complete_data.label == Constants.NOT_SURE].shape[0],
                                      unlabeled_count=Constants.complete_data[Constants.complete_data.label == Constants.NOT_LABELED].shape[0],
                                      tokens_per_attribute=20)
        )

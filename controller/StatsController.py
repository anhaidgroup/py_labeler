from PyQt5.QtCore import QObject, pyqtSlot

from utils import Constants


# todo should we pass around data frame or set in a context and use the same
class StatsController(QObject):
    def __init__(self, main_page):
        super(StatsController, self).__init__(None)
        self.main_page = main_page

    @pyqtSlot()
    def count_matched_tuple_pairs(self, data_frame):
        """ Returns a count of tuple pairs whose label value is MATCH

        :param data_frame:
        :return:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        # todo check data type of label column
        return data_frame[data_frame.label == Constants.MATCH].shape[0]

    @pyqtSlot()
    def count_non_matched_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NON-MATCH

        :param data_frame:
        :return:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        # todo check data type of label column
        return data_frame[data_frame.label == Constants.NON_MATCH].shape[0]

    @pyqtSlot()
    def count_not_labeled_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NOT_LABELED

        :param data_frame:
        :return:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        # todo check data type of label column
        return data_frame[data_frame.label == Constants.NOT_LABELED].shape[0]

    @pyqtSlot()
    def count_not_sure_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NOT_SURE

        :param data_frame:
        :return:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        # todo check data type of label column
        return data_frame[data_frame.label == Constants.NOT_SURE].shape[0]

    @pyqtSlot()
    def count_tuple_pairs(self, data_frame):
        return data_frame.shape[0]

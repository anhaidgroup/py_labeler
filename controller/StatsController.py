from PyQt5.QtCore import QObject

from utils import ApplicationContext


class StatsController(QObject):
    """
    Computes statistics to be displayed
    """

    def __init__(self, main_page):
        super(StatsController, self).__init__(None)
        self.main_page = main_page

    def count_matched_tuple_pairs(self, data_frame):
        """ Returns a count of tuple pairs whose label value is MATCH.

        Args: 
            data_frame (DataFrame): Pandas data frame with label column.
        
        Returns:
            Count of tuple pairs with label == MATCH (int).

        Raises:
                        
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        return data_frame[data_frame.label == ApplicationContext.MATCH].shape[0]

    def count_non_matched_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NON-MATCH

        Args: 
            data_frame (DataFrame): Pandas data frame with label column.
        
        Returns:
            Count of tuple pairs with label == NON MATCH (int).

        Raises:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        return data_frame[data_frame.label == ApplicationContext.NON_MATCH].shape[0]

    def count_not_labeled_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NOT_LABELED

        Args: 
            data_frame (DataFrame): Pandas data frame with label column.
        
        Returns:
            Count of tuple pairs with label == NOT LABELED (int).

        Raises:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        return data_frame[data_frame.label == ApplicationContext.NOT_LABELED].shape[0]

    def count_not_sure_tuple_pairs(self, data_frame):
        """Returns a count of tuple pairs whose label value is NOT_SURE

        Args: 
            data_frame (DataFrame): Pandas data frame with label column.
        
        Returns:
            Count of tuple pairs with label == NOT SURE (int).

        Raises:
        """
        # todo check if assertion is correct thing to do
        assert ('label' in data_frame.columns)
        return data_frame[data_frame.label == ApplicationContext.NOT_SURE].shape[0]

from utils.Constants import MATCH, NON_MATCH


def get_matching_tuple_pairs(data_frame):
    """Gets tuple pairs whose label value is currently "MATCH"

    :param
        dataFrame: Data Frame consisting of matched and non-matched tuple pairs
    :return:
        Data frame with tuple pairs whose label value is currently NON-MATCH
    """
    # todo check if assertion is correct thing to do
    assert ('label' in data_frame.columns)
    # todo check data type of label column
    return data_frame[data_frame.label == MATCH]


def get_non_matched_tuple_pairs(data_frame):
    """Gets tuple pairs whose label value is currently NON-MATCH

    :param
        dataFrame: Data Frame consisting of matched and non-matched tuple pairs
    :return:
        Data frame with tuple pairs whose label value is currently NON-MATCH
    """
    # todo check if assertion is correct thing to do
    assert ('label' in data_frame.columns)
    # todo check data type of label column
    return data_frame[data_frame.label == NON_MATCH]

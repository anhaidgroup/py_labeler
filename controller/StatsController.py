from utils.Constants import MATCH, NON_MATCH


# todo should we pass around data frame or set in a context and use the same

def count_matched_tuple_pairs(data_frame):
    """ Returns a count of tuple pairs whose label value is MATCH

    :param data_frame:
    :return:
    """
    # todo check if assertion is correct thing to do
    assert ('label' in data_frame.columns)
    # todo check data type of label column
    return data_frame[data_frame.label == MATCH].shape[0]


def count_non_matched_tuple_pairs(data_frame):
    """Returns a count of tuple pairs whose label value is NON-MATCH

    :param data_frame:
    :return:
    """
    # todo check if assertion is correct thing to do
    assert ('label' in data_frame.columns)
    # todo check data type of label column
    return data_frame[data_frame.label == NON_MATCH].shape[0]

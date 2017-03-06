def getMatchingTuplePairs(dataFrame):
    """Gets tuple pairs whose label value is currently "MATCH"

    :param
        dataFrame: Data Frame consisting of matched and non-matched tuple pairs
    :return:
        Data frame with tuple pairs whose label value is currently NON-MATCH
    """
    # todo check if assertion is correct thing to do
    assert ('label' in dataFrame.columns)
    # todo check data type of label column
    return (dataFrame[dataFrame.label == '1'])


def getNonMatchedTuplePairs(dataFrame):
    """Gets tuple pairs whose label value is currently NON-MATCH

    :param
        dataFrame: Data Frame consisting of matched and non-matched tuple pairs
    :return:
        Data frame with tuple pairs whose label value is currently NON-MATCH
    """
    # todo check if assertion is correct thing to do
    assert ('label' in dataFrame.columns)
    # todo check data type of label column
    return (dataFrame[dataFrame.label == '0'])

def countMatchedTuplePairs(dataFrame):
    # todo check if assertion is correct thing to do
    assert ('label' in dataFrame.columns)
    # todo check data type of label column
    return (dataFrame[dataFrame.label == '1'].shape[0])


def countNonMatchedTuplePairs(dataFrame):
    # todo check if assertion is correct thing to do
    assert ('label' in dataFrame.columns)
    # todo check data type of label column
    return (dataFrame[dataFrame.label == '0'].shape[0])

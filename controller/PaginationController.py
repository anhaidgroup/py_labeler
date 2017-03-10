from utils.Constants import COUNT_PER_PAGE


def set_per_page_count(count_per_page):
    """ Set the number of tuple pairs to be shown per page

    :param count_per_page: value to set
    :return:
    """
    assert count_per_page > 0, "count of tuple pairs per page can not be negative"
    COUNT_PER_PAGE = count_per_page


def get_page(data_frame, page_number):

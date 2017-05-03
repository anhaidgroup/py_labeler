from jinja2 import Environment, PackageLoader, select_autoescape

# load all templates from 'view' package and 'templates' folder
from utils import ApplicationContext

env = Environment(
    loader=PackageLoader('view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def renderSampleTemplate(title, users, data):
    # get a template from the folder
    template = env.get_template('sample.html')
    return template.render(title="templated page", users=["me", "them", "who"], data=data)


def render_options_page(tags_col, comments_col):
    options_page = env.get_template('options.html')
    return options_page.render(tags_col=tags_col, comments_col=comments_col)


# def render_main_page(tuple_pairs, currentPage, countPerPage, numberOfPages, matched_count, un_matched_count,
#                      not_sure_count, total_count, display_title="Tuple Pairs"):
#     main_window = env.get_template('main_window.html')
#     return main_window.render(data=tuple_pairs.to_dict(orient='records'), currentPage=currentPage,
#                               countPerPage=countPerPage, numberOfPages=numberOfPages,
#                               matched_count=matched_count,
#                               not_sure_count=not_sure_count,
#                               unmatched_count=un_matched_count, total_count=total_count, display_title=display_title)


def render_dummy_page():
    main_window = env.get_template('dummy_page.html');
    return main_window.render()


def render_tuple_pair(tuple_pair):
    tuple_pair_template = env.get_template('tuple_pair.html');
    # todo 3/31/17 change
    return tuple_pair_template.render(row=tuple_pair.to_dict(orient='records'), headers=['ID', 'birth_year', 'name']);


def compute_page_numbers(current_page):
    if current_page - ApplicationContext.PAGE_DISPLAY_COUNT / 2 < 0:
        start_page = 0
        end_page = ApplicationContext.PAGE_DISPLAY_COUNT
    else:
        start_page = current_page - ApplicationContext.PAGE_DISPLAY_COUNT // 2
        end_page = start_page + ApplicationContext.PAGE_DISPLAY_COUNT
    return [start_page, end_page]


def render_main_page(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                     match_count, not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute=ApplicationContext.alphabets_per_attribute_display,
                     save_file_name=ApplicationContext.DEFAULT_SAVE_FILE_NAME):
    # todo 4/14/17 check which attributes can be used from constants

    [start_page_number, end_page_number] = compute_page_numbers(current_page)
    if ApplicationContext.current_layout == "horizontal":
        return render_horizontal_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages,
                                          total_count,
                                          match_count,
                                          not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)
    elif ApplicationContext.current_layout == "vertical":
        return render_vertical_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages,
                                        total_count,
                                        match_count,
                                        not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)
    elif ApplicationContext.current_layout == "single":
        return render_single_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages,
                                      total_count,
                                      match_count,
                                      not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)


def render_horizontal_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages,
                               total_count,
                               match_count,
                               not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('horizontal_layout.html')
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      start_page_number=start_page_number, end_page_number=end_page_number,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name,
                                      comments_col=ApplicationContext.COMMENTS_COLUMN, tags_col=ApplicationContext.TAGS_COLUMN)


def render_vertical_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages, total_count,
                             match_count,
                             not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('vertical_layout.html')
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      start_page_number=start_page_number, end_page_number=end_page_number,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name,
                                      comments_col=ApplicationContext.COMMENTS_COLUMN, tags_col=ApplicationContext.TAGS_COLUMN)


def render_single_template(tuple_pairs, attributes, current_page, start_page_number, end_page_number, count_per_page, number_of_pages, total_count,
                           match_count,
                           not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('single_layout.html')
    # todo 4/7/17 check params
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      start_page_number=start_page_number, end_page_number=end_page_number,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name,
                                      comments_col=ApplicationContext.COMMENTS_COLUMN, tags_col=ApplicationContext.TAGS_COLUMN)

from jinja2 import Environment, PackageLoader, select_autoescape

# load all templates from 'view' package and 'templates' folder
from utils import Constants

env = Environment(
    loader=PackageLoader('view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def renderSampleTemplate(title, users, data):
    # get a template from the folder
    template = env.get_template('sample.html')
    return template.render(title="templated page", users=["me", "them", "who"], data=data)


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


def render_main_page(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                     match_count,
                     not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute=Constants.TOKENS_PER_ATTRIBUTE,
                     save_file_name=Constants.DEFAULT_SAVE_FILE_NAME):
    if Constants.CURRENT_TEMPLATE == "horizontal":
        return render_horizontal_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                                          match_count,
                                          not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)
    elif Constants.CURRENT_TEMPLATE == "vertical":
        return render_vertical_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                                        match_count,
                                        not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)
    elif Constants.CURRENT_TEMPLATE == "single":
        return render_single_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                                      match_count,
                                      not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name)


def render_horizontal_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                               match_count,
                               not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('horizontal_layout.html')
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name)


def render_vertical_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                             match_count,
                             not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('vertical_layout.html')
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name)


def render_single_template(tuple_pairs, attributes, current_page, count_per_page, number_of_pages, total_count,
                           match_count,
                           not_match_count, not_sure_count, unlabeled_count, tokens_per_attribute, save_file_name):
    horizontal_template = env.get_template('single_layout.html')
    # todo 4/7/17 check params
    return horizontal_template.render(tuple_pairs=tuple_pairs.to_dict(orient='records'), attributes=attributes,
                                      count_per_page=count_per_page, number_of_pages=number_of_pages,
                                      current_page=current_page, match_count=match_count,
                                      not_match_count=not_match_count, not_sure_count=not_sure_count,
                                      unlabeled_count=unlabeled_count, total_count=total_count,
                                      completed_percent=str(round((total_count - unlabeled_count) * 100 / total_count)),
                                      tokens_per_attribute=tokens_per_attribute, save_file_name=save_file_name)

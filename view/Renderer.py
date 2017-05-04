from jinja2 import Environment, PackageLoader, select_autoescape
from math import ceil

from utils import ApplicationContext

# load all templates from 'view' package and 'templates' folder
env = Environment(
    loader=PackageLoader('view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


# todo 5/3/17 Delete this method. This is just used to stub jinja changes
def renderSampleTemplate(title, users, data):
    # get a template from the folder
    template = env.get_template('sample.html')
    return template.render(title="templated page", users=["me", "them", "who"], data=data)


def render_options_page(tags_col, comments_col):
    options_page = env.get_template('options.html')
    return options_page.render(tags_col=tags_col, comments_col=comments_col)


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


def render_main_page(current_page_tuple_pairs, match_count, not_match_count, not_sure_count, unlabeled_count):
    template = env.get_template('horizontal_layout.html')
    if ApplicationContext.current_layout == "horizontal":
        template = env.get_template('horizontal_layout.html')
    elif ApplicationContext.current_layout == "vertical":
        template = env.get_template('vertical_layout.html')
    elif ApplicationContext.current_layout == "single":
        template = env.get_template('single_layout.html')

    [start_page_number, end_page_number] = compute_page_numbers(ApplicationContext.current_page_number)
    return template.render(tuple_pairs=current_page_tuple_pairs.to_dict(orient='records'),
                           attributes=ApplicationContext.current_attributes,
                           count_per_page=ApplicationContext.tuple_pair_count_per_page,
                           number_of_pages=ceil(
                               ApplicationContext.current_data_frame.shape[0] / ApplicationContext.tuple_pair_count_per_page),
                           start_page_number=start_page_number, end_page_number=end_page_number,
                           current_page=ApplicationContext.current_page_number, match_count=match_count,
                           not_match_count=not_match_count, not_sure_count=not_sure_count,
                           unlabeled_count=unlabeled_count, total_count=ApplicationContext.current_data_frame.shape[0],
                           tokens_per_attribute=ApplicationContext.alphabets_per_attribute_display,
                           save_file_name=ApplicationContext.save_file_name,
                           comments_col=ApplicationContext.COMMENTS_COLUMN, tags_col=ApplicationContext.TAGS_COLUMN)

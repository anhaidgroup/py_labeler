from jinja2 import Environment, PackageLoader, select_autoescape

# load all templates from 'view' package and 'templates' folder
env = Environment(
    loader=PackageLoader('view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def renderSampleTemplate(title, users, data):
    # get a template from the folder
    template = env.get_template('sample.html')
    return template.render(title="templated page", users=["me", "them", "who"], data=data)


def render_main_page(tuple_pairs, matched_count, un_matched_count, total_count):
    main_window = env.get_template('main_window.html');
    print(un_matched_count)
    return main_window.render(data=tuple_pairs.to_dict(orient='records'), matched_count=matched_count,
                              un_matched_count=un_matched_count, total_count=total_count)


def render_dummy_page():
    main_window = env.get_template('dummy_page.html');
    return main_window.render()

from jinja2 import Environment, PackageLoader, select_autoescape

# load all templates from 'view' package and 'templates' folder
env = Environment(
    loader=PackageLoader('view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def renderSampleTemplate(title, users):
    # get a template from the folder
    template = env.get_template('sample.html')
    return template.render(title="templated page", users=["me", "them", "who"])

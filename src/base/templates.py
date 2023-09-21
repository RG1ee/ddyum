import jinja2


def render_template(template: str, **kwargs):
    templateLoader = jinja2.FileSystemLoader(searchpath="src/templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)

    return templ.render(**kwargs)

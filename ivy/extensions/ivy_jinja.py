# ------------------------------------------------------------------------------
# This extension adds support for Jinja templates.
# ------------------------------------------------------------------------------

import sys
from ivy import hooks, site, templates

try:
    import jinja2
except ImportError:
    jinja2 = None


# Stores an initialized Jinja environment instance.
env = None


# The jinja2 package is an optional dependency.
if jinja2:

    # Initialize our Jinja environment on the 'init' event hook.
    # Check the site's config file for any custom settings.
    @hooks.register('init')
    def init():
        settings = {
            'loader': jinja2.FileSystemLoader(site.theme('templates'))
        }
        settings.update(site.config.get('jinja', {}))
        global env
        env = jinja2.Environment(**settings)

    # Register our template engine callback for files with a .jinja extension.
    @templates.register('jinja')
    def callback(page, filename):
        template = env.get_template(filename)
        return template.render(page)

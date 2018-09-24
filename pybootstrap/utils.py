"""
Bootstrap utils
"""
from pybootstrap.core import Component


class Header(object):
    BOOTSTRAP_URL="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    BOOTSTRAP_INTEGRITY="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"

    META_CHARSET="utf-8"
    META_VIEWPORT_CONTENT="width=device-width, initial-scale=1, shrink-to-fit=no"
    LANG="en"

    def __init__(self, title, *scripts):
        self.title = title
        self.scripts = scripts

    def __str__(self):
        bootstrap = Component(
            "link",
            rel="stylesheet",
            href=self.BOOTSTRAP_URL,
            integrety=self.BOOTSTRAP_INTEGRITY,
            crossorigin="anonymous",
        )
        meta_charset = Component(
            "meta",
            charset=self.META_CHARSET
        )
        meta_viewport = Component(
            "meta",
            name="viewport",
            content=self.META_VIEWPORT_CONTENT,
        )
        text += '<!doctype html>\n'
        text += '<html lang={}>\n'.format(self.LANG)
        text += '    <head>\n'
        text += '        <!-- Required met tags -->\n'
        text += '        {}\n'.format(meta_charset)
        text += '        {}\n'.format(meta_viewport)
        text += '\n'
        text += '        <!-- Bootstrap css -->\n'
        text += '        {}\n'.format(bootstrap.html_open())

        for script in self.scripts:
            text += '        ' + str(script)

        text += '\n'
        text += '        <title>{}</title>\n'.format(self.title)
        text += '    </head>\n'
        text += '    <body>\n'

        return text


class Footer(object):
    def __init__(self, *scripts):
        self.scripts = scripts

    def __str__(self):
        text = ""
        for script in self.scripts:
            text += '        ' + str(script)

        text += '    </body>\n'
        text += '</html>\n'
        return text

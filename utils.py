"""
Bootstrap utils
"""
from .core import Component

class Header(object):
    BOOTSTRAP_URL="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
    BOOTSTRAP_INTEGRITY="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
    LANG="en"

    def __init__(self, title, *scripts):
        self.title = title
        self.scripts = scripts

    def __str__(self):
        bootstrap = Component(
            "link",
            indent=2,
            inline=True,
            rel="stylesheet",
            href=self.BOOTSTRAP_URL,
            integrety=self.BOOTSTRAP_INTEGRITY,
            crossorigin="anonymous",
        )
        text = 'Content-Type: text/html\n'
        text += '\n'
        text += '<!doctype html>\n'
        text += '<html lang={}>\n'.format(self.LANG)
        text += '    <head>\n'
        text += '        <!-- Required met tags -->\n'
        text += '        <meta charset="utf-8">\n'
        text += '        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n'
        text += '\n'
        text += '        <!-- Bootstrap css -->\n{}\n'.format(bootstrap.html_open())

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

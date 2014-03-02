__version__ = '0.1.0'

from docutils import nodes
from docutils.parsers.rst import directives, Directive

import bandcamp_embed as bce

LAYOUTS = {
    'standard': lambda: bce.StandardLayout(False),
    'minimal': bce.MinimalLayout,
    'horizontal': lambda: bce.HorizontalLayout(False),
    'small': lambda: bce.SmallLayout(False)
}
THEMES = {
    'light': bce.LightTheme,
    'dark': bce.DarkTheme
}
BASE_URL = 'http://bandcamp.com'

class BandcampEmbed(Directive):

    def layout(argument):
        return directives.choice(argument, LAYOUTS.keys())

    def theme(argument):
        return directives.choice(argument, THEMES.keys())

    def color(argument):
        return directives.choice(argument, bce.COMMON_COLORS.keys())

    has_content = False
    required_arguments = 4
    optional_arguments = 4
    option_spec = {
        'layout': layout,
        'theme': theme,
        'track_number': directives.positive_int,
        'links_color': color
    }

    def run(self):
        url = self.arguments[0]
        if not url:
            raise self.error('Bandcamp embed URL is empty')

        album_id = int(self.arguments[1])
        if album_id <= 0:
            raise self.error('Incorrect album ID')

        title = self.arguments[2]
        artist_name = self.arguments[3]

        layout_name = self.options.get('layout', 'standard')
        if layout_name in LAYOUTS:
            layout = LAYOUTS[layout_name]()
        else:
            raise self.error('Unknown layout')

        links_color = self.options.get('links_color', 'blue')

        theme_name = self.options.get('theme', 'light')
        if theme_name in THEMES:
            theme = THEMES[theme_name](links_color)
        else:
            raise self.error('Unknown theme')

        track_number = None
        if 'track_number' in self.options:
            try:
                track_number = int(self.options['track_number'])
            except ValueError:
                raise self.error('Incorrect track number')

        html = bce.build_player(url, BASE_URL, album_id, title,
            artist_name, layout, theme, track_num=track_number)

        return [nodes.raw('', html, format='html')]

def register():
    directives.register_directive('bandcamp_embed', BandcampEmbed)

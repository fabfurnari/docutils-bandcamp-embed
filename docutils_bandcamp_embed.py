__version__ = '0.2.1'

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

OPTION_URL = 'url'
OPTION_ALBUM_ID = 'album_id'
OPTION_TITLE = 'title'
OPTION_ARTIST_NAME = 'artist_name'
OPTION_LAYOUT = 'layout'
OPTION_THEME = 'theme'
OPTION_TRACK_NUMBER = 'track_number'
OPTION_LINKS_COLOR = 'links_color'

class BandcampEmbed(Directive):

    def layout(argument):
        return directives.choice(argument, LAYOUTS.keys())

    def theme(argument):
        return directives.choice(argument, THEMES.keys())

    def color(argument):
        return directives.choice(argument, bce.COMMON_COLORS.keys())

    def url(arg):
        return directives.uri(directives.unchanged_required(arg))

    def album_id(arg):
        return directives.positive_int(directives.unchanged_required(arg))

    has_content = False
    final_argument_whitespace = True
    required_arguments = 0
    option_spec = {
        OPTION_URL: url,
        OPTION_ALBUM_ID: album_id,
        OPTION_TITLE: directives.unchanged_required,
        OPTION_ARTIST_NAME: directives.unchanged_required,
        OPTION_LAYOUT: layout,
        OPTION_THEME: theme,
        OPTION_TRACK_NUMBER: directives.positive_int,
        OPTION_LINKS_COLOR: color
    }
    optional_arguments = len(option_spec)

    def run(self):
        (url, album_id, title, artist_name) = self.get_required_options(
            OPTION_URL, OPTION_ALBUM_ID, OPTION_TITLE, OPTION_ARTIST_NAME)

        layout_name = self.options.get(OPTION_LAYOUT, 'standard')
        layout = LAYOUTS[layout_name]()

        links_color = self.options.get(OPTION_LINKS_COLOR, 'blue')

        theme_name = self.options.get(OPTION_THEME, 'light')
        theme = THEMES[theme_name](links_color)

        track_number = self.options.get(OPTION_TRACK_NUMBER, None)

        html = bce.build_player(url, BASE_URL, album_id, title,
            artist_name, layout, theme, track_num=track_number)

        return [nodes.raw('', html, format='html')]

    def get_required_options(self, *options):
        for option_name in options:
            option = self.options.get(option_name, None)
            if option:
                yield option
            else:
                raise self.error('Option {0} is empty'.format(option_name))

def register():
    directives.register_directive('bandcamp_embed', BandcampEmbed)

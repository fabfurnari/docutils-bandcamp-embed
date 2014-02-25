import docutils.core as duc

import docutils_bandcamp_embed as dbe

dbe.register()

with open('test.rst', 'r') as f:
    rst = f.read()

html = duc.publish_string(source=rst, writer_name='html')

with open('result.html', 'w') as f:
    f.write(html.decode('utf-8'))

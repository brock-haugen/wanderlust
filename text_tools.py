import hashlib
import re

def parse_link(m):
    text = re.sub(r'[\[\]]', '', m.group(0))
    if 'http' in text:
        pieces = text.split(' ')
    elif 'Image:' in text:
        return ''
    else:
        pieces = text.split('|')
        if len(pieces) == 1:
            pieces.insert(0, '/' + pieces[0])
    return '<a href="{}">{}</a>'.format(pieces[0], pieces[-1])

def image_src(name):
    url = 'https://upload.wikimedia.org/wikipedia/commons'
    name = re.sub(' ', '_', name)
    m = hashlib.md5(name.encode('utf-8')).hexdigest()
    return '/'.join([url, m[0], m[0:2], name])

def banner_image(voyage):
    if 'sections' in voyage and 'summary' in voyage['sections']:
        for s in voyage['sections']['summary']:
            if 'pagebanner' in s:
                if 'image' in s['pagebanner']:
                    return image_src(s['pagebanner']['image'])
                else:
                    return None
    return None

def text2html(text):
    if not isinstance(text, str):
        return text

    text = re.sub(r'\[+[^\]]+\]+', parse_link, text)

    return text

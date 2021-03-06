import json
import re
import sys
import xmltodict
from functools import reduce

def parse_text(text):
    obj = {}
    for m in re.findall(r'(\{\{pagebanner|\n\=\=(\w+)\=\=\n)(((.|\n)(?!\n\=\=))*)', text):
        label = m[1].lower()
        group = m[2]
        if len(label) < 1:
            if "summary" in obj: continue
            label = "summary"
            group = m[0] + group
        paragraphs = []

        for g in re.findall(r'([^\{]+|\{\{[^\}]+\}\})', group):
            if len(g) < 5: continue

            if '{' in g:
                p = g[2:-2].split('|')
                pk = p[0].strip()
                new_obj = {}

                for s in p[1:]:
                    s = s.split('=')
                    k = s[0].strip()
                    if pk == 'pagebanner' and len(s) == 1:
                        v = k
                        k = 'image'
                    else:
                        v = s[1].strip() if len(s) > 1 else None
                    if v and len(v) > 2:
                        new_obj[k] = v

                if len(new_obj.keys()) > 0:
                    paragraphs.append({pk: new_obj})
            else:
                paragraphs.append(g.strip())

        obj[label] = paragraphs

    return obj

def main(filename):
    file_data = open(filename).read()
    xml_obj = xmltodict.parse(file_data)
    pages = []

    for page in xml_obj['mediawiki']['page']:
        try:
            text = page['revision']['text']['#text']
        except Exception:
            continue
        id = page['id']
        title = page['title']
        text_obj = parse_text(text)

        data_len = len(set([k for k in text_obj.keys() if k not in ['summary']]))
        has_image = False
        has_detailed_summary = False
        if 'summary' in text_obj:
            for s in text_obj['summary']:
                if isinstance(s, str):
                    if len(s) > 150 and len(s.split('.')) > 1:
                        has_detailed_summary = True
                elif 'pagebanner' in s:
                    if 'image' in s['pagebanner']:
                        img = s['pagebanner']['image']
                        if img and 'default' not in img:
                            has_image = True

        if data_len > 0 and has_image and has_detailed_summary:
            pages.append({
                'id': id,
                'title': title,
                'sections': text_obj
            })

    with open('wikivoyage.json', 'w') as f:
        f.write(json.dumps(pages, indent=2))

if __name__ == '__main__':
    """
        data gathered from the latest Wikivoyage data dump
        https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
    """
    main(sys.argv[-1])

import sys
import json
from functools import reduce
import xmltodict

def flatten_json(data):
    out = {}
    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '__')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '__')
        else:
            out[name[:-2]] = x

    flatten(data)
    return out

def xml2json(data):
    xml_obj = xmltodict.parse(data)
    pages = xml_obj['mediawiki']['page']
    pages = [flatten_json(p) for p in pages]
    return pages

def json2csv(data):
    headers = reduce(lambda x, y: x + y, map(lambda x: list(x.keys()), data))
    headers = sorted(list(set(headers)))
    rows = [headers]

    for rd in data:
        row = []
        for h in headers:
            v = rd.get(h, '')
            if isinstance(v, str):
                v = '"' + v + '"'
            else:
                v = str(v)
            row.append(v)
        rows.append(row)

    return rows

def main(filename):
    xml = open(filename).read()

    print("Parsing XML to JSON...")
    obj = xml2json(xml)
    with open('wikivoyage.json', 'w') as output:
        output.write(json.dumps(obj, indent=2))
        output.close()

#     print("Parsing JSON to CSV...")
#     csv = json2csv(obj)
#     with open('wikivoyage.csv', 'w') as output:
#         for row in csv:
#             output.write(','.join(row) + '\n')
#         output.close()

if __name__ == '__main__':
    """
        data gathered from the latest Wikivoyage data dump
        https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
    """
    main(sys.argv[-1])

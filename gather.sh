#!/bin/bash

mkdir -p temp
curl -O https://dumps.wikimedia.org/enwikivoyage/latest/enwikivoyage-latest-pages-articles.xml.bz2
bzip2 -d enwikivoyage-latest-pages-articles.xml.bz2
mv enwikivoyage-latest-pages-articles.xml temp/
python3 parser.py temp/enwikivoyage-latest-pages-articles.xml

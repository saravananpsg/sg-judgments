# -*- coding: utf-8 -*-

import os
import sys
import bs4
import re
# from readability.readability import Document


'''
def get_readable(html_file):
    with open(html_file, 'r') as f:
        return Document(f.read()).summary()
'''


def get_title(html_file):
    with open(html_file, 'r') as f:
        return " ".join(bs4.BeautifulSoup(
            f.read(), 'lxml').find(class_='title').get_text().split())


def get_authors(html_file):
    with open(html_file, 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        return ';'.join(
            [" ".join(t.get_text().split())
                for t in soup('p', class_=re.compile(r'[Jj]udg-[Aa]uthor'))
                if t.get_text(strip=True) and
                not any(s in t.get_text()
                        for s in ['Introduction', 'Background'])
             ])


def get_case_details(html_file):
    with open(html_file, 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        return '\t'.join(
            [" ".join(t.get_text().split())
                for t in soup('td', class_='txt-body')
                if t.get_text(strip=True) and
                not any('Parties' in sibling.get_text() for sibling in
                        t.find_previous_siblings())
             ])


''' def get_case_details(html_file):
    with open(html_file, 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        return "\t".join(
            [" ".join(soup('td', class_='txt-body')[i].get_text().split())
             for i in range(5)])
'''


def get_catchwords(html_file):
    with open(html_file, 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        return ';'.join(
            ["_".join(t.get_text().split())
                for t in soup('p', class_='txt-body')
                if t.get_text(strip=True)])


def get_url(html_file):
    with open(html_file, 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        return soup.find('base').get('href').strip()


'''
def get_readable_all(src, dest):
    for file in os.listdir(src):
        with open(os.path.join(dest, file), 'w') as f:
            f.write(get_readable(os.path.join(src, file)))
'''

if __name__ == '__main__':
    try:
        for filename in os.listdir(sys.argv[1]):
            file = os.path.join(sys.argv[1], filename)
            with open(sys.argv[2], 'a') as f:
                f.write(get_title(file) + '\t' + get_authors(file) + '\t' +
                        get_case_details(file) + '\t' + get_catchwords(file) +
                        # '\t' + get_url(file) +
                        '\n')
    except Exception as e:
        raise e

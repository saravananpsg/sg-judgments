# -*- coding: utf-8 -*-

import os
import sys
import bs4
import re
import calendar

# from readability.readability import Document


def get_title(soup):
    return " ".join(soup.find(class_='title').get_text().split()).strip()


def get_authors(soup):
    return ';'.join(
        [" ".join(t.get_text().split())
         for t in soup('p', class_=re.compile(
             r'[Jj]udg-[Aa]uthor|Judg-Date-Reserved'))
         if t.get_text(strip=True) and
         not any(s in t.get_text().lower()
                 for s in ['introduction', 'background', 'reserved', '.'] +
                 [m.lower() for m in calendar.month_name if m])
         ])


def get_case_details(soup):
    return '\t'.join(
        [" ".join(t.get_text().split())
            for t in soup('td', class_='txt-body')
            if t.get_text(strip=True) and
            not any('Parties' in sibling.get_text() for sibling in
                    t.find_previous_siblings()) and
            'Editorial note' not in t.get_text()
         ])


def get_catchwords(soup):
    return ';'.join(
        [" ".join(t.get_text().split())
            for t in soup('p', class_='txt-body')
            if t.get_text(strip=True)]).strip()


if __name__ == '__main__':
    try:
        for filename in os.listdir(sys.argv[1]):
            file = os.path.join(sys.argv[1], filename)

            with open(file, 'r') as f_read:
                soup = bs4.BeautifulSoup(f_read.read(), 'lxml')

            with open(sys.argv[2], 'a') as f_write:
                f_write.write(
                    "\t".join([filename.split('.')[0],
                               get_title(soup),
                               get_authors(soup),
                               get_case_details(soup),
                               get_catchwords(soup)]).strip() +
                    '\n')
    except Exception as e:
        raise e

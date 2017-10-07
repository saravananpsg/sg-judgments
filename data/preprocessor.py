import os
import sys
import bs4
import re


def get_title(soup):
    return '\t['.join(
        " ".join(soup.find(
            class_='title').get_text().split()).split('[', maxsplit=1))


def get_authors(soup):
    return ';'.join(
        [" ".join(p.get_text().split())
         for p in soup('p', class_=re.compile(
             r'[Jj]udg-[Aa]uthor'))
         if p.get_text(strip=True) and
         not any(s in p.get_text().lower()
                 for s in ['introduction', 'background'])
         ])


def get_case_details(soup):
    return '\t'.join(
        [" ".join(td.get_text().replace('\n', ';').split())
            for td in soup('td', class_='txt-body')
            if td.get_text(strip=True) and
            not any('Parties' in sibling.get_text() for sibling in
                    td.find_previous_siblings()) and
            'Editorial note' not in td.get_text()
         ])


def get_catchwords(soup):
    return ';'.join(
        [" ".join(p.get_text().split())
            for p in soup('p', class_='txt-body')
            if p.get_text(strip=True)]).strip()


def get_paras(html_code):
    soup = bs4.BeautifulSoup(html_code, 'lxml')
    paras = '\n\n'.join(' '.join(p.get_text().split())
        for p in soup('p', class_=re.compile(r'[Jj]udg-([Qq]uote-)?[\d]+'))
        if p.get_text(strip=True)
        )
    soup.decompose()
    if not paras:
        malformed_re = r'(<i>\s*<b>\s*<font.*?>)\s*(<p.*?>)\s*(</font>)(.+?)(</b>\s*</i>\s*</p>)'
        html_code = re.sub(
            malformed_re, r'\g<2>\g<1>\g<2>\g<4>\g<3>\g<5>', html_code)
        soup = bs4.BeautifulSoup(html_code, 'lxml')
        paras = soup.find('span', class_='txt-body').get_text()
    return paras


if __name__ == '__main__':
    try:
        for filename in os.listdir(sys.argv[1]):
            html_file = os.path.join(sys.argv[1], filename)
            text_file = os.path.join(sys.argv[3], filename.split('.')[0])

            with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
                html_code = f.read()
                soup = bs4.BeautifulSoup(html_code, 'lxml')

            with open(
                sys.argv[2], 'a', encoding='utf-8', errors='replace') as f:
                f.write(
                    "\t".join([filename.split('.')[0],
                               get_title(soup),
                               get_authors(soup),
                               get_case_details(soup),
                               get_catchwords(soup)]).strip() + '\n')

            with open(text_file, 'w', encoding='utf-8', errors='replace') as f:
                f.write(get_paras(html_code))

    except Exception as e:
        raise e

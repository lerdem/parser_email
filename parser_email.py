#!/usr/bin/python3
import argparse
import requests
import re

import sys


# Need to read parm from user
parser = argparse.ArgumentParser(
    description='''
        program to parse email from web page with
        deep contol
        ''',
    epilog='for bag-report example@com'
)

parser.add_argument(
    'url',
    help='enter url to start parse')

parser.add_argument(
    '--deep',
    type=int,
    default=1,
    help='''
        set up deep, must be a number,
        default parse only start url
    ''')

args = parser.parse_args()
print('program start on url {0.url} with deep {0.deep}'.format(args))


# check if relative urls exists
def check_domain(url):
    regex = re.compile(r'(http[s]?://[a-z0-9-.]*[a-z.]{3,4}[a-z]{2,3})')
    url = regex.findall(url)
    answer = input('correct domain name? {} (yes/no) '.format(url[0].split('//')[-1]))

    http_domain = ''
    if answer == 'yes':
        http_domain = url[0]
    elif answer == 'no':
        domain = input('enter domain name ')
        http_domain = 'http://' + domain
    else:
        print('end program')
        sys.exit()

    return http_domain

BASE_URL = args.url
DEEP = args.deep
DOMAIN_NAME = check_domain(BASE_URL)
print('info domain name is {}'.format(DOMAIN_NAME))

RESULT_EMAIL = []
CURRENT_DEEP = 0

CRAWLED_URLS = []
CURRENT_DEEP_URLS = []
NEXT_DEEP_URLS = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
}


def get_html(url):
    CRAWLED_URLS.append(url)
    try:
        r = requests.get(url, headers=headers).text
    except:
        r = ''
    return r


def filter_unique(_random_urls, _unique_urls):
    _unique_urls = list(filter(lambda url: url not in _unique_urls, _random_urls))
    return _unique_urls


def get_email(html):
    regex = re.compile(r'([a-z]+[a-z0-9._]*@[a-z-]+.[a-z]{2,3})')
    list_emails = list(set(regex.findall(html)))

    list_emails = filter_unique(list_emails, RESULT_EMAIL)
    RESULT_EMAIL.extend(list_emails)

    return True


def get_url(html):
    regex = re.compile(r'href=.[\w/._-]*')
    list_urls = regex.findall(html)

    relative_list_urls = list(set(DOMAIN_NAME + i[6:] for i in list_urls if i.find('//') == -1))
    abs_list_urls = list(set(i for i in list_urls if i.find('//') != -1))

    list_urls = relative_list_urls + abs_list_urls

    return list_urls


def put_urls(_list, place=CURRENT_DEEP_URLS):
    unique_urls = filter_unique(_list, CRAWLED_URLS)
    place.extend(unique_urls)

    return True


if __name__ == '__main__':
    # first start from base_url
    html = get_html(BASE_URL)
    get_email(html)
    grub_new_urls = get_url(html)
    put_urls(grub_new_urls)

    # work with level parsing
    for i in range(DEEP + 1):
        if CURRENT_DEEP < DEEP:
            while CURRENT_DEEP_URLS:
                url = CURRENT_DEEP_URLS[0]
                html = get_html(url)
                get_email(html)
                grub_new_urls = get_url(html)
                put_urls(grub_new_urls, place=NEXT_DEEP_URLS)

                CURRENT_DEEP_URLS.pop(0)

            CURRENT_DEEP_URLS = list(set(NEXT_DEEP_URLS[:]))
            NEXT_DEEP_URLS.clear()
            CURRENT_DEEP += 1

    print(RESULT_EMAIL)

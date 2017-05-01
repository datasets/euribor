# -*- coding: utf8 -*-
import csv
import re
import requests
from lxml import html
from datetime import datetime as date

base_url = 'http://www.euribor-rates.eu'
url = 'euribor-{}.asp?i1={}&i2=1'
current_year_url = 'euribor-rate-{}-{}.asp'

granularity = 'monthly'

# To get infos from 1999 to last year. Notice that end of range is not included
years_available_in_history = [str(year) for year in range(1999, date.now().year)]

# Pattern for file naming
file_name = 'euribor_{}{}_by_month.csv'.format


def get_available_maturity_levels(year, **kwargs):
    page = requests.get(base_url + '/' + url.format(year, "1"))
    tree = html.fromstring(page.text)
    # To get possibles values for each year
    options = tree.xpath('//option')
    if kwargs.get('type') and kwargs.get('type') == 'labels':
        return list(set([i.text for i in options]))
    else:
        return list(set([i.attrib['value'] for i in options]))


def shorten_label(label):
    label = label.replace(
        ' ', ''
    ).replace(
        'weeks',
        'w'
    ).replace(
        'week',
        'w'
    ).replace(
        'months',
        'm'
    ).replace(
        'month',
        'm'
    )
    return label


def shorten_labels(labels):
    return list(map(lambda x: shorten_label(x), labels))


def select_and_write_data(tree, maturity_level, year, xpath_selector, **kwargs):
    trs = tree.xpath(xpath_selector)
    if kwargs.get('reverse_order'):
        trs.reverse()
    # Prepare to write and loop on scrapped data for url
    with open(file_name(maturity_level, year), 'w') as csvfile:
        # Initialize csv writer
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for tr in trs:
            # Get td from tr parent
            date = tr.getchildren()[0].text.strip()
            value = tr.getchildren()[1].text.replace('%', '').replace(',', '.').strip()
            splitted_date = date.split('-')
            if splitted_date[-1] != str(year): # Current year page shows past year data as well, omit it
                continue
            if kwargs.get('dateformat') and kwargs.get('dateformat') == 'mm-dd-yyyy':
                splitted_date = [splitted_date[2], splitted_date[0], splitted_date[1]]
            else:
                splitted_date.reverse()
            iso_8601 = '-'.join(splitted_date)

            try:
                numeric_value = float(value)
                csv_writer.writerow([
                    iso_8601,
                    '{0:.3f}'.format(numeric_value),
                    maturity_level,
                    granularity
                ])
            except:
                # Empty value (during 2013 change)
                pass


def get_history_data():
    for year in years_available_in_history:
        print year
        values = get_available_maturity_levels(year)
        # Loop now for each year
        for value in values:
            page = requests.get(base_url + '/' + url.format(year, value))
            tree = html.fromstring(page.text)
            # Get Name for the file from options where selected
            maturity_level = tree.xpath('//option[@selected]')[0].text
            maturity_level = shorten_label(maturity_level)
            select_and_write_data(
                tree,
                maturity_level,
                year,
                '//div[@class="maincontent"]/table/tr/td/table/tr/td/table/tr'
            )


def get_current_year_data():
    labels = [x for x in get_available_maturity_levels('2014', type='labels')]
    year = date.now().year
    for label in labels:
        maturity_level = shorten_label(label)
        splitted_label = label.split(' ')
        maturity = splitted_label[0] # for example '12' in the case of '12 months'
        timeunit = splitted_label[1] # for example 'months' in the case of '12 months'
        page = requests.get(base_url + '/' + current_year_url.format(maturity, timeunit))
        tree = html.fromstring(page.text)
        #trs = tree.xpath('//div[@class="maincontent"]/table/tr/td[2]/table/tr/td/table/tr')
        #print trs
        select_and_write_data(
            tree,
            maturity_level,
            year,
            '//div[@class="maincontent"]/table/tr/td[2]/table/tr/td/table/tr',
            dateformat='mm-dd-yyyy',
            reverse_order=True
        )


# MAIN

if __name__ == '__main__':
    get_history_data()
    get_current_year_data()

# -*- coding: utf8 -*-
import csv
import re
import requests
from lxml import html

base_url = 'http://www.euribor-rates.eu'
url = 'euribor-{}.asp?i1={}&i2=1'

# To get infos from 1999 to 2014
years_available_in_history = [str(year) for year in range(1999, 2015)]

# Pattern for file naming
file_name = 'euribor_{}_{}_by_month.csv'.format

for year in years_available_in_history:
    print year
    page = requests.get(base_url + '/' + url.format(year, "1"))
    tree = html.fromstring(page.text)
    # To get possibles values for each year
    options_values = tree.xpath('//option')
    values = list(set([i.attrib['value'] for i in options_values]))
    # Loop now for each year
    for value in values:
        page = requests.get(base_url + '/' + url.format(year, value))
        tree = html.fromstring(page.text)
        # Get Name for the file from options where selected
        maturity_level = tree.xpath('//option[@selected]')[0].text
        maturity_level = maturity_level.replace(' ', '_')
        if int(re.sub(r"\D", "", maturity_level)) < 10:
            maturity_level = '0' + maturity_level
        trs = tree.xpath('//div[@class="maincontent"]/table/tr/td/table/tr/td/table/tr')
        # Prepare to write and loop on scrapped data for url
        with open(file_name(maturity_level, year), 'w') as csvfile:
            # Initialize csv writer
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            # Write header
            # csv_writer.writerow(['date', 'rate', 'maturity_level'])
            for tr in trs:
                # Get td from tr parent
                date = tr.getchildren()[0].text
                value = tr.getchildren()[1].text.replace(' %', '').replace(',', '.')
                # if '-' not in value:
                #     value = float(value)
                splitted_date = date.split('-')
                splitted_date.reverse()
                iso_8601 = '-'.join(splitted_date)
                csv_writer.writerow([iso_8601, value, maturity_level])

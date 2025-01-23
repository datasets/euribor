# -*- coding: utf8 -*-
import csv
import requests
import pandas as pd
from lxml import html
from datetime import datetime as date

base_url = 'http://www.euribor-rates.eu'
url = 'euribor-{}.asp?i1={}&i2=1'

granularity = 'monthly'

current_year = date.now().year + 1

# To get infos from 1999 to last year. Notice that end of range is not included
years_available_in_history = [str(year) for year in range(1999, current_year)]

# Pattern for file naming
file_name = 'euribor_{}-{}.csv'.format

# Data From 2019 to current year is available in a different format 1m, 3m, 6m, 12m
# Data from 2001 to 2018 is available in a different format 1w, 2w, 1m,2m,3m,4m,5m,6m,7m,8m,9m,10m,11m,12m


def get_available_maturity_levels(year, **kwargs):
    page = requests.get(base_url + '/' + url.format(year, "1"))
    return page.url

def remove_percentages(value):
    return value.replace('%', '').replace(' ', '')

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
    ).replace(
        'Euribor',
        ''
    )
    return label


def shorten_labels(labels):
    return list(map(lambda x: shorten_label(x), labels))

def get_data():
    for year in years_available_in_history:
        page = requests.get(base_url + '/' + url.format(year, "1"))
        tree = html.fromstring(page.content)
        # Fetch all the rows
        dates = []
        values = []
        rows = tree.xpath("//table//tr")
        header = None
        if rows:
            for row in rows:
                cells = row.xpath(".//th//text() | .//td//text()")
                cells = [cell.strip() for cell in cells if cell.strip()]
                if header is None:
                    if cells:
                        header = cells
                        for i, label in enumerate(header):
                            header[i] = shorten_label(label)
                else:
                    dates.append(cells[0])
                    values.append(cells[1:])
                    # Remove the percentage sign and the space
                    for i, label in enumerate(values):
                        for j, value in enumerate(label):
                            values[i][j] = remove_percentages(value)
            df = pd.DataFrame(values, columns=header)
            
            # Format dates with leading zeros for single-digit months and days
            for i, dt in enumerate(dates):
                dates[i] = dt.replace(' ', '')
                dates[i] = dt.split('/')
                # Ensure month and day are two digits by formatting
                dates[i] = f"{dates[i][2]}-{int(dates[i][1]):02d}-{int(dates[i][0]):02d}"
                
            for granularity, level in zip(header, values):
                if 'm' in granularity:
                    level = 'monthly'
                elif 'w' in granularity:
                    level = 'weekly'
                
                # Open the CSV file in append mode ('a') to add more data
                with open(f'data/{file_name(granularity, level)}', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    if csvfile.tell() == 0:  # Check if the file is empty
                        writer.writerow(['date', 'value', 'granularity', 'level'])
                    
                    # Track the written dates to prevent duplicates
                    written_dates = set()
                    
                    # Iterate over the values and write each row only if it's not a duplicate
                    for i, dt in enumerate(dates):
                        if dt not in written_dates:
                            vals = df[granularity].values[i]
                            if vals == '-' or not vals:
                                vals = ""
                            writer.writerow([dt, vals, granularity, level])
                            written_dates.add(dt)

        else:
            print(f"No rows found for year {year}")

if __name__ == '__main__':
    get_data()

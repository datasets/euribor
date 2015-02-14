# -*- coding: utf8 -*-
import glob
import fileinput
import os
import re

# Get all maturity levels (13 before 2013 and 8 nowadays) to be able to concatenate by maturity
maturity_levels = [
        file.replace('euribor_', '').replace('2009_by_month.csv', '')
        for file in glob.glob('*2009_by_month.csv')
]

for maturity_level in maturity_levels:
	# Get files list for each maturiy
    to_concatenate = glob.glob('euribor_' + maturity_level + '*_by_month.csv')
    to_concatenate.sort()
    # Get years to name output file with min, max
    years = [
        int(re.sub(r"\D", "", year.replace(maturity_level, '')))
        for year in to_concatenate
    ]
    # Concatenate files and add header
    with open('euribor-' + maturity_level + '-' + 'monthly' + '.csv', 'w') as fout:
        fout.write('date,rate,maturity_level\n')
        for line in fileinput.input(to_concatenate):
            fout.write(line)

# Remove intermediate files
for file in glob.glob('euribor_*'):
    os.remove(file)
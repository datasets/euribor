The Euribor Benchmark rates by year and granularity. Only monthly granularity is provided.

## Data

Data is taken from the [EMMI website](http://www.euribor-rates.eu/euribor-rates-by-year.asp).

The Euribor Benchmark is defined as below

> The Euribor Benchmark is short for Euro Interbank Offered Rate. The Euribor Benchmark rates are based on the interest rates at which a a panel of European banks borrow funds from one another. In the calculation, the highest and lowest 15% of all the quotes collected are eliminated. The remaining rates will be averaged and rounded to three decimal places. The Euribor Benchmark is determined and published at about 11:00 am each day, Central European Time.
> When the Euribor Benchmark is being mentioned it is often referred to as THE Euribor, like there’s only 1 Euribor interest rate. This is not correct, since there are in fact 8 different the Euribor Benchmark rates, all with different maturities (until November 1st 2013, there were 15 maturities).

### data/*.csv

All files in directory `data` are using the following naming convention pattern:

    euribor-{maturity}-{granularity}.csv

For instance, you can have

    euribor-1w-monthly.csv
    euribor-1m-monthly.csv
    euribor-10m-monthly.csv
    ...

`w` means `week(s)` and `m` means `months` for the maturity section

The columns are the same for all csv files.

They are three of them :

* `date` is the date for the rate value. It follows by convention ISO 8601 formatting and is for the first day of the month
* `rate` is the Euribor Benchmark rate. It uses percentage (%)
* `maturity_level` express the same information you have in file naming convention. Before nov 2013, there was 15 rates and now only 8 are available due to EU banking regulations.

The oldest available data are from 1999.

In the future, we may provide an additionnal column for granularity but at the moment, it's not useful as we only use monthly granularity.

## Preparation

This package includes a bash script executing two python scripts, one `scripts/scrap_euribor.py` to fetch content, the other `scripts/concat_files_by_maturity.py` to concat files per maturity for each granularity. At the moment, we only get monthly granularity.

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).

Refer to the [terms of use](http://www.euribor-rates.eu/disclaimer.asp) of the source dataset for any specific restrictions on using these data in a public or commercial product. You should also be aware that this data comes indirectly from <http://www.emmi-benchmarks.eu/euribor-org/euribor-rates.html>.
Note that underlying rights, terms and conditions in the data from the source are unclear and may exists.

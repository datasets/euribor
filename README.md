<a className="gh-badge" href="https://datahub.io/core/euribor"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The Euribor Benchmark rates by year and granularity. Only monthly granularity is provided.

## Data

Data is taken from the [EMMI website](http://www.euribor-rates.eu/euribor-rates-by-year.asp).

The Euribor Benchmark is defined as below

> Euribor is short for Euro Interbank Offered Rate. The Euribor rates are based on the interest rates at which a a panel of European banks borrow funds from one another. In the calculation, the highest and lowest 15% of all the quotes collected are eliminated. The remaining rates will be averaged and rounded to three decimal places. Euribor is determined and published at about 11:00 am each day, Central European Time.
> When Euribor is being mentioned it is often referred to as THE Euribor, like there’s only 1 Euribor interest rate. This is not correct, since there are in fact 8 different Euribor rates, all with different maturities (until november 1st 2013, there were 15 maturities).

### Data folder 

All files in directory `data` are using the following naming convention pattern:

    euribor-{maturity}-{granularity}.csv

For instance, you can have

    euribor-1w-weekly.csv
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

In the future, we may provide an additional column for granularity but at the moment, it's not useful as we only use monthly granularity.

## Preparation

This package includes a python script `scripts/scrap_euribor.py` that executes the process of creating the euribor data at `data/` folder, also `scripts/` folder contains `requirements.txt` file, and workflow looks like this:

```bash
pip install -r scripts/requirements.txt
python scripts/scrap_euribor.py
```

## Automation
Up-to-date (auto-updates every month) euribor dataset could be found on the datahub.io: https://datahub.io/core/euribor

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License PDDL](http://opendatacommons.org/licenses/pddl/1.0).

Refer to the [terms of use](http://www.euribor-rates.eu/disclaimer.asp) of the source dataset for any specific restrictions on using these data in a public or commercial product. You should also be aware that this data comes indirectly from [http://www.emmi-benchmarks.eu/euribor-org/euribor-rates.html](http://www.emmi-benchmarks.eu/euribor-org/euribor-rates.html).
Note that underlying rights, terms and conditions in the data from the source are unclear and may exists.

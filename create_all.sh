#!/usr/bin/env bash
cd data
python ../scripts/scrap_euribor.py
python ../scripts/concat_files_by_maturity.py

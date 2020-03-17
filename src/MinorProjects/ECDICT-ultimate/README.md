# ECDICT-ultimate

Difference between ECDICT: added an option ho hide translations of names.

## Build instruction

Prerequisites:
- python3
- Apple's Dictionary Development Kit
- gnu make

1. Download Dictionary Development Kit from apple developer website and decompress.
2. Download csv file from [ECDICT-ultimate](https://github.com/skywind3000/ECDICT-ultimate/releases) project.
3. Edit Dictionary Development Kit path in Makefile.
4. run `python3 csv2xml.py <path-to-csv-file>`
5. run `make;make install`

MarketDates.py creates a CSV with NYSE non-trading days (with or without weekends)
This is a python3 program.

usage: 
python3 MarketDates.py --help

Design:
The program uses the freely available Yahoo Finance SPX index csv file. At publish date this is found at:
   https://finance.yahoo.com/quote/%5ESPX/history?p=%5ESPX

This program creates a new csv using missing dates in the input.
These dates are the non-NYSE trading days (holidays and weekends). The output defaults to writing just holidays. 
Optionally, weekend dates can be written. The date format can be customized as needed. 

This program is distributed under the MIT License: 
This is a permissive and simple open-source license, allowing unrestricted use, modification, and distribution with minimal restrictions.
Please keep author credit information intact.

Author: Dave Latka
Original release: 2 February 2024
Version 1.0.0
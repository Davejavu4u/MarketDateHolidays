"""
MarketDates.py
Version 1.0.0
Original release: 2 February 2024
Author: Dave Latka

MIT License: Permissive and simple open-source license, allowing unrestricted use, modification, and distribution with minimal restrictions.
"""

import csv
import sys
import os
import argparse
from datetime import datetime, timedelta

# Default values
defaults = {
    'in_filename': '^SPX.csv',
    'out_filename': 'dates.csv',
    'out_date_format': 'YYYY-MM-DD',
    'data_format': 'N',
    'start_date': 'All',
    'end_date': 'All'
}

#=======================================================================================
def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        dict: A dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='''This program outputs all NYSE non-trading days from 30 December 1927. 
    It functions by loading the Yahoo Finance provided SPX CSV file to reference all SPX trading data on market open days.
    Using the SPX CSV file as your source, you can create a new CSV file with all the non-trading dates going back to 30 December 1927.
    
    Download the CSV by visiting https://finance.yahoo.com/quote/%5ESPX/history?p=%5ESPX.
    Click on the Historical Data tab, select the date range, and click Apply. Then click on Download.
    Save the CSV file in the same directory as this program as ^SPX.csv

    You can optionally specify the output filename, date format, data format, start date, and end date.
    The default behavior is to save the file as just non-trading days without Saturday and Sunday.
    However you can use --data_format="W" to include weekends.

    This python program is distributed with the MIT License:
    You can use, modify, and share this code freely, just remember to give credit!
    Have Fun, Dave Latka (-: Remember, if you have a strange feeling you've seen Dave before, that's a Davejavu :-)
    Version 1.0.0 
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--in_filename', default='^SPX.csv', help='Input CSV file.')
    parser.add_argument('--out_filename', default='dates.csv', help='Output CSV filename.')
    parser.add_argument('--out_date_format', default='YYYY-MM-DD', help='Output date format.')
    parser.add_argument('--data_format', default='N', help='Data format. N for just Non-trading days, W for Non-Trading days and weekends.')
    parser.add_argument('--start_date', default='All', help='Start date. YYYY-MM-YY Use All for all dates.')
    parser.add_argument('--end_date', default='All', help='End date. YYYY-MM-YY Use All for all dates.')
    args = parser.parse_args()

    # Validate start_date
    if args.start_date != 'All':
        try:
            datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            print("Error: --start_date is not in the 'YYYY-MM-DD' format.")
            sys.exit(1)

    # Validate end_date
    if args.end_date != 'All':
        try:
            datetime.strptime(args.end_date, '%Y-%m-%d')
        except ValueError:
            print("Error: --end_date is not in the 'YYYY-MM-DD' format.")
            sys.exit(1)
                
    return vars(args)

#=======================================================================================
def find_missing_dates(dates, start_date, end_date, data_format):
    """
    Find missing dates between a given date range.

    Args:
        dates (set): A set of dates.
        start_date (datetime): The start date of the range.
        end_date (datetime): The end date of the range.
        data_format (str): The data format. 'N' for just non-trading days, 'W' for non-trading days and weekends.

    Returns:
        list: A sorted list of missing dates.
    """
    # Create a set with all dates in the range
    all_dates = {start_date + timedelta(days=x) for x in range((end_date-start_date).days + 1)}

    # Convert dates to a set and subtract it from all_dates
    dates = set(datetime.strptime(date, "%Y-%m-%d") for date in dates)
    missing_dates = all_dates - dates

    # If data_format is 'N', exclude weekends
    if data_format == 'N':
        missing_dates = [date for date in missing_dates if date.weekday() < 5]

    return sorted(missing_dates)

#=======================================================================================
def format_date(date, format):
    """
    Format a date according to the specified format.

    Args:
        date (datetime): The date to format.
        format (str): The desired date format.

    Returns:
        str: The formatted date.
    """
    format = format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
    return date.strftime(format)

#=======================================================================================
def main():
    """
    Main function.
    """
    args = parse_arguments()
    
    if not os.path.exists(args['in_filename']):
        print(f"File {args['in_filename']} not found. Please make sure the file exists and try again.")
        sys.exit(1)

    # Load and sort CSV data
    with open(args['in_filename'], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = sorted(reader, key=lambda row: datetime.strptime(row['Date'], '%Y-%m-%d'))

    dates = [row['Date'] for row in data]

    # Determine the date range
    start_date = datetime.strptime(dates[0], '%Y-%m-%d') if args['start_date'] == "All" else datetime.strptime(args['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(dates[-1], '%Y-%m-%d') if args['end_date'] == "All" else datetime.strptime(args['end_date'], '%Y-%m-%d')

    missing_dates = find_missing_dates(set(dates), start_date, end_date, args['data_format'])

    # Write missing dates to output file
    with open(args['out_filename'], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date']) # Header
        for missing_date in missing_dates:
            formatted_date = format_date(missing_date, args['out_date_format'])
            writer.writerow([formatted_date])   

    # Get the actual start and end dates from your data
    start_date = format_date(missing_dates[0], args['out_date_format'])
    end_date = format_date(missing_dates[-1], args['out_date_format'])

    # Print the success message
    if args['data_format'] == 'N':
        print(f"Non-trading days without weekends written to {args['out_filename']} from {start_date} to {end_date} complete.")
    else:
        print(f"Non-trading days with weekends written to {args['out_filename']} from {start_date} to {end_date} complete.")
    
    

#=======================================================================================
if __name__ == "__main__":
    main()


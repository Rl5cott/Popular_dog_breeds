# read the popular dog breeds file
from ctypes import pythonapi
from distutils.command import clean
from numpy import result_type
import pandas


books_df = pandas.read_csv
books_df = pandas.DataFrame
books_df = pandas.Series

result_type


import argparse
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np

# Clean data in the AKC_Popular_breeds_2013-2016.csv
#
# Usage: 
# $ python3 clean.py AKC_Popular_Breeds_2013-2016.csv results/AKC_Popular_Breeds_2013-2016.csv
#
# where:
#   AKC_Popular_Breeds_2013-2016.csv            = path to the input file
#   results/AKC_Popular_Breeds_2013-2016clean.csv     = path to the output file
#


def get_file_names() -> tuple:
    """Get the input and output file names from the arguments passed in
    @return a tuple containing (input_file_name, output_file_name)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", "AKC_Popular_Breeds_2013-2016.csv")
    parser.add_argument("output_file","AKC_Popular_Breeds_2013-2016_clean.csv")
    args = parser.parse_args()
    return args.input_file, args.output_file


def validate_columns(df: pd.DataFrame) -> None:
    """Validates that the data in the input file has the expected columns. \
    Exits with an error if the expected columns are not present.
    @param df - The DataFrame object with the data from the input file.
    """
    EXPECTED_COLUMNS = ['Breeds', '2016 Rank', '2015 Rank', '2014 Rank', '2013 Rank']
    if not all(item in list(df.columns) for item in EXPECTED_COLUMNS):
       logging.error('Input file does not have the expected columns.')
       exit(1)
    return None


def build_size_column(df: pd.DataFrame) -> pd.DataFrame:
    """Creates a new column in the DataFrame called Genre that is based on the\
    ItemCollection column.
    @param df - the original DataFrame
    @return a DataFrame with a new column added
    """
    json_path = Path('data/size.json')
    with open(json_path, 'r') as json_file:
        genre_data = json.load(json_file)
        genre_conditions = [
            (df['ItemCollection'].isin(genre_data['Breeds'])),
            (df['ItemCollection'].isin(genre_data['2015 Rank'])),
            (df['ItemCollection'].isin(genre_data['2016 Rank']))
        ]
        genre_values = ['Breed', '2016 Rank', 'Unknown']
        df['Genre'] = np.select(genre_conditions, genre_values)
        return df


# TODO: define a function to create the Breed column here
def build_audience_column():
    pass


def main() -> None:
    """Main cleaning logic
    """
    logging.info('Getting file names from arguments.')
    input_file, output_file = get_file_names()
    logging.info(f'Input file is: {input_file}')
    logging.info(f'Output file is: {output_file}')
 
    logging.info('Loading data from input file.')
    input_path = Path(input_file)
    if not input_path.exists():
        logging.error(f'Input file not found: {input_file}')
        exit(1)
    Breeds_df = pd.read_csv(input_path)

    logging.info('Validating columns in input file.')
    validate_columns(Breeds_df)

   
    
 
    logging.info('Saving output file.')
    output_path = Path(output_file)
    if output_path.suffix == '.csv.gz':
        Breeds_df.to_csv(output_path, index=False, compression="gzip")
    else:
        Breeds_df.to_csv(output_path, index=False)
    
    return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    main()
